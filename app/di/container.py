from typing import Any
import inspect


class Container:
    def __init__(self):
        self.dependencies = {}

    def register(self, key: type, dependency: Any):
        self.dependencies[key] = dependency

    def resolve(self, key: type):
        dependency = self.dependencies.get(key)

        if dependency is None:
            raise Exception(f"No dependency registered for key {key}")

        if isinstance(dependency, type):
            dependencies = self._get_dependencies_for_class(dependency)
            return dependency(*dependencies)

        if isinstance(dependency, callable):
            return dependency()

        return dependency

    def _get_dependencies_for_class(self, cls):
        dependencies = []

        for parameter in self._get_constructor_parameters(cls):
            dependency = self.resolve(parameter.annotation)
            dependencies.append(dependency)

        return dependencies

    def _get_constructor_parameters(self, cls):
        constructor = getattr(cls, '__init__')

        if not constructor:
            return []

        signature = inspect.signature(constructor)

        return signature.parameters.values()
