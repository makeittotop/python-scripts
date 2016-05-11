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


__all__ = ['ChartWdg', 'ChartData', 'AbhishekBarChartWdg']

from pyasm.common import Environment, Common, jsonloads
from pyasm.search import Search
from pyasm.biz import Project
from pyasm.web import Widget, DivWdg, HtmlElement, WebContainer, Canvas
from pyasm.web import Table

from tactic.ui.common import BaseRefreshWdg

from datetime import datetime, timedelta, date


class AbhishekBarChartWdg(BaseRefreshWdg):

    ARGS_KEYS = {
    'width': {
        'description': 'Width of widget',
        'category': 'Options',
        'order': 0
    },
    'height': {
        'description': 'Height of widget',
        'category': 'Options',
        'order': 1
    },
    }



    def get_display(my):

        top = my.top

        #top.add_gradient("background", "background", 5, -20)
        top.add_color("background", "background", -5)
        #top.add_style("padding-top: 10px")

        #title = "Sample Chart"
        title = my.kwargs.get("title")
        if title:
            date = "@FORMAT(@STRING($TODAY),'Dec 31, 1999')"
            date = Search.eval(date, single=True)

            title_wdg = DivWdg()
            top.add(title_wdg)
            title_wdg.add(title)
            title_wdg.add(" [%s]" % date)
            title_wdg.add_style("font-size: 1.1em")
            title_wdg.add_color("background", "background3")
            title_wdg.add_color("color", "color3")
            title_wdg.add_style("padding: 10px")
            title_wdg.add_style("font-weight: bold")
            title_wdg.add_style("text-align: center")

        colors = [
            'rgba(255,0,0,0.5)',
            'rgba(0,255,0,0.5)',
            'rgba(0,0,255,0.5)',
            'rgba(128,0,255,0.5)',
            'rgba(0,128,255,0.5)',
            'rgba(255,0,255,0.5)',
        ]

        # draw a legend
        legend = None
        from chart2_wdg import ChartLegend

        #import pdb; pdb.set_trace();

        labels = my.kwargs.get("labels")
        my.user = my.kwargs.get("user")

        if labels:
            legend = ChartLegend()
            labels = labels.split("|")
            legend.set_labels(labels)
            top.add(legend)
            legend.add_style("width: %s" % str(len(labels)*200))
            legend.add_style("margin-left: auto")
            legend.add_style("margin-right: auto")

            #legend.add_style("width: 200px")
            #legend.add_style("position: absolute")
            #legend.add_style("top: 40px")
            #legend.add_style("left: 300px")


        if legend:
            legend.set_colors(colors)


        #############
        # table for start-end date
        search_table = Table()
        search_table.add_style("margin-left: auto")
        search_table.add_style("margin-right: auto")
        search_table.add_style("margin-top: 35px")
        search_table.add_style("margin-bottom: 45px")
        top.add(search_table)
 
        search_table.add_row()

        td = search_table.add_cell()
        start_date = DivWdg("Start Date")
        td.add(start_date)
        start_date.add_style("margin-left: 5px")
        #td = table.add_cell()
        #op = DivWdg(" between&nbsp;&nbsp;&nbsp;")
        #op.add_style("margin-left: 5px")
        #td.add(op)

        from tactic.ui.widget import CalendarInputWdg
        td = search_table.add_cell()
        cal1 = CalendarInputWdg("start_date")
        td.add(cal1)

        search_table.add_row()
        end_date = DivWdg("End Date")
        end_date.add_style("margin-left: 5px")
        td = search_table.add_cell()
        td.add(end_date)
        #td.add(spacing)

        td = search_table.add_cell()
        cal2 = CalendarInputWdg("end_date")
        td.add(cal2)

        search_table.add_row()
        td = search_table.add_cell()

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
        #############


        task_data = my.get_task_data()
        
        labels = [label[0] for label in task_data.get(task_data.keys()[0])]

        #labels = ['chr001', 'chr002', 'chr003', 'chr004', 'prop001', 'prop002', 'cow001']
        #labels = ['week 1', 'week 2', 'week 3', 'week 4', 'week 5', 'week 6', 'week 7', 'week 8']
        #values = [1,2,4,5,6,7,8]
        values = [i+1 for i in range(len(labels))]

        width = my.kwargs.get("width")
        if not width:
            width = '1600px'
        height = my.kwargs.get("height")
        if not height:
            height = '1000px'


        chart_div = DivWdg()
        top.add(chart_div)
        chart_div.add_style("text-align: center")

        chart = ChartWdg(
            height=height,
            width=width,
            chart_type='bar',
            labels=labels
        )
        chart_div.add(chart)

        data = ChartData(
            color=colors[0], #"rgba(255, 0, 0, 1.0)",
            #data=[task_data['Pending'], 5.5, 7.5, 14.3, 10.2, 1.1, 3.3],
            data = [data[1] for data in task_data.get('Pending')]
        )
        chart.add(data)

        data = ChartData(
            color=colors[1], #"rgba(0, 255, 0, 1.0)",
            #data=[task_data['Assignment'], 4.3, 8.4, 6.2, 8.4, 2.2],
            data = [data[1] for data in task_data.get('Assignment')]
        )
        chart.add(data)


        data = ChartData(
            color=colors[2], #"rgba(0, 0, 255, 1.0)",
            #data=[task_data['In Progress'], 3.5, 2.2, 6.6, 1.3, 9.4],
            data = [data[1] for data in task_data.get('In Progress')]
        )
        chart.add(data)


        #data = [task_data['Approved'], 17, 15.5, -3, 17, 16.8, 11.4]
        data = [data[1] for data in task_data.get('Approved')]
        data = ChartData(data=data, color=colors[3]) #"rgba(128, 0, 255, 1.0)")
        chart.add(data)


        data = [data[1] for data in task_data.get('Review')] 
        data = ChartData(data=data, color=colors[4]) #"rgba(0, 128, 255, 1.0)")
        chart.add(data)

        table = Table()
        table.add_color("color", "color")
        top.add(table)
        table.add_row()
        table.center()
        table.add_style("width: 1%")


        x_title = my.kwargs.get("x_title")
        y_title = my.kwargs.get("y_title")

        if y_title:
            y_title = y_title.replace(" ", "&nbsp;")

            y_axis_div = DivWdg()
            td = table.add_cell(y_axis_div)
            td.add_style("vertical-align: middle")
            td.add_style("width: 1%")
            y_axis_div.add(y_title)
            y_axis_div.add_style("-moz-transform: rotate(-90deg)")
            y_axis_div.add_style("-webkit-transform: rotate(-90deg)")
            y_axis_div.add_style("font-size: 1.33em")
            y_axis_div.add_style("height: 100%")
            y_axis_div.add_style("width: 30px")

        table.add_row()

        # add the x-axis title
        if x_title:
            x_title = x_title.replace(" ", "&nbsp;")

            x_axis_div = DivWdg()
            td = table.add_cell(x_axis_div)
            td.add_style("text-align: center")
            td.add_style("width: 1%")
            x_axis_div.add(x_title)
            x_axis_div.add_style("font-size: 1.33em")
            x_axis_div.add_style("width: 100%")
            x_axis_div.add_style("height: 30px")

        return top

    def get_week_data(my, today_date):
        from datetime import datetime, timedelta, date

        #today = date.today()
        dt = datetime.strptime(today_date, '%d/%b/%Y')
        start = dt - timedelta(days=(dt.weekday() + 1) % 7)
        end = start + timedelta(days=6)
        start_str = "{0} {1}".format(start.strftime("%d"), start.strftime("%b"))
        end_str = "{0} {1}".format(end.strftime("%d"), end.strftime("%b"))
        week_str = "{0} - {1}".format(start_str, end_str)
        return week_str

    def get_task_data(my):
        import sys
        sys.path.append('/nas/projects/development/productionTools/tactic/src/client/tactic_client_lib')

        from tactic_server_stub import TacticServerStub

        server = TacticServerStub.get()
        server_IP = '172.16.15.100'
        server.set_server(server_IP)
        server.set_project('ziryab')
        ticket = server.get_ticket("abhishek", "barajoun@2014foobarnul")
        server.set_ticket(ticket)

	task_data = {}
        
	#expr = "@COUNT(@SOBJECT(sthpw/task['status', 'Pending']))"
	#task_data['Pending'] = server.eval(expr)

	#expr = "@COUNT(@SOBJECT(sthpw/task['status', 'Assignment']))"
	#task_data['Assignment'] = server.eval(expr)

	#expr = "@COUNT(@SOBJECT(sthpw/task['status', 'In Progress']))"
	#task_data['In Progress'] = server.eval(expr)

	#expr = "@COUNT(@SOBJECT(sthpw/task['status', 'Approved']))"
	#task_data['Approved'] = server.eval(expr)

	#expr = "@COUNT(@SOBJECT(sthpw/task['status', 'Review']))"
	#task_data['Review'] = server.eval(expr)

	for state in ['Pending', 'Assignment', 'In Progress', 'Approved', 'Review']:
	    print state
	    task_data[state] = []
	    for i in range(datetime.strptime('01/Feb/2016', "%d/%b/%Y").isocalendar()[1], date.today().isocalendar()[1] + 1):
		(start, end)=my.get_week_days(2016, i)
		start_str="{0}{1}".format(start.strftime('%d'), start.strftime('%b'))
		end_str="{0}{1}".format(end.strftime('%d'), end.strftime('%b'))
		week="{0}-{1}".format(start_str, end_str)
		expr = "@COUNT(@SOBJECT(sthpw/task['status', '" + state + "']['assigned', '" + my.user + "']['timestamp', '>', '" + start.strftime('%Y-%m-%d') + "']['timestamp', '<', '" + end.strftime('%Y-%m-%d') + "']))"
		#expr = "@COUNT(@SOBJECT(sthpw/task['status', '" + state + "']['assigned', 'maha']['timestamp', '>', '" + start.strftime('%Y-%m-%d') + "']['timestamp', '<', '" + end.strftime('%Y-%m-%d') + "']))"
		val = server.eval(expr)
		task_data[state].append((week, val))

        return task_data
 
    def get_week_days(my, year, week):                                                                                                         
        d = date(year,1,1)                                                                                                                 
        if(d.weekday()>3):                                                                                                                 
            d = d+timedelta(6-d.weekday())                                                                                                 
	else:                                                                                                                              
	    d = d - timedelta(d.weekday() - 1)                                                                                             
	dlt = timedelta(days =(week-1)*7)                                                                                                  
	return d + dlt, d + dlt + timedelta(days=6)  


