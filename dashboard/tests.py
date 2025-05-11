from django.test import TestCase

# Create your tests here.
# This is a simple test case to check if 1 + 1 equals 2
class SimpleTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)