###########################################################
#
# Copyright (c) 2014, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#


__all__ = ['SandboxSelectWdg']

from pyasm.common import Environment, jsonloads, jsondumps, Config
from pyasm.biz import Project
from pyasm.web import DivWdg, Table, WidgetSettings
from tactic.ui.common import BaseRefreshWdg
from pyasm.widget import IconWdg, RadioWdg
from tactic.ui.widget import IconButtonWdg

from pyasm.search import Search, SearchType

class SandboxSelectWdg(BaseRefreshWdg):


    def get_display(my):

        top = my.top
        top.add_class("spt_sandbox_select_top")

        sandbox_options = [
                {
                    'name': 'fast',
                    'base_dir': 'C:/Fast',
                },
                {
                    'name': 'faster',
                    'base_dir': 'C:/Faster',
                },
                {
                    'name': 'slow',
                    'base_dir': 'Z:/Slow',
                }
        ]

        process = my.kwargs.get("process")

        search_key = my.kwargs.get("search_key")
        sobject = Search.get_by_search_key(search_key)


        search_type = sobject.get_base_search_type()

        client_os = Environment.get_env_object().get_client_os()
        if client_os == 'nt':
            prefix = "win32"
        else:
            prefix = "linux"
        alias_dict = Config.get_dict_value("checkin", "%s_sandbox_dir" % prefix)

        search_key = sobject.get_search_key()
        key = "sandbox_dir:%s" % search_key
        from pyasm.web import WidgetSettings
        value = WidgetSettings.get_value_by_key(key)


        sandboxes_div = DivWdg()
        top.add(sandboxes_div)

        sandboxes_div.add_relay_behavior( {
            'type': 'mouseenter',
            'bvr_match_class': 'spt_sandbox_option',
            'cbjs_action': '''
            var last_background = bvr.src_el.getStyle("background-color");
            bvr.src_el.setAttribute("spt_last_background", last_background);
            bvr.src_el.setStyle("background-color", "#E0E0E0");
            bvr.src_el.setStyle("opacity", "1.0");
            '''
        } )

        sandboxes_div.add_relay_behavior( {
            'type': 'mouseleave',
            'bvr_match_class': 'spt_sandbox_option',
            'cbjs_action': '''
            var last_background = bvr.src_el.getAttribute("spt_last_background");
            bvr.src_el.setStyle("background-color", last_background);
            if (!bvr.src_el.hasClass("spt_selected")) {
                bvr.src_el.setStyle("opacity", "0.5");
            }
            '''
        } )




        sandboxes_div.add_relay_behavior( {
            'type': 'mouseup',
            'key': key,
            'bvr_match_class': 'spt_sandbox_option',
            'cbjs_action': '''
            var sandbox_dir = bvr.src_el.getAttribute("spt_sandbox_dir");
            var server = TacticServerStub.get();
            server.set_widget_setting(bvr.key, sandbox_dir);


            var applet = spt.Applet.get();

            applet.makedirs(sandbox_dir);

            //var top = bvr.src_el.getParent(".spt_sandbox_select_top");
            var top = bvr.src_el.getParent(".spt_checkin_top");
            spt.panel.refresh(top);
            '''
        } )



        #search = Search("config/naming")
        #search.add_filter("search_type", search_type)
        #search.add_filter("process", process)
        #namings = search.get_sobjects()
        #naming = namings[0]

        from pyasm.biz import Snapshot, Naming
        virtual_snapshot = Snapshot.create_new()
        virtual_snapshot.set_value("process", process)
        # for purposes of the sandbox folder for the checkin widget,
        # the context is the process
        virtual_snapshot.set_value("context", process)

        naming = Naming.get(sobject, virtual_snapshot)
        if naming:
            naming_expr = naming.get_value("sandbox_dir_naming")
            alias_options = naming.get_value("sandbox_dir_alias")
        else:
            naming_expr = None
            alias_options = None

        if alias_options == "__all__":
            alias_options = alias_dict.keys()
        elif alias_options:
            alias_options = alias_options.split("|")
        else:
            alias_options = ['default']

        for alias in alias_options:

            from pyasm.biz import DirNaming
            dir_naming = DirNaming(sobject=sobject, snapshot=virtual_snapshot)
            dir_naming.set_protocol("sandbox")
            dir_naming.set_naming(naming_expr)
            base_dir = dir_naming.get_dir(alias=alias)

            sandbox_div = DivWdg()
            sandboxes_div.add(sandbox_div)
            sandbox_div.add_class("spt_sandbox_option")
            sandbox_div.add_attr("spt_sandbox_dir", base_dir)

            if value == base_dir:
                sandbox_div.add_color("background", "background3")
                #sandbox_div.set_box_shadow()
                sandbox_div.add_class("spt_selected")
            else:
                sandbox_div.add_style("opacity", "0.5")


            sandbox_div.add_style("width: auto")
            sandbox_div.add_style("height: 55px")
            sandbox_div.add_style("padding: 5px")
            #sandbox_div.add_style("float: left")
            sandbox_div.add_style("margin: 15px")

            sandbox_div.add_border()


            if alias:
                alias_div = DivWdg()
                sandbox_div.add(alias_div)
                alias_div.add(alias)
                alias_div.add_style("font-size: 1.5em")
                alias_div.add_style("font-weight: bold")
                alias_div.add_style("margin-bottom: 15px")

            icon_wdg = IconWdg("Folder", IconWdg.FOLDER)
            sandbox_div.add(icon_wdg)
            sandbox_div.add(base_dir)


        return top




