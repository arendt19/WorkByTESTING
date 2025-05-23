from typing import Any, Generic, TypeVar, overload, Optional, Union, Dict, List, Callable, Iterable, Iterator

# Определение основных типов для моделей Django
_T = TypeVar('_T')
_M = TypeVar('_M', bound='Model')
_F = TypeVar('_F', bound='Field')
_DEC = TypeVar('_DEC')
_I = TypeVar('_I')
_R = TypeVar('_R')

# Определение базовых классов для моделей
class Model:
    id: int
    pk: Any
    objects: 'BaseManager[Any]'
    
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def delete(self, *args: Any, **kwargs: Any) -> None: ...
    def __str__(self) -> str: ...
    def get_absolute_url(self) -> str: ...
    
    def get_status_display(self) -> str: ...
    def get_transaction_type_display(self) -> str: ...
    def get_method_type_display(self) -> str: ...
    def get_notification_type_display(self) -> str: ...
    
class BaseManager(Generic[_M]):
    def all(self) -> 'QuerySet[_M]': ...
    def filter(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def exclude(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def get(self, **kwargs: Any) -> _M: ...
    def create(self, **kwargs: Any) -> _M: ...
    def get_or_create(self, **kwargs: Any) -> tuple[_M, bool]: ...
    def update_or_create(self, **kwargs: Any) -> tuple[_M, bool]: ...
    def count(self) -> int: ...
    def exists(self) -> bool: ...
    def first(self) -> Optional[_M]: ...
    def last(self) -> Optional[_M]: ...
    def create_user(self, **kwargs: Any) -> _M: ...
    def aggregate(self, *args: Any, **kwargs: Any) -> Dict[str, Any]: ...
    def __getitem__(self, key: Union[int, slice]) -> Union[_M, 'QuerySet[_M]']: ...

class QuerySet(Generic[_M]):
    def filter(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def exclude(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def order_by(self, *fields: str) -> 'QuerySet[_M]': ...
    def all(self) -> 'QuerySet[_M]': ...
    def get(self, **kwargs: Any) -> _M: ...
    def first(self) -> Optional[_M]: ...
    def last(self) -> Optional[_M]: ...
    def count(self) -> int: ...
    def exists(self) -> bool: ...
    def aggregate(self, *args: Any, **kwargs: Any) -> Dict[str, Any]: ...
    def values(self, *fields: str) -> 'ValuesQuerySet[Dict[str, Any]]': ...
    def values_list(self, *fields: str, flat: bool = False) -> 'ValuesQuerySet[Any]': ...
    def update(self, **kwargs: Any) -> int: ...
    def delete(self) -> tuple[int, Dict[str, int]]: ...
    def select_related(self, *fields: str) -> 'QuerySet[_M]': ...
    def prefetch_related(self, *lookups: str) -> 'QuerySet[_M]': ...
    def annotate(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def __iter__(self) -> Iterator[_M]: ...
    def __getitem__(self, key: Union[int, slice]) -> Union[_M, 'QuerySet[_M]']: ...

class ValuesQuerySet(Generic[_R]):
    def filter(self, **kwargs: Any) -> 'ValuesQuerySet[_R]': ...
    def exclude(self, **kwargs: Any) -> 'ValuesQuerySet[_R]': ...
    def order_by(self, *fields: str) -> 'ValuesQuerySet[_R]': ...
    def all(self) -> 'ValuesQuerySet[_R]': ...
    def first(self) -> Optional[_R]: ...
    def last(self) -> Optional[_R]: ...
    def count(self) -> int: ...
    def exists(self) -> bool: ...
    def __iter__(self) -> Iterator[_R]: ...
    def __getitem__(self, key: Union[int, slice]) -> Union[_R, 'ValuesQuerySet[_R]']: ...

# Определение полей моделей
class Field:
    name: str
    verbose_name: str
    primary_key: bool
    blank: bool
    null: bool
    default: Any
    choices: List[tuple[Any, str]]
    
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __get__(self, instance: Any, owner: Any) -> Any: ...
    def __set__(self, instance: Any, value: Any) -> None: ...
    
class CharField(Field):
    max_length: int
    def __getitem__(self, key: int) -> str: ...

class TextField(Field): 
    def __getitem__(self, key: int) -> str: ...

class IntegerField(Field): ...

class BooleanField(Field): ...

class DateField(Field): ...

class DateTimeField(Field): ...

class ForeignKey(Field):
    related_name: str
    on_delete: Callable[..., None]

class ManyToManyField(Field):
    related_name: str

class OneToOneField(Field):
    related_name: str
    on_delete: Callable[..., None]

class DecimalField(Field):
    max_digits: int
    decimal_places: int
    
class PositiveSmallIntegerField(Field): ...

class ImageField(Field):
    upload_to: str
    
class FileField(Field):
    upload_to: str
    
class URLField(Field): ...

class EmailField(Field): ...

# Определение связанных моделей для связей
class RelatedManager(Generic[_M]):
    def all(self) -> 'QuerySet[_M]': ...
    def filter(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def exclude(self, **kwargs: Any) -> 'QuerySet[_M]': ...
    def get(self, **kwargs: Any) -> _M: ...
    def create(self, **kwargs: Any) -> _M: ...
    def get_or_create(self, **kwargs: Any) -> tuple[_M, bool]: ...
    def update_or_create(self, **kwargs: Any) -> tuple[_M, bool]: ...
    def count(self) -> int: ...
    def exists(self) -> bool: ...
    def first(self) -> Optional[_M]: ...
    def last(self) -> Optional[_M]: ...
    def add(self, *objs: _M, **kwargs: Any) -> None: ...
    def remove(self, *objs: _M, **kwargs: Any) -> None: ...
    def clear(self, **kwargs: Any) -> None: ...
    def set(self, objs: Iterable[_M], **kwargs: Any) -> None: ...
    def __getitem__(self, key: Union[int, slice]) -> Union[_M, 'QuerySet[_M]']: ...