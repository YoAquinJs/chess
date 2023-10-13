"""This module contains the generic test class"""

class Tests:
    tests = []

    @classmethod
    def register_test(cls, func):
        Tests.tests.append(func)
        return func

    @classmethod
    def execute_tests(cls):
        for method in cls.tests:
            if not method():
                break