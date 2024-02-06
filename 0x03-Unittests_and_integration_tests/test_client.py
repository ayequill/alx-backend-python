#!/usr/bin/env python3
""" Test client module """

from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
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
                return_value={
                    "repos_url": "https://api.github.com/orgs/google"
                }
        ) as mock_org:
            instance = GithubOrgClient("google")
            res = instance._public_repos_url
        self.assertEqual(res, "https://api.github.com/orgs/google")
        mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock):
        """ Test public repos """
        with patch.object(
                GithubOrgClient,
                attribute='_public_repos_url',
                new_callable=PropertyMock,
                return_value="https://api.github.com/orgs/google"
        ) as mock_org:
            mock.return_value = [{"name": "google"}]
            instance = GithubOrgClient("google")
            res = instance.public_repos()
            mock.assert_called_once_with("https://api.github.com/orgs/google")
            mock_org.assert_called_once()
            self.assertEqual(res, [mock.return_value[0]["name"]])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, _license, res):
        """ Test has_license """
        instance = GithubOrgClient("google")
        self.assertEqual(instance.has_license(repo, _license), res)
