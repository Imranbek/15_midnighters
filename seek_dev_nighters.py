import json
from datetime import datetime, timedelta

import pytz
import requests


def main():
    attempts = load_attempts()

    for users_data in attempts:
        midnighters = get_midnighters(users_data[0])
        print_users_information(midnighters)


def load_attempts():
    page = 1
    while get_attempt(page=page):
        attempt = get_attempt(page=page)
        page += 1
        yield attempt


def get_attempt(page: int = 1):
    url = 'http://devman.org/api/challenges/solution_attempts/'
    params = {'page': page}
    response = requests.get(url=url,
                            params=params)
    if (response.status_code != 200) or (not response.text):
        return None
    users_information = [json.loads(response.text)['records']]

    return users_information


def get_midnighters(users_information: list):
    hour_from = timedelta(hours=0, minutes=00)
    hour_to = timedelta(hours=5, minutes=59)
    midnighters = []
    for user_information in users_information:
        timestamp = pytz.utc.localize(
            datetime.utcfromtimestamp(user_information['timestamp'])
        )
        timezone = pytz.timezone(user_information['timezone'])
        check_time = timezone.normalize(timestamp)

        pushing_time = timedelta(hours=check_time.hour, minutes=check_time.minute)

        if time_in_delta(time_to_check=pushing_time,
                         time_from=hour_from,
                         time_to=hour_to):
            user_information.update({'date_time': check_time})
            midnighters.append(user_information)

    return midnighters


def time_in_delta(time_to_check: timedelta,
                  time_from: timedelta,
                  time_to: timedelta):
    return time_from < time_to_check < time_to


def print_users_information(users_information: list):
    for user_information in users_information:
        user_name = user_information['username']
        check_setting_time = str(normalize_date_time_to_print(user_information['date_time']))
        row = 'User with name {} ' \
              'sent task to check at {}'.format(user_name,
                                                check_setting_time)
        print(row)


def normalize_date_time_to_print(date_time: datetime):
    date_time_to_print = date_time.replace(tzinfo=None).replace(microsecond=0)

    return date_time_to_print


if __name__ == '__main__':
    main()