class ChartWdg(BaseRefreshWdg):

    ARGS_KEYS = {
    'height': 'Height of the canvas',
    'width': 'Width of the canvas',
    }

    def init(my):
        top = my.top
        #top.add_gradient("background", "background", -5)

    def add_style(my, name, value):
        my.top.add_style(name, value)

    def add_color(my, name, value):
        my.top.add_color(name, value)

    def add_gradient(my, name, value, offset=0, gradient=-10):
        my.top.add_gradient(name, value, offset, gradient)


    def get_display(my):

        top = my.top
        top.add_style("position: relative")

        labels = my.kwargs.get("labels")
        if not labels:
            labels = []
        label_values = my.kwargs.get("label_values")

        width = my.kwargs.get("width")
        height = my.kwargs.get("height")

        default_chart_type = my.kwargs.get("chart_type")
        if not default_chart_type:
            default_chart_type = 'bar'

        canvas = Canvas()
        top.add(canvas)
        canvas.set_id("chart1")
        canvas.add_attr("width", width)
        canvas.add_attr("height", height)
        canvas.add("Your web-browser does not support the HTML 5 canvas element.")

        canvas.add_behavior( {
            'type': 'load',
            'cbjs_action': ONLOAD_JS
        } )


        bar_chart_index = 0
        num_bar_charts = 0
        for widget in my.widgets:
            # count the number of bar charts
            chart_type = widget.get_chart_type()
            if not chart_type:
                chart_type = default_chart_type
                widget.set_chart_type(chart_type)


            if chart_type == 'bar':
                num_bar_charts += 1



        # auto figure out the range
        xmax = 1
        ymax = 0

        for widget in my.widgets:

            # count the number of bar charts
            chart_type = widget.get_chart_type()
            if not chart_type:
                chart_type = default_chart_type
                widget.set_chart_type(chart_type)


            widget.set_index(bar_chart_index, num_bar_charts)
            if chart_type == 'bar':
                bar_chart_index += 1


            # remember the largest value
            data = widget.get_data()
            for value in data:
                if value > ymax:
                    ymax = value


            x_data = widget.get_xdata()
            if not x_data:
                if len(data)-1 > xmax:
                    xmax = len(data)-1
            else:
                last = x_data[-1]
                if last > xmax:
                    xmax = last

            top.add(widget)

        # FIXME: doesn't handle small numbers too well
        ymax += 1

        if len(labels) > xmax:
            xmax = len(labels)
        if not xmax:
            xmax = 1



        # initialize the canvas
        canvas.add_behavior( {
            'type': 'load',
            'xmax': xmax,
            'ymax': ymax,
            'cbjs_action': '''
            spt.chart.top = bvr.src_el;
            spt.chart.set_range(bvr.xmax, bvr.ymax);
            '''
        } )


        # draw the grid
        grid = ChartGrid(labels=labels, label_values=label_values)
        top.add(grid)


        # draw a legend
        if my.kwargs.get("legend"):
            legend = ChartLegend(labels=my.kwargs.get('legend'))
            legend.add_style("position: absolute")
            legend.add_style("left: %s" % 50)
            legend.add_style("top: %s" % 10)

            top.add(legend)

        return top


