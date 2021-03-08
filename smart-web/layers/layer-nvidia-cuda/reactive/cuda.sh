#!/bin/bash
set -e

source charms.reactive.sh

CUDA_VERSION=$(config-get cuda-version | awk 'BEGIN{FS="-"}{print $1}')
CUDA_SUB_VERSION=$(config-get cuda-version | awk 'BEGIN{FS="-"}{print $2}')
LAYER_BLACKLIST_CONF="/etc/modprobe.d/blacklist-layer-nvidia-cuda.conf"
LAYER_LD_CONF="/etc/ld.so.conf.d/layer-nvidia-cuda.conf"
LAYER_PROFILE_CONF="/etc/profile.d/layer-nvidia-cuda.sh"
LAYER_RC_CONF="/home/ubuntu/.bashrc"
ROOT_URL="http://developer.download.nvidia.com/compute/cuda/repos"
SUPPORT_CUDA="$(lspci -nnk | grep -iA2 NVIDIA | wc -l)"

# translate our cuda major.minor.patch-revision into the cuda meta package name
# eg: 9.1.85-1 becomes 9-1
CUDA_META_VERSION=$(config-get cuda-version | awk 'BEGIN{FS="."; OFS="-"}{print $1, $2}')

#####################################################################
#
# Basic Functions
#
#####################################################################

function bash::lib::get_ubuntu_codename() {
    lsb_release -a 2>/dev/null | grep Codename | awk '{ print $2 }'
}

UBUNTU_CODENAME="$(bash::lib::get_ubuntu_codename)"

case "${UBUNTU_CODENAME}" in
    "trusty" )
        UBUNTU_VERSION=ubuntu1404
    ;;
    "xenial" )
        UBUNTU_VERSION=ubuntu1604
    ;;
    * )
        juju-log "Your version of Ubuntu is not supported. Exiting"
        exit 1
    ;;
esac

case "$(arch)" in
    "x86_64" | "amd64" )
        ARCH="x86_64"
        REPO_KEY="${ROOT_URL}/${UBUNTU_VERSION}/x86_64/7fa2af80.pub"
        REPO_PKG="cuda-repo-${UBUNTU_VERSION}_${CUDA_VERSION}-${CUDA_SUB_VERSION}_amd64.deb"
        REPO_URL="${ROOT_URL}/${UBUNTU_VERSION}/x86_64/${REPO_PKG}"
    ;;
    "ppc64le" | "ppc64el" )
        ARCH="ppc64le"
        REPO_KEY="${ROOT_URL}/${UBUNTU_VERSION}/ppc64el/7fa2af80.pub"
        REPO_PKG="cuda-repo-${UBUNTU_VERSION}_${CUDA_VERSION}-${CUDA_SUB_VERSION}_ppc64el.deb"
        REPO_URL="${ROOT_URL}/${UBUNTU_VERSION}/ppc64el/${REPO_PKG}"
    ;;
    * )
        juju-log "Your architecture is not supported. Exiting"
        exit 1
    ;;
esac


#####################################################################
#
# Handle prerequisite steps
#
#####################################################################

function all::all::prereqs() {
    # Blacklist the nouveau module, which conflicts with nvidia.
    # NB: do not remove nouveau pkgs because of the many x11/openjdk deps. For
    # example, removing libdrm-nouveau* also removes openjdk-8-[jre|jdk].
    #   BAD: apt-get remove -yqq --purge libdrm-nouveau*
    #        apt-get -yqq autoremove
    #   GOOD: unload and blacklist the module
    juju-log "Blacklisting nouveau module"
    modprobe --remove nouveau || \
        juju-log "No nouveau module was found. No modprobe action is needed."
    cat > ${LAYER_BLACKLIST_CONF} <<EOF
blacklist nouveau
blacklist lbm-nouveau
options nouveau modeset=0
alias nouveau off
alias lbm-nouveau off
EOF
    # update the initramfs since we altered our module blacklist
    update-initramfs -u

    juju-log "Installing linux-image-extra"
    # some kernels do not have an -extra subpackage; proceed anyway
    apt-get install -yqq  linux-image-extra-`uname -r` || \
        juju-log "linux-image-extra-`uname -r` not available. Skipping"
}

#####################################################################
#
# Purge nvidia packages per architecture
#
#####################################################################

