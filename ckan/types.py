from functools import partial
from typing import (
    Any, Callable, Dict, Iterable, List,
    Mapping, Optional, Tuple, Union,
    TYPE_CHECKING
)
from sqlalchemy.orm.scoping import ScopedSession, scoped_session
from typing_extensions import Protocol, TypedDict

from sqlalchemy.orm import Session, Query

if TYPE_CHECKING:
    from ckan.model import User

AlchemySession = ScopedSession
# class AlchemySession(scoped_session):
#     def __call__(self): ...
#     def remove(self) -> None: ...
#     def rollback(self) -> None: ...
#     def commit(self) -> None: ...
#     def configure(self, **kwargs: Any) -> None: ...


Config = Dict[str, Union[str, Mapping[str, str]]]

TuplizedKey = Tuple[Any, ...]

DataDict = Dict[str, Any]
ErrorDict = Dict[str, Union[List[Union[str, Dict[str, Any]]], str]]

class Context(TypedDict, total=False):
    user: str
    model: Any
    session: AlchemySession
    ignore_auth: Optional[bool]
    auth_user_obj: Optional['User']

    group: Optional[str]

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
        errors: ErrorDict,
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


class PUploader(Protocol):
    ...


class PResourceUploader(Protocol):
    ...

CKANApp = Any
