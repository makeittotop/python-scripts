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
__all__ = ["PageNavContainerWdg", 'MainBodyTabWdg']

import types

from pyasm.common import Common, Environment, TacticException, Xml, Container, Config
from pyasm.web import *
from pyasm.biz import *   # Project is part of pyasm.biz
from pyasm.search import Search
from pyasm.widget import WidgetConfig, Error403Wdg, IconWdg, IconButtonWdg

from tactic.ui.common import BaseRefreshWdg, WidgetClassHandler
from tactic.ui.container import RoundedCornerDivWdg, PopupWdg, TabWdg
from tactic.ui.panel import SideBarPanelWdg, ViewPanelWdg
from tactic.ui.panel import TableLayoutWdg

from help_wdg import HelpWdg


class PageNavContainerWdg(BaseRefreshWdg):

    def init(my):

        link = my.kwargs.get('link')
        hash = my.kwargs.get('hash')
        
        my.widget = None

        if link:
            from tactic.ui.panel import SideBarBookmarkMenuWdg
            personal = False
            if '.' in link:
                personal = True

            config = SideBarBookmarkMenuWdg.get_config("SideBarWdg", link, personal=personal)
            options = config.get_display_options(link)

            # this is vital for view saving
            element_name = link
            attr_dict = config.get_element_attributes(link)
            title = attr_dict.get('title')

            hash = "/tab/%s" % link

           
            config = '''
            <config>
            <application>
            <element name="left_nav">
              <display class="tactic.ui.panel.SideBarPanelWdg">
              </display>
            </element>

            <element name="main_body">
              <display class="tactic.ui.panel.HashPanelWdg">
                <hash>%s</hash>
                <element_name>%s</element_name>
                <title>%s</title>
              </display>
              <web/>
            </element>
            </application>
            </config>
            ''' % (hash, element_name, title)


        elif hash:
            from tactic.ui.panel import HashPanelWdg
            my.widget = HashPanelWdg.get_widget_from_hash(hash, force_no_index=True)
            config = None
 
        else:
            security = Environment.get_security()
            start_link = security.get_start_link()
            if start_link:
                my.kwargs['link'] = start_link
                return my.init()



            # search for a defined welcome view
            search = Search("config/widget_config")
            search.add_filter("category", "top_layout")
            search.add_filter("view", "welcome")
            config_sobj = search.get_sobject()
            if config_sobj:
                config = config_sobj.get_value("config")

            else:
                config = WidgetSettings.get_value_by_key("top_layout")


        if not config:
            config = my.get_default_config()


        my.config_xml = Xml()
        my.config_xml.read_string(config)



    def get_default_config(my):
        use_sidebar = my.kwargs.get('use_sidebar')
        if use_sidebar==False:
            config = '''
            <config>
            <application>
            <element name="main_body">
              <display class="tactic.ui.startup.MainWdg"/>
              <web/>
            </element>
            </application>
            </config>
            '''
        else:
            config = '''
            <config>
            <application>
            <element name="left_nav">
              <display class="tactic.ui.panel.SideBarPanelWdg">
                <auto_size>True</auto_size>
              </display>
            </element>

            <element name="main_body">
              <display class="tactic.ui.startup.MainWdg"/>
              <web/>
            </element>
            </application>
            </config>
            '''
        return config









    def set_state(my, panel_name, widget_class, options, values):
        '''this is called by side_bar.js mostly'''

        # set the class name
        display_node = my.config_xml.get_node("config/application/element[@name='%s']/display" % (panel_name) )
        my.config_xml.set_attribute(display_node, "class", widget_class)

        # remove all the old options
        #display_node = my.config_xml.get_node("config/application/element[@name='%s']/display" % panel_name )
        for child_node in my.config_xml.get_children(display_node):
            my.config_xml.remove_child(display_node, child_node)

        # set the options
        for name, value in options.items():
            node = my.config_xml.get_node("config/application/element[@name='%s']/display/%s" % (panel_name, name) )

            if isinstance( value, basestring ):
                #print "WARNING: set application: skipping [%s] with value [%s]" % (name, value)
                #continue
                element = my.config_xml.create_text_element(name, value)
                my.config_xml.append_child(display_node, element)

            elif isinstance( value, dict): # if it is a dictionary
                # TODO: run recursively.. supports 2 level only now
                sub_element = my.config_xml.create_element(name)
                my.config_xml.append_child(display_node, element)
                for name2, value2 in value.items():
                    if isinstance(value2, dict):
                        sub_element2 = my.config_xml.create_element(name2)
                        my.config_xml.append_child(sub_element, sub_element2)
                        for name3, value3 in value2.items():
                            element = my.config_xml.create_text_element(name3, value3)
                            my.config_xml.append_child(sub_element2, element)
                    else:        
                        element = my.config_xml.create_text_element(name2, value2)
                        my.config_xml.append_child(sub_element, element)
                    
                
        # web value node
        value_node = my.config_xml.get_node("config/application/element[@name='%s']/web" % (panel_name) )
        if value_node != None:
            for child_node in my.config_xml.get_children(value_node):
                my.config_xml.remove_child(value_node, child_node)
        else: # create it
            value_node = my.config_xml.create_element('web')
            element_node = my.config_xml.get_node("config/application/element[@name='%s']" % (panel_name) )
            my.config_xml.append_child(element_node, value_node)

        # set the values
        for name, value in values.items():
            node = my.config_xml.get_node("config/application/element[@name='%s']/web/%s" % (panel_name, name) )

            if not isinstance(value, basestring):
                print "WARNING: set application: skipping [%s] with value [%s]" % (name, value)
                continue
            element = my.config_xml.create_text_element(name, value)
            my.config_xml.append_child(value_node, element)
        WidgetSettings.set_key_values("top_layout", [my.config_xml.to_string()])



    def get_state(my):
        return my.config_xml



    def get_side_bar_cache(my, left_nav_wdg):
        project = Project.get()
        project_code = project.get_code()

        # do it with sobject
        #key = "%s_side_bar" % project.get_code()
        #cache = Search.get("sthpw/widget_cache")
        #cache.add_filter("key", key)
        #sobject = cache.get_sobject()
        #value = sobject.get_value("cache")

        login = Environment.get_user_name()
        tmp_dir = "%s/cache/side_bar" % Environment.get_tmp_dir()

        filename = "%s__%s.html" % (project_code, login)
        path = "%s/%s" % (tmp_dir, filename)

        # use files
        import os
        if os.path.exists(path):
            f = open(path, "r")
            html = f.read()
            f.close()
        else:            
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            f = open(path, "w")
            html = left_nav_wdg.get_buffer_display()
            f.write(html)
            f.close()

        return html




    def get_display(my):
        is_admin_project = Project.get().is_admin()
        security = Environment.get_security() 
        if is_admin_project and not security.check_access("builtin", "view_site_admin", "allow"):
            return Error403Wdg()
                
        # create the elements
        config = WidgetConfig.get(xml=my.config_xml, view="application")

        left_nav_handler = config.get_display_handler("left_nav")
        left_nav_options = config.get_display_options("left_nav")

        view_side_bar = None
        if left_nav_handler:
            left_nav_wdg = Common.create_from_class_path(left_nav_handler, [], left_nav_options)

            # caching
            side_bar_cache = my.get_side_bar_cache(left_nav_wdg)
        else:
            view_side_bar = False

        # create the main table
        core_table = Table()
        core_table.add_tbody()
        core_table.set_style("border: 0px; border-collapse: collapse; width: 100%;")


        # add a spacer row
        #spacer_tr = core_table.add_row()
        #spacer_tr.add_style("width: 100%")
        #td = core_table.add_cell()
        #td.set_style("min-height: 1px; height: 1px;")
        #core_table.add_cell()
        #core_table.add_cell()

        # determine if the side bar is visible
        if view_side_bar == None:
            view_side_bar = security.check_access("builtin", "view_side_bar", "allow", default='allow')


        # add the main cells
        tr, td = core_table.add_row_cell()
        td.add_style("padding: 0px")
        td.add_style("margin: 0px")

        # add the main resizable table
        from tactic.ui.container import ResizableTableWdg
        main_table = ResizableTableWdg()
        main_table.set_keep_table_size()

        main_table.add_style("width: 100%")

        td.add(main_table)

        left_nav_td = main_table.add_cell()
        if view_side_bar:
            left_nav_td.add_class("spt_panel")
            left_nav_td.add_style("padding: 0px")

        main_body_td = main_table.add_cell(resize=False)
        main_body_td.add_style("padding: 10px")
        main_body_td.set_style( "width: 100%; vertical-align: top; text-align: center; padding-top: 3px" )

        if view_side_bar:
            left_nav_td.set_style( "vertical-align: top" )

            # create the left navigation panel
            left_nav_div = DivWdg()
            left_nav_td.add(left_nav_div)

            left_nav_div.set_id("side_bar" )
            # add the detail to the panel
            left_nav_div.add_attr("spt_class_name", left_nav_handler)
            for name, value in left_nav_options.items():
                left_nav_div.add_attr("spt_%s" % name, value)


            left_nav_div.add_style("max_width: 185px")
            left_nav_div.add_style("width: 185px")
            left_nav_div.add_style("text-align: right")
            left_nav_div.add_style("vertical-align: top")
            left_nav_div.add_style("overflow: hidden")

            left_nav_div.add_class("spt_resizable")
            side_bar_inner = DivWdg()
            left_nav_div.add(side_bar_inner)

            #side_bar_inner.add_style("padding-left: 1px")
            side_bar_inner.add_style("width: 100%")

            # add side bar to nav
            side_bar_inner.add(side_bar_cache)

            left_nav_div.add_style("border-style: solid")
            left_nav_div.add_style("border-width: 0px 1px 0px 0px")
            #left_nav_div.add_color("border-color", "border")
            left_nav_div.add_color("border-color", "border", -10)

            web = WebContainer.get_web()
            browser = web.get_browser()
            if browser in ['Qt','Webkit']:
                min_width = "1px"
            else:
                min_width = "0px"

            left_nav_div.add_behavior( {
                'type': 'listen',
                'event_name': 'side_bar|hide_now',
                'min_width': min_width,
                'cbjs_action': '''
                var size = bvr.src_el.getSize();
                bvr.src_el.setAttribute("spt_size", size.x);
                bvr.src_el.setStyle("width", bvr.min_width);

                '''
            } )


            left_nav_div.add_behavior( {
                'type': 'listen',
                'event_name': 'side_bar|hide',
                'min_width': min_width,
                'cbjs_action': '''
                var size = bvr.src_el.getSize();
                bvr.src_el.setAttribute("spt_size", size.x);
                new Fx.Tween(bvr.src_el, {duration:'short'}).start('width', bvr.min_width);

                '''
            } )


            left_nav_div.add_behavior( {
                'type': 'listen',
                'event_name': 'side_bar|show',
                'min_width': min_width,
                'cbjs_action': '''
                var width = bvr.src_el.getAttribute("spt_size");
                if (!width) {
                   width = 185;
                }
                if (parseInt(width) < 5) {
                    width = 185;
                }
                //bvr.src_el.setStyle("width", width + "px");
                new Fx.Tween(bvr.src_el, {duration:'short'}).start('width', bvr.min_width, width+"px");
                '''
            } )


            left_nav_div.add_behavior( {
                'type': 'listen',
                'event_name': 'side_bar|toggle',
                'cbjs_action': '''
                var size = bvr.src_el.getSize();
                if (size.x < 5) {
                    spt.named_events.fire_event("side_bar|show", {} );
                }
                else {
                    spt.named_events.fire_event("side_bar|hide", {} );
                }
                '''
            } )




        # create the main body panel

        palette = WebContainer.get_palette()
        color = palette.color("background2")
        main_body_rounded = DivWdg()
        main_body_inner = main_body_rounded

        main_body_inner.add_style("min-height: 500px")


        # DEBREACATED
        """
        # add a breadcrumb
        breadcrumb_wdg = DivWdg()
        # hide the breadcrumb
        breadcrumb_wdg.add_style("display", "none")
        Container.put("breadcrumb", breadcrumb_wdg)
        breadcrumb_wdg.set_id("breadcrumb")
        breadcrumb_wdg.add_style("text-align: left")
        breadcrumb_wdg.add_looks( "fnt_title_3" )
        main_body_inner.add(breadcrumb_wdg)
        """

        main_body_panel = DivWdg()
        main_body_panel.set_id("main_body")
        main_body_panel.add_class("spt_main_panel")
        main_body_inner.add(main_body_panel)


        tab = MainBodyTabWdg()
        main_body_panel.add(tab)

        # TEST: NEW LAYOUT
        if Config.get_value("install", "layout") == "fixed":
            main_body_panel.add_style("margin-top: 31px")
            main_body_rounded.add_color("background", "background")
            main_body_rounded.add_style("padding: 3px 0px 0px 0px")



        # add the content to the main body panel
        try:
            if my.widget:
                tab.add(my.widget)
                element_name = my.widget.get_name()

            else:
                main_body_handler = config.get_display_handler("main_body")
                main_body_options = config.get_display_options("main_body")
                element_name = main_body_options.get("element_name")
                title = main_body_options.get("title")

                main_body_content = Common.create_from_class_path(main_body_handler, [], main_body_options)
                # get the web values from top_layout
                main_body_values = config.get_web_options("main_body")
                web = WebContainer.get_web()
                if isinstance(main_body_values, dict):
                    for name, value in main_body_values.items():
                        web.set_form_value(name, value)

                main_body_content.set_name(element_name)
                tab.add(main_body_content, element_name, title)

                my.set_as_panel(main_body_panel, class_name=main_body_handler, kwargs=main_body_options)

            main_body_panel.add_behavior( {
                'type': 'load',
                'element_name': element_name,
                'cbjs_action': '''
                if (spt.help)
                    spt.help.set_view(bvr.element_name);
                '''
            } )


           
        except Exception, e:
            # handle an error in the drawing
            buffer = my.get_buffer_on_exception()
            error_wdg = my.handle_exception(e)
            main_body_content = DivWdg()
            main_body_content.add(error_wdg)
            main_body_content = main_body_content.get_buffer_display()
            tab.add(main_body_content, element_name, title)


        # add the main container
        container_div = DivWdg()
        container_div.set_style("width: 100%;")


        # NOTE: the td should not be the sliding element! So we create a div inside the TD to be the sliding element
        main_body_div = DivWdg()
        main_body_div.set_id("horizontal_main_body_slider")

        main_body_div.add(main_body_inner)



        """
        # get the global drag_ghost_div
        drag_ghost_div = my.get_drag_ghost_div()
        drag_ghost_div.set_id( "drag_ghost_copy" )
        drag_ghost_div.add_class( "SPT_PUW" )  # make it a Page Utility Widget (now processed client side)

        drag_ghost_div.set_z_start( 400 )
        """
       

        from page_header_wdg import PageHeaderWdg
        header_panel = DivWdg()
        header_panel.set_id("main_header")
        header_panel.add_attr("spt_class_name", "tactic.ui.app.PageHeaderWdg")
        header_wdg = PageHeaderWdg()
        header_panel.add(header_wdg)

        container_div.add( header_panel.get_buffer_display() )
       

        main_body_dis = main_body_div.get_buffer_display()
        main_body_td.add(main_body_dis) 


        container_div.add( core_table )
        #container_div.add( drag_ghost_div )


        is_admin = False
        security = Environment.get_security()
        if security.check_access("builtin", "view_site_admin", "allow"):
            is_admin = True

        if is_admin:
            from quick_box_wdg import QuickBoxWdg
            quick_box = QuickBoxWdg()
            container_div.add(quick_box)


        container_div.add_behavior( {
            'type': 'load',
            'cbjs_action': '''
            spt.named_events.fire_event("close_admin_bar");
            '''
        } )


        return container_div



    def handle_exception(my, e):
        '''The tab widget is a special widget concerning exceptions because
        it usually represents the outer skin of the content of the web page.
        The titles of the tab must be displayed in order for the site to remain
        functional in the case of an exception'''
        from pyasm.widget import ExceptionWdg
        widget = ExceptionWdg(e)
        my.error_wdg = Widget()
        my.error_wdg.add(widget)
        return my.error_wdg



    """
    def get_drag_ghost_div(my):
        drag_ghost_div = HtmlElement.div()
        drag_ghost_div.set_attr( "id", "drag_ghost_copy" )
        drag_ghost_div.set_attr( "element_copied", "_NONE_" )
        drag_ghost_div.add_class( "REG_ID" )
        drag_ghost_div.set_style("background: #393950; color: #c2c2c2; border: solid 1px black;' \
                                 'text-align: left; padding: 10px;', filter: alpha(opacity=60); " +
                                 "opacity: 0.6; position: absolute; display: none; left: 0px; top: 0px;" +
                                 " z-index: 110;" )
        drag_ghost_div.add("Ghost Div")
        return drag_ghost_div
    """


    def get_drag_div(my):
        drag_div = HtmlElement.div()
        drag_div.set_style( "position: absolute; left: 100px; top: 400px; min-width: 400px; width: 400px; " +
                            "background-color: white; border: solid black;" )

        drag_handle_div = HtmlElement.div()
        drag_handle_div.set_style( "cursor: default; background-color: gray; border-bottom: dotted black; " +
                                    "padding: 3px; font-family: sans-serif; font-weight: bold;" )

        # NOTE: to specify behaviors on a widget, you can use the .add_behavior() method ... use one behavior
        #       specification dictionary (hash) string per call to add_behavior (but you can add multiple
        #       behaviors by making multiple calls to add_behavior)
        #
        drag_handle_div.add_behavior( "{type:'click', mouse_btn:'LMB', modkeys:'SHIFT', dst_el:'@.parentNode', " +
                                      "cbfn_action: spt.cb.change_color_action}" )
        drag_handle_div.add_behavior( "{type:'drag', mouse_btn:'LMB', modkeys:'', src_el:'@.parentNode'}" )
        drag_handle_div.add("Drag Handle -- click and drag me!")

        drag_div.add( drag_handle_div )
        drag_div.add( "<p>This is a draggable div ... click on the drag handle above and drag this thing around!</p>" )

        return drag_div






