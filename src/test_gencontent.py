import unittest
from gencontent import extract_title, generate_page

class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        md ="""
# this is a test_title
"""
        result = extract_title(md)
        self.assertEqual(
            result,
            "this is a test_title"
        )
    
    def test_no_title(self):
        md = """
this is a test
"""
        with self.assertRaises(Exception):
            extract_title(md)
