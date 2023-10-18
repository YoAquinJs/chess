"""This module contains the generic test class"""

from core.consts import TestType
from typing import List

class Tests:
    """Class containing the logic for registering and running the Unit Tests"""
    
    tests = {}
    breakIfFailedTest = True

    for type in TestType:
        tests[type] = []
    
    @classmethod
    def register_test(cls, type: TestType):
        """Decorator for registering Unit tests and their type

        Args:
            type (TestType): Test type.
        """
        
        def decorator(func):
            cls.tests[type].append(func)
            return func
        return decorator

    @classmethod
    def execute_tests(cls, types: List[str]):
        """Run tests method, running all if no type specified or running the specified tests

        Args:
            types (List[str]): _description_
        """
        
        #Execute all test types
        if len(types) == 0:
            for t in cls.tests.values():
                for method in t:
                    print(f"Start test {method.__name__}")
                    if not method() and cls.breakIfFailedTest:
                        break
        else:
            for type in (TestType[_type] for _type in types):
                for method in cls.tests[type]:
                    print(f"Start test {method.__name__}")
                    if not method() and cls.breakIfFailedTest:
                        break