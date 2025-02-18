from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
import re
from io import StringIO
import csv
from zoneinfo import ZoneInfo

# ,IVCA CALENDAR 2022,,,,,
# Description,Date,Detail,Type,Distance,Sign-on/Venue,Time
#

cal = Calendar()
txt = """1,LL_01,"Sun, 12 Jan",East Kildare Tour,Tour,75km,"Wheelworx, Clondalkin",,
2,LL_02,"Sun, 09 Feb",Wheel Meath in February,Tour,70km,"Grasshopper, Clonee",,
3,LL_03,"Sun, 09 Mar",50 in 4,Tour,80km,"Grasshopper, Clonee",,
4,SR_01,"Sun, 30 Mar",IVCA,DMS,,"Dunsany/Green Sheds",09:00,
5,SR_02,"Sun, 06 Apr",IVCA,DMS,,"Jack White's",09:00,
6,SR_03,"Sun, 13 Apr",IVCA,DMS,,"Hatchet/Dorey's Forge",09:00,
7,LL_04,"Sun, 13 Apr",Liam Horner Memorial,Tour,75km,"Grasshopper, Clonee",,
8,SR_04,"Sun, 20 Apr",IVCA,DMS,,Carlow,09:00,
9,TT_01,"Tue, 22 Apr",IVCA,TT,10,Batterstown,,20:38
10,SR_05,"Sun, 27 Apr",IVCA,DMS,,Clonard,09:00,
11,TT_02,"Tue, 29 Apr",Oliver Bright,TT,10,Batterstown,,20:51
12,SR_06,"Sun, 04 May",Henry Whelan [BLACK],DMS,,"Summerhill (Long)",09:00,
13,TueR_01,"Tue, 06 May",IVCA,DMS,,"Dunsany/Green Sheds",19:00,21:03
14,TT_03,"Sat, 10 May",Tom Dempsey,TT,10,Moyvalley,,
15,SR_07,"Sun, 11 May",IVCA,DMS,,Curragh,09:00,
16,LL_05,"Sun, 11 May",Mind the Gaps,Tour,100km,"Cycle Superstore, Tallaght",,
17,TueR_02,"Tue, 13 May",IVCA,DMS,,"Kiltale/Culmullin",19:00,21:15
18,TT_04,"Sat, 17 May",IVCA,TT,10,Dunshaughlin,,
19,AR_01,"Sun, 18 May",40/50/60/70 Champs,Age DMS,,Kilcullen,09:00,
20,TueR_03,"Tue, 20 May",IVCA,DMS,,"S.Hill/Dorey's Forge",19:00,21:26
21,SR_08,"Sun, 25 May",Gerry Brannigan [BLUE],DMS,,"Dunsany/Green Sheds",09:00,
22,TueR_04,"Tue, 27 May",IVCA,DMS,,"Dunsany/Kilmessan",19:00,21:36
23,TT_05,"Tue, 27 May",Kelly Cup,TT,25,Batterstown,,21:36
24,Non League,"Sat, 31 May",Gerry Kinsella 2-Day,DMS,,TBC,,
25,TT_06,"Sun, 01 Jun",Championship,TT,10,Moyvalley,,
26,Non League,"Mon, 02 Jun",Gerry Kinsella 2-Day,DMS,,TBC,,
27,TueR_05,"Tue, 03 Jun",IVCA,DMS,,"Summerhill (Short)",19:00,21:45
28,LL_06 / Tour,"Sun, 08 Jun",Wicklow 200,Tour,,Russborough House,07:00,
29,TueR_06,"Tue, 10 Jun",IVCA,DMS,,"Kiltale/Dorey's Forge",19:00,21:51
30,TRK_1,"Fri, 13 Jun",Omnium,Track,,Sundrive,,
31,TT_07,"Sat, 14 Jun",Joe Sherwin,TT,25,Moyvalley,,
32,SR_09,"Sun, 15 Jun",Dermot McGrath [GREEN],DMS,,Kilcullen,09:00,
33,TueR_07,"Tue, 17 Jun",IVCA,DMS,,"Dunsany/Kilmessan",19:00,21:55
34,AR_02,"Sun, 22 Jun",Founders 50,Age CP,,"Summerhill (Long)",09:00,
35,TueR_08,"Tue, 24 Jun",IVCA,DMS,,"Summerhill (Short)",19:00,21:57
36,SR_10,"Sun, 29 Jun",IVCA,DMS,,Curragh,09:00,
37,TT_08,"Sun, 29 Jun",Championship,TT,25,Moyvalley,,
38,TueR_09,"Tue, 01 Jul",IVCA,DMS,,"Dunsany/Green Sheds",19:00,21:55
39,TRK_2,"Fri, 04 Jul",Omnium,Track,,Sundrive,,
40,SR_11,"Sun, 06 Jul",Millenium Cup [ORANGE],DMS,,"Jack White's",09:00,
41,TueR_10,"Tue, 08 Jul",IVCA,DMS,,"Kiltale/Culmullin",19:00,21:51
42,TT_09,"Sat, 12 Jul",IVCA,TT,10,"Jack White's",,
43,SR_12,"Sun, 13 Jul",Sonny Cullen [RED/WHITE],DMS,100km,Kilcullen,09:00,
44,LL_07,"Sun, 13 Jul","We'll Meath Again",Tour,70km,"Grasshopper, Clonee",,
45,TueR_11,"Tue, 15 Jul",IVCA,DMS,,"Dunsany/Kilmessan",19:00,21:45
46,TRK_3,"Sat, 19 Jul",Championship,Track,,Sundrive,,
47,TRK_4,"Sun, 20 Jul",Championship,Track,,Sundrive,,
48,SR_13,"Sun, 20 Jul",IVCA,DMS,,Clonard,09:00,
49,TueR_12,"Tue, 22 Jul",IVCA,DMS,,"Summerhill (Short)",19:00,21:36
50,TT_10,"Sat, 26 Jul",Championship,TT,50,Moyvalley,,
51,SR_14,"Sun, 27 Jul",Phoenix Cup [RED/WHITE],DMS,,Tullamore,09:00,
52,TueR_13,"Tue, 29 Jul",IVCA,DMS,,"Dunsany/Green Sheds",19:00,21:25
53,TT_11,"Sat, 02 Aug",Sanyo Cup,TT,,"Hattons - Summerhill",,
54,SR_15,"Sun, 03 Aug",IVCA,DMS,100km,"Hatchet/Green Sheds",09:00,
55,TueR_14,"Tue, 05 Aug",IVCA,DMS,,"S.Hill/Dorey's Forge",19:00,21:12
56,TT_12,"Sat, 09 Aug",IVCA,TT,10,Dunshaughlin,,
57,AR_03,"Sun, 10 Aug",IVCA Age Champs,Age CP,,"Summerhill (Long)",09:00,
58,LL_08,"Sun, 10 Aug",100 in 8,Tour,160km,"Grasshopper, Clonee",,
59,TT_13,"Tue, 12 Aug",IVCA,TT,10,Batterstown,,20:58
60,SR_16,"Sun, 17 Aug",Memorial Cups,DMS,,Carlow,09:00,
61,SR_17,"Sun, 24 Aug",IVCA,DMS,,Curragh,09:00,
62,TT_14,"Sun, 24 Aug",Alfresco Shield,TT,25,Moyvalley,,
63,SR_18,"Sun, 31 Aug",IVCA,DMS,,"Dunsany/Green Sheds",09:00,
64,TT_15,"Sat, 06 Sep",Options,TT,25/50,Moyvalley,,
65,AR_04,"Sun, 07 Sep","Kevin Simms (40, 50, 60, 70)",Age DMS,,"Summerhill (Long)",09:00,
66,Non League,"Sun, 14 Sep",IVCA,DMS,,Kilcullen,09:00,
67,LL_09,"Sun, 14 Sep",Joe Hoare Reliability Trial,Tour,65km,"Grasshopper, Clonee",,
68,SR_19,"Sun, 21 Sep",IVCA,DMS,,"Dunsany/Green Sheds",09:00,
69,TueR_15,"Tue, 23 Sep",AGM,DMS,,"Summerhill (Short)",19:00,19:30
70,SR_20,"Sun, 28 Sep",IVCA,DMS,,"Hatchet/Dorey's Forge",09:00,
71,TT_16,"Sun, 05 Oct",Hill Climb,TT,,Rathcoole,,
72,LL_10,"Sun, 12 Oct",Gay Farran Memorial Tour,Tour,40km/70km,"Grasshopper, Clonee",,"""
# 0 - Event #,1 - Code, 2- Date,3 - Details,4- Type,5-Distance,6-Sign-On/Location,7 - Time,Sunset


