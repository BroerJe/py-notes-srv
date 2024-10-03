#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the py-notes-srv Project.
# See AUTHORS file for copyright information.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
The storage.py module is used to both read and write notes to a implemented 
persistent storage.
"""
import sqlite3
from uuid import uuid4
from warnings import warn
from src.configuration import Configuration
from src.body import Note


class Storage:
    """
    This class handles the notes database and allows for both inserting and 
    retrieving of content.
    """
    _DB_TABLE_NAME = "notes"


    def __init__(self, configuration: Configuration):
        """
        Initialize the class.

        Args:
            self (Storage): The instance to initialize.
        """
        self._connection = sqlite3.connect(configuration.db_path)
        self._cursor = self._connection.cursor()


    def _ensure_table(self, create) -> bool:
        """
        Ensure that a table exists for the notes, and create it if needed.

        Args:
            self (Storage): The instance to use.
            create(bool): If the table should be created if it is missing.

        Returns:
            bool: True if the database table is available, False if not.
        """
        res = None

        try:
            res = self._cursor.execute(
                f"""
                SELECT name 
                FROM sqlite_master 
                WHERE name="{self._DB_TABLE_NAME}"
                """)
        except:
            warn("Failed to perform select from table!")

        if res.fetchone() is not None:
            return True
        elif create is False:
            return False

        try:
            res = self._cursor.execute(
                f"""
                CREATE TABLE "{self._DB_TABLE_NAME}" (uuid, content, unix_time_s)
                """)

            # Make sure that table exists after function
            self._connection.commit()
            return True
        except:
            warn("Failed to insert table into database!")

        # Exception, end etc -> At this point we failed
        return False


    def get_note(self, uuid: str) -> Note | None:
        """
        Return a note for a given UUID.

        Args:
            self (Storage): The instance to use.
            uuid (str): The UUID which identifies the note.

        Returns:
            Note: The note to return.
            None: If no note was found.
        """
        # Does the required table exist? We can simply return nothing if not,
        # but the table should not be created (DB might be spammed otherwise)
        if self._ensure_table(False) is False:
            return None

        try:
            # Get all matches, and return the first one
            res = self._cursor.execute(
                f"""
                SELECT uuid, content, unix_time_s
                FROM "{self._DB_TABLE_NAME}"
                WHERE uuid LIKE "%{uuid}%"
                """)

            for row in res:
                return Note(
                    content=row[1],
                    unixTimeS=row[2])
        except:
            warn("Could not read table content!")

        # Failure
        return None


    def add_note(self, note: Note) -> str | None:
        """
        Add a new note, either creating or expanding a database table.

        Args:
            self (Storage): The instance to use.
            note (Note): The note to add.

        Returns:
            str: The UUID of the newly inserted note.
            None: If no note was inserted.
        """
        # We need to make sure that our table exists, which also means
        # that we need to create a new empty table if missing
        if self._ensure_table(True) is False:
            warn("Could not ensure existence of table!")
            return

        # Roll a new UUID for identification
        # We rely on the DB to show any issues
        uuid = str(uuid4())

        try:
            self._cursor.execute(
                f"""
                INSERT INTO "{self._DB_TABLE_NAME}"
                VALUES ("{uuid}", "{note.content}", {note.unixTimeS})
                """)

            # Always commit, we only get single values from requests
            # The next valie to commit might not come for a while
            self._connection.commit()

            # Return the UUID of the newly inserted note
            return uuid
        except:
            warn("Could not insert note into table!")

        # Default assumes failure, return empty
        return None
