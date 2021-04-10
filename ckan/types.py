import datetime
from functools import partial
from typing import (
    Any, Callable, Dict, Iterable, List,
    Mapping, Optional, Tuple, Union,
    TYPE_CHECKING
)
from sqlalchemy.orm.scoping import ScopedSession
from typing_extensions import Protocol, TypedDict

from sqlalchemy.orm import Query

if TYPE_CHECKING:
    import ckan.model as model_

AlchemySession = ScopedSession
Query = Query

Config = Dict[str, Union[str, Mapping[str, str]]]

TuplizedKey = Tuple[Any, ...]

DataDict = Dict[str, Any]
ErrorDict = Dict[str, Union[List[Union[str, Dict[str, Any]]], str]]
TuplizedErrorDict = Dict[Tuple, List[str]]

class Context(TypedDict, total=False):
    user: str
    model: 'model_'
    session: AlchemySession

    auth_user_obj: Optional['model_.User']
    user_obj: Optional['model_.User']

    id: Optional[str]
    user_id: Optional[str]
    user_is_admin: Optional[bool]
    return_query: Optional[bool]

    reset_password: Optional[bool]
    save: Optional[bool]
    active: Optional[bool]
    allow_partial_update: Optional[bool]
    for_edit: Optional[bool]
    for_view: Optional[bool]
    ignore_auth: Optional[bool]
    preview: Optional[bool]
    allow_state_change: Optional[bool]
    is_member: Optional[bool]

    message: Optional[str]

    keep_email: Optional[bool]
    keep_apikey: Optional[bool]


    group: Optional['model_.Group']
    package: Optional['model_.Package']

    api_version: Optional[int]
    dataset_counts: Optional[Dict]
    limits: Optional[Dict]
    metadata_modified: Optional[str]
    with_capacity: Optional[bool]


class AuthResult(TypedDict, total=False):
    success: bool
    msg: Optional[str]


class ValueValidator(Protocol):
    def __call__(self, value: Any) -> Any: ...


class ContextValidator(Protocol):
    def __call__(self, *, value: Any, context: Context) -> Any: ...


class DataValidator(Protocol):
    def __call__(
        self,
        key: TuplizedKey,
        data: Dict[TuplizedKey, Any],
        errors: TuplizedErrorDict,
        context: Context,
    ) -> Any: ...


Validator = Union[ValueValidator, ContextValidator, DataValidator]


Schema = Dict[str, Iterable[Validator]]
ComplexSchemaFunc = Callable[..., Schema]
PlainSchemaFunc = Callable[[], Schema]

AuthFunction = Union[
    Callable[[Context, Optional[DataDict]], AuthResult],
    partial
]
Action = Callable[[Context, DataDict], Dict]

class PFeed(Protocol):
    def __init__(
        self,
        feed_title: str,
        feed_link: str,
        feed_description: str,
        language: Optional[str],
        author_name: Optional[str],
        feed_guid: Optional[str],
        feed_url: Optional[str],
        previous_page: Optional[str],
        next_page: Optional[str],
        first_page: Optional[str],
        last_page: Optional[str],
    ) -> None: ...
    def add_item(
            self,
            title: str,
            link: str,
            description: str,
            updated: datetime.datetime,
            publised: datetime.datetime,
            unique_id: str,
            author_name: Optional[str],
            author_email: Optional[str],
            categories: List[str],
            enclosure: Any,
            **additional_fields: Any
    ) -> None: ...

    def writeString(self, encoding: str) -> str: ...



class PUploader(Protocol):
    def __init__(self, object_type: str, old_filename: Optional[str]=None) -> None: ...
    def upload(self, max_size: int=...) -> None: ...



class PResourceUploader(Protocol):
    def __init__(self, resource: Dict) -> None: ...
    def get_path(self, id: str) -> str: ...
    def upload(self, id: str, max_size: int=...) -> None: ...
CKANApp = Any
