from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
import re
from io import StringIO
import csv

#,IVCA CALENDAR 2022,,,,,
#Description,Date,Detail,Type,Distance,Sign-on/Venue,Time
#

cal = Calendar()
txt='''12/04/23,Corkagh Park,19:00:00,Limit/Semi Limit Corkagh Park,Orwell
13/04/23,Corkagh Park,19:00:00,Scratch/Semi Scratch Corkagh Park,Orwell
20/04/23,Brittas,19:00:00,Lap of the Lakes,STCC
27/04/23,unknown,19:00:00,Hill Climb TT,IRC
04/05/23,Green Sheds,19:00:00,Donal Gleeson Memorial,Blanch Wheelies
11/05/23,Coolquay,19:00:00,Coolquay,Lucan
25/05/23,Johnstown Bridge,19:30:00,10 mile TT,IRC
01/06/23,Brittas,19:00:00,Sally Gap Finish,Lucan
08/06/23,Mondello,19:30:00,Mondello,Lucan
15/06/23,Corkagh Park,19:00:00,Devil takes the hindmost,Sundrive
22/06/23,Curragh,19:30:00,Newbridge GP Circuit,Blanch Wheelies
29/06/23,Brittas,19:00:00,Brittas,Orwell
01/07/23,Curragh,10:00:00,Club Champs,STCC
06/07/23,Mondello,19:30:00,Mondello,Sundrive
13/07/23,Trim Road,19:00:00,25 mile 1T,IRC
20/07/23,Doreys/Green Sheds,19:00:00,Doreys/Green Sheds,Sundrive
27/07/23,Blessington,19:00:00,Point to Point,Orwell
10/08/23,Doreys/Green Sheds,19:00:00,Doreys/Green Sheds,Blanch Wheelies
17/08/23,Blessington,19:00:00,Prize Giving,STCC'''
#0 = date, 1=location, 2=time, 3=details, 4 organiser,


def text_to_events(text: str):
    """
    Convert the text to a list of events
    :param text:
    :return:
    """

    events = []
    for l in text.splitlines():
        m = l.split(",")
        _event = Event()
        _event.add('summary', "[ICL] {} at {} organised by {}".format(m[3], m[1], m[4]))
        st = datetime.strptime("{} {} +0100".format(m[2], m[0]), "%H:%M:%S %d/%m/%y %z")
        et = st + timedelta(hours=3)
        _event.add('dtstart', st)
        _event.add('dtend', et)
        #_event.add('dtend', datetime.strptime("21:00 {} 2022 +0100".format(m.group(1)), "%H:%M %d %b %Y %z"))
        _event['organizer'] = m[4]
        _event['location'] = vText('{}, Ireland'.format(m[1]))
        events.append(_event)

    return events


for event in text_to_events(txt):
    cal.add_component(event)

# Adding events to calendar

f = open('icl_2023.ics', 'wb')
f.write(cal.to_ical())
f.close()