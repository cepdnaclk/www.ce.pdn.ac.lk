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


helpers = load_module("helpers", "python_scripts/utils/helpers.py")


class TestHelpers(unittest.TestCase):
    def test_get_updated_at_parses_utc(self):
        dt = helpers.get_updated_at("2024-01-02T03:04:05.123Z")
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 2)
        self.assertEqual(dt.tzinfo, helpers.timezone.utc)

    def test_download_image_skips_empty_or_hash(self):
        self.assertEqual(helpers.download_image(None, "/tmp"), "#")
        self.assertEqual(helpers.download_image("#", "/tmp"), "#")

    def test_download_image_handles_request_failure(self):
        with mock.patch.object(
            helpers.requests, "get", side_effect=requests.RequestException
        ):
            self.assertEqual(
                helpers.download_image("http://example.com/a.png", "/tmp"), "#"
            )

    def test_download_image_writes_file(self):
        response = mock.Mock(status_code=200, content=b"data")
        with mock.patch.object(helpers.requests, "get", return_value=response):
            with mock.patch.object(helpers.os, "makedirs") as makedirs:
                with mock.patch("builtins.open", mock.mock_open()) as mock_file:
                    result = helpers.download_image(
                        "http://example.com/images/photo.jpg", "/tmp/save"
                    )

        self.assertEqual(result, "/tmp/save/photo.jpg")
        makedirs.assert_called_once_with("../tmp/save", exist_ok=True)
        mock_file.assert_called_once_with("../tmp/save/photo.jpg", "wb")

    def test_prepare_gallery_orders_and_defaults(self):
        details = {
            "id": 10,
            "gallery": [
                {
                    "order": 2,
                    "urls": {"original": "o2", "medium": "m2", "thumb": "#"},
                    "caption": "  caption2 ",
                    "alt_text": "  alt2 ",
                },
                {
                    "order": 1,
                    "urls": {"original": "o1", "medium": "#", "thumb": "#"},
                    "caption": "caption1",
                    "alt_text": "",
                },
                {
                    "order": 3,
                    "urls": {"original": "#", "medium": "#", "thumb": "#"},
                    "caption": "skip",
                    "alt_text": "skip",
                },
            ],
        }

        def download_side_effect(url, _save_dir):
            if url == "o1":
                return "/img/o1"
            if url == "o2":
                return "/img/o2"
            if url == "m2":
                return "/img/m2"
            return "#"

        with mock.patch.object(
            helpers, "download_image", side_effect=download_side_effect
        ):
            enabled, items = helpers.prepare_gallery(details, "events")

        self.assertTrue(enabled)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["original"], "/img/o1")
        self.assertEqual(items[0]["medium"], "/img/o1")
        self.assertEqual(items[0]["thumb"], "/img/o1")
        self.assertEqual(items[1]["thumb"], "/img/m2")
        self.assertEqual(items[1]["caption"], "caption2")
        self.assertEqual(items[1]["alt_text"], "alt2")

    def test_prepare_gallery_single_image_returns_false(self):
        details = {
            "gallery": [
                {"order": 1, "urls": {"original": "o1", "medium": "#", "thumb": "#"}}
            ]
        }
        with mock.patch.object(helpers, "download_image", return_value="/img/o1"):
            enabled, items = helpers.prepare_gallery(details, "events")
        self.assertFalse(enabled)
        self.assertEqual(items, [])


if __name__ == "__main__":
    unittest.main()
