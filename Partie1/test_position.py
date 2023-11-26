import unittest
from position import Position

class TestPosition(unittest.TestCase):
    def test_creation_position(self):
        pos = Position(2, 3)
        self.assertEqual(repr(pos), '(2, 3)')

    def test_equality(self):
        pos1, pos2, pos3 = Position(2, 3), Position(2, 3), Position(4, 5)
        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)

if __name__ == '__main__':
    unittest.main()
