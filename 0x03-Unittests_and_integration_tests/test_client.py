#!/usr/bin/env python3
""" Test client module """

from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(TestCase):
    """ Integration test class for GithubOrgClient """
    get_patcher = None

    @classmethod
    def setUpClass(cls, ):
        """ Set up class """
        mock = Mock()
        repos = TEST_PAYLOAD[0][1]
        mock.json.return_value = repos
        cls.get_patcher = patch('requests.get', side_effect=mock)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """ Tear down class """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test public repos """
        instance = GithubOrgClient("google")
        res = instance.public_repos()
        self.assertEqual(res, self.expected_repos)

    def test_public_repos_with_license(self):
        """ Test public repos with license """
        instance = GithubOrgClient("google")
        res = instance.public_repos("apache-2.0")
        self.assertEqual(res, self.apache2_repos)
