#!/usr/bin/env python3
""" Utils Test Module """
import unittest
import unittest.mock
import requests
from parameterized import parameterized
from utils import access_nested_map, get_json
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
    @unittest.mock.patch('requests.get')
    def test_get_json(self, url: str, expected: Mapping, mock_get):
        """
            Tests that the `utils.get_json` method returns the correct
            response.
        """
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = expected
        requests.get.return_value = mock_response

        mock_get.assert_called_once_with(url)

        self.assertEqual(get_json(url), expected)