function all:all:purge_nvidia_driver() {
    ##remove any nvidia-* or libcuda1-* packages that aren't held
    ## the nvidia-docker binary needs to held to resist this
    ## but the awk means apt will play nicely with that
    PCKGS=`dpkg -l | awk '$2~/^nvidia-/|| $2~/^libcuda1-/{if($1!~/^h/){printf " "$2}}'`
    if [ -n "$PCKGS" ]; then
        juju-log "removing $PCKGS"
        apt-get remove --ignore-hold -yqq --purge $PCKGS
    fi
}

function trusty::x86_64::purge_nvidia_driver() {
    all:all:purge_nvidia_driver
}

function xenial::x86_64::purge_nvidia_driver() {
    all:all:purge_nvidia_driver
}

function trusty::ppc64le::purge_nvidia_driver() {
    bash::lib::log warn "This task is handled by the cuda installer"
}

function xenial::ppc64le::purge_nvidia_driver() {
    bash::lib::log info "This task is handled by the cuda installer"
}

#####################################################################
#
# Install OpenBlas per architecture
#
#####################################################################

function trusty::x86_64::install_openblas() {
    apt-get install -yqq --no-install-recommends \
        libopenblas-base \
        libopenblas-dev
}

function xenial::x86_64::install_openblas() {
    apt-get install -yqq --no-install-recommends \
        libopenblas-base \
        libopenblas-dev
}

function trusty::ppc64le::install_openblas() {
    [ -d "/mnt/openblas" ] \
        || git clone https://github.com/xianyi/OpenBLAS.git /mnt/openblas \
        && { cd "/mnt/openblas" ; git pull ; cd - ; }
        cd /mnt/openblas
        make && make PREFIX=/usr install
}

function xenial::ppc64le::install_openblas() {
    apt-get install -yqq --no-install-recommends \
        libopenblas-base \
        libopenblas-dev
}

#####################################################################
#
# Install CUDA per architecture
#
#####################################################################

function all::all::install_cuda() {
    cd /tmp
    [ -f ${REPO_PKG} ] && rm -f ${REPO_PKG}
    wget ${REPO_URL}
    dpkg -i /tmp/${REPO_PKG}
    apt-key adv --fetch-keys ${REPO_KEY}
    apt-get update -qq && \
    apt-get install -yqq --allow-downgrades --allow-remove-essential --allow-change-held-packages --no-install-recommends \
        cuda-${CUDA_META_VERSION}
    rm -f ${REPO_PKG}
}

function trusty::x86_64::install_cuda() {
    all::all::install_cuda
}

function xenial::x86_64::install_cuda() {
    all::all::install_cuda
}

function trusty::ppc64le::install_cuda() {
    bash::lib::die This OS is not supported by nVidia for CUDA 8.0. Please upgrade to 16.04
}

function xenial::ppc64le::install_cuda() {
    all::all::install_cuda
}

#####################################################################
#
# Add CUDA libraries & paths
#
#####################################################################

function all::all::add_cuda_path() {
    # Create required symlinks
    ln -sf "/usr/local/cuda-$CUDA_VERSION" "/usr/local/cuda"

    # Return the given path if it's a valid directory; empty string if not.
    find_path() {
        # NB: the -H treats $1 as a dir even if it's a symlink
        find -H $1 -maxdepth 0 -type d -print 2>/dev/null || echo ""
    }
    CUDA_BIN=$(find_path "/usr/local/cuda/bin")
    CUDA_32=$(find_path "/usr/local/cuda/lib")
    CUDA_64=$(find_path "/usr/local/cuda/lib64")
    NVIDIA_BIN=$(find_path "/usr/local/nvidia/bin")
    NVIDIA_32=$(find_path "/usr/local/nvidia/lib")
    NVIDIA_64=$(find_path "/usr/local/nvidia/lib64")

    # Configuring libraries for paths that are not empty.
    true > ${LAYER_LD_CONF}
    [ -n "${CUDA_32}" ] && echo ${CUDA_32} >> ${LAYER_LD_CONF}
    [ -n "${CUDA_64}" ] && echo ${CUDA_64} >> ${LAYER_LD_CONF}
    [ -n "${NVIDIA_32}" ] && echo ${NVIDIA_32} >> ${LAYER_LD_CONF}
    [ -n "${NVIDIA_64}" ] && echo ${NVIDIA_64} >> ${LAYER_LD_CONF}
    ldconfig

    # Create path strings with colon separator if paths are not empty. This
    # uses param substitution of the form ${var:+alt_text}.
    BIN_PATH=${CUDA_BIN:+$CUDA_BIN:}${NVIDIA_BIN:+$NVIDIA_BIN:}
    LD_PATH=${CUDA_32:+$CUDA_32:}${CUDA_64:+$CUDA_64:}${NVIDIA_32:+$NVIDIA_32:}${NVIDIA_64:+$NVIDIA_64:}

    # Configuring system profile paths
    true > ${LAYER_PROFILE_CONF}
    echo "export PATH=\"${BIN_PATH}\${PATH}\"" >> ${LAYER_PROFILE_CONF}
    echo "export LD_LIBRARY_PATH=\"${LD_PATH}\${LD_LIBRARY_PATH}\"" >> ${LAYER_PROFILE_CONF}

    # Configuring user paths with a comment to ease removal if necessary
    echo "export PATH=\"${BIN_PATH}\${PATH}\" # layer-nvidia-cuda" >> ${LAYER_RC_CONF}
    echo "export LD_LIBRARY_PATH=\"${LD_PATH}\${LD_LIBRARY_PATH}\" # layer-nvidia-cuda" >> ${LAYER_RC_CONF}

    # NB: fix "cannot find -lnvcuvid" when linking cuda programs
    # see: https://devtalk.nvidia.com/default/topic/769578/cuda-setup-and-installation/cuda-6-5-cannot-find-lnvcuvid/2
    if [ ! -f /usr/lib/libnvcuvid.so.1 ]; then
        LINK_SRC=$(find /usr/lib/nvidia-* -name libnvcuvid.so.1 -print -quit)
        ln -s ${LINK_SRC} /usr/lib/libnvcuvid.so.1
    fi
    if [ ! -f /usr/lib/libnvcuvid.so ]; then
        LINK_SRC=$(find /usr/lib/nvidia-* -name libnvcuvid.so -print -quit)
        ln -s ${LINK_SRC} /usr/lib/libnvcuvid.so
    fi
}

