#!/usr/bin/env python3
""" Client Tests Module """
import unittest
from unittest.mock import patch, PropertyMock
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

        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org}')

    def test_public_repos_url(self):
        """ Tests `client.GithubOrgClient.public_repos_url` returns
            expected results
        """
        expected_payload = {
            'login': 'abc',
            'repos_url': 'https://api.github.com/orgs/abc/repos'
        }
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public:
            mock_public.return_value = expected_payload

            test_client = GithubOrgClient('abc')

            self.assertEqual(
                test_client._public_repos_url,
                expected_payload
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
            Tests `client.GithubOrgClient.public_repos` returns
            expected results
        """
        mock_get_json.return_value = {'login': 'google'}
        expected_payload = {
            'login': 'abc',
            'repos_url': 'https://api.github.com/orgs/abc/repos'
        }
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public:
            mock_public.return_value = expected_payload
            test_client = GithubOrgClient('abc')

            self.assertEqual(
                test_client._public_repos_url,
                expected_payload
            )
        test_client_json = GithubOrgClient('google')
        self.assertEqual(test_client_json.org, {'login': 'google'})
        mock_get_json.assert_called_once()
        mock_public.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license",  True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, license_dict, license_key, expected):
        """
            Tests `client.GithubOrgClient.has_license` returns
            expected results
        """
        test_client = GithubOrgClient('google')
        self.assertEqual(
            test_client.has_license(
                license_dict, license_key
            ),
            expected
        )
