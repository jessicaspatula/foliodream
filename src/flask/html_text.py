def html_headers():
    h = "<!DOCTYPE html>"
    h += "<html>"
    h += "   <head>"
    h += "     <meta charset=\"utf-8\">"
    h += "     <title>FolioDream</title>"
    return h

def html_headers_b():
    h = "  </head>"
    h += "  <body>"
    h += "     <h1>FolioDream</h1>"
    return h

def display_opportunity_div(opps, action):
    ht =  "<div class=\"AlertDiv\" >"
    ht += "<h2>"+ action  +"</h2>"
    ht += "<ul>"
    for row in opps:
        ht += "<li>"
        for i in row:
           ht +=  " " + i
        ht += "</li>"
    ht += "</ul>"
    ht += "</div>"
    return ht
