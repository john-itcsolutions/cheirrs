#!/bin/bash
# hooks/website-relation-joined

relation-set "hostname=$(unit-get private-address)"
relation-set "port=5000"

# Set an optional service name, allowing more config-based
# customization
relation-set "service_name=docker-registry"
