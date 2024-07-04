#!/usr/bin/env python3
""" Client Tests Module """
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Test Github Org Client Class """
    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'}),
    ])
    @patch('client.get_json')
    def test_org(self, org, expected, mock_get_json):
        """ Tests `client.GithubOrgClient.org` returns expected results """
        mock_get_json.return_value = expected
        
        test_client = GithubOrgClient(org)

        self.assertEqual(test_client.org, expected)
        
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org}')
