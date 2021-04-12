
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


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
