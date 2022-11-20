"""
Test custom Django management commands
"""

from unittest.mock import patch  # Mock behavior of the database

# Possible errors to get before db is ready during connection
from psycopg2 import OperationalError as Psycopg2Error

# Helps to call commands by name (**simulate)
# helper function to call comand by the name
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Check helps to check status of the db
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # When check is call return true
        patched_check.return_value = True

        # execute code in wait_for_db. Check if db is
        # ready and check if cmd is set up correctly.
        call_command('wait_for_db')

        # ensures the mock value(check in our cmd) is
        # called with the right param
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [
            Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
