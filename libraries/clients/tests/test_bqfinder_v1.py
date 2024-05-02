import unittest

from unittest.mock import patch, MagicMock
from clients.model.table import Table
from clients.bqfinder_v1 import BQFinder


class TestBQFinder(unittest.TestCase):

    @patch('logger.logger.Logger', autospec=True)
    @patch('google.cloud.bigquery.client.Client', autospec=True)
    def test_init_with_target(self, mock_client, mock_logger):
        # Create a Table object
        target_table = Table(project='project1', dataset='dataset1', table_name='table1')

        # Initialize BQFinder with target and logger
        finder = BQFinder(client=mock_client, target=target_table, logger=mock_logger)

        # Assertions
        self.assertEqual(finder.client, mock_client)
        self.assertEqual(finder.target, target_table)
        self.assertEqual(finder.logger, mock_logger)

    @patch('logger.logger.Logger', autospec=True)
    @patch('google.cloud.bigquery.client.Client', autospec=True)
    def test_init_without_target(self, mock_client, mock_logger):
        # Simulate user input for target N.B. using patch as a Context Manager implies that you mock the function,
        # only inside the context Here the input is patched only during creation of the instance finder side_effects
        # are useful, when you need to return exception or multiple values (if you invoke the function more than
        # once; ex. input is called 3 times when creating the object Table). .return_value is the  DEFAULT value of
        # side_effects (see: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect and
        # https://stackoverflow.com/questions/56191199/what-happens-when-a-python-mock-has-both-a-return-value-and-a-list-of-side-effec )

        with patch('builtins.input', side_effect=['table1', 'dataset1', 'project1']):
            finder = BQFinder(client=mock_client, logger=mock_logger)

        # Expected target table
        target_table = Table(project='project1', dataset='dataset1', table_name='table1')

        # Assertions
        self.assertEqual(finder.client, mock_client)
        self.assertEqual(finder.target, target_table)
        self.assertEqual(finder.logger, mock_logger)

    @patch('logger.logger.Logger')
    @patch('google.cloud.bigquery.client.Client')
    def test_find_existing_table(self, mock_client, mock_logger):
        # Mock BigQuery client to return a table
        mock_table = MagicMock()
        mock_client.get_table.return_value = mock_table

        # Create a Table object
        target_table = Table(project='project1', dataset='dataset1', table_name='table1')

        # Create BQFinder with target and logger
        finder = BQFinder(client=mock_client, target=target_table, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertTrue(result)
        mock_logger.info.assert_called_once_with(
            f"The table'{target_table.project}':'{target_table.dataset}'.'{target_table.table_name}' exists!")

    @patch('logger.logger.Logger')
    @patch('google.cloud.bigquery.client.Client')
    def test_find_not_existing_table(self, mock_client, mock_logger):
        # Mock BigQuery client to raise an exception. This is what the method returns using a side_effect
        mock_client.get_table.side_effect = Exception('Table not found')

        # Create a Table object
        target_table = Table(project='project1', dataset='dataset1', table_name='table1')

        # Create BQFinder with target and logger
        finder = BQFinder(client=mock_client, target=target_table, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertFalse(result)
        mock_logger.error.assert_called_once_with(
            f"The table'{target_table.project}':'{target_table.dataset}'.'{target_table.table_name}' doesn't exists!")
        mock_logger.exception.assert_called_once()


if __name__ == '__main__':
    unittest.main()
