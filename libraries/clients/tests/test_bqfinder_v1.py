from unittest.mock import patch, MagicMock

from clients.model.absclient_v1 import AbsClient1
from clients.model.table import Table
from google.cloud.bigquery.client import Client
from logger.logger import Logger

from clients.bqfinder_v1 import BQFinder  # Replace with your script path
import unittest


class TestBQFinder(unittest.TestCase):

    @patch('google.cloud.bigquery.client',  autospec=True)
    def test_init_with_target(self, mock_client):
        # Create a Table object
        target_table = Table('project1', 'dataset1', 'table1')

        # Create a mock logger
        mock_logger = MagicMock()

        # Initialize BQFinder with target and logger
        mock_client = mock_client.return_value
        mock_client.Client.get_table = True
        finder = BQFinder(target=target_table, logger=mock_logger)

        # Assertions
        #self.assertEqual(finder.client, mock_client.return_value)
        self.assertEqual(finder.target, target_table)
        self.assertEqual(finder.logger, mock_logger)

    @patch('logger.logger.Logger')
    def test_find_existing_table(self, mock_logger):
        # Mock the get_table method to return a success response (no exception)
        mock_client = MagicMock()
        mock_client.get_table.return_value = True  # Or any non-exception value

        # Create a Table object
        target_table = Table('project1', 'dataset1', 'table1')

        # Create BQFinder with target and logger
        finder = BQFinder(target=target_table, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertTrue(result)
        # Assert logger messages as needed

    @patch('google.cloud.bigquery.client.Client.get_table')
    @patch('logger.logger.Logger')
    def test_find_existing_table(self, mock_logger, mock_get_table):
        # Mock the get_table method to return a table object
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table

        # Create a Table object
        target_table = Table('project1', 'dataset1', 'table1')

        # Create BQFinder with target and logger
        finder = BQFinder(target=target_table, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertTrue(result)
        # Assert logger messages and potentially interactions with mock_client

    @patch('google.cloud.bigquery.client.Client')
    def test_init_without_target(self, mock_client):
        # Create a mock logger
        mock_logger = MagicMock()

        # Simulate user input for target
        with patch('builtins.input', side_effect=['table2', 'dataset2', 'project2']):
            finder = BQFinder(logger=mock_logger)

        # Expected target table
        expected_target = Table('project2', 'dataset2', 'table2')

        # Assertions
        self.assertEqual(finder.client, mock_client.return_value)
        self.assertEqual(finder.target, expected_target)
        self.assertEqual(finder.logger, mock_logger)
        # Assert that the logger.info method was called with user prompt messages (optional)

    @patch('google.cloud.bigquery.client.Client')
    @patch('logger.logger.Logger')
    def test_find_existing_table(self, mock_logger, mock_client):
        # Mock BigQuery client to return a table
        mock_table = MagicMock()
        mock_client.return_value.get_table.return_value = mock_table

        # Create a Table object
        target_table = Table('project1', 'dataset1', 'table1')

        # Create BQFinder with target and logger
        finder = BQFinder(target=target_table, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertTrue(result)
        mock_logger.info.assert_called_once_with(
            f"The table'{target_table.project}':'{target_table.dataset}'.'{target_table.table_name}' exists!")

    @patch('google.cloud.bigquery.client.Client')
    @patch('logger.logger.Logger')
    def test_find_nonexistent_table(self, mock_logger, mock_client):
        # Mock BigQuery client to raise an exception
        mock_client.return_value.get_table.side_effect = Exception('Table not found')

        # Create a Table object
        target_table = Table('project1', 'dataset1', 'table1')

        # Create BQFinder with target and logger
        finder = BQFinder(target=target_table, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertFalse(result)
        mock_logger.error.assert_called_once_with(
            f"The table'{target_table.project}':'{target_table.dataset}'.'{target_table.table_name}' doesn't exists!")
        mock_logger.exception.assert_called_once()
