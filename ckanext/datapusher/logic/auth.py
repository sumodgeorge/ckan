# encoding: utf-8

from typing import Any, Dict
from ckan.types import AuthResult, Context
import ckanext.datastore.logic.auth as auth


def datapusher_submit(
        context: Context, data_dict: Dict[str, Any]) -> AuthResult:
    return auth.datastore_auth(context, data_dict)


def datapusher_status(
        context: Context, data_dict: Dict[str, Any]) -> AuthResult:
    return auth.datastore_auth(context, data_dict)
