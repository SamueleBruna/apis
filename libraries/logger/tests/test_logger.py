import unittest
import logging

from unittest.mock import patch
from pathlib import Path
from logger.logger import Logger  # Replace with your script path


# TODO: improve test_log_messages_complete test
class TestConfigReading(unittest.TestCase):

    @patch('configparser.ConfigParser.read')
    def test_config_read_success(self, mock_read):
        # Mock successful reading of the config file
        mock_read.return_value = []
        path = Path(__file__).parent.parent / Path("src/logger/logger.py") / Path("../../../config/logging.ini")
        logger = Logger()
        self.assertEqual(logger.config_file, path)

    @patch('configparser.ConfigParser.read')
    def test_config_read_failure(self, mock_read):
        # Mock config file read failure (e.g., file not found)
        mock_read.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            Logger()

    @patch('logging.getLogger')
    def test_log_level_debug(self, mock_getLogger):
        """
        Mock logger creation and set level to DEBUG The return_value attribute of a mock object specifies what
        value the mock object will return when it's called. we assign to the mock_logger the ability to store and
        return what will be returned from return mock_getLogger, when Logger constructor is invoked. In particular,
        we want to test the correctness when we set the severity level. So we test the method setLevel, and we tell
        it, when it's called (called_with) to match any argument passed to the method (unittest.mock.ANY).
        """

        mock_logger = mock_getLogger.return_value
        mock_logger.setLevel.called_with = unittest.mock.ANY
        logger = Logger(Path(__file__) / Path("../config/logging_debug.ini"))
        logger.debug('Test debug message')
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)

    @patch('logging.getLogger')
    def test_log_level_info(self, mock_getLogger):
        # Mock logger creation and set level to INFO
        mock_logger = mock_getLogger.return_value
        mock_logger.setLevel.called_with = unittest.mock.ANY
        logger = Logger(Path(__file__) / Path("../config/logging_info.ini"))
        logger.info('Test info message')
        mock_logger.setLevel.assert_called_once_with(logging.INFO)

    @patch('logging.getLogger')
    def test_log_level_warning(self, mock_getLogger):
        # Mock logger creation and set level to WARNING
        mock_logger = mock_getLogger.return_value
        mock_logger.setLevel.called_with = unittest.mock.ANY
        logger = Logger(Path(__file__) / Path("../config/logging_warning.ini"))
        logger.error('Test warning message')
        mock_logger.setLevel.assert_called_once_with(logging.WARNING)

    @patch('logging.getLogger')
    def test_log_level_error(self, mock_getLogger):
        # Mock logger creation and set level to ERROR
        mock_logger = mock_getLogger.return_value
        mock_logger.setLevel.called_with = unittest.mock.ANY
        logger = Logger(Path(__file__) / Path("../config/logging_error.ini"))
        logger.error('Test error message')
        mock_logger.setLevel.assert_called_once_with(logging.ERROR)

    @patch('logging.getLogger')
    def test_log_level_critical(self, mock_getLogger):
        # Mock logger creation and set level to CRITICAL
        mock_logger = mock_getLogger.return_value
        mock_logger.setLevel.called_with = unittest.mock.ANY
        logger = Logger(Path(__file__) / Path("../config/logging_critical.ini"))
        logger.critical('Test critical message')
        mock_logger.setLevel.assert_called_once_with(logging.CRITICAL)

    @patch('logging.getLogger')
    def test_log_messages_complete(self, mock_getLogger):
        """
        Mock logger creation and capture logged messages. The return_value attribute of a mock object specifies what
        value the mock object will return when it's called. We assign to the mock_logger the ability to store and
        return what will be returned from return mock_getLogger, when Logger constructor is invoked. In particular,
        we want to test if the functions debug, info, warning, error and critical return correctly a message. So we
        test the methods by mocking them with the function capture_message when invoked (instead of returning
        self.logger.debug(message)). capture message just appends the string to a list.
        """
        captured_messages = []

        def capture_message(message):
            captured_messages.append(message)

        mock_logger = mock_getLogger.return_value
        mock_logger.debug = capture_message
        mock_logger.info = capture_message
        mock_logger.warning = capture_message
        mock_logger.error = capture_message
        mock_logger.critical = capture_message

        logger = Logger()

        # Test debug message, the string is passed as message
        logger.debug('Test debug message')
        self.assertEqual(captured_messages, ['Test debug message'])

        # Clear captured messages for other tests
        captured_messages.clear()

        # Test info message
        logger.info('Test info message')
        self.assertEqual(captured_messages, ['Test info message'])

        # Clear captured messages for other tests
        captured_messages.clear()

        # Test warning message
        logger.warning('Test warning message')
        self.assertEqual(captured_messages, ['Test warning message'])

        # Clear captured messages for other tests
        captured_messages.clear()

        # Test error message
        logger.error('Test error message')
        self.assertEqual(captured_messages, ['Test error message'])

        # Clear captured messages for other tests
        captured_messages.clear()

        # Test critical message
        logger.critical('Test critical message')
        self.assertEqual(captured_messages, ['Test critical message'])


if __name__ == '__main__':
    unittest.main()
