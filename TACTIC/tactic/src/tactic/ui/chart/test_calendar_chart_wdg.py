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


__all__ = ["TestCalendarChartWdg"]

# DEPRECATED

from pyasm.common import Environment, Common, jsonloads
from pyasm.biz import Project
from pyasm.web import Widget, DivWdg, HtmlElement, WebContainer, Table
from pyasm.widget import SelectWdg, TextWdg
from pyasm.search import Search, SearchType
from tactic.ui.common import BaseRefreshWdg

import types

#from chart_wdg import ChartWdg
#from chart_data import ChartData, ChartElement

class TestCalendarChartWdg(BaseRefreshWdg):
    ''' '''


    ARGS_KEYS = {
    'chart_type': 'line|bar|area - type of chart',
    'width': 'The starting width of the chart',
    'search_keys': 'List of search keys to display',
    'x_axis': 'The x_axis element',
    'y_axis': 'List of elements to put on the y_axis'
    }

    def preprocess(my):
        my.max_value = 0
        my.min_value = 0
        my.steps = 0

        web = WebContainer.get_web()
        my.width = web.get_form_value("width")
        if not my.width:
            my.width = my.kwargs.get("width")


        my.chart_type = web.get_form_value("chart_type")
        if not my.chart_type:
            my.chart_type = my.kwargs.get("chart_type")
        if not my.chart_type:
            my.chart_type = 'bar'


        my.x_axis = web.get_form_value("x_axis")
        if not my.x_axis:
            my.x_axis = my.kwargs.get("x_axis")
        if not my.x_axis:
            my.x_axis = 'code'


        # FIXME: which should override???
        my.y_axis = web.get_form_values("y_axis")
        if not my.y_axis:
            my.y_axis = my.kwargs.get("y_axis")

        if my.y_axis:
            my.elements = my.y_axis
        else:
            my.elements = my.kwargs.get("elements")
            if not my.elements:
                my.elements = web.get_form_value("elements")

        if isinstance(my.elements,basestring):
            if my.elements:
                my.elements = my.elements.split('|')
            else:
                my.elements = []




        my.search_type = web.get_form_value("search_type")
        if not my.search_type:
            my.search_type = my.kwargs.get("search_type")


        my.search_keys = my.kwargs.get("search_keys")
        if my.search_type and my.search_type.startswith("@SOBJECT("):
            my.sobjects = Search.eval(my.search_type)
        elif my.search_keys:
            if isinstance(my.search_keys, basestring):
                my.search_keys = eval(my.search_keys)
            my.sobjects = Search.get_by_search_keys(my.search_keys)
        else:
            search = Search(my.search_type)
            search.add_limit(100)
            my.sobjects = search.get_sobjects()

        # get the definition
        sobjects = my.sobjects
        if sobjects:
            sobject = sobjects[0]
            search_type = sobject.get_search_type()
            view = 'definition'

            from pyasm.widget import WidgetConfigView
            my.config = WidgetConfigView.get_by_search_type(search_type, view)
        else:
            my.config = None


        my.widgets = {}


    def get_data(my, sobject):

        values = []
        labels = []

        if not my.config:
            return values, labels


        for element in my.elements:

            if element.startswith("{") and element.endswith("}"):
                expr = element.strip("{}")
                value = Search.eval(expr, sobject, single=True)
                labels.append(element)

            else:

                options = my.config.get_display_options(element)
                attrs = my.config.get_element_attributes(element)


                label = attrs.get('title')
                if not label:
                    label = Common.get_display_title(element)
                labels.append(label)

                widget = my.widgets.get(element)
                if not widget:
                    widget = my.config.get_display_widget(element)
                    my.widgets[element] = widget

                widget.set_sobject(sobject)

                try:
                    value = widget.get_text_value()
                except:
                    value = 0

            if isinstance(value, basestring):
                if value.endswith("%"):
                    value = float( value.replace("%",'') )
                else:
                    value = 0

            if not value:
                value = 0

            #expression = options.get("expression")
            #if not expression:
            #    value = 0
            #else:
            #    value = Search.eval(expression, sobject, single=True)

            if value > my.max_value:
                my.max_value = value

            values.append(value)        


        return values, labels



    def get_display(my):
        div = DivWdg()

        table = Table()
        div.add(table)
        table.add_row()

        if my.title:
            title_div = DivWdg()

            table.add_cell(title_div)

            name = "Ym"

            title = my.title
            if not title:
                title = name
            title = Common.get_display_title(title)
            title_div.add("%s:" % title )
            title_div.add_style("width: 80px")
            title_div.add_style("font-weight: bold")
            title_div.add_style("margin-left: 15px")
            title_div.add_style("padding-top: 2px")

        td = table.add_cell()
        start_date = DivWdg("Start Date")
        td.add(start_date)
        start_date.add_style("margin-left: 5px")
        #td = table.add_cell()
        #op = DivWdg(" between&nbsp;&nbsp;&nbsp;")
        #op.add_style("margin-left: 5px")
        #td.add(op)

        from tactic.ui.widget import CalendarInputWdg
        td = table.add_cell()
        cal1 = CalendarInputWdg("start_date")
        td.add(cal1)

        table.add_row()
        end_date = DivWdg("End Date")
        end_date.add_style("margin-left: 5px")
        td = table.add_cell()
        td.add(end_date)
        #td.add(spacing)

        td = table.add_cell()
        cal2 = CalendarInputWdg("end_date")
        td.add(cal2)

        table.add_row()
        td = table.add_cell()

        from pyasm.widget import ButtonWdg
        button = ButtonWdg()
        #button.add_style("width: %s" % top_width)
        button.add_class('spt_label')

        icon = my.kwargs.get("icon")
        if icon:
            icon_div = DivWdg()
            icon = IconWdg(title, icon, width=16 )
            icon_div.add(icon)
            button.add(icon_div)
            my.table.add_style("position: relative")
            icon_div.add_style("position: absolute")
            icon_div.add_style("left: 5px")
            icon_div.add_style("top: 6px")
            title = " &nbsp; &nbsp; %s" % title
            button.add_style("padding: 2px")

        button.set_name("Reload")

        td.add(button)

        return div


