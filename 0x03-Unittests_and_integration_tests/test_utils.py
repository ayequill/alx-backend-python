#!/usr/bin/env python3
""" Test module for utils """

from unittest import TestCase
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(TestCase):
    """ Testing access_nested_map function """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, res):
        """ Test correct output """
        self.assertEqual(access_nested_map(nested_map, path), res)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested, path, res):
        """ Test key error exception """
        with self.assertRaises(res):
            access_nested_map(nested, path)


class TestGetJson(TestCase):
    """ Testing get_json function """

    # @patch('requests.get')
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://google.com", {"payload": False}),
    ])
    def test_get_json(self, url, payload):
        """ Test get_json """
        mock_obj = Mock()
        mock_obj.json.return_value = payload
        with patch(target='requests.get', return_value=mock_obj) as mock_req:
            res = get_json(url)
        mock_req.assert_called_once_with(url)
        self.assertEqual(res, payload)


class TestMemoize(TestCase):
    """ Testing memoize function """

    def test_memoize(self):
        """ Test memoize decorator """

        class TestClass:
            """ Test class """

            def a_method(self):
                """ A method """
                return 42

            @memoize
            def a_property(self):
                """ A property """
                return self.a_method()

        with patch.object(target=TestClass, attribute='a_method', return_value=42) as mock_method:
            test = TestClass()
            self.assertEqual(test.a_property, 42)
            self.assertEqual(test.a_property, 42)
            mock_method.assert_called_once()
