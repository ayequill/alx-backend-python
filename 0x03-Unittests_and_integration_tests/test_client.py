#!/usr/bin/env python3
""" Test client module """

from unittest import TestCase
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """ Test class for GithubOrgClient """

    @parameterized.expand([
        "google",
        "abc",
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock):
        """ Test org method """
        instance = GithubOrgClient(org_name)
        instance.org()
        mock.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    # @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self):
        """ Test public_repos_url method """
        with patch.object(
                GithubOrgClient,
                attribute='org',
                new_callable=Mock,
                return_value={"repos_url": "https://api.github.com/orgs/google"}
        ) as mock_org:
            instance = GithubOrgClient("google")
            res = instance._public_repos_url
        self.assertEqual(res, "https://api.github.com/orgs/google")
        mock_org.assert_called_once()
