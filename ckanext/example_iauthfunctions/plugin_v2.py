# encoding: utf-8

from typing import Any, Dict, Optional
from ckan.types import AuthResult, Context
import ckan.plugins as plugins


def group_create(
        context: Context,
        data_dict: Optional[Dict[str, Any]] = None) -> AuthResult:
    return {'success': False, 'msg': 'No one is allowed to create groups'}


class ExampleIAuthFunctionsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthFunctions)

    def get_auth_functions(self):
        return {'group_create': group_create}
