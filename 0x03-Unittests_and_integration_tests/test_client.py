#!/usr/bin/env python3
""" Client Tests Module """
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient, get_json


class TestGithubOrgClient(unittest.TestCase):
    """ Test Github Org Client Class """
    @patch('client.get_json')
    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'}),
    ])
    def test_org(self, org, expected, mock_get_json):
        """ Tests `client.GithubOrgClient.org` returns expected results """
        mock_get_json.return_value = expected
        
        test_class = GithubOrgClient(org)

        self.assertEqual(test_class.org, expected)
        
        mock_get_json.assert_called_once_with(f'https://api.github.com/{org}')