class ChartGrid(BaseRefreshWdg):

    def get_display(my):


        labels = my.kwargs.get("labels")
        if not labels:
            labels = None

        xmax = my.kwargs.get("xmax")
        ymax = my.kwargs.get("ymax")

        #mode = 'integer'
        mode = 'float'


        my.label_values = my.kwargs.get("label_values")
        if not my.label_values:
            my.label_values = [0]

        top = my.top

        font_color = top.get_color("color")
        #font = '12px san-serif';
        font = '12px arial';
        grid_color = top.get_color("border")

        rotate_x_axis = my.kwargs.get("rotate_x_axis") 
        if rotate_x_axis in [True, 'true']:
            rotate_x_axis = True
        else:
            rotate_x_axis = False

        top.add_behavior( {
            'type': 'load',
            'mode': mode,
            'font': font,
            'font_color': font_color,
            'grid_color': grid_color,
            'rotate_x_axis': rotate_x_axis,
            'labels': labels,
            'label_values': my.label_values,
            'cbjs_action': '''

            var size = spt.chart.get_size();
            var color = bvr.grid_color;


            var origin = spt.chart.get_origin();
            var outer = spt.chart.get_outer();

            var interval = spt.chart.get_interval();

            // draw the main grid lines
            spt.chart.draw_line( origin, {x: origin.x, y: outer.y}, color );
            spt.chart.draw_line( origin, {x: outer.x, y: origin.y}, color );

            // draw lines on the x axis
            var last_x = 0;
            var last_label = null;
            for (var i = 0; ; i++) {
                if (i > 1000) break;

                var label_value = bvr.label_values[i];
                var x;
                if (typeof(label_value) == 'undefined') {
                    x = last_x + interval.x;
                }
                else {
                    x = origin.x + label_value*interval.x;
                }


                var y = origin.y;
                if (x > outer.x) break;

                var start = {x: x, y: y};
                var end = {x: x, y: y+5};
                spt.chart.draw_line( start, end, color );

                var label = null;
                if (bvr.labels == null) {
                    label = i + "";
                }
                else {
                    if (i < bvr.labels.length)
                        label = bvr.labels[i];
                }


                // if diff is too small, don't draw it
                var diff = x - last_x;
                if (diff < 20) {
                    continue;
                }
                last_x = x;



                var ctx = spt.chart.get_ctx();
                ctx.fillStyle = bvr.font_color;
                ctx.font = bvr.font;
                ctx.textBaseline = 'bottom';

                if (label && label != last_label) {
                    var length = (label+"").length;
                    //var offset = length * 2;
                    var offset_x = 5;
                    var offset_y = 10;
                    

                    ctx.save();
                    ctx.translate(+(x-offset_x), +(origin.y+offset_y));
                    if (bvr.rotate_x_axis)
                        ctx.rotate(Math.PI/4);
                    ctx.translate(-(x-offset_x), -(origin.y+offset_y));
                    ctx.translate(0, 15);
                    ctx.fillText(label, x - offset_x, origin.y + offset_y);
                    ctx.restore();
                }
                last_label = label;
            }

            // draw the  axis titles
            /*
            ctx.font = '14px san-serif';
            var title = "Wow";
            ctx.fillText(title, (origin.x+outer.x)/2, origin.y+40);
            var title = "MB";
            var x = origin.x-30;
            var y = (origin.y+outer.y)/2;

            ctx.save();
            ctx.translate(+x, +y);
            ctx.rotate(-Math.PI/2);
            ctx.translate(-x, -y);
            ctx.fillText(title, +x, +y);
            ctx.restore();
            */



            // draw the vertical grid lines
            var multiplier = 1;

            var too_big = false;
            while (1) {
                var num_lines = (origin.y - outer.y) / (interval.y * multiplier);
                if (num_lines > 10) {
                    multiplier = multiplier * 10;
                }
                else if (num_lines < 5) {
                    multiplier = multiplier / 2;
                }
                else {
                    break;
                }
            }
            interval.y = interval.y * multiplier;

            if (bvr.mode == 'integer') {
                multiplier = parseInt(multiplier);
            }


            var color2 = 'rgba(240, 240, 240, 0.5)';
            for (var i = 0; ; i++) {
                if (i > 1000) break;

                var label = i*multiplier

                var y = origin.y - i*interval.y;
                if (y < outer.y) break;

                var start = {x: origin.x-1, y: y};
                var end = {x: origin.x-5, y: y};
                spt.chart.draw_line( start, end, "#999" );

                if (i == 0) continue;

                var start = {x: origin.x+1, y: y};
                var end = {x: outer.x, y: y};
                spt.chart.draw_line( start, end, color2 );

                // draw the label
                var ctx = spt.chart.get_ctx();
                ctx.fillStyle = bvr.font_color;
                ctx.font = bvr.font;
                ctx.textBaseline = 'bottom';
                var length = (label+"").length;
                var offset = (length-1) * 3;
                ctx.fillText(label, origin.x - 20 - offset, origin.y - i*interval.y+8);

            }

            '''
        } )

        return top




