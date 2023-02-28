from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from app.shared import dto

DtoType = TypeVar('DtoType', bound=dto.BaseDto)
ReturnType = TypeVar('ReturnType')


class Handler(ABC, Generic[DtoType, ReturnType]):
    @abstractmethod
    async def execute(self, obj: DtoType) -> ReturnType:
        raise NotImplementedError