def parse_csv_string_to_list(csv_string):
    # Create a file-like object from the string
    csv_file = StringIO(csv_string)

    # Use csv reader to parse the string
    csv_reader = csv.reader(csv_file)

    # Convert to list of lists
    data = [row for row in csv_reader]

    return data


def text_to_events(data_to_csv: list):
    """
    Convert the text to a list of events
    :param text:
    :return:
    """

    events = []
    for m in data_to_csv:
        _event = Event()
        if m[7] == "":
            _time = "09:00"
        else:
            _time = m[7]

        _event.add("summary", f"[IVCA] #{m[0]} {m[1]} {m[3]} {m[4]} in {m[6]} at {_time}")
        st = datetime.strptime(f"{_time} {m[2]} 2025", "%H:%M %a, %d %b %Y").replace(tzinfo=ZoneInfo("Europe/Dublin"))
        et = st + timedelta(hours=3)
        _event.add("dtstart", st)
        _event.add("dtend", et)
        # _event.add('dtend', datetime.strptime("21:00 {} 2022 +0100".format(m.group(1)), "%H:%M %d %b %Y %z"))
        _event["organizer"] = organizer
        _event["location"] = vText("{}, Ireland".format(m[6]))
        events.append(_event)

    return events


data_to_csv = parse_csv_string_to_list(txt)

organizer = vCalAddress("MAILTO:racecom@theivca.com")
organizer.params["cn"] = vText("IVCA")
organizer.params["role"] = vText("Race Comms")
for event in text_to_events(data_to_csv):
    cal.add_component(event)

# Adding events to calendar

f = open("ivca_2025.ics", "wb")
f.write(cal.to_ical())
f.close()
