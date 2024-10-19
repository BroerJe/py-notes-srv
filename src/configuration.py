#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the py-notes-srv project.
# See the included AUTHORS file for copyright information.
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
The configuration.py module provides a "Configuration" class which can be used 
to load and store values from a configuration file.
"""
import os
import json


class Configuration:
    """
    The configuration class stores all service configuation.
    """
    _ENV_VAR_NAME = "PY_NOTES_SRV_CONFIGURATION"


    def __init__(self):
        """
        Initialize the class.

        Args:
            self (Configuration): The instance to initialize.
        """
        path = os.getenv(self._ENV_VAR_NAME, "/var/py-notes-srv/configuration.json")

        try:
            content = json.load(open(path, "r", encoding="utf-8"))
            self.db_path = content.get("dbPath") or "/var/py-notes-srv/user_values.db"
        except Exception as e:
            raise FileNotFoundError(
                f"""
                Could not open configuration file at {path}. You either forgot
                to set the {self._ENV_VAR_NAME} environment variable, or the
                file does not exist.
                """) from e
