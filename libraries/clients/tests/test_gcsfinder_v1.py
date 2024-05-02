import unittest

from unittest.mock import patch, MagicMock, call
from clients.model.blob import Blob
from clients.gcsfinder_v1 import GCSFinder
from datetime import datetime


class TestGCSFinderFinder(unittest.TestCase):

    @patch('logger.logger.Logger', autospec=True)
    @patch('google.cloud.storage.client.Client', autospec=True)
    def test_init_with_target(self, mock_client, mock_logger):
        # Create a Table object
        target_blob = Blob(project='project', bucket='bucket1', path='path/to/file1.txt')

        # Initialize GCSFinder with target and logger
        finder = GCSFinder(client=mock_client, target=target_blob, logger=mock_logger)

        # Assertions
        self.assertEqual(finder.client, mock_client)
        self.assertEqual(finder.target, target_blob)
        self.assertEqual(finder.logger, mock_logger)

    @patch('logger.logger.Logger', autospec=True)
    @patch('google.cloud.storage.client.Client', autospec=True)
    def test_init_without_target(self, mock_client, mock_logger):
        # Simulate user input for target N.B. using patch as a Context Manager implies that you mock the function,
        # only inside the context Here the input is patched only during creation of the instance finder side_effects
        # are useful, when you need to return exception or multiple values (if you invoke the function more than
        # once; ex. input is called 3 times when creating the object Blob). .return_value is the  DEFAULT value of
        # side_effects (see: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect and
        # https://stackoverflow.com/questions/56191199/what-happens-when-a-python-mock-has-both-a-return-value-and-a-list-of-side-effec )

        with patch('builtins.input', side_effect=['project', 'bucket1', 'path/to/file.txt']):
            finder = GCSFinder(client=mock_client, logger=mock_logger)

        # Expected target table
        target_blob = Blob(project='project', bucket='bucket1', path='path/to/file.txt')

        # Assertions
        self.assertEqual(finder.client, mock_client)
        self.assertEqual(finder.target, target_blob)
        self.assertEqual(finder.logger, mock_logger)

    @patch('logger.logger.Logger')
    @patch('google.cloud.storage.client.Client')
    def test_find_existing_blob(self, mock_client, mock_logger):
        # Mock GCS client to return a table
        mock_blob = MagicMock()
        mock_blob.name = 'file.txt'
        mock_blob.project = 'project1'
        mock_blob.bucket.name = 'bucket1'
        mock_blob.storage_class = 'STANDARD'
        mock_blob.id = 'blob-id'
        mock_blob.size = 1024  # 1KB
        mock_blob.updated = datetime(2024, 3, 30, 17, 30)
        mock_client.bucket.return_value.get_blob.return_value = mock_blob

        # Create a Table object
        target_blob = Blob(project='project', bucket='bucket1', path='path/to/file1.txt')

        # Create GCSFinder with target and logger
        finder = GCSFinder(client=mock_client, target=target_blob, logger=mock_logger)
        # Call the find method
        result = finder.find()

        # Assertions
        self.assertTrue(result)
        # useful attributes of mock_library are mock_calls and call_args_list, that can be accessed as lists
        self.assertListEqual(mock_logger.info.mock_calls, [
            call(f"Blob instance: {target_blob.project}: {target_blob.bucket} {target_blob.path} exists!"),
            call(f"Blob: {mock_blob.name}"),
            call(f"Bucket: {mock_blob.bucket.name}"),
            call(f"Storage class: {mock_blob.storage_class}"),
            call(f"ID: {mock_blob.id}"),
            call(f"Size: {mock_blob.size / 1048576:0.6f} Mb"),
            call(f"Updated: {mock_blob.updated}")
        ])

    @patch('logger.logger.Logger')
    @patch('google.cloud.bigquery.client.Client')
    def test_find_not_existing_table(self, mock_client, mock_logger):
        # Mock BigQuery client to raise an exception. This is what the method returns using a side_effect
        mock_client.get_table.side_effect = Exception('Table not found')

        # Create a Table object
        target_blob = Blob(project='project', bucket='bucket1', path='path/to/file1.txt')

        # Create GCSFinder with target and logger
        finder = GCSFinder(client=mock_client, target=target_blob, logger=mock_logger)

        # Call the find method
        result = finder.find()

        # Assertions
        self.assertFalse(result)
        mock_logger.error.assert_called_once_with(
            f"The blob {target_blob.bucket} {target_blob.path} doesn't exists!")
        mock_logger.exception.assert_called_once()


if __name__ == '__main__':
    unittest.main()
