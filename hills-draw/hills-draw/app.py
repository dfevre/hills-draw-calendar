from time import sleep
import requests
from icalendar import Calendar, Event, vDatetime
from datetime import datetime, timezone
import pytz
import boto3
import urllib.parse
import json

calendars = {}


def lambda_handler(event, context):
    seasons_data = call_api(
        'https://hillshornets.com.au/members/api/draw/seasons')
    upload_to_s3('data/seasons', json.dumps(seasons_data), 'application/json')
    for season in seasons_data["data"]:
        divisions_data = call_api(
            f"https://hillshornets.com.au/members/api/draw/seasons/{season['season_id']}/divisions")
        upload_to_s3(f"data/season/{season['season_id']}/divisions", json.dumps(divisions_data), 'application/json')
        # Each season + division + team will become a calendar
        for division in divisions_data['data']:
            teams_data = call_api(
                f"https://hillshornets.com.au/members/api/draw/seasons/divisions/{division['division_id']}/teams"
            )
            upload_to_s3(f"data/season/{season['season_id']}/division/{division['division_id']}/teams", json.dumps(teams_data), 'application/json')
            sleep(1)  # go easy on the API
            draw_data = call_api(
                f"https://hillshornets.com.au/members/api/draw/seasons/divisions/{division['division_id']}/draw")
            sleep(1)  # go easy on the API
            games = get_games_from_draw(draw_data['data']['divisionDraw'])
            if 'Semi_Final' in draw_data['data']['finalSeries']:
                games += get_games_from_draw(draw_data['data']
                                             ['finalSeries']['Semi_Final'])
            if 'Grand_Final' in draw_data['data']['finalSeries']:
                games += get_games_from_draw(draw_data['data']
                                             ['finalSeries']['Grand_Final'])
            for game in games:
                if game['match'] != "No Match" and game['team_a_id'] is not None and game['team_a_id'] is not None:
                    # Each game will be an entry in 2 calendars since each team gets its own calendar
                    for team_id in [game['team_a_id'], game['team_b_id']]:
                        cal_event = None
                        cal_event = draw_entry_to_event(
                            game, season, division, team_id)
                        calendar = get_calendar(
                            f"{season['season_id']}-{division['division_id']}-{team_id}")
                        calendar.add_component(cal_event)
    # Print all calendars
    calendar_count = 0
    for calendar_key in calendars.keys():
        upload_to_s3(f'cals/{urllib.parse.quote_plus(calendar_key)}.ics', 
                     calendars[calendar_key].to_ical(), 
                     'text/calendar; charset=utf-8')
        calendar_count += 1
    print(f'Done. Uploaded {calendar_count} calendars')

def upload_to_s3(file_name, file_content, content_type):
    s3 = boto3.resource(
        's3',
        region_name='ap-southeast-2'
    )
    print(f'Uploading file {file_name} to S3')
    s3.Object('fevre.io', file_name).put(
        Body=file_content, ContentType=content_type)

def draw_entry_to_event(draw_entry, season, division, team_id):
    us = team_id
    them = draw_entry['team_a_id'] if draw_entry['team_a_id'] != us else draw_entry['team_b_id']
    event = Event()
    summary = '🏀 '  # Always start with a 🏀
    summary += f'{us} vs {them}'
    event.add('summary', summary)
    description = f"{draw_entry['court']}\n{division['division_name']}"
    if draw_entry['double_points'] == 'Yes':
        description += '\nDouble points round!'
    event.add('description', description)
    start_time = datetime.strptime(
        f"{draw_entry['date_time_from']}", '%Y%m%dT%H%M%S')
    end_time = datetime.strptime(
        f"{draw_entry['date_time_to']}", '%Y%m%dT%H%M%S')
    mytz = pytz.timezone('Australia/Sydney')
    event.add('dtstart', vDatetime(
        mytz.localize(start_time).astimezone(pytz.UTC)))
    event.add('dtend', vDatetime(mytz.localize(end_time).astimezone(pytz.UTC)))
    event.add('dtstamp', datetime.now(timezone.utc))
    event.add('location', draw_entry['venueLabel'])
    event['uid'] = f"{season['season_id']}-{division['division_id']}-{team_id}-{draw_entry['game']}@hills.fevre.io"
    return event


def get_calendar(calendar_name):
    if not calendar_name in calendars:
        calendars[calendar_name] = Calendar()
        # calendars[calendar_name].name = calendar_name
        calendars[calendar_name].add(
            'prodid', '-//Hills Basketball Draw Calendar//fevre.io//')
        calendars[calendar_name].add('version', '2.0')
        calendars[calendar_name].add('description', calendar_name)
    return calendars[calendar_name]


def get_games_from_draw(draw_data):
    # The draw data from the Hills API is in an inconsistent format.
    # The first set of games is in a list but each following game is in a schedule object
    # Convert it all to a simple list of games.

    # The first item in 'divisionDraw' is a 'schedule' as a list of games.
    # Start with that list
    games = []

    # Each other 'schedule' in 'divisionDraw' is an object with the game number
    # as a key (string) rather than an index (int)
    for i in range(0, len(draw_data)):
        if i == 0:
            for game in draw_data[i]['schedule']:
                games.append(game)
        else:
            for schedule_key in draw_data[i]['schedule'].keys():
                games.append(draw_data[i]['schedule'][schedule_key])
    return games


def call_api(url: str):
    while True:
        print(f"Calling {url}")
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_secs = int(response.headers['retry-after'])
            print(f"Got rate limited by API. Retrying in {retry_secs} seconds")
            sleep(retry_secs + 1)
        else:
            raise Exception(
                f"Got response {response.status_code} from {url}\n Headers {response.headers}")

if __name__ == "__main__":
    # Example of a test event that simulates an AWS Lambda event
    sample_event = {
        # Add any event data your function expects (can leave as empty dict if not used)
    }
    # Simulate the AWS Lambda context (can leave as None if not needed)
    sample_context = None

    # Call the lambda_handler function
    lambda_handler(sample_event, sample_context)
