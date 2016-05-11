from pyasm.web import DivWdg
from tactic.ui.common import BaseTableElementWdg

class MyElementWdg(BaseTableElementWdg):
  def get_display(my):
    sobject = my.get_current_sobject()

    first_name = sobject.get_value("first_name")
    last_name = sobject.get_value("last_name")

    div = DivWdg()
    div.add("%s %s" % (first_name, last_name) )
    div.add("<a target='_blank' href='/tactic/ziryab/link/reports_homepage'>Graph</a>&nbsp;&nbsp;")

    info_div = DivWdg()

    #info_div.add( sobject.get_name() )
    #info_div.add( " <i style='font-size: 0.8em; opacity: 0.5'>(%s)</i>" % sobject.get_code() )
    #info_div.add("<hr/>")

    info_div.add_attr("spt_search_key", '/tactic/ziryab/link/reports_homepage')

    info_div.add("<a href='%s' target='_blank'>" % '/tactic/ziryab/link/reports_homepage')
    info_div.add("%s %s" % (first_name, last_name))

    info_div.add(" <i style='opacity: 0.5; font-size: 0.8em'> - ")
    info_div.add("Foo Bar")
    info_div.add(" (v%0.3d)" % 7)


    info_div.add("</i></a><br/>")

    return info_div

