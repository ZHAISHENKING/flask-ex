#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
from flask import current_app


class MongoConnection():
    def __init__(self):
        MON_URL = "127.0.0.1:27017"
        client = pymongo.MongoClient(MON_URL)
        DATABASE_NAME = current_app.config['MONGO_DB']
        self.db = client[DATABASE_NAME]
        self.colls_name = self.db.collection_names()

    def sure_db_in_collo(self, name):
        if name not in self.colls_name:
            return False
        return True

class TagsApi(MongoConnection):
    def __init__(self):
        super().__init__()
        self.__tag_name_list = []
        self.__tag_get_count_list = []

    def _get_tags(self):

        db_coll_name = 'tags'
        if super().sure_db_in_collo(db_coll_name):
            db_coll = self.db[db_coll_name]
            projection_fields = {'_id': False, 'name': True, 'get_count': True}
            return db_coll.find(projection=projection_fields)
        return None

    @property
    def get_tags(self):
        result = self._get_tags()
        for tag in result:
            self.__tag_name_list.append(tag['name'])
            self.__tag_get_count_list.append(tag['get_count'])
        tags_list = (self.__tag_name_list, self.__tag_get_count_list)
        return tags_list


class UserApi(MongoConnection):
    def __init__(self):
        super().__init__()
        self.__user_name_list = []
        self.__user_post_number = []

    def _get_user(self):
        db_coll_name = 'user'
        if super().sure_db_in_collo(db_coll_name):
            db_coll = self.db[db_coll_name]
            projection_fields = {'_id': False, 'name': True, 'post_number': True}
            return db_coll.find(projection=projection_fields)

    @property
    def get_user(self):
        result = self._get_user()
        for tag in result:
            self.__user_name_list.append(tag['name'])
            self.__user_post_number.append(tag['post_number'])
        user_list = (self.__user_name_list, self.__user_post_number)
        return user_list