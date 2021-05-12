# encoding: utf-8

from collections import defaultdict
from typing import Any
import ckan.plugins as plugins


class ExampleIResourceControllerPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IResourceController)

    def __init__(self, *args: Any, **kwargs: Any):
        self.counter = defaultdict(int)

    def before_create(self, context: Any, resource: Any):
        self.counter['before_create'] += 1

    def after_create(self, context: Any, resource: Any):
        self.counter['after_create'] += 1

    def before_update(self, context: Any, current: Any, resource: Any):
        self.counter['before_update'] += 1

    def after_update(self, context: Any, resource: Any):
        self.counter['after_update'] += 1

    def before_delete(self, context: Any, resource: Any, resources: Any):
        self.counter['before_delete'] += 1

    def after_delete(self, context: Any, resources: Any):
        self.counter['after_delete'] += 1

    def before_show(self, resource: Any):
        self.counter['before_show'] += 1
