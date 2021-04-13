# encoding: utf-8

from ckan.model import domain_object
from typing import Optional


class System(domain_object.DomainObject):

    name = u'system'

    def __str__(self) -> str:
        return u'<%s>' % self.__class__.__name__

    def purge(self) -> None:
        pass

    @classmethod
    def by_name(cls,
                name: str,
                autoflush: bool = True,
                for_update: bool = False) -> Optional["System"]:
        return System()
