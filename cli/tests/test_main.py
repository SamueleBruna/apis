import unittest
from typer.testing import CliRunner
from cli.__main__ import app, bqfinder
from unittest.mock import patch, MagicMock

# This will invoke the app when testing
runner = CliRunner()

#TODO adding test using patching of clients (following the normal tests) and GCS

class MyTestCase(unittest.TestCase):

# you need to call the method from the script and not from the source. This will mock it when it is called in main
    @patch('cli.__main__.BQFinder', autospec=True)
    def test_app_bqfinder_short_args(self, mock_bqfinder):
        mock_bqfinder.return_value.find.return_value = True
        # mock_bqfinder.return_value.find.return_value = False
        result = runner.invoke(app, ["bqfinder", "-pr", "skyita-da-daita-test", "-d", "contract", "-t", "contract1"])
        output = "The table skyita-da-daita-test:contract.contract1 exists!"
        print(result.stdout)
        assert output in result.stdout

    def test_app_bqfinder_long_args(self):
        result = runner.invoke(app,
                         ["bqfinder", "--project", "skyita-da-daita-test", "--dataset", "contract", "--table", "contract"])
        output = "The table skyita-da-daita-test:contract.contract exists!"
        assert output in result.stdout

    @patch('clients.bqfinder_v1.BQFinder')
    def test_bqfinder_with_target(self, mock_bqfinder):
        # Set up arguments with target information
        project = "myproject"
        dataset = "mydataset"
        table_name = "mytable"

        # Create a mock BQFinder object
        mock_bqfinder.return_value = MagicMock()
        mock_bqfinder.return_value.find.return_value = True  # Simulate table existence

        # Call the bqfinder command
        bqfinder(project=project, dataset=dataset, table_name=table_name)

        # Assertions
        # Verify that BQFinder was called with the expected target
        mock_bqfinder.assert_called_once_with(target=Table(project=project, dataset=dataset, table_name=table_name))
        # You can add further assertions based on the expected behavior

    @patch('clients.bqfinder_v1.BQFinder')
    def test_bqfinder_without_target(self, mock_bqfinder):
        # No arguments provided (target will be asked in the function)

        # Simulate user input for target (optional)
        with patch('builtins.input', side_effect=["otherproject", "otherdataset", "othertable"]):
            bqfinder()

        # Assertions
        # Verify that BQFinder was called with the user-provided target
        # ... (similar to the previous test)


if __name__ == '__main__':
    unittest.main()