class ChartData(BaseRefreshWdg):

    def init(my):
        my.index = 0
        my.total_index = 0

    def get_chart_type(my):
        return my.chart_type

    def set_chart_type(my, chart_type):
        my.chart_type = chart_type


    def get_data(my):
        return my.data

    def set_data(my, data):
        my.data = data

    def get_xdata(my):
        return my.x_data

    def set_index(my, index, total_index):
        my.index = index
        my.total_index = total_index


    def init(my):
        my.chart_type = my.kwargs.get("chart_type")
        my.index = my.kwargs.get("index")
        my.data = my.kwargs.get("data")
        my.x_data = my.kwargs.get("x_data")

        if my.chart_type == 'function':
            my.data = my.handle_func(my.data)
            my.chart_type = 'line'
        elif my.chart_type == 'polynomial':
            my.data = my.handle_polynomial(my.data)
            my.chart_type = 'line'


    def get_display(my):

        labels = my.kwargs.get("labels")
        color = my.kwargs.get("color")

        if not my.chart_type:
            my.chart_type = 'bar'


        my.x_data = my.kwargs.get("x_data")
        if not my.x_data:
            my.x_data = [0]

        top = my.top

        top.add_behavior( {
        'type': 'load',
        'color': color,
        'index': str(my.index),
        'total_index': str(my.total_index),
        'chart_type': my.chart_type,
        'data': my.data,
        'x_data': my.x_data,
        'cbjs_action': '''
        var size = spt.chart.get_size();
        var index = parseInt(bvr.index);
        var total_index = parseInt(bvr.total_index);

        var type = bvr.chart_type;

        var origin = spt.chart.get_origin();
        var outer = spt.chart.get_outer();

        var interval = spt.chart.get_interval();

        var last = null;
        var last_x = 0;
        for (var i = 0; i < bvr.data.length; i++) {

            var x_value = bvr.x_data[i];
            var x;
            if (typeof(x_value) == 'undefined') {
                x = last_x + interval.x;
            }
            else {
                x = x_value*interval.x;
            }
            last_x = x;


            var y = bvr.data[i]*interval.y;
            var cur = spt.chart.get_pos(x, y);

            // skip first
            if (type != 'bar') {
                if (i == 0) {
                    last = cur;
                    //spt.chart.draw_dot( x, y, 3, "#000" );
                    continue;
                }
            }


            if (type == 'area') {
                spt.chart.draw_area( last, cur, bvr.color );
                //spt.chart.draw_dot( x, y, 3, "#000" );
            }
            else if (type == 'line') {
                spt.chart.draw_line( last, cur, bvr.color );
                //spt.chart.draw_dot( x, y, 3, "#000" );
            }
            else {
                var width = interval.x * 0.5 / bvr.total_index;
                var pos = {x: cur.x - (bvr.total_index*width/2), y: cur.y};
                spt.chart.draw_bar( pos, index, bvr.color, width );
            }


            last = cur;
        }

        '''
        } )

        return top



    def handle_func(my, data):
        # take the data and fit it?
        """
        data = [10, 8, 5, 3, 1.5]
        slope = 0
        last = 0
        for i, item in enumerate(data):
            if i == 0:
                last = item
                continue

            slope += item - last
            last = item

        slope = slope / i
        print "slope: ", slope
        """

        # find b: this isn't so necessary here because we have point 0
        m = data.get("m")
        b = data.get("b")
        start = data.get("start")
        end = data.get("end")

        # linear
        func = 'm*x + b'
        func = func.replace("m", str(m))
        func = func.replace("b", str(b))
        data = []
        for x in range(0, 10):
            y = eval(func)
            if y < 0:
                break
            data.append(y)

        return data


    def handle_polynomial(my, data):
        func = 'a*x*x + b*x *c'

        # find b: this isn't so necessary here because we have point 0
        a = data.get("a")
        b = data.get("b")
        c = data.get("c")
        start = data.get("start")
        end = data.get("end")

        # linear
        func = func.replace("a", str(a))
        func = func.replace("b", str(b))
        func = func.replace("c", str(c))
        data = []
        for x in range(0, 10):
            x = float(x)
            y = eval(func)
            if y < 0:
                break
            data.append(y)

        return data