#####################################################################
#
# Remove CUDA configuration
#
#####################################################################

function all::all::remove_cuda_config() {
    # remove system config files created by this layer
    [ -f ${LAYER_BLACKLIST_CONF} ] && rm -f ${LAYER_BLACKLIST_CONF}
    [ -f ${LAYER_LD_CONF} ] && rm -f ${LAYER_LD_CONF}
    [ -f ${LAYER_PROFILE_CONF} ] && rm -f ${LAYER_PROFILE_CONF}

    # remove user config updated by this layer
    [ -f ${LAYER_RC_CONF} ] && sed -i '/layer-nvidia-cuda/d' ${LAYER_RC_CONF}

    # update the initramfs since we altered our module blacklist
    update-initramfs -u
}

#####################################################################
#
# Reactive Handlers
#
#####################################################################

@when_not 'cuda.supported'
function check_cuda_support() {
    case "${SUPPORT_CUDA}" in
        "0" )
            juju-log "This instance does not run an nVidia GPU."
        ;;
        * )
            charms.reactive set_state 'cuda.supported'
        ;;
    esac
}

@when 'cuda.supported'
@when_not 'cuda.installed'
function install_cuda() {
    # Return if we're configured to skip installation
    INSTALL=$(config-get install-cuda)
    if [ "${INSTALL}" = "False" ]; then
      juju-log "Skip cuda installation"
      return
    fi

    status-set maintenance "Installing CUDA"
    all::all::prereqs

    # Purge existing libcuda/nvidia packages
    juju-log "Purging any existing libcuda/nvidia packages"
    ${UBUNTU_CODENAME}::${ARCH}::purge_nvidia_driver

    ${UBUNTU_CODENAME}::${ARCH}::install_openblas
    ${UBUNTU_CODENAME}::${ARCH}::install_cuda
    all::all::add_cuda_path

    status-set active "CUDA Installed"
    charms.reactive set_state 'cuda.installed'
}

@when 'cuda.installed'
@when 'config.changed.cuda-version'
function config_cuda_version() {
    # Remove config and reinstall if a new cuda-repo version is configured
    if dpkg -l cuda-repo-* 2>/dev/null | grep -q "${CUDA_VERSION}"; then
        juju-log "cuda-repo-${CUDA_VERSION} is already installed"
    else
        juju-log "Reinstalling with new CUDA version"
        all::all::remove_cuda_config
        install_cuda
    fi
}

@when 'cuda.installed'
@when 'config.changed.install-cuda'
function config_cuda_install() {
    # Remove config if user sets install-cuda to false
    INSTALL=$(config-get install-cuda)
    if [ "${INSTALL}" = "False" ]; then
        juju-log "Removing CUDA configuration"
        all::all::remove_cuda_config
        charms.reactive remove_state 'cuda.installed'
    fi
}

reactive_handler_main
