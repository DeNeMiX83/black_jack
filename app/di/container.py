from typing import Any, Callable, AsyncGenerator
import asyncio
import inspect
from app.common.logger import logger


class Container:
    def __init__(self):
        self.dependencies = {}

    def register(self, key: type, dependency: Any):
        self.dependencies[key] = dependency

    async def resolve(self, key: type):
        dependency = self.dependencies.get(key)

        if dependency is None:
            raise Exception(f"No dependency registered for key {key}")

        if isinstance(dependency, type):
            dependencies = await self._get_dependencies_for_class(dependency)
            return dependency(*dependencies)

        if callable(dependency):
            dependencies = await self._get_dependencies_for_func(dependency)
            if inspect.isasyncgenfunction(dependency):
                async for value in dependency(*dependencies):
                    return value
            return dependency(*dependencies)

        return dependency

    async def _get_dependencies_for_class(self, cls):
        dependencies = []

        for parameter in self._get_constructor_parameters(cls):
            if parameter.name == "self":
                continue
            dependency = await self.resolve(parameter.annotation)
            dependencies.append(dependency)

        return dependencies

    def _get_constructor_parameters(self, cls):
        constructor = getattr(cls, "__init__")

        if not constructor:
            return []

        signature = inspect.signature(constructor)
        return signature.parameters.values()

    async def _get_dependencies_for_func(self, func):
        dependencies = []

        for parameter in inspect.signature(func).parameters.values():
            dependency = await self.resolve(parameter.annotation)
            dependencies.append(dependency)
        # print(func)
        # print(dependencies)
        # print()
        return dependencies
