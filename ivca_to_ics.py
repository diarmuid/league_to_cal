from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
import re
from io import StringIO
import csv

#,IVCA CALENDAR 2022,,,,,
#Description,Date,Detail,Type,Distance,Sign-on/Venue,Time
#

cal = Calendar()
txt='''1,Pre-Race,Sat 16 Mar 2024,Safety Briefing 1a Springfield Hotel,,Leixlip,14:00
2,Pre-Race,Sat 16 Mar 2024,Safety Briefing 1b Springfield Hotel,,Leixlip,16:00
3,Pre-Race,Sun 24 Mar 2024,Safety Briefing 2a Springfield Hotel,,Leixlip,14:00
4,Pre-Race,Sun 24 Mar 2024,Safety Briefing 2b Springfield Hotel,,Leixlip,16:00
5,Pre-Race,Tue 26 Mar 2024,Safety Briefing 3 Springfield Hotel,,Leixlip,19:30
6,SR_01,Sun 31 Mar 2024,IVCA,DMS,Dunsany/Green Sheds,09:00
7,SR_02,Sun 07 Apr 2024,IVCA,DMS,Jack White's,09:00
8,SR_03,Sun 14 Apr 2024,IVCA,DMS,Hatchet/Dorey's Forge,09:00
9,SR_04,Sun 21 Apr 2024,IVCA,DMS,Carlow,09:00
10,TT_01,Tue 23 Apr 2024,IVCA,TT 10M,Batterstown,09:00
11,SR_05,Sun 28 Apr 2024,IVCA,DMS,Dromiskin GAA,09:00
12,TT_02,Tue 30 Apr 2024,Oliver Bright,TT 10M,Batterstown,09:00
13,SR_06,Sun 05 May 2024,Henry Whelan,DMS,Summerhill (Long),09:00
14,TueR_01,Tue 07 May 2024,IVCA,DMS,Dunsany/Kilmessan,19:00
15,TT_03,Sat 11 May 2024,Tom Dempsey,TT 10M,Moy Valley,09:00
16,SR_07,Sun 12 May 2024,IVCA,DMS,Curragh,09:00
17,TueR_02,Tue 14 May 2024,IVCA,DMS,Hatchet/Culmullin,19:15
18,TT_04,Sat 18 May 2024,IVCA,TT 10M,Kilcock,09:00
19,AR_1,Sun 19 May 2024,40/50/60/70 Champs Age,DMS,Kilcullen,09:00
20,TueR_03,Tue 21 May 2024,IVCA,DMS,S.Hill/Dorey's Forge,19:15
21,SR_08,Sun 26 May 2024,Gerry Brannigan Mem,DMS,Dunsany/Green Sheds,09:00
22,TueR_04,Tue 28 May 2024,IVCA,DMS,Dunsany/Kilmessan,19:15
23,TT_05,Tue 28 May 2024,Kelly Cup,TT 25M,Batterstown,19:00
24,TT_06,Sun 02 Jun 2024,Championship,TT 10M,Moy Valley,09:00
25,Non_League,Mon 03 Jun 2024,Gerry Kinsella Classic,DMS,Hatchet/Culmullin,09:00
26,TueR_05,Tue 04 Jun 2024,IVCA,DMS,Summerhill (Short),19:15
27,Tour,Sun 09 Jun 2024,Wicklow 200,Tour,09:00 Bray Emmets GAA,07:00
28,TueR_06,Tue 11 Jun 2024,IVCA,DMS,Hatchet/Culmullin,19:15
29,TRK_1,Fri 14 Jun 2024,Omnium,Track,Sundrive,09:00
30,TT_07,Sat 15 Jun 2024,Fred Smith,TT 25M,Moy Valley,09:00
31,SR_09,Sun 16 Jun 2024,Dermot McGrath,DMS,Kilcullen,09:00
32,TueR_07,Tue 18 Jun 2024,IVCA,DMS,Dunsany/Kilmessan,19:15
33,AR_2,Sun 23 Jun 2024,Founders 50,CP,Summerhill (Long),09:00
34,TueR_08,Tue 25 Jun 2024,IVCA,DMS,Hatchet/Culmullin,19:15
35,SR_10,Sun 30 Jun 2024,IVCA,DMS,Curragh,09:00
36,TT_08,Sun 30 Jun 2024,Championship,TT 25M,Moy Valley,09:00
37,TueR_09,Tue 02 Jul 2024,IVCA,DMS,S.Hill/Dorey's Forge,19:15
38,TRK_2,Fri 05 Jul 2024,Omnium,Track,Sundrive,09:00
39,SR_11,Sun 07 Jul 2024,Millenium Cup,DMS,Carlow,09:00
40,TueR_10,Tue 09 Jul 2024,IVCA,DMS,Dunsany/Green Sheds,19:15
41,TT_09,Sat 13 Jul 2024,IVCA,TT 10M,Jack White's,19:00
42,SR_12,Sun 14 Jul 2024,Sonny Cullen,DMS,Kilcullen,09:00
43,TueR_11,Tue 16 Jul 2024,IVCA,DMS,Hatchet/Culmullin,19:15
44,TRK_3,Sat 20 Jul 2024,Championship,Track,Sundrive,09:00
45,TRK_4,Sun 21 Jul 2024,Championship,Track,Sundrive,09:00
46,SR_13,Sun 21 Jul 2024,IVCA,DMS,Clonard,09:00
47,TueR_12,Tue 23 Jul 2024,IVCA,DMS,Summerhill (Short),19:15
48,TT_10,Sat 27 Jul 2024,Championship,TT 50M,Moy Valley,09:00
49,SR_14,Sun 28 Jul 2024,Phoenix Cup,DMS,Tullamore,09:00
50,TueR_13,Tue 30 Jul 2024,IVCA,DMS,Dunsany/Green Sheds,19:15
51,SR_15,Sun 04 Aug 2024,IVCA,DMS,Hatchet/Green Sheds,09:00
52,TueR_14,Tue 06 Aug 2024,IVCA,DMS,S.Hill/Dorey's Forge,19:00
53,TT_11,Sat 10 Aug 2024,IVCA,TT 10M,Kilcock,09:00
54,AR_3,Sun 11 Aug 2024,IVCA Age,CP,Summerhill (Long),09:00
55,TT_12,Tue 13 Aug 2024,IVCA,TT 10M,Batterstown,19:00
56,SR_16,Sun 18 Aug 2024,Memorial Cups,DMS,Jack White's,09:00
57,SR_17,Sun 25 Aug 2024,IVCA,DMS,Curragh,09:00
58,TT_13,Sun 25 Aug 2024,Alfresco Shield,TT 25M, Moy Valley,09:00
59,SR_18,Sun 01 Sep 2024,IVCA,DMS,Dunsany/Green Sheds,09:00
60,TT_14,Sat 07 Sep 2024,Options,TT 25/50M,Moy Valley,09:00
61,AR_4,Sun 08 Sep 2024,Kevin Simms Age,CP,Summerhill (Long),09:00
62,Non_League,Sun 15 Sep 2024,IVCA,DMS,Kilcullen,09:00
63,TT_15,Sat 21 Sep 2024,Sanyo Cup,TT Hattons,Summerhill,09:00
64,SR_19,Sun 22 Sep 2024,IVCA,DMS,Dunsany/Green Sheds,09:00
65,AGM,Sun 22 Sep 2024,After Race,,Dunsany GAA,12:00
66,SR_20,Sun 29 Sep 2024,IVCA,DMS,Hatchet/Dorey's Forge,09:00
67,TT_16,Sun 06 Oct 2024,Hill Climb,TT,Rathcoole,09:00'''
#0 = number 1= code 2=date, 3=title,4= code 5=location, 6=time


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
        _event.add('summary', "[IVCA] #{} {} {} {} in {} at {}".format(m[0], m[1], m[3],m[4], m[5], m[6]))
        st = datetime.strptime("{} {} +0100".format(m[6], m[2]), "%H:%M %a %d %b %Y %z")
        et = st + timedelta(hours=3)
        _event.add('dtstart', st)
        _event.add('dtend', et)
        #_event.add('dtend', datetime.strptime("21:00 {} 2022 +0100".format(m.group(1)), "%H:%M %d %b %Y %z"))
        _event['organizer'] = organizer
        _event['location'] = vText('{}, Ireland'.format(m[4]))
        events.append(_event)

    return events


organizer = vCalAddress('MAILTO:racecom@theivca.com')
organizer.params['cn'] = vText('IVCA')
organizer.params['role'] = vText('Race Comms')
for event in text_to_events(txt):
    cal.add_component(event)

# Adding events to calendar

f = open('ivca_2024.ics', 'wb')
f.write(cal.to_ical())
f.close()