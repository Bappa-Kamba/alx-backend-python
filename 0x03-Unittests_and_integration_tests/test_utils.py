#!/usr/bin/env python3
""" Utils Test Module """
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
    memoize
)
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """
        Test class to test `utils.access_nested_map`, inherits from
        `unittest.TestCase`.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
        self, nested_map: Mapping,
        path: Sequence, expected: Any
    ):
        """
            Tests that the `utils.access_nested_map` method functions
            correctly.

        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ('a'), KeyError('a')),
        ({'a': 1}, ('a', 'b'), KeyError('b'))
    ])
    def test_access_nested_map_exception(
        self, nested_map: Mapping,
        path: Sequence, expected: Any
    ):
        """
            Tests that the `utils.access_nested_map` method raises the correct
            exception.
        """
        with self.assertRaises(KeyError):
            self.assertEqual(access_nested_map(nested_map, path), expected)


class TestGetJson(unittest.TestCase):
    """
        Test class to test `utils.get_json` method, inherits from
        `unittest.Testcase`.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, url: str, expected: Mapping, mock_get):
        """
            Tests that the `utils.get_json` method returns the correct
            response.
        """
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """
        Test class to test `utils.memoize` method, inherits from
        `unittest.Testcase`.
    """

    def test_memoize(self):
        """
            Tests that the `utils.memoize` method returns the correct
            response.
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, 'a_method',
            return_value=42
        ) as mock_method:
            test_class = TestClass()

            # Call the memoized property twice
            result1 = test_class.a_property
            result2 = test_class.a_property

            # Assert that the mock was called exactly once
            mock_method.assert_called_once()

            # Assert that the result is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
