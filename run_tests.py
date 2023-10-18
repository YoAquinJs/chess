from sys import argv

from tests.tests import Tests

# Import Tests
import tests.piece_tests
import tests.board_tests

#Run tests
Tests.execute_tests(argv[1:])