class ChartLegend(BaseRefreshWdg):

    def add_style(my, name, value=None):
        my.top.add_style(name, value)

    def set_labels(my, labels):
        my.kwargs['labels'] = labels

    def set_colors(my, colors):
        my.kwargs['colors'] = colors

    def get_display(my):

        top = my.top
        labels = my.kwargs.get("labels")
        if not labels:
            return top

        if isinstance(labels, basestring):
            labels = labels.split("|")


        top.add_style("padding: 3px")
        top.add_color("background", "background3")
        top.add_border()


        colors = my.kwargs.get("colors")


        # draw a legend
        for i, label in enumerate(labels):

            label_div = DivWdg()
            top.add(label_div)
            label_div.add_style("float: left")

            #label_div.set_round_corners()
            label_div.add_style("padding: 0 15 3 15")

            color_div = DivWdg()
            color_div.add_style("width: 12px")
            color_div.add_style("height: 12px")

            if colors:
                color_div.add_style("background: %s" % colors[i])
                label_div.add(color_div)
                color_div.add_style("float: left")
                color_div.add_style("margin-right: 10px")
                color_div.add_style("margin-top: 2px")
            else:
                label_div.add("+ ")
            label_div.add(label)

        top.add("<br/>")

        return top



ONLOAD_JS = '''

spt.chart = {}

spt.chart.top = null;

spt.chart.data = {};
spt.chart.data.scale = {x: 1.0, y: 1.0};

spt.chart.get_top = function() {
    return spt.chart.top;
}


spt.chart.get_data = function() {
    return spt.chart.data;
}


spt.chart.set_range = function(x, y) {
    var data = spt.chart.get_data();
    data.xmax = x;
    data.ymax = y;
}



spt.chart.get_size = function() {
    var top = spt.chart.get_top();
    return top.getSize();
}


spt.chart.set_scale = function(x, y) {
    spt.chart.data.scale = {x: x, y: y};

}

spt.chart.get_scale = function() {
    return spt.chart.data.scale;
}




spt.chart.get_origin = function() {
    var size = spt.chart.get_size();
    var x_offset = 50;
    var y_offset = 50;
    var origin = {
        x: x_offset,
        y: size.y - y_offset
    }
    return origin;
}


spt.chart.get_outer = function() {
    var size = spt.chart.get_size();
    var x_offset = 50;
    var y_offset = 15;
    var outer = {
        x: size.x - x_offset,
        y: y_offset 
    }
    return outer;
}


spt.chart.get_pos = function(x, y) {
    var origin = spt.chart.get_origin();
    var pos = {
        x: origin.x + x,
        y: origin.y - y
    }
    return pos;
}


spt.chart.get_interval = function() {
    var origin = spt.chart.get_origin();
    var outer = spt.chart.get_outer();

    var data = spt.chart.get_data();

    var interval = {};

    var grid_height = origin.y - outer.y;

    if (data.ymax == 0) {
        interval.y = 1;
    }
    else {
        interval.y = grid_height / data.ymax;
    }


    var grid_width = outer.x - origin.x;

    if (data.xmax == 0) {
        interval.x = 1;
    }
    else {
        interval.x = grid_width / data.xmax;
    }


    return interval;
}



spt.chart.get_ctx = function() {
    var top = spt.chart.get_top();
    //var chart = top.getElement(".spt_chart");
    var ctx = top.getContext('2d');
    return ctx;
}
 
spt.chart.draw_line = function(start, end, color, width) {
    var origin = spt.chart.get_origin();

    var ctx = spt.chart.get_ctx();
    ctx.strokeStyle = color;  
    if (!width) width = 1;
    ctx.lineWidth = width;
    ctx.beginPath();

    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
}


spt.chart.draw_area = function(start, end, color) {
    var origin = spt.chart.get_origin();

    var ctx = spt.chart.get_ctx();
    ctx.strokeStyle = color;  

    //ctx.fillStyle = color;  
    var gradient = ctx.createLinearGradient(0,0,0,origin.y);
    gradient.addColorStop(0, '#FFF');
    //gradient.addColorStop(0.75, color);
    gradient.addColorStop(1, color);
    ctx.fillStyle = gradient;
 

    ctx.beginPath();

    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.lineTo(end.x, origin.y-1);
    ctx.lineTo(start.x, origin.y-1);
    ctx.closePath();

    ctx.fill();

    var width = 1;
    spt.chart.draw_line(start, end, 'rgba(100,145,164,1)', width);

}


spt.chart.draw_bar = function(pos, index, color, width) {
    var origin = spt.chart.get_origin();

    var ctx = spt.chart.get_ctx();

    ctx.strokeStyle = spt.css.modify_color_value(color, -5);
    //ctx.strokeStyle = color;

    //var gradient = ctx.createLinearGradient(0,pos.y,0,origin.y);
    var gradient = ctx.createLinearGradient(0,0,0,origin.y);
    gradient.addColorStop(0, '#FFF');
    gradient.addColorStop(0.75, color);
    gradient.addColorStop(1, color);
    ctx.fillStyle = gradient;
    //ctx.fillStyle = color;  



    ctx.lineWidth = 2;
    ctx.beginPath();

    var width;
    if (!width) {
        width = 10;
    }

    var offset = index * (width+3);

    ctx.moveTo(pos.x+offset, origin.y-1);
    ctx.lineTo(pos.x+offset, pos.y);
    ctx.lineTo(pos.x+offset+width, pos.y);
    ctx.lineTo(pos.x+offset+width, origin.y-1);
    ctx.closePath();
    ctx.stroke();

    ctx.fill();

}



spt.chart.draw_dot = function(x, y, size, color) {

    var pos = spt.chart.get_pos(x, y);

    var ctx = spt.chart.get_ctx();
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, size, 0, Math.PI*2, true);
    ctx.closePath();
    ctx.fill();
}


        '''





