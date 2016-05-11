###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#

__all__ = ["UndoCmd", "RedoCmd"]


from pyasm.common import *
from pyasm.biz import Project
from pyasm.search import *

from command import *

class UndoCmd(Command):

    def __init__(my, ignore_files=False, is_sync=True, transaction_log=None):
        super(UndoCmd,my).__init__()
        my.transaction_log = transaction_log
        my.ignore_files = ignore_files
        my.is_sync = is_sync


    def get_title(my):
        return "Undo"

    def is_undoable(cls):
        return False
    is_undoable = classmethod(is_undoable)



    def check(my):
        return True

    def set_transaction_log(my, transaction_log):
        '''manually set the translation log'''
        my.transaction_log = transaction_log

    def set_transaction_id(my, transaction_id):
        '''manually set the translation id'''
        my.transaction_log = Search.get_by_id("sthpw/transaction_log", transaction_id)
        if not my.transaction_log:
            raise CommandException("Transaction with id [%s] does not exist" % transaction_id)


    def set_transaction_code(my, transaction_code):
        '''manually set the translation code'''
        my.transaction_log = Search.get_by_code("sthpw/transaction_log", transaction_code)
        if not my.transaction_log:
            raise CommandException("Transaction with code [%s] does not exist" % transaction_code)




    def execute(my):
        if not my.transaction_log:
            search = Search("sthpw/transaction_log")
            search.add_filter("type", "undo")

            # get the current project.  If the project is admin, then undo
            # works differently
            project = Project.get_global_project_code()
            assert project
            search.add_filter("namespace", project)

            user = Environment.get_user_name()
            assert user
            search.add_filter("login", user)

            search.add_order_by("timestamp desc")

            search.add_limit(1)
            my.transaction_log = search.get_sobject()

        if not my.transaction_log:
            print("WARNING: No transaction log found for undo")
            return CommandExitException()

        my.transaction_log.undo(ignore_files=my.ignore_files)

        my.transaction_log.set_value("type", "redo")
        my.transaction_log.commit()

        # undo triggers a special sync
        # if this is a sync undo, then do not propgate remote undos
        if not my.is_sync:
            my.transaction_log.trigger_remote_undo()




class RedoCmd(Command):

    def __init__(my,**kwargs):
        super(RedoCmd,my).__init__()
        my.kwargs = kwargs
        my.transaction_log = my.kwargs.get("transaction_log")
        my.ignore = my.kwargs.get("ignore")
        if not my.ignore:
            my.ignore = []

    def get_title(my):
        return "Redo"

    def is_undoable(cls):
        return False
    is_undoable = classmethod(is_undoable)


    def check(my):
        #from pyasm.web import WebContainer
        #web = WebContainer.get_web()
        #if web.get_form_value("Redo") != "":
        return True

    def set_transaction_log(my, transaction_log):
        '''manually set the translation log to undo'''
        my.transaction_log = transaction_log


    def get_transaction_log(my):
        '''get the transaction log'''
        return my.transaction_log



    def set_transaction_id(my, transaction_id):
        '''manually set the translation id'''
        my.transaction_log = Search.get_by_id("sthpw/transaction_log", transaction_id)
        if not my.transaction_log:
            raise CommandException("Transaction with id [%s] does not exist" % transaction_id)


    def set_transaction_code(my, transaction_code):
        '''manually set the translation code'''
        my.transaction_log = Search.get_by_code("sthpw/transaction_log", transaction_code)
        if not my.transaction_log:
            raise CommandException("Transaction with code [%s] does not exist" % transaction_code)




    def execute(my):
        import time
        start = time.time()

        security = Environment.get_security()
        ticket = security.get_ticket_key()

        if not my.transaction_log:
            search = Search("sthpw/transaction_log")
            search.add_filter("type", "redo")

            # get the current project
            project = Project.get_global_project_code()
            search.add_filter("namespace", project)

            user = Environment.get_user_name()
            search.add_filter("login", user)

            search.add_order_by("timestamp")
            search.add_limit(1)

            my.transaction_log = search.get_sobject()

        if not my.transaction_log:
            return CommandExitException()

        base_dir = my.kwargs.get("base_dir")

        my.transaction_log.redo(ignore=my.ignore, base_dir=base_dir)
        my.transaction_log.set_value("type", "undo")
        my.transaction_log.commit()

        # get the transaction and set it to not record this transaction
        transaction = Transaction.get()
        transaction.set_record(False)

        # update the change timestamps
        transaction.update_change_timestamps(my.transaction_log)

        print "RedoCmd: ", time.time() - start
        print




