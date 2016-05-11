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


__all__ = ['UndoLogWdg']

from pyasm.common import Date, Xml, Common, Environment
from pyasm.command import Command, CommandExitException
from pyasm.search import TransactionLog, SearchType, Search
from pyasm.web import DivWdg, Table, SpanWdg, WebContainer
from pyasm.widget import FilterSelectWdg, IconRefreshWdg, CheckboxWdg, DateSelectWdg, DateTimeWdg
from pyasm.biz import Project



class UndoLogWdg(DivWdg):
    def __init__(my, is_refresh=False):
        super(UndoLogWdg,my).__init__()
        my.all_users_flag = False
        my.all_namespaces_flag = False
        my.add_class("spt_panel")
        my.add_attr("spt_class_name", Common.get_full_class_name(my) )

    def set_all_namespaces(my, flag=True):
        my.all_namespaces_flag = flag

    def set_all_users(my, flag=True):
        my.all_users_flag = flag
        

    def set_admin(my):
        my.set_all_namespaces()
        my.set_all_users()


    def get_display(my):

        #WebContainer.register_cmd("pyasm.admin.UndoLogCbk")

        # add a time filter
        div = DivWdg()
        div.add_color('background','background', -10)
        div.add_color('color','color')
        div.add_style("padding: 15px")
        div.add_border()
        project = ''
        # add a project filter
        if my.all_namespaces_flag:
            span = SpanWdg("Project: ")
            span.add_color('color','color')
            project_select = FilterSelectWdg("project")
            project_select.add_empty_option(label="-- All Projects --")
            project_select.set_option("query", "sthpw/project|code|title")
            span.add(project_select)
            div.add(span)

            project = project_select.get_value()
        else:
            from pyasm.biz import Project
            project = Project.get_global_project_code()


        # add a time filter
        from pyasm.prod.web import DateFilterWdg
        select = DateFilterWdg("undo_time_filter", label="Show Transaction Log From: ")
        select.set_label(["1 Hour Ago", "Today", "1 Day Ago", "1 Week Ago", "1 Month Ago"])
        select.set_value(["1 Hour", "today", "1 Day", "1 Week", "1 Month"])
        select.set_option("default", "1 Hour")
        div.add(select)

        time_interval = select.get_value() 

        my.add(div)

        if not my.all_users_flag:
            user = Environment.get_user_name()
        else:
            span = SpanWdg(css="med")
            span.add("User: ")
            user_select = FilterSelectWdg("user")
            user_select.set_option("query", "sthpw/login|login|login")
            user_select.add_empty_option()
            span.add(user_select)
            div.add(span)

            user = user_select.get_value()

        transaction_log = TransactionLog.get( user_name=user, \
            namespace=project, time_interval=time_interval)

        from tactic.ui.panel import FastTableLayoutWdg, TableLayoutWdg
        table = FastTableLayoutWdg(search_type="sthpw/transaction_log", view="table", show_shelf='false', show_select="false")
        #table = TableLayoutWdg(search_type="sthpw/transaction_log", view="table", mode='simple', show_row_select="false")
        table.set_sobjects(transaction_log)
        #table.set_refresh_mode("table")
        my.add(table)

        return super(UndoLogWdg, my).get_display()


# TODO: this code is commented out until such a time as a better solution is
# found.  It is hightly questionable whether it is desireable to allow users
# to undo a previous command outside the order of the stack.  This may leave
# the database in an unstable state (deleting sobjects that have dependencies
# on them)
"""
class UndoLogCbk(Command):

    def get_title(my):
        return "Undo Log Command"

    def check(my):
        web = WebContainer.get_web()
        return True

    def execute(my):
        
        web = WebContainer.get_web()
        transaction_ids = web.get_form_values("transaction_log_id")
        if not transaction_ids:
            return

        search = Search(TransactionLog.SEARCH_TYPE)
        search.add_filters("id", transaction_ids)
        transactions = search.get_sobjects()

        # start with just the first one
        transaction = transactions[0]

        transaction.undo()

        my.description = "Undo #%s: %s" % (transaction.get_id(), transaction.get_value("description") )
"""
        


        

         