class MainBodyTabWdg(BaseRefreshWdg):

    def get_config(my):
        config = None

        if not config:
            search = Search("config/widget_config")
            if my.category:
                search.add_filter("category", 'TabWdg')
            if my.search_type:
                search.add_filter("search_type", my.search_type)
            search.add_filter("view", my.view)
            config = search.get_sobject()

        return config


    def get_config_xml(my):

        from pyasm.web import WidgetSettings
        config_xml  = WidgetSettings.get_value_by_key("main_body_tab")
        config_xml = None

        if not config_xml:
            config_xml = '''<config><tab/></config>'''
            """
            config_xml = '''<config><tab>
            <element name='Ingestion'>
              <display class='tactic.ui.widget.file_browser_wdg.FileBrowserWdg'>
                <search_type>sthpw/login_group</search_type>
                <view>table</view>
              </display>
            </element>
            </tab>
            </config>'''
            """
 
        return config_xml



    def get_display(my):

        my.search_type = None

        my.view = 'tab'
        config_xml = my.get_config_xml()
        config = WidgetConfig.get(view=my.view, xml=config_xml)

        top = DivWdg()
        tab = TabWdg(config=config, view=my.view, width=1000)
        top.add(tab)
        for widget in my.widgets:
            tab.add(widget)


        # set the current one active
        div = DivWdg()
        div.add_style("display: hidden")
        div.add_behavior( {
        'type': 'load',
        'cbjs_action': '''
        spt.tab.set_main_body_top();
        var headers = spt.tab.get_headers();
        // if there are no headers, then there was an error
        if (headers.length == 0) {
            return;
        }

        var name = headers[headers.length-1].getAttribute("spt_element_name");
        spt.tab.select(name);
        '''
        } )

        top.add(div)



        return top



from pyasm.command import Command
class TabSaveStateCmd(Command):
    def execute(my):

        class_names = my.kwargs.get("class_names")
        attrs_list = my.kwargs.get("attrs_list")
        kwargs_list = my.kwargs.get("kwargs_list")

        xml = Xml()
        xml.create_doc("config")
        root = xml.get_root_node()

        view = xml.create_element("tab")
        xml.append_child(root, view)

        for class_name, attrs, kwargs in zip(class_names, attrs_list, kwargs_list):

            element = xml.create_element("element")
            xml.append_child(view, element)

            for key, value in attrs.items():
                xml.set_attribute(element, key, value)

            display = xml.create_element("display")
            xml.append_child(element, display)

            xml.set_attribute(display, "class", class_name)

            for key, value in kwargs.items():
                attr = xml.create_text_element(key, value, node=display)
                xml.append_child(display, attr)

        xml_string = xml.to_string()

        from pyasm.web import WidgetSettings
        WidgetSettings.set_value_by_key("tab", xml_string)



