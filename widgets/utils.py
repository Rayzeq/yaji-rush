from typing import Dict, Any, List, Callable, TypeVar, Tuple, Set
# import functools
# import inspect

Property = TypeVar("Property")


class PropertyMatrix:
    """
    A collection that holds every possible variations of a property
    based on a set of attributes.
    """

    # Format: {{(attr1, val1), (attr2, val2)}: property}
    variations: Dict[Set[Tuple[str, Any]], Property]

    def __init__(self, generator: Callable, **attributes: Dict[str, List[Any]]):
        self.variations = {}

        for attribute_variation in self._generate(attributes):
            self.variations[frozenset(attribute_variation)] = generator(
                **dict(attribute_variation))

    # Not optimized but good enough
    def _generate(self, attributes: Dict[str, List[Any]]) -> List[Set[Tuple[str, Any]]]:
        if not attributes:
            return [set()]

        name, values = attributes.popitem()
        result = []
        sub_results = self._generate(attributes)

        for value in values:
            for sub_result in sub_results:
                a = sub_result.copy()
                a.add((name, value))
                result.append(a)

        return result

    def get(self, **attributes: Dict[str, Any]) -> Property:
        return self.variations[frozenset(attributes.items())]


# def override_kwargs(func):
#     signature = inspect.signature(func)
#     default_kwargs = {
#         k: v.default
#         for k, v in signature.parameters.items()
#         if v.default is not inspect.Parameter.empty
#     }

#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         kwargs = {**default_kwargs, **kwargs}
#         return func(**args, **kwargs)

#     return wrapper
