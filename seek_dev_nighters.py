from collections import defaultdict
from datetime import datetime, timedelta

import pytz
import requests


def main():
    attempts = load_attempts()
    all_midnighters = defaultdict(list)
    for users_data in attempts:
        midnighters = get_midnighters(users_data)
        for midnighter in midnighters:
            all_midnighters[midnighter['username']].append(midnighter)

    print_users_information(all_midnighters)


def load_attempts():
    page = 1
    attempt = True
    while attempt:
        attempt = get_attempt(page=page)
        if attempt:
            page += 1
            yield from attempt


def get_attempt(page: int = 1):
    url = 'http://devman.org/api/challenges/solution_attempts/'
    params = {'page': page}
    response = requests.get(url=url,
                            params=params)

    if not response.ok:
        return None
    users_information = [response.json()['records']]

    return users_information


def get_midnighters(users_information: list):
    hour_from = timedelta(hours=0, minutes=00)
    hour_to = timedelta(hours=5, minutes=59)
    midnighters = []
    for user_information in users_information:
        timezone = pytz.timezone(user_information['timezone'])
        check_time = datetime.fromtimestamp(
            user_information['timestamp'],
            tz=timezone)

        pushing_time = timedelta(
            hours=check_time.hour,
            minutes=check_time.minute)

        if is_time_in_delta(
                time_to_check=pushing_time,
                time_from=hour_from,
                time_to=hour_to):
            user_information.update({'date_time': check_time})
            midnighters.append(user_information)

    return midnighters


def is_time_in_delta(time_to_check: timedelta,
                     time_from: timedelta,
                     time_to: timedelta):
    return time_from < time_to_check < time_to
    ''' Знаю, что тут легче сравнить простые числа, 
    но я здесь следую принципу 'работать со временем как со временем', 
    ибо если граничные параметры изменятся, проще поменять 
    или добавить дни(часы, минуты, секунды) во входных параметрах, 
    чем дописывать дополнительные проверки с простыми числами. 
    Если моя идея не верна или не находит отклика, 
    на повторной доработке поправлю.'''


def print_users_information(users_information: dict):
    for user_name, user_information in users_information.items():
        row = 'User with name {} ' \
              'sent task to check at:'.format(user_name)
        print(row)
        for check_setting_attempt in user_information:
            check_setting_time = str(normalize_date_time_to_print(
                check_setting_attempt['date_time']))
            print('\t' + check_setting_time)
        print('------------------------------')


def normalize_date_time_to_print(date_time: datetime):
    date_time_to_print = date_time.replace(tzinfo=None).replace(microsecond=0)

    return date_time_to_print


if __name__ == '__main__':
    main()
