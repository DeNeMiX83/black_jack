from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Union
from pydantic import BaseModel

DtoType = TypeVar("DtoType", bound=BaseModel)
ReturnType = TypeVar("ReturnType")


class Handler(ABC, Generic[DtoType, ReturnType]):
    @abstractmethod
    async def execute(self, obj: Union[DtoType, Any]) -> ReturnType:
        raise NotImplementedError
