from collections import defaultdict
from datetime import datetime, timedelta
import argparse
import pytz
import requests


def main():
    parameters = parse_parameters()
    hour_from = parameters.hour_from
    hour_to = parameters.hour_to

    for parameter in [hour_from, hour_to]:
        assert check_value_none_zero_or_positive_number(parameter), \
            'One ore more parameters are negative. ' \
            'Please restart script with positive numeric parameters.'

    attempts = load_attempts()
    midnighters = defaultdict(list)
    midnighte_attempts = get_midnight_attempts(attempts=attempts,
                                               hour_from=hour_from,
                                               hour_to=hour_to)
    for midnighte_attempt in midnighte_attempts:
        midnighters[midnighte_attempt['username']].append(midnighte_attempt)

    print_midnighters(midnighters)


def load_attempts():
    page = 1
    attempt = True
    while attempt:
        attempt = get_attempts(page=page)
        if attempt:
            page += 1
            yield from attempt


def get_attempts(page: int = 1):
    url = 'http://devman.org/api/challenges/solution_attempts/'
    params = {'page': page}
    response = requests.get(url=url,
                            params=params)

    if not response.ok:
        return None
    send_to_check_attempts = response.json()['records']

    return send_to_check_attempts


def get_midnight_attempts(attempts,
                          hour_from: int,
                          hour_to: int):
    hour_from = timedelta(hours=hour_from)
    hour_to = timedelta(hours=hour_to)
    midnight_attempts = []
    for attempt in attempts:
        timezone = pytz.timezone(attempt['timezone'])
        check_time = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=timezone)

        pushing_time = timedelta(
            hours=check_time.hour,
            minutes=check_time.minute)

        if is_time_in_delta(
                time_to_check=pushing_time,
                time_from=hour_from,
                time_to=hour_to):
            attempt.update({'date_time': check_time})
            midnight_attempts.append(attempt)

    return midnight_attempts


def is_time_in_delta(time_to_check: timedelta,
                     time_from: timedelta,
                     time_to: timedelta):
    return time_from < time_to_check < time_to


def print_midnighters(midnighters: dict):
    for user_name, attempts in midnighters.items():
        row = 'User with name {} ' \
              'sent task to check at:'.format(user_name)
        print(row)
        for attempt in attempts:
            attempt_time = attempt['date_time'].strftime("%m-%d-%Y %H:%M:%S")

            print('\t' + attempt_time)
        print('------------------------------')


def normalize_date_time_to_print(date_time: datetime):
    date_time_to_print = date_time.replace(tzinfo=None).replace(microsecond=0)

    return date_time_to_print


def parse_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ht', '--hour_to', type=int, default=6)
    parser.add_argument('-hf', '--hour_from', type=int, default=0)

    parameters = parser.parse_args()
    return parameters


def check_value_none_zero_or_positive_number(parameter_value):
    if parameter_value is None:
        return True

    return parameter_value >= 0

if __name__ == '__main__':
    main()
