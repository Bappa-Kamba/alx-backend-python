#!/usr/bin/env python3
""" Client Tests Module """
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError

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
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()