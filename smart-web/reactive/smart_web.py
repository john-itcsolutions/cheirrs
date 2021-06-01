import pwd
import os
from . import tlslib
from charms import layer
from charmhelpers.core import unitdata
from charmhelpers.core import host, hookenv, templating
from charms.reactive import hook
from charms.reactive import when
from charms.reactive import when_file_changed
from charms.reactive import set_state
from charms.reactive import remove_state
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.templating import render
from charms.reactive import when_not, set_flag
from charms.reactive import endpoint_from_flag
from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive.helpers import data_changed

class ProvidesDockerHost(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:dockerhost}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:dockerhost}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.connected')

    def configure(self, url):
        relation_info = {
            'url': url,
        }

        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')


class RequiresDockerHost(RelationBase):
    scope = scopes.GLOBAL

    auto_accessors = ['url']

    @hook('{requires:dockerhost}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('url'):
            conv.set_state('{relation_name}.available')

    @hook('{requires:dockerhost}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    def configuration(self):
        conv = self.conversation()
        return {k: conv.get_remote(k) for k in self.auto_accessors}


@when_not('smart-web.installed')
def install_smart_web():
    # Do your setup here.

    database = unitdata.kv()
    cert = database.get('tls.server.certificate')

    @when('db.connected')
    def request_db(pgsql):
        pgsql.set_database('haus')

    @when('config.changed')
    def check_admin_pass():
        admin_pass = hookenv.config()['admin-pass']
        if admin_pass:
            set_state('admin-pass')
        else:
            remove_state('admin-pass')

    @when('db.master.available', 'admin-pass')
    def render_config(pgsql):
        render_template('app-config.j2', '/etc/app.conf', {
            'db_conn': pgsql.master,
            'admin_pass': hookenv.config('admin-pass'),
        })

    
    @when('cert-provider.ca.changed')
    def install_root_ca_cert():
        cert_provider = endpoint_from_flag('cert-provider.ca.available')
        host.install_ca_cert(cert_provider.root_ca_cert)
        clear_flag('cert-provider.ca.changed')


    @when('cert-provider.available')
    def request_certificates():
        cert_provider = endpoint_from_flag('cert-provider.available')

        # get ingress info
        ingress_for_clients = hookenv.network_get('clients')['ingress-addresses']
        ingress_for_db = hookenv.network_get('db')['ingress-addresses']

        # use first ingress address as primary and any additional as SANs
        server_cn, server_sans = ingress_for_clients[0], ingress_for_clients[:1]
        client_cn, client_sans = ingress_for_db[0], ingress_for_db[:1]

        # request a single server and single client cert; note that multiple certs
        # of either type can be requested as long as they have unique common names
        cert_provider.request_server_cert(server_cn, server_sans)
        cert_provider.request_client_cert(client_cn, client_sans)


    @when('cert-provider.certs.changed')
    def update_certs():
        cert_provider = endpoint_from_flag('cert-provider.available')
        server_cert = cert_provider.server_certs[0]  # only requested one
        smart-web.update_server_cert(server_cert.cert, server_cert.key)

        client_cert = cert_provider.client_certs[0]  # only requested one
        smart-web.update_client_cert(client_cert.cert, client_cert.key)
        clear_flag('cert-provider.certs.changed')

    @when('certificates.available')
    def send_data(tls):
        '''Send the data that is required to create a server certificate for
        this server.'''
        # Use the public ip of this unit as the Common Name for the certificate.
        common_name = hookenv.unit_public_ip()
        # Get a list of Subject Alt Names for the certificate.
        sans = []
        sans.append(hookenv.unit_public_ip())
        sans.append(hookenv.unit_private_ip())
        sans.append(socket.gethostname())
        layer.tls_client.request_server_cert(common_name, sans,
                                            crt_path='/etc/certs/server.crt',
                                            key_path='/etc/certs/server.key')

    @when('certificates.server.cert.available')
    def store_server(tls):
        '''Read the server certificate from the relation object and install it on
        this system.'''
        server_cert, server_key = tls.get_server_cert()
        write_file('/home/ubuntu/server.cert', server_cert)
        write_file('/home/ubuntu/server.key', server_key)


    @when('endpoint.docker-registry.ready')
    def registry_ready():
        registry = endpoint_from_flag('endpoint.docker-registry.ready')
        configure_registry(registry.registry_netloc)
        if registry.has_auth_basic():
            configure_auth(registry.basic_user,
                            registry.basic_password)

    @when('image.joined')
    def download_image(relation):
        image = start_downloading_image()
        relation.send_configuration(image, 'smart')

    @when('image.available')
    def run_images(relation):
        images = relation.images
        if images:
            for image in images:
                run_image(image)

    @when('layer.docker-resource.smart.available')
    @when_not('charm.smart-web.started')
    def start_container():
        layer.status.maintenance('configuring container')
        image_info = layer.docker-resource.get_info('smart')
        layer.caas_base.pod_spec_set({
            'containers': [
                {
                    'name': 'smart',
                    'imageDetails': {
                        'imagePath': image_info.registry_path,
                        'username': image_info.username,
                        'password': image_info.password,
                    },
                    'ports': [
                        {
                            'name': 'service',
                            'containerPort': 8001,
                        },
                    ],
                },
            ],
        })
        layer.status.maintenance('creating container')


    @when_file_changed('/etc/app.conf')
    def restart_service():
        hookenv.service_restart('smart-web')


    @when('reverseproxy.available')
    def update_reverse_proxy_config(reverseproxy):
        services = reverseproxy.services()
        if not data_changed('reverseproxy.services', services):
            return
        for service in services:
            for host in service['hosts']:
                hookenv.log('{} has a unit {}:{}'.format(
                    services['smart-web-service'],
                    host['smart-web'],
                    host['8001']))

    @when('etcd.available', 'docker.available')
    def swarm_etcd_cluster_setup(etcd):
        con_string = etcd.connection_string().replace('http', 'etcd')
        opts = {}
        opts['connection_string'] = con_string
        render('docker-compose.yml', 'files/swarm/docker-compose.yml', opts)


        # If your charm has other dependencies before it can install,
        # add those as @when() clauses above., or as additional @when()
        # decorated handlers below
        #
        # See the following for information about reactive charms:
        #
        #  * https://jujucharms.com/docs/devel/developer-getting-started
        #  * https://github.com/juju-solutions/layer-basic#overview
    
    set_flag('smart-web.installed')
