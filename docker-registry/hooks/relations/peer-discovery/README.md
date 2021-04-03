# Overview

This interface is practically only a placeholder peer interface which provides
no special functionality, except access to the 'private-address' field of all
peers which is provided by juju implicitly.

# Usage

## Peers

By using the `peer-discovery` interface on a peer type relation, you will get
notified when peers join or leave.


```python
@when('relation-name.joined ')
def connected(peers):
    hosts = peers.units()
    if data_changed('my-peers', hosts):
        do_something(hosts)
    remove_state('ssh-peers.joined')
```

The interface sets those states for you:
* `*.connected`
* `*.joined`
* `*.departed`

`connected` is set while at least one peer is connected.

`joined` and `departed` states will clear at the end of the hook invocation.
They behave more like events than states.

The units() method only works inside of the relation hook which triggered the handler.
