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
The main.py module implements the FastAPI endpoints which allow interaction 
over REST calls.
"""
from fastapi import FastAPI, HTTPException
from src.body import Note, NoteIdentifier
from src.configuration import Configuration
from src.storage import Storage


storage = Storage(Configuration())
app = FastAPI()


@app.post("/add/")
async def add_note(note: Note):
    """
    Add a new user value.

    Args:
        note (Note): The note to add.
    
    Returns:
        NoteIdentifier: The identification for the added note.
        None: If the note could not be added.
    """
    try:
        return NoteIdentifier(uuid=storage.add_note(note=note))
    except Exception as e:
        raise HTTPException(status_code=500) from e


@app.get("/get/{uuid}")
async def get_note(uuid: str):
    """
    Get a stored note.

    Args:
        uuid (uuid): The UUID of the note.

    Returns:
        Note: The selected note.
        None: If no note was selected.
    """
    try:
        return storage.get_note(uuid=uuid)
    except Exception as e:
        raise HTTPException(status_code=500) from e
