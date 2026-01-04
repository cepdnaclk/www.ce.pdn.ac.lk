import importlib.util
import os
import unittest
from unittest import mock

import requests


def load_module(module_name, rel_path):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    module_path = os.path.join(base_dir, rel_path)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


intranet = load_module("intranet", "python_scripts/taxonomy/intranet.py")


class TestIntranetTaxonomy(unittest.TestCase):
    def test_safe_index(self):
        self.assertEqual(intranet.safe_index({"metadata": {"index": "3"}}), 3)
        self.assertEqual(intranet.safe_index({"metadata": {"index": None}}), float("inf"))
        self.assertEqual(intranet.safe_index({"metadata": {"index": "bad"}}), float("inf"))
        self.assertEqual(intranet.safe_index({}), float("inf"))

    def test_sort_terms_recursive(self):
        terms = [
            {"metadata": {"index": "2"}},
            {"metadata": {"index": "1"}, "terms": [{"metadata": {"index": "5"}}, {"metadata": {"index": "4"}}]},
        ]
        sorted_terms = intranet.sort_terms(terms)
        self.assertEqual(intranet.safe_index(sorted_terms[0]), 1)
        self.assertEqual(intranet.safe_index(sorted_terms[1]), 2)
        inner = sorted_terms[0]["terms"]
        self.assertEqual(intranet.safe_index(inner[0]), 4)
        self.assertEqual(intranet.safe_index(inner[1]), 5)

    def test_fetch_and_transform_success(self):
        api_response = {
            "status": "success",
            "data": {
                "terms": [
                    {
                        "name": "Category B",
                        "metadata": {"index": "2"},
                        "terms": [
                            {"name": "Link 2", "metadata": {"index": "2", "link": "/b2"}},
                            {"metadata": {"index": "1", "title": "Link 1", "link": "/b1"}},
                        ],
                    },
                    {
                        "name": "Category A",
                        "metadata": {"index": "1"},
                        "terms": [
                            {"name": "Link A", "metadata": {"index": "1", "link": "/a"}},
                            {"name": None, "metadata": {"index": "2", "link": "/skip"}},
                        ],
                    },
                ]
            },
        }
        response = mock.Mock()
        response.raise_for_status = mock.Mock()
        response.json = mock.Mock(return_value=api_response)

        with mock.patch.object(intranet.requests, "get", return_value=response):
            result = intranet.fetch_and_transform()

        self.assertEqual(result[0]["name"], "Category A")
        self.assertEqual(result[0]["links"], [{"name": "Link A", "url": "/a"}])
        self.assertEqual(result[1]["links"][0]["name"], "Link 1")
        self.assertEqual(result[1]["links"][1]["url"], "/b2")

    def test_fetch_and_transform_failure_status(self):
        response = mock.Mock()
        response.raise_for_status = mock.Mock()
        response.json = mock.Mock(return_value={"status": "error"})
        with mock.patch.object(intranet.requests, "get", return_value=response):
            with self.assertRaises(ValueError):
                intranet.fetch_and_transform()


if __name__ == "__main__":
    unittest.main()
