import unittest
from typer.testing import CliRunner
from cli.__main__ import app
from unittest.mock import patch

# This will invoke the app when testing
runner = CliRunner()


class MyTestCase(unittest.TestCase):

    # you need to call the method from the script and not from the source. This will mock it when it is called in main
    @patch('cli.__main__.BQFinder', autospec=True)
    def test_bqfinder_found_short_args(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = True
        mock_bqfinder.return_value.target.table_name = "table1"
        mock_bqfinder.return_value.target.dataset = "dataset1"
        mock_bqfinder.return_value.target.project = "project1"

        result = runner.invoke(app, ["bqfinder", "-pr", "project1", "-d", "dataset1", "-t", "table1"])
        output = "The table project1:dataset1.table1 exists!"
        assert output in result.stdout

    @patch('cli.__main__.BQFinder', autospec=True)
    def test_bqfinder_not_found_short_args(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = False
        mock_bqfinder.return_value.target.table_name = "table1"
        mock_bqfinder.return_value.target.dataset = "dataset1"
        mock_bqfinder.return_value.target.project = "project1"

        result = runner.invoke(app, ["bqfinder", "-pr", "project1", "-d", "dataset1", "-t", "table1"])
        output = "The table project1:dataset1.table1 doesn't exists!"
        assert output in result.stdout

    @patch('cli.__main__.BQFinder', autospec=True)
    def test_bqfinder_found_long_args(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = True
        mock_bqfinder.return_value.target.table_name = "table1"
        mock_bqfinder.return_value.target.dataset = "dataset1"
        mock_bqfinder.return_value.target.project = "project1"

        result = runner.invoke(app,
                               ["bqfinder", "--project", "project1", "--dataset", "dataset1", "--table",
                                "table1"])
        output = "The table project1:dataset1.table1 exists!"
        assert output in result.stdout

    @patch('cli.__main__.BQFinder', autospec=True)
    def test_bqfinder_not_found_long_args(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = False
        mock_bqfinder.return_value.target.table_name = "table1"
        mock_bqfinder.return_value.target.dataset = "dataset1"
        mock_bqfinder.return_value.target.project = "project1"

        result = runner.invoke(app,
                               ["bqfinder", "--project", "project1", "--dataset", "dataset1", "--table",
                                "table1"])
        output = "The table project1:dataset1.table1 doesn't exists!"
        assert output in result.stdout

    @patch('cli.__main__.BQFinder', autospec=True)
    def test_bqfinder_without_target_found(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = True
        mock_bqfinder.return_value.target.table_name = "table1"
        mock_bqfinder.return_value.target.dataset = "dataset1"
        mock_bqfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["table1", "dataset1", "project1"]):
            result = runner.invoke(app, ["bqfinder"])

        output = "The table project1:dataset1.table1 exists!"
        print(result.stdout)
        assert output in result.stdout

    @patch('cli.__main__.BQFinder', autospec=True)
    def test_bqfinder_without_target_not_found(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = False
        mock_bqfinder.return_value.target.table_name = "table1"
        mock_bqfinder.return_value.target.dataset = "dataset1"
        mock_bqfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["table1", "dataset1", "project1"]):
            result = runner.invoke(app, ["bqfinder"])

        output = "The table project1:dataset1.table1 doesn't exists!"
        print(result.stdout)
        assert output in result.stdout

    @patch('cli.__main__.GCSFinder', autospec=True)
    def test_gcsfinder_found_short_args(self, mock_gcsfinder):
        mock_gcsfinder.return_value.find.return_value = True
        mock_gcsfinder.return_value.target.path = "path1"
        mock_gcsfinder.return_value.target.bucket = "bucket1"
        mock_gcsfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["project1", "bucket1", "path1"]):
            result = runner.invoke(app, ["gcsfinder", "-pr", "project1", "-b", "bucket1", "-pt", "path1"])

        output = "The blob project1:bucket1/path1 exists!"
        assert output in result.stdout

    @patch('cli.__main__.GCSFinder', autospec=True)
    def test_gcsfinder_not_found_short_args(self, mock_gcsfinder):
        mock_gcsfinder.return_value.find.return_value = False
        mock_gcsfinder.return_value.target.path = "path1"
        mock_gcsfinder.return_value.target.bucket = "bucket1"
        mock_gcsfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["project1", "bucket1", "path1"]):
            result = runner.invoke(app, ["gcsfinder", "-pr", "project1", "-b", "bucket1", "-pt", "path1"])

        output = "The blob project1:bucket1/path1 doesn't exists!"
        assert output in result.stdout

    @patch('cli.__main__.GCSFinder', autospec=True)
    def test_gcsfinder_found_long_args(self, mock_gcsfinder):
        mock_gcsfinder.return_value.find.return_value = True
        mock_gcsfinder.return_value.target.path = "path1"
        mock_gcsfinder.return_value.target.bucket = "bucket1"
        mock_gcsfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["project1", "bucket1", "path1"]):
            result = runner.invoke(app,
                                   ["gcsfinder", "--project", "project1", "--bucket", "bucket1", "--path",
                                    "path1"])

        output = "The blob project1:bucket1/path1 exists!"
        assert output in result.stdout

    @patch('cli.__main__.GCSFinder', autospec=True)
    def test_gcsfinder_not_found_long_args(self, mock_gcsfinder):
        mock_gcsfinder.return_value.find.return_value = False
        mock_gcsfinder.return_value.target.path = "path1"
        mock_gcsfinder.return_value.target.bucket = "bucket1"
        mock_gcsfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["project1", "bucket1", "path1"]):
            result = runner.invoke(app,
                                   ["gcsfinder", "--project", "project1", "--bucket", "bucket1", "--path",
                                    "path1"])

        output = "The blob project1:bucket1/path1 doesn't exists!"
        assert output in result.stdout

    @patch('cli.__main__.GCSFinder', autospec=True)
    def test_gcsfinder_without_target_found(self, mock_gcsfinder):
        mock_gcsfinder.return_value.find.return_value = True
        mock_gcsfinder.return_value.target.path = "path1"
        mock_gcsfinder.return_value.target.bucket = "bucket1"
        mock_gcsfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["project1", "bucket1", "path1"]):
            result = runner.invoke(app, ["gcsfinder"])

        output = "The blob project1:bucket1/path1 exists!"
        assert output in result.stdout

    @patch('cli.__main__.GCSFinder', autospec=True)
    def test_gcsfinder_without_target_not_found(self, mock_gcsfinder):
        mock_gcsfinder.return_value.find.return_value = False
        mock_gcsfinder.return_value.target.path = "path1"
        mock_gcsfinder.return_value.target.bucket = "bucket1"
        mock_gcsfinder.return_value.target.project = "project1"

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["project1", "bucket1", "path1"]):
            result = runner.invoke(app, ["gcsfinder"])

        output = "The blob project1:bucket1/path1 doesn't exists!"
        assert output in result.stdout


if __name__ == '__main__':
    unittest.main()
