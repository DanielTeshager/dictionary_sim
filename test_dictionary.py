import unittest
from dictionary import Dictionary


class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.dict = Dictionary()

    def test_set_value(self):
        # Test setting a new key-value pair
        self.dict.set_value('apple', 'fruit')
        self.assertEqual(
            self.dict.values[self.dict.calculate_hash('apple')], 'fruit')

    def test_calculate_hash(self):
        # Test hashing consistency
        key = 'banana'
        expected_index = hash(key) % Dictionary.DK_INDICES
        self.assertEqual(self.dict.calculate_hash(key), expected_index)

    def test_quadratic_probing(self):
        # Ensure quadratic probing provides different index on collision
        initial_index = 2
        i = 1
        new_index = self.dict.quadratic_probing(initial_index, i)
        self.assertNotEqual(new_index, initial_index)

    def test_find_slot(self):
        # Test finding an empty slot correctly
        self.dict.set_value('cherry', 'fruit')
        index = self.dict.calculate_hash('cherry')
        # Assume no collision and find_slot should return the same index
        self.assertEqual(self.dict.find_slot('cherry'), index)


if __name__ == '__main__':
    unittest.main()
