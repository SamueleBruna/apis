import unittest
from typer.testing import CliRunner
from cli.__main__ import app

# This will invoke the app when testing
runner = CliRunner()

#TODO adding test using patching of clients (following the normal tests) and GCS

class MyTestCase(unittest.TestCase):
    def test_app_bqfinder_short_args(self):
        result = runner.invoke(app, ["bqfinder", "-pr", "skyita-da-daita-test", "-d", "contract", "-t", "contract"])
        output = "The table skyita-da-daita-test:contract.contract exists!"
        assert output in result.stdout

    def test_app_bqfinder_long_args(self):
        result = runner.invoke(app,
                         ["bqfinder", "--project", "skyita-da-daita-test", "--dataset", "contract", "--table", "contract"])
        output = "The table skyita-da-daita-test:contract.contract exists!"
        assert output in result.stdout


if __name__ == '__main__':
    unittest.main()
