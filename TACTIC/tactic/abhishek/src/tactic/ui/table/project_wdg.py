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

__all__ = ['ProjectWdg', 'ProjectTemplateUpdateWdg']

from pyasm.common import Environment
from pyasm.search import DbContainer, Search
from pyasm.web import Widget, Table, HtmlElement, WebContainer
from pyasm.widget import IconWdg, IconButtonWdg
from button_wdg import ButtonElementWdg
from tactic.ui.common import BaseTableElementWdg
from button_wdg import ButtonElementWdg

class ProjectWdg(BaseTableElementWdg):

    def get_title(my):
        return "Database"

    def preprocess(my):
        my.version = Environment.get_release_version()

    def get_width(my):
        return 100

    def get_display(my):

        widget = Widget()

        project = my.get_current_sobject()

        table = Table()
        widget.add(table)
        table.add_style("width: 140px")

        table.add_row()
        table.add_cell("Exists: ")
        table.add_cell("&nbsp;")


        try:
            exists = project.database_exists()
        except:
            #print "Error checking if database exists for project [%s]" % project.get_code()
            exists = False

        if exists:
            table.add_cell( IconWdg("database", IconWdg.DOT_GREEN) )
        else:
            table.add_cell( IconWdg("database", IconWdg.DOT_RED) )


        table.add_row()
        table.add_cell("Version: ")
        last_version_update = project.get_value("last_version_update")
        table.add_cell( last_version_update)
        if last_version_update >= my.version:
            table.add_cell( IconWdg("database", IconWdg.DOT_GREEN) )
        else:
            table.add_cell( IconWdg("database", IconWdg.DOT_RED) )

        widget.add("<br/>")
 
        """
        widget.add("Schema: ")
        widget.add("<br/>")

        widget.add("Context: ")
        widget.add("<br/>")

        widget.add("Data: ")
        widget.add("<br/>")
        """

        return widget



class ProjectTemplateUpdateWdg(ButtonElementWdg):
    '''Update the template project zip file in the system'''
    def get_title(my):
        return "Update"

  
    def preprocess(my):

        icon = my.kwargs.get('icon')
        icon_link = eval("IconWdg.%s" % icon.upper() )
        my.kwargs['icon_tip'] = "Update Template"
        my.kwargs['cbjs_action'] = '''
         var row = bvr.src_el.getParent(".spt_table_row");

        try {
             var server = TacticServerStub.get();
             var search_key = row.getAttribute("spt_search_key");
             var proj = server.get_by_search_key(search_key);
             var proj_code = proj['code'];
             var ok = function(proj_code) {
               var server = TacticServerStub.get();
               var cmd = 'tactic.command.ProjectTemplateCreatorCmd';
               server.execute_cmd(cmd, {project_code: proj_code});
               
               spt.notify.show_message('Updating of Template project [' + proj_code + '] completed.');
            };
             var cancel = null;
             spt.confirm("Update the template project zip file for [" + proj_code + "]?", ok, cancel, {ok_args: proj_code} );

        } catch(e) {
            spt.alert(spt.exception.handler(e));
        }
        

          
        '''
        super(ProjectTemplateUpdateWdg, my).preprocess()
  
