"""This file implements the actions with game (save, load, scoreboard)"""
import pickle
import json
from operator import itemgetter
from collections import OrderedDict
from core import *


def save_in_file(field, filename):
    """Save game in file"""
    with open(filename, "wb") as file:
        pickle.dump(field, file)


def load_from_file(filename):
    """Load game from file"""
    with open(filename, 'rb') as file:
        field = pickle.load(file)
        if not isinstance(field, Field):
            raise LoadError()
        return field


def add_record(player_name, score):
    """Add a new entry to the record table"""
    try:
        file = open('records.json', 'r', encoding='utf-8')
        records = json.load(file)
        file.close()
        if records.get(player_name) is None or records.get(player_name) < score:
            records.update({player_name: score})
            sorted_records = OrderedDict(sorted(records.items(), key=lambda y: y[1], reverse=True))
            records.clear()
            records.update(sorted_records)
            file = open('records.json', 'w', encoding='utf-8')
            json.dump(records, file, indent=4)
            file.close()
        if len(records) > 8:
            sorted_records = OrderedDict(sorted(records.items(), key=lambda y: y[1], reverse=True))
            sorted_records.popitem()
            records.clear()
            records.update(sorted_records)
    except FileNotFoundError:
        file = open('records.json', 'w', encoding='utf-8')
        records = {}
        records.update({player_name: score})
        json.dump(records, file, indent=4)
        file.close()
    except Exception as exception:
        raise AddRecordError(exception)


def get_records():
    """Get record from file"""
    try:
        with open('records.json', 'r', encoding='utf-8') as file:
            records = json.load(file)
            return records
    except Exception as exception:
        raise GetRecordsError(exception)


class AddRecordError(Exception):
    """Can not add record error"""
    pass


class GetRecordsError(Exception):
    """Can not get records error"""
    pass

class LoadError(Exception):
    """Load game from file exception"""
    pass