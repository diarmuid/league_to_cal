from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
import re
from io import StringIO
import csv

#,IVCA CALENDAR 2022,,,,,
#Description,Date,Detail,Type,Distance,Sign-on/Venue,Time
#

cal = Calendar()
txt='''TOUR1,Sun 15 Jan 2023, East Kildare Tour Tour 75km, Liffey Valley,10:00
TOUR2,Sun 12 Feb 2023, Wheel Meath Tour 70km ,Clonee,10:00
TOUR3,Sun 12 Mar 2023, 50 in 4 Tour 80km ,Clonee,10:00
SR_01,Sun 02 Apr 2023, IVCA DMS,Dunsany/Green Sheds,09:00
SR_02,Sun 09 Apr 2023, IVCA DMS, Jack White's,09:00
TOUR4,Sun 09 Apr 2023, Liam Horner Tour 75km ,Clonee,10:00
SR_03,Sun 16 Apr 2023, IVCA DMS,Hatchet/Dorey's Forge,09:00
SR_04,Sun 23 Apr 2023, IVCA DMS ,Carlow,09:00
TTL_01,Tue 25 Apr 2023, IVCA TT 10mls ,Batterstown,19:15
SR_05,Sun 30 Apr 2023, IVCA DMS/Wm,Dromiskin GAA,09:00
TTL_02,Tue 02 May 2023, Oliver Bright TT 10mls ,Batterstown,19:15
SR_06,Sun 07 May 2023, Henry Whelan DMS ,Monasterevin,09:00
TTL_03,Sat 13 May 2023, Tom Dempsey TT 10mls, Moy Valley,09:00
TOUR5,Sun 14 May 2023, Mind the Gaps Tour 120km ,Tallaght,09:00
SR_07,Sun 14 May 2023, IVCA DMS ,Curragh,09:00
TueR_01,Tue 16 May 2023, IVCA DMS,Dunsany/Kilmessan,19:15
Sat TT_01,Sat 20 May 2023, Saturday 10 TT Series TT 10mls ,Kilcock,09:00
SR_08,Sun 21 May 2023, IVCA DMS/Wm ,Kilcullen,09:00
TueR_02,Tue 23 May 2023, IVCA DMS, Hatchet/Culmullin,19:15
SR_09,Sun 28 May 2023, Gerry Brannigan Mem DMS, Dunsany/Green Sheds,09:00
TTL_04,Tue 30 May 2023, Kelly Cup TT 25mls ,Batterstown,19:15
TueR_03,Tue 30 May 2023, IVCA DMS,Hatchet/Dorey's Forge,19:15
TTL_05,Sun 04 Jun 2023, Championship TT 10mls, Moy Valley,09:00
Non League,Mon 05 Jun 2023, Gerry Kinsella Classic DMS,Hatchet/Culmullin,09:00
TueR_04,Tue 06 Jun 2023, IVCA DMS,Dunsany/Kilmessan,19:15
TRK_1,Fri 09 Jun 2023, Accreditation Track,Sundrive Velodrome,18:30
Tour 6,Sun 11 Jun 2023, Wicklow 200 Tour 200/150/10, Bray Emmets GAA,07:00
TueR_05,Tue 13 Jun 2023, IVCA DMS,Summerhill (Short),19:15
TTL_06,Sat 17 Jun 2023, Fred Smith TT 25mls, Moy Valley,09:00
AR 1,Sun 18 Jun 2023, Founders 50 CP ,Kilcullen,09:00
TueR_06,Tue 20 Jun 2023, IVCA DMS,Dunsany/Green Sheds,19:15
SR_10,Sun 25 Jun 2023, Phoenix Cup DMS/Wm ,Tullamore,09:00
TueR_07,Tue 27 Jun 2023, IVCA DMS,Summerhill (Short) ,19:15
TRK_2,Fri 30 Jun 2023, Racing Track,Sundrive Velodrome,18:30
AR 2,Sun 02 Jul 2023, 40/50/60/70 Champs Age DMS,Summerhill (Long) ,09:00
TueR_08,Tue 04 Jul 2023, IVCA DMS,Dunsany/Kilmessan,19:15
TTL_07,Tue 04 Jul 2023, Championship TT 25mls,Moy Valley,19:15
TOUR7,Sun 09 Jul 2023, Meath Again Tour 70km,Clonee,10:00
SR_11,Sun 09 Jul 2023, Millenium Cup DMS,Carlow,09:00
TueR_09,Tue 11 Jul 2023, IVCA DMS,Hatchet/Dorey's Forge,19:15
TTL_08,Sat 15 Jul 2023, Alfresco Shield TT 25mls,Moy Valley,09:00
SR_12,Sun 16 Jul 2023, Sonny Cullen DMS ,Kilcullen,09:00
TueR_10,Tue 18 Jul 2023, IVCA DMS,Hatchet/Green Sheds,19:15
TRK_3,Sat 22 Jul 2023, Championship Track,Sundrive Velodrome,09:00
TRK_4,Sun 23 Jul 2023, Championship Track,Sundrive Velodrome,09:00
TueR_11,Tue 25 Jul 2023, IVCA DMS,Summerhill (Short),19:15
TTL_09,Sat 29 Jul 2023, Championship TT 50mls,Moy Valley,09:00
SR_13,Sun 30 Jul 2023, Dermot McGrath DMS/Wm,Hatchet/Mullagh X,09:00
TueR_12,Tue 01 Aug 2023, IVCA DMS,Hatchet/Culmullin,19:15
SR_14,Sun 06 Aug 2023, IVCA DMS/Wm ,Monasterevin,09:00
Sat TT_02,Sat 12 Aug 2023, Saturday 10 TT Series TT 10mls,Jack White's,09:00
AR 3,Sun 13 Aug 2023, IVCA Age CP,Summerhill (Long) ,09:00
TOUR8,Sun 20 Aug 2023, 100 in 8 Tour 160km ,Clonee,09:00
SR_15,Sun 27 Aug 2023, Memorial Cups DMS,Jack White's,09:00
SR_16,Sun 03 Sep 2023, IVCA DMS ,Curragh,09:00
TOUR9,Sun 10 Sep 2023, Joe Hoare Tour 70km ,Clonee,09:00
AR 4,Sun 10 Sep 2023, Age Champs Age CP,Summerhill (Long) ,09:00
TT,Sat 16 Sep 2023, Sanyo Cup TT 30km ,Warrenstown,10:00
SR_17,Sun 17 Sep 2023, IVCA DMS,Dunsany/Green Sheds,09:00
AGM,Sun 17 Sep 2023, After race,Dunsany GAA,12:00
SR_18,Sun 24 Sep 2023, IVCA DMS,Jack White's,09:00
SR_19,Sun 01 Oct 2023, IVCA DMS,Monasterevin,09:00
TOUR10,Sun 08 Oct 2023, Gay Farnan Tour 40/70km ,Clonee,10:00'''
#0 = title, 1=date, 2=title, 3=location, 4=time


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
        _event.add('summary', "[IVCA] {} {} in {} at {}".format(m[0], m[2], m[3], m[4]))
        st = datetime.strptime("{} {} +0100".format(m[4], m[1]), "%H:%M %a %d %b %Y %z")
        et = st + timedelta(hours=3)
        _event.add('dtstart', st)
        _event.add('dtend', et)
        #_event.add('dtend', datetime.strptime("21:00 {} 2022 +0100".format(m.group(1)), "%H:%M %d %b %Y %z"))
        _event['organizer'] = organizer
        _event['location'] = vText('{}, Ireland'.format(m[3]))
        events.append(_event)

    return events


organizer = vCalAddress('MAILTO:racecom@theivca.com')
organizer.params['cn'] = vText('IVCA')
organizer.params['role'] = vText('Race Comms')
for event in text_to_events(txt):
    cal.add_component(event)

# Adding events to calendar

f = open('ivca_2023.ics', 'wb')
f.write(cal.to_ical())
f.close()