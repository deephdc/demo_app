# -*- coding: utf-8 -*-
"""
Its good practice to have tests checking your code runs correctly.
Here we included a dummy test checking the api correctly returns
expected metadata. We suggest to extend this file to include, for
example, test for checking the predict() function is indeed working
as expected.

These tests will run in the Jenkins pipeline after each change
you make to the code.
"""

import unittest

import demo_app.api as api


class TestModelMethods(unittest.TestCase):
    def setUp(self):
        self.meta = api.get_metadata()

    def test_model_metadata_type(self):
        """
        Test that get_metadata() returns dict
        """
        self.assertTrue(type(self.meta) is dict)

    def test_model_metadata_values(self):
        """
        Test that get_metadata() returns right values (subset)
        """
        self.assertEqual(
            self.meta["name"].lower().replace("-", "_"),
            "demo_app",
        )
        self.assertEqual(
            self.meta["author"].lower(), "ignacio heredia"
        )
        self.assertEqual(
            self.meta["license"].lower(),
            "mit",
        )


if __name__ == "__main__":
    unittest.main()
