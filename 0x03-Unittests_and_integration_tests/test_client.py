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
