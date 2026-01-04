import importlib.util
import os
import unittest
from unittest import mock


def load_module(module_name, rel_path):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    module_path = os.path.join(base_dir, rel_path)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ug_utils = load_module("ug_utils", "python_scripts/undergraduate_courses/utils.py")


class TestUndergraduateUtils(unittest.TestCase):
    def test_get_semesters_list(self):
        response = mock.Mock()
        response.json = mock.Mock(return_value={"data": [{"id": 1}, {"id": 2}]})
        with mock.patch.object(ug_utils.requests, "get", return_value=response) as get:
            result = ug_utils.get_semesters_list("http://example.com/{0}", "rev-2022")
        get.assert_called_once_with("http://example.com/rev-2022", timeout=30)
        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    def test_get_courses_list_pagination(self):
        response_page1 = mock.Mock()
        response_page1.status_code = 200
        response_page1.json = mock.Mock(
            return_value={
                "data": [{"id": 1}],
                "links": {"next": "next"},
            }
        )
        response_page2 = mock.Mock()
        response_page2.status_code = 200
        response_page2.json = mock.Mock(
            return_value={
                "data": [{"id": 2}],
                "links": {"next": None},
            }
        )
        with mock.patch.object(
            ug_utils.requests, "get", side_effect=[response_page1, response_page2]
        ) as get:
            courses = ug_utils.get_courses_list("http://example.com/{0}?page={1}", "rev-2013")

        self.assertEqual(courses, [{"id": 1}, {"id": 2}])
        self.assertEqual(get.call_count, 2)
        get.assert_any_call("http://example.com/rev-2013?page=1", timeout=30)
        get.assert_any_call("http://example.com/rev-2013?page=2", timeout=30)

    def test_delete_existing_course_pages_handles_missing(self):
        with mock.patch.object(ug_utils.shutil, "rmtree", side_effect=FileNotFoundError):
            ug_utils.delete_existing_course_pages()


if __name__ == "__main__":
    unittest.main()
