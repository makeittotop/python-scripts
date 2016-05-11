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

__all__ = ['Error403Wdg', 'Error404Wdg' ]

from pyasm.web import Widget, DivWdg, HtmlElement, Table, SpanWdg, WebContainer
from input_wdg import HiddenWdg, TextWdg, PasswordWdg
from web_wdg import SignOutLinkWdg
from header_wdg import ProjectSwitchWdg


class ErrorWdg(Widget):

    LOGIN_MSG = 'login_message'
    def get_display(my):

        box = DivWdg(css='login')

        box.add_style("margin-top: auto")
        box.add_style("margin-bottom: auto")
        box.add_style("text-align: center")

        script = HtmlElement.script('''function login(e) {
                if (!e) var e = window.event;
                if (e.keyCode == 13) {
                submit_icon_button('Submit');
                }}
                ''')
        
        div = DivWdg()
        div.add_style("margin: 0px 0px")
        div.add_class("centered")

        div.add( HtmlElement.br(6) )
        sthpw = SpanWdg("SOUTHPAW TECHNOLOGY INC", css="login_sthpw")
        sthpw.add_style("color: #333")
        div.add( sthpw )
        div.add( HtmlElement.br(2) )

        div.add(my.get_error_wdg() )
        box.add(div)

        widget = Widget()
        #widget.add( HtmlElement.br(3) )
        table = Table()
        table.add_style("width: 100%")
        table.add_style("height: 85%")
        table.add_row()
        td = table.add_cell()
        td.add_style("vertical-align: middle")
        td.add_style("text-align: center")
        td.add_style("background: transparent")
        td.add(box)
        widget.add(table)
        
        return widget


    def get_error_wdg(my):
        '''function to override'''
        pass


    def set_message(my, message):
        my.message = message

    def set_status(my, status):
        my.status = status

class Error404Wdg(ErrorWdg):
    ''' this should be displaying the error status and message, not necessarily 404'''

    def __init__(my):
        # just defaults to 404
        my.status = 404
        my.message = ''
        super(Error404Wdg, my).__init__()

    def get_error_wdg(my):
        div = DivWdg()
        error_div = DivWdg()
        error_div.add("Error %s" % my.status)
        div.add(error_div)
        error_div.add_style("font-size: 16px")
        error_div.add_style("font-weight: bold")
        error_div.add_style("width: auto")
        error_div.add_gradient("background", "background")
        error_div.add_border()
        error_div.add_style("margin-left: 5px")
        error_div.add_style("margin-right: 5px")
        error_div.add_style("margin-top: -10px")

        div.add("<br/>")


        span = DivWdg()
        #span.add_color("color", "color")
        span.add_style("color", "#FFF")
        if my.status == 404:
            span.add(HtmlElement.b("You have tried to access a url that is not recognized."))
        else:
            span.add(HtmlElement.b(my.message))
        span.add(HtmlElement.br(2))

        web = WebContainer.get_web()
        root = web.get_site_root()
        if my.message.startswith('No project ['):
            label = 'You may need to correct the default_project setting in the TACTIC config.'
        else:
            label = "Go to the Main page for a list of valid projects"
        span.add(label)
        div.add(span)
        div.add(HtmlElement.br())

        from tactic.ui.widget import ActionButtonWdg
        button_div = DivWdg()
        button_div.add_style("width: 90px")
        button_div.add_style("margin: 0px auto")

        div.add(button_div)
        button = ActionButtonWdg(title="Go to Main", tip='Click to go to main page')
        button_div.add(button)
        
        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        document.location = '/';
        '''
        } )
        button.add_event("onmouseup", "document.location='/'")

        return div


"""
class Error403Wdg(ErrorWdg):
    def get_error_wdg(my):
        div = DivWdg()
        #div.add_color("color", "color3")
        div.add_style("color", "white")
        div.add("<h3>Error 403: Permission Denied</h3>")
        span = SpanWdg()
        span.add("<b>You have tried to access a url that is not permitted.</b>")
        span.add(HtmlElement.br(2))
        #inner_div = DivWdg(my._get_project_switch())
        inner_div.add_style('margin-right', '130px')
        span.add(inner_div)
        #span.add(SignOutLinkWdg())
        div.add(span)
        return div

    def _get_project_switch(my):
        # can't use anything relying on behavior here
        widget = ProjectSwitchWdg()
        return widget
"""



class Error403Wdg(ErrorWdg):
    ''' this should be displaying the error status and message, not necessarily 404'''

    def __init__(my):
        # just defaults to 404
        my.status = 403
        my.message = ''
        super(Error403Wdg, my).__init__()

    def get_error_wdg(my):
        div = DivWdg()

        error_div = DivWdg()
        error_div.add("Error %s - Permission Denied" % my.status)
        div.add(error_div)
        error_div.add_style("font-size: 16px")
        error_div.add_style("font-weight: bold")
        error_div.add_style("width: 97%")
        error_div.add_gradient("background", "background")
        error_div.add_border()
        error_div.add_style("margin-left: 5px")
        error_div.add_style("margin-top: -10px")

        div.add("<br/>")


        span = DivWdg()
        #span.add_color("color", "color")
        span.add_style("color", "#FFF")
        if my.status == 403:
            span.add("<b>You have tried to access a url that is not permitted.</b>")
        else:
            span.add(HtmlElement.b(my.message))
        span.add(HtmlElement.br(2))

        web = WebContainer.get_web()
        root = web.get_site_root()

        span.add("Go back to the Main page for a list of valid projects")
        div.add(span)
        div.add(HtmlElement.br())

        table = Table()
        div.add(table)
        table.add_row()
        table.add_style("margin-left: auto")
        table.add_style("margin-right: auto")


        from tactic.ui.widget import ActionButtonWdg
        button = ActionButtonWdg(title="Go to Main", tip='Click to go to main page')
        table.add_cell(button)
        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        document.location = '/projects';
        '''
        } )
        button.add_style("margin-left: auto")
        button.add_style("margin-right: auto")

        button = ActionButtonWdg(title="Sign Out", tip='Click to Sign Out')
        table.add_cell(button)
        button.add_behavior( {
        'type': 'click_up',
        'login': web.get_user_name(),
        'cbjs_action': '''
        var server = TacticServerStub.get();
        server.execute_cmd("SignOutCmd", {login: bvr.login} );
        window.location.href='%s';
        ''' % root
        } )
        button.add_style("margin-left: auto")
        button.add_style("margin-right: auto")




        return div


