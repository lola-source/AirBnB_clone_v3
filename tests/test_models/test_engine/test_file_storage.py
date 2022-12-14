#!/usr/bin/python3
'''
    Testing the file_storage module.
'''

import os
import time
import json
import unittest
import models
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.engine.file_storage import FileStorage
from models import User

db = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db == 'db', "Testing DBstorage only")
class testFileStorage(unittest.TestCase):
    '''
        Testing the FileStorage class
    '''

    def setUp(self):
        '''
            Initializing classes
        '''
        self.storage = FileStorage()
        self.my_model = BaseModel()

    def tearDown(self):
        '''
            Cleaning up.
        '''

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_return_type(self):
        '''
            Tests the data type of the return value of the all method.
        '''
        storage_all = self.storage.all()
        self.assertIsInstance(storage_all, dict)

    def test_new_method(self):
        '''
            Tests that the new method sets the right key and value pair
            in the FileStorage.__object attribute
        '''
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        self.assertTrue(key in self.storage._FileStorage__objects)

    def test_objects_value_type(self):
        '''
            Tests that the type of value contained in the FileStorage.__object
            is of type obj.__class__.__name__
        '''
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        val = self.storage._FileStorage__objects[key]
        self.assertIsInstance(self.my_model, type(val))

    def test_save_file_exists(self):
        '''
            Tests that a file gets created with the name file.json
        '''
        self.storage.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_save_file_read(self):
        '''
            Testing the contents of the files inside the file.json
        '''
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = json.load(fd)

        self.assertTrue(isinstance(content, dict))

    def test_the_type_file_content(self):
        '''
            testing the type of the contents inside the file.
        '''
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = fd.read()

        self.assertIsInstance(content, str)

    def test_reaload_without_file(self):
        '''
            Tests that nothing happens when file.json does not exists
            and reload is called
        '''

        try:
            self.storage.reload()
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_delete(self):
        '''
            Test delete method
        '''
        fs = FileStorage()
        new_state = State()
        fs.new(new_state)
        state_id = new_state.id
        fs.save()
        fs.delete(new_state)
        with open("file.json", encoding="UTF-8") as fd:
            state_dict = json.load(fd)
        for k, v in state_dict.items():
            self.assertFalse(state_id == k.split('.')[1])

    def test_model_storage(self):
        '''
            Test State model in Filestorage
        '''
        self.assertTrue(isinstance(storage, FileStorage))

    def test_get_fs(self):
        """Testing the get method in file_storage
        """
        fs = FileStorage()
        self.assertIs(fs.get("User", "test"), None)
        self.assertIs(fs.get("test", "randon"), None)
        new_state = State()
        new_user = User()
        new_user.save()
        self.assertIs(fs.get("User", new_user.id), new_user)
        fs.new(new_state)
        first_state_id = list(storage.all("State").values())[0].id
        self.assertEqual(type(storage.get("State", first_state_id)), State)

    def test_count_file(self):
        """
        Testing thecount method in file_storage
        """
        storage.reload()
        fs = FileStorage()
        initial_len = len(storage.all())
        self.assertEqual(storage.count(), initial_len)
        state = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state)
        result = storage.all("")
        count = storage.count(None)
        self.assertEqual(len(result), count)
        result = storage.all("State")
        count = storage.count("State")
        self.assertEqual(len(result), count)

    def test_filestorage_count(self):
        '''
            Tests the count method
        '''
        all_obj = models.storage.all()
        count_all_obj = models.storage.count()
        self.assertEqual(len(all_obj), count_all_obj)

    def test_filestorage_count_cls(self):
        '''
            Tests the count method with class name
        '''
        all_obj = models.storage.all('State')
        count_all_obj = models.storage.count('State')
        self.assertEqual(len(all_obj), count_all_obj)

    def test_get_method_cls(self):
        '''
            Tests the get method with class name and id given
        '''
        state = State(name='Texas')
        state.save()
        state_id = state.id
        get_state = models.storage.get('State', state_id)
        self.assertEqual(state, get_state)

    def test_get_method(self):
        '''
            Tests the get method
        '''
        get_state = models.storage.get('State', '12343')
        self.assertEqual(get_state, None)

    def test_storage_count(self):
        storage = FileStorage()
        initial_length = len(storage.all())
        self.assertEqual(storage.count(), initial_length)
        state_len = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), initial_length + 1)
        self.assertEqual(storage.count("State"), state_len + 1)

    def test_storage_get(self):
        """Test that the get method properly retrievs objects"""
        storage = FileStorage()
        self.assertIs(storage.get("User", "blah"), None)
        self.assertIs(storage.get("blah", "blah"), None)
        new_user = User()
        new_user.save()
        self.assertIs(storage.get("User", new_user.id), new_user)

    def test_all_returns_storage(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)
