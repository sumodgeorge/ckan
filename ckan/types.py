# -*- coding: utf-8 -*-

import datetime
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    Union,
    TYPE_CHECKING,
)
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy import Table
from typing_extensions import Protocol, TypedDict

from sqlalchemy.orm import Query

if TYPE_CHECKING:
    import ckan.model as model_


AlchemySession = ScopedSession
Query = Query

Config = Dict[str, Union[str, Mapping[str, str]]]
CKANApp = Any

TuplizedKey = Tuple[Any, ...]

DataDict = Dict[str, Any]
ErrorDict = Dict[str, Union[List[Union[str, Dict[str, Any]]], str]]
TuplizedErrorDict = Dict[Tuple, List[str]]


class Context(TypedDict, total=False):
    user: str
    model: "model_"
    session: AlchemySession

    __auth_user_obj_checked: bool
    __auth_audit: List[Tuple[str, int]]
    auth_user_obj: Optional["model_.User"]
    user_obj: "model_.User"

    id: str
    user_id: str
    user_is_admin: bool
    search_query: bool
    return_query: bool
    return_minimal: bool
    return_id_only: bool
    defer_commit: bool
    reset_password: bool
    save: bool
    active: bool
    allow_partial_update: bool
    for_update: bool
    for_edit: bool
    for_view: bool
    ignore_auth: bool
    preview: bool
    allow_state_change: bool
    is_member: bool
    use_cache: bool

    message: str

    keep_email: bool
    keep_apikey: bool
    skip_validation: bool
    validate: bool
    count_private_and_draft_datasets: bool

    schema: "Schema"
    group: "model_.Group"
    package: "model_.Package"

    tag: "model_.Tag"
    activity: "model_.Activity"
    task_status: "model_.TaskStatus"
    resource: "model_.Resource"
    resource_view: "model_.ResourceView"
    relationship: "model_.PackageRelationship"
    api_version: int
    dataset_counts: Dict
    limits: Dict
    metadata_modified: str
    with_capacity: bool

    table_names: List[str]


class AuthResult(TypedDict, total=False):
    success: bool
    msg: Optional[str]


class ValueValidator(Protocol):
    def __call__(self, value: Any) -> Any:
        ...


class ContextValidator(Protocol):
    def __call__(self, value: Any, context: Context) -> Any:
        ...


class DataValidator(Protocol):
    def __call__(
        self,
        key: TuplizedKey,
        data: Dict[TuplizedKey, Any],
        errors: TuplizedErrorDict,
        context: Context,
    ) -> Any:
        ...


Validator = Union[ValueValidator, ContextValidator, DataValidator]

Schema = Dict[str, Union[Iterable[Validator], "Schema"]]
ComplexSchemaFunc = Callable[..., Schema]
PlainSchemaFunc = Callable[[], Schema]

AuthFunctionWithOptionalDataDict = Callable[
    [Context, Optional[DataDict]], AuthResult
]
AuthFunctionWithMandatoryDataDict = Callable[[Context, DataDict], AuthResult]
AuthFunction = Union[
    AuthFunctionWithOptionalDataDict,
    AuthFunctionWithMandatoryDataDict,
    # partial
]
Action = Callable[[Context, DataDict], Any]


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
    ) -> None:
        ...

    def add_item(self, **kwargs: Any) -> None:
        ...

    def writeString(self, encoding: str) -> str:
        ...


class PUploader(Protocol):
    def __init__(
        self, object_type: str, old_filename: Optional[str] = None
    ) -> None:
        ...

    def upload(self, max_size: int = ...) -> None:
        ...

    def update_data_dict(
        self,
        data_dict: Dict[str, Any],
        url_field: str,
        file_field: str,
        clear_field: str,
    ) -> None:
        ...


class PResourceUploader(Protocol):
    mimetype: Optional[str]
    filesize: int

    def __init__(self, resource: Dict) -> None:
        ...

    def get_path(self, id: str) -> str:
        ...

    def upload(self, id: str, max_size: int = ...) -> None:
        ...


class PModel(Protocol):
    Session: AlchemySession
    State: Type["model_.State"]
    System: Type["model_.System"]
    Package: Type["model_.Package"]
    PackageMember: Type["model_.PackageMember"]
    Tag: Type["model_.Tag"]
    PackageTag: Type["model_.PackageTag"]
    Member: Type["model_.Member"]
    User: Type["model_.User"]
    Group: Type["model_.Group"]
    GroupExtra: Type["model_.GroupExtra"]
    PackageExtra: Type["model_.PackageExtra"]
    Resource: Type["model_.Resource"]
    ResourceView: Type["model_.ResourceView"]
    TrackingSummary: Type["model_.TrackingSummary"]
    Rating: Type["model_.Rating"]
    PackageRelationship: Type["model_.PackageRelationship"]
    TaskStatus: Type["model_.TaskStatus"]
    Vocabulary: Type["model_.Vocabulary"]
    Activity: Type["model_.Activity"]
    ActivityDetail: Type["model_.ActivityDetail"]
    UserFollowingUser: Type["model_.UserFollowingUser"]
    UserFollowingDataset: Type["model_.UserFollowingDataset"]
    UserFollowingGroup: Type["model_.UserFollowingGroup"]
    SystemInfo: Type["model_.SystemInfo"]
    Dashboard: Type["model_.Dashboard"]
    ApiToken: Type["model_.ApiToken"]

    resource_table: Table
    member_table: Table
    tracking_raw_table: Table
    tracking_summary_table: Table
    resource_view_table: Table
    package_extra_table: Table
    group_extra_table: Table
    group_table: Table
    user_table: Table
    package_tag_table: Table
    tag_table: Table
    package_member_table: Table
    system_info_table: Table
    term_translation_table: Table
    activity_detail_table: Table
    activity_table: Table
    task_status_table: Table
    package_relationship_table: Table

    repo: "model_.Repository"
