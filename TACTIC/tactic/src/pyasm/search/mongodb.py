###########################################################
#
# Copyright (c) 2013, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#


__all__ = ['MongoDbConn', 'MongoDbImpl']

from pyasm.common import Environment, SetupException, Config, Container, TacticException

from database_impl import DatabaseImplException, DatabaseImpl


try:
    import bson
    import pymongo
    pymongo.OperationalError = Exception
    pymongo.Error = Exception
except ImportError, e:
    pass



class MongoDbConn(object):
    '''A wrapper class around a MongoDb connection to conform to the interface
    required by the Sql class'''


    def __init__(my, database_name):
        my.database_name = database_name

        my.client = pymongo.MongoClient()
        my.conn = my.client[database_name]


    def get_client(my):
        return my.client

    def get_collection(my, table):
        return my.conn[table]

    def collection_names(my):
        return my.conn.collection_names()


    def cursor(my):
        return {}

    def connect(my):
        pass

    def commit(my):
        pass

    def rollback(my):
        pass

    def close(my):
        pass
        #my.client.disconnect()






class MongoDbImpl(DatabaseImpl):

    def get_database_type(my):
        return "MongoDb"

    def get_id_col(my, db_resource, search_type):
        return "_id"


    def get_code_col(my, db_resource, search_type):
        return "code"



    def create_database(my, database):
        '''create a database
        In MongoDb, databases are dynamically created so there is no need
        for a function to create a database to do anything
        '''
        #from sql import DbContainer, DbResource
        #db_resource = DbResource.get_default("")
        #sql = DbContainer.get(db_resource)
        #conn = sql.get_connection()
        pass


    def get_default_columns(my):
        return ['code','name','description']


    def get_columns(cls, db_resource, table):
        from pyasm.search import DbResource, DbContainer
        sql = DbContainer.get(db_resource)
        conn = sql.get_connection()
        collection = conn.get_collection(table)

        # FIXME:
        # This just gets the first one to discover the columns.  This is
        # not accurate because each item in a collection can contain
        # different "attributes". The key here is to define a location
        # for where this "schema" description is stored
        result = collection.find_one()
        if not result:
            return ['_id']
        else:
            columns = result.keys()

            # assume existence of both code and _id
            #if "code" in columns:
            #    columns.remove("code")
            #columns.insert(0, "code")

            if "_id" in columns:
                columns.remove("_id")
            columns.insert(0, "_id")


            return columns


    def get_column_info(cls, db_resource, table, use_cache=True):

        #info_dict = {'data_type': data_type, 'nullable': is_nullable, 'size': size}
        # TODO: use a collection spt_schema


        columns = cls.get_columns(db_resource, table)
        info_dict = {}
        for column in columns:
            if column == "_id":
                info = {'data_type': 'bson.objectid'}
            elif column == "code":
                info = {'data_type': 'varchar'}
            else:
                info = {}
            info_dict[column] = info

        return info_dict


    def get_table_info(my, database):

        from pyasm.search import DbResource, DbContainer
        sql = DbContainer.get(database)
        conn = sql.get_connection()
        collections = conn.collection_names()

        table_info = {}
        for collection in collections:
            table_info[collection] = { }

        return table_info



    def is_column_sortable(my, db_resource, table, column):
        # All columns are sortable in MongoDb
        return True



    def table_exists(my, db_resource, table):
        sql = db_resource.get_sql()
        conn = sql.get_connection()
        collections = conn.collection_names()
        if table in collections:
            return True
        else:
            return False


    def has_savepoint(my):
        return False


    def has_sequences(my):
        return False



    def build_filters(cls, filters):
        # interpret the assmebled filter data
        nosql_filters = {}
        for filter in filters:
            column = filter.get("column")
            value = filter.get("value")
            op = filter.get("op")

            if column == "_id" and value not in [-1, '-1']:
                if isinstance(value, list):
                    values = []
                    for x in value:
                        try:
                            tmp = bson.ObjectId(str(x))
                            values.append(tmp)
                        except Exception, e:
                            print "WARNING: ", e
                    value = values
                elif not isinstance(value, bson.ObjectId):
                    value = bson.ObjectId(str(value))

            if op == "=":
                nosql_filters[column] = value
            else:
                if op in ["<","$lt"]:
                    mongo_op = "$lt"
                elif op in ["<=","$lte"]:
                    mongo_op = "$lte"
                elif op in [">=","$gte"]:
                    mongo_op = "$gte"
                elif op in [">" or "$gt"]:
                    mongo_op = "$gt"
                elif op in ["!=","$ne"]:
                    mongo_op = "$ne"
                elif op in ["in", "$in"]:
                    mongo_op = "$in"

                elif op in ["not in", "nin", "$nin"]:
                    mongo_op = "$nin"
                elif op in ["all", "$all"]:
                    mongo_op = "$all"
                elif op in ["==", "=", "is"]:
                    mongo_op = ""

                elif not op:
                    pass
                else:
                    raise Exception("Filter operator [%s] is not supported" % op)
                if not op:
                    nosql_filters[column] = value
                else:
                    nosql_filters[column] = {mongo_op: value}

        return nosql_filters
    build_filters = classmethod(build_filters)



    def execute_query(my, sql, select):
        '''Takes a select object and operates
        
        NOTE: this requires a lot of internal knowledge of the Select object 
        '''
        conn = sql.get_connection()

        # select data
        table = select.tables[0]
        filters = select.raw_filters
        order_bys = select.order_bys
        limit = select.limit
        offset = select.offset

        collection = conn.get_collection(table)

        nosql_filters = my.build_filters(filters)
        cursor = collection.find(nosql_filters)

        select.cursor = cursor

        if order_bys:
            sort_list = []
            for order_by in order_bys:
                parts = order_by.split(" ")
                order_by = parts[0]
                if len(parts) == 2:
                    direction = parts[1]
                else:
                    direction = "asc"

                if direction == "desc":
                    sort_list.append( [order_by, -1] )
                else:
                    sort_list.append( [order_by, 1] )

                cursor.sort(sort_list)


        if limit:
            cursor.limit(limit)
        if offset:
            cursor.skip(offset)

        results = []
        for result in cursor:
            results.append(result)

        return results


    def execute_update(my, sql, update):
        conn = sql.get_connection()

        # select data
        table = update.table
        data = update.data
        filters = update.raw_filters

        collection = conn.get_collection(table)
        nosql_filters = my.build_filters(filters)
        item = collection.find_one(nosql_filters)


        result = collection.update( {'_id': item.get('_id')}, {'$set': data} )

        err = result.get("err")
        if err:
            raise Exception(result)

        # FIXME: Hacky ... should make use of return value below
        sql.last_row_id = item.get("_id")

        return sql.last_row_id





    def execute_insert(my, sql, update):

        conn = sql.get_connection()

        # select data
        table = update.table
        data = update.data
        if table == "search_object":
            dada

        if data.get("_id") in ["-1", -1, '']:
            del(data['_id'])

        collection = conn.get_collection(table)
        object_id = collection.insert(data)

        sql.last_row_id = object_id




    def execute_delete(my, sql, table, id):
        conn = sql.get_connection()

        collection = conn.get_collection(table)

        collection.remove( {"_id": id} )






    def execute_create_table(my, sql, create):

        conn = sql.get_connection()

        # select data
        table = create.table
        data = create.data

        # data will some something like:
        # data = {
        #    column': 'code', 
        #    data_type': 'integer', 
        #    nullable': True, 

        # because there is no explicit schema definition for each collection,
        # something has to state what is inside a collection.  The current
        # approach simply stores this info in a collection called "spt_schema"

        collection = conn.get_collection("spt_schema")

        item = collection.find_one({ 'table': table })
        if item:
            print "Entry for [%s] already exists" % table
            return

        item_data = {
            'table': table,
            'data': data
        }

        object_id  = collection.insert(data)

        return object_id





