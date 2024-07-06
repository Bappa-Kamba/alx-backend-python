#!/usr/bin/env python3
""" Client Tests Module """
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

org_payload = TEST_PAYLOAD[0][0]
repos_payload = TEST_PAYLOAD[0][1]
expected_repos = TEST_PAYLOAD[0][2]
apache2_repos = TEST_PAYLOAD[0][3]


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


@parameterized_class(
    (
        'org_payload',
        'repos_payload',
        'expected_repos',
        'apache2_repos'
    ),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
        Tests `client.GithubOrgClient` integration with `client.GithubOrg`}
    """
    @classmethod
    @patch('requests.get')
    def setUpClass(cls, mock_get):
        """Set up any state specific to the test class."""
        cls.get_patcher = patch(
            'requests.get',
            side_effect=cls.get_side_effect
        )
        cls.mock_get = cls.get_patcher.start()

        print("Setting up the class resources")

    @classmethod
    def tearDownClass(cls):
        """Clean up any state specific to the test class."""
        cls.get_patcher.stop()
        print("Cleaning up the class resources")

    @staticmethod
    def get_side_effect(url):
        """Side effect method for requests.get to return different payloads based on the URL."""
        if 'orgs/' in url:
            return Mock(json=lambda: org_payload)
        if 'repos' in url:
            return Mock(json=lambda: repos_payload)
        return Mock(json=lambda: {})
