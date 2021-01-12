import requests
import math

def get_int_array_from_file(file_name):
    response = []
    with open(file_name) as file:
        #Content_list is the list that contains the read lines.
        for line in file:
            response.append(int(line))

    return response

def get_participants_per_minute(participants_per_hour):
    response = []

    participants = participants_per_hour
    participants_per_minute = math.floor(participants_per_hour / 60)

    for minute in range(60):
        if minute == 59:
            response.append(participants)
        else:
            response.append(participants_per_minute if participants >= participants_per_minute else 0)

        participants -= participants_per_minute

    return response

participants_per_hours = get_int_array_from_file('/app/participants_per_hour.csv')
participants_per_minute = []
for participants_per_hour in participants_per_hours:
    participants_per_minute = participants_per_minute + get_participants_per_minute(participants_per_hour)


TOTAL_MINUTES = 17460
minutes_left = TOTAL_MINUTES

TOTAL_PRICES = 1400
prices_left = TOTAL_PRICES

while minutes_left > 0:
    minutes_left -= 1

    participants = participants_per_minute[minutes_left]
    for participant in range(participants):
        prices_left_in_percent = ((prices_left * 100) / TOTAL_PRICES)
        time_left_in_percent = ((minutes_left * 100) / TOTAL_MINUTES)

        if requests.get('http://10.11.12.110:5000?pricesLeftInPercent=' + str(prices_left_in_percent) + '&timePassedInPercent=' + str(100 - time_left_in_percent) + ' &pricesGiveOutTendencyInPercent=20').json()['give_out_price']:
            prices_left -= 1

    if minutes_left % 100 == 0:
        print('prices_left_in_percent:')
        print(prices_left_in_percent)

        print('time_left_in_percent:')
        print(time_left_in_percent)
