from sys import argv

from tests.tests import Tests

#Tests
import tests.piece_tests
import tests.board_tests
import tests.game_tests

#Run tests
Tests.execute_tests(argv[1:])