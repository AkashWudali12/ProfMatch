import unittest
from verification import valid_researcher

class TestVerification(unittest.TestCase):
    def test_valid_researcher_true(self):
        self.assertTrue(valid_researcher("Derek A. Paley", "University of Maryland"))
        self.assertTrue(valid_researcher("Sinéad Farrell", "University of Maryland"))
        self.assertTrue(valid_researcher("Andres De Los Reyes", "University of Maryland"))
        self.assertTrue(valid_researcher("Reza Ghodssi", "University of Maryland"))

    def test_valid_researcher_false(self):
        self.assertFalse(valid_researcher("Andrew Ng", "University of Maryland"))
        self.assertFalse(valid_researcher("Soheil Feizi", "University of Maryland"))
        self.assertFalse(valid_researcher("Shiladitya DasSarma", "University of Maryland"))
        self.assertFalse(valid_researcher("Peter Shawhan", "University of Maryland"))
        self.assertFalse(valid_researcher("Elizabeth Beise", "University of Maryland"))
        self.assertFalse(valid_researcher("Balakumar Balachandran", "University of Maryland"))
        self.assertFalse(valid_researcher("Mohammad Hajiaghayi", "University of Maryland"))
        self.assertFalse(valid_researcher("Alisa Morss Clyne", "University of Maryland"))
        self.assertFalse(valid_researcher("Mia A. Smith-Bynum", "University of Maryland"))

if __name__ == "__main__":
    unittest.main()