"""
<config>
  <burndown_chart_wdg>
<html>
  <style type="text/css">
    table {color:#000;}
  </style>


  <div class="spt_top" style="background:none; padding:10px; width:100%; text-align:center">
    <h4>Burndown Report</h4>
    <![CDATA[

    <canvas class="spt_canvas" id="canvas" width="1000" height="300" style="background:#FFF;">No HTML5 Canvas Support</canvas>


    ]]>

  </div>
</html>



   <behavior class='spt_top'>{
      "type": "load",
      "cbjs_action": <![CDATA['''
        try {

            // Options
            var x_pad = 30;
            var y_pad = 30;
            var label_pad = 10;           

            // Setup
            var server = TacticServerStub.get();

            var canvas;
            var ctx;
            var x_spacing;
            var max_value;
            var x = 0;
            var y = 0;
            var x_vals = [];
            var WIDTH;
            var HEIGHT;


          // Init
          function init() {
              // Get the top elements
              var top_el = bvr.src_el;
              var canvas = top_el.getElement(".spt_canvas");
              WIDTH = canvas.getAttribute("width") - x_pad*2;
              HEIGHT = canvas.getAttribute("height") - y_pad*2;
              ctx = canvas.getContext("2d");
              draw();
          }



          // Draw the graph
          function draw() {
              clear();
              
              // Get the x-axis values
              x_vals = server.eval("@GET(project/burndown.code)")
              x_spacing = WIDTH / x_vals.length;
              max_value = server.eval("@COUNT(sthpw/task['project_code', $PROJECT])")

              // Setup the base graph
              drawaxes();
              addlabels();
              drawgrid();

              // Get the Data
              var y_proj_vals = server.eval("@GET(project/burndown.tasks_due)");
              var y_curr_vals = server.eval("@GET(project/burndown['tasks_remaining', '>', 0].tasks_remaining)");
              var y_velo_vals = server.eval("@GET(project/burndown.velocity)");

              // Draw the date 
              plotdata(y_proj_vals, "#000", "rgba(255,100,100, 0.5)", 1)
              plotdata(y_curr_vals, "#000","rgba(100,255,100, 0.5)", 1)
              plotdata(y_velo_vals, "red", "rgba(0,0,0, 0)", 0)
          }



          // Clear Rect
          function clear() {
              ctx.clearRect(0, 0, WIDTH, HEIGHT);
          }


          // Get the Max value for the y-axis
          function getmax(values) {
              var curr = 0;
              for (i=0; i<values.length; i++) {
                  if (values[i] > curr) {
                      curr = values[i];
                  }
              }
              return curr;
          }



          // Draw the axes
          function drawaxes(){
              ctx.strokeStyle = "black";

              /* y axis along the left edge of the canvas*/

              ctx.beginPath();
              ctx.moveTo(x_pad, HEIGHT+y_pad*2);
              ctx.lineTo(x_pad,0);
              ctx.stroke();

              /* x axis along the bottom edge of the canvas*/
              ctx.moveTo(0,HEIGHT+y_pad);
              ctx.lineTo(WIDTH+x_pad*2,HEIGHT+y_pad);
              ctx.stroke();
          }


          // Draw the Grid
          function drawgrid() {
              /* y axis grid */
              ctx.strokeStyle = "rgba(100, 100, 100, 0.25)";
              ctx.beginPath();
              var y_spacing = HEIGHT / 10;
              for (i=0; i<10; i++) {
                  var y_pos = HEIGHT+y_pad - (y_spacing * i);
                  ctx.moveTo(x_pad, y_pos);
                  ctx.lineTo(WIDTH, y_pos);                
              }                
              ctx.stroke();
          }


          // Add Labels to the graph
          function addlabels(){
              ctx.font = '12px san-serif';
  
              /* y axis labels */
              var y_spacing = HEIGHT / 10;
              var y_units = max_value / 10;
              for (i=0; i<10; i++) {
                  var y_val = Math.round(y_units * i);
                  var y_pos = HEIGHT+y_pad - (y_spacing * i);
                  ctx.fillText(y_val, label_pad, y_pos);                
              }                

              /* x axis labels */
              for (i=0; i<x_vals.length; i++) {
                  var x_val =x_vals[i];
                  var x_pos = x_pad +(x_spacing * i);
                  ctx.fillText(x_val, x_pos, (HEIGHT+y_pad*2) - label_pad);                
              } 
          }  


          // Draw a graph dot 
          function drawdot(x, y, size) {
              ctx.fillStyle = "rgba(0, 0, 0, 1)"
              ctx.beginPath();
              ctx.arc(x, y, size, 0, Math.PI*2, true);
              ctx.closePath();
              ctx.fill();
          }


          // Plot Data
          function plotdata(values, stroke_color, fill_style, has_dots){
              ctx.strokeStyle = stroke_color;
              ctx.fillStyle = fill_style;
              ctx.beginPath();
              ctx.moveTo(x_pad, HEIGHT+y_pad);
            
              for (j=0; j<values.length; j++){
                  x = x_pad + (j*x_spacing);
                  y = (HEIGHT+y_pad) -((HEIGHT+y_pad) * (values[j]/max_value));
                  ctx.lineTo(x,y);
              }
              ctx.lineTo(x, HEIGHT+y_pad);
              ctx.closePath();
              ctx.stroke();
              ctx.fill();
              if (has_dots == 1) {
                  for (j=0; j<values.length; j++){
                      var x = x_pad + (j*x_spacing);
                      var y = (HEIGHT+y_pad) -((HEIGHT+y_pad) * (values[j]/max_value));
                      drawdot(x, y, 3);
                  }
              }
          }


        init();



        }
        catch(err) {
          alert(err)
          spt.app_busy.hide();
        }
        
      ''']]>
    }</behavior>



 </burndown_chart_wdg>
</config>
"""
