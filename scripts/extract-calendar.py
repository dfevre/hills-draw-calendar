from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz

# init the calendar
cal = Calendar()

# Some properties are required to be compliant
cal.add('prodid', '-//Hills Basketball Draw Calendar//fevre.io//')
cal.add('version', '2.0')

# Add subcomponents
event = Event()
event.add('summary', 'Awesome Meeting')
event.add('description', 'Define the roadmap of our awesome project')
event.add('dtstart', datetime(2022, 5, 25, 8, 0, 0,
          tzinfo=pytz.timezone('Australia/Sydney')))
event.add('dtend', datetime(2022, 5, 25, 10, 0, 0,
          tzinfo=pytz.timezone('Australia/Sydney')))
event.add('location', 'Hill Sports Stadium')
event['uid'] = '2022125T111010/272356262376@example.com'

# Add the event to the calendar
cal.add_component(event)

# Add 2nd subcomponents
event = Event()
event.add('summary', 'Another awesome Meeting')
event.add('description', '...and again')
event.add('dtstart', datetime(2022, 5, 25, 10, 0, 0,
          tzinfo=pytz.timezone('Australia/Sydney')))
event.add('dtend', datetime(2022, 5, 25, 11, 0, 0,
          tzinfo=pytz.timezone('Australia/Sydney')))
event.add('location', 'Hill Sports Stadium')
event['uid'] = '2022125T111010/2723562623762@example.com'

# Add the event to the calendar
cal.add_component(event)

# Write to disk
directory = Path.cwd() / 'MyCalendar'
try:
    directory.mkdir(parents=True, exist_ok=False)
except FileExistsError:
    print("Folder already exists")
else:
    print("Folder was created")

f = open(os.path.join(directory, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()
