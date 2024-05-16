
import unittest

class TestClass(unittest.TestCase):
    def transfer(self):
        input1 = 1
        input2 = 2
        expected_op = 3
        self.assertEqual(test(input1, input2), expected_op)

if __name__ == "__main__":
    unittest.main()