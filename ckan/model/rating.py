# encoding: utf-8

import datetime

from sqlalchemy import orm, types, Column, Table, ForeignKey

import ckan.model.meta as meta
import ckan.model.package as _package
import ckan.model.user as user
import ckan.model.domain_object as domain_object
import ckan.model.types as _types

__all__ = ['Rating', 'MIN_RATING', 'MAX_RATING']

MIN_RATING = 1.0
MAX_RATING = 5.0


rating_table = Table('rating', meta.metadata,
                     Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                     Column('user_id', types.UnicodeText, ForeignKey('user.id')),
                     Column('user_ip_address', types.UnicodeText), # alternative to user_id if not logged in
                     Column('package_id', types.UnicodeText, ForeignKey('package.id')),
                     Column('rating', types.Float),
                     Column('created', types.DateTime, default=datetime.datetime.now),
                     )

class Rating(domain_object.DomainObject):
    id: str
    user_id: str
    user_ip_address: str
    package_id: str
    rating: float
    created: datetime.datetime

    user: user.User
    package: _package.Package

meta.mapper(Rating, rating_table,
       properties={
            'user': orm.relation(user.User,
                backref=orm.backref('ratings',
                cascade='all, delete, delete-orphan'
                )),
            'package': orm.relation(_package.Package,
                backref=orm.backref('ratings',
                cascade='all, delete, delete-orphan'
                )),
            },
       )
