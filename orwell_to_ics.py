from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta


cal = Calendar()
txt = """10 April 2024, Corkagh Park,19:00,L/SL Corkagh Park ,Orwell
11 April 2024, Corkagh Park,19:00,S/SS ThursdayCorkagh Park ,Orwell
18 April 2024,Brittas,19:00,Lap of the Lakes ,Sundrive
25 April 2024,Coolquay,19:00,Coolquay,Lucan
02 May 2024,Dunboyne,19:00,Donal Gleeson Memorial,Blanch Wheelies
09 May 2024,Corkagh Park,19:00,L/SL @ 7.00 - S/SS @ 7.45 ,Clondalkin
16 May 2024,Dunboyne,19:00,10 mile TT,Lucan
23 May 2024,Doreys/Green Sheds,19:00,Doreys/Green Sheds ,Blanch Wheelies
30 May 2024,Brittas,19:00,Sally Gap Finish ,STCC
06 June 2024,Mondello,19:30 ,Mondello,Clondalkin
13 June 2024,Hill Climb TT,19:00,Hill Climb TT,STCC
20 June 2024,Curragh,19:30 ,Newbridge GP Circuit,Blanch Wheelies
27 June 2024,Blessington,19:00,Russborough,Orwell
11 July 2024,Mondello,19:30,Mondello,Sundrive
18 July 2024,Trim Road TT,19:00,25 mile TT,Clondalkin
25 July 2024,Point to Point,19:00,Blessington roll out,Orwell
08 August 2024,Doreys/Green Sheds,19:00,Doreys/Green Sheds,Sundrive
15 August 2024,Blessington,19:00,Prize Giving,STCC
17 August 2024,Curragh,10:00,Club Champs,Lucan"""
# 0 = date, 1=location, 2=time, 3=details, 4 organiser,


def text_to_events(text: str):
    """
    Convert the text to a list of events
    :param text:
    :return:
    """

    events = []
    for _l in text.splitlines():
        m = _l.split(",")
        _event = Event()
        _event.add("summary", "[ICL] {} at {} organised by {}".format(m[3], m[1], m[4]))
        st = datetime.strptime("{} {} +0100".format(m[2], m[0]), "%H:%M %d %B %Y %z")
        et = st + timedelta(hours=3)
        _event.add("dtstart", st)
        _event.add("dtend", et)
        # _event.add('dtend', datetime.strptime("21:00 {} 2022 +0100".format(m.group(1)), "%H:%M %d %b %Y %z"))
        _event["organizer"] = m[4]
        _event["location"] = vText("{}, Ireland".format(m[1]))
        events.append(_event)
        print(f"Found Event {_event['summary']} at {_event["location"]} on {repr(st)}")

    return events


for event in text_to_events(txt):
    cal.add_component(event)

# Adding events to calendar

f = open("icl_2024.ics", "wb")
f.write(cal.to_ical())
f.close()
