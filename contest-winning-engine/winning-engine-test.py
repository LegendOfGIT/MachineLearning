import random
import requests
import math
import numpy as np
import csv

def get_int_array_from_file(file_name):
    response = []
    with open(file_name) as file:
        #Content_list is the list that contains the read lines.
        for line in file:
            response.append(int(line))

    return response

def get_participants_per_minute(participants_per_hour):
    response = [0] * 60

    for participant_per_hour in range(participants_per_hour):
        random_minute_index = random.randint(0, 59)

        response[random_minute_index] += 1

    return response

participants_per_hours = get_int_array_from_file('/app/participants_per_hour.csv')
participants_per_minute = []
for participants_per_hour in participants_per_hours:
    participants_per_minute = participants_per_minute + get_participants_per_minute(participants_per_hour)

TOTAL_MINUTES = 41760
minutes_left = TOTAL_MINUTES

TOTAL_PRICES = 1400
prices_left = TOTAL_PRICES

def get_percentage(current_amount, total_amount):
  if total_amount == 0:
    return 100

  return (current_amount * 100) / total_amount

print('Verbleibende Zeit;Verbleibende Preise;Gewinnanteil;Teilnehmer;Ausgespielte Preise;')

current_minute = 0
price_distribution = []
given_out_prices = 0
participants_for_statistics = 0
while minutes_left > 0:
    minutes_left -= 1

    prices_left_in_percent = ((prices_left * 100) / TOTAL_PRICES)
    time_left_in_percent = ((minutes_left * 100) / TOTAL_MINUTES)

    participants = participants_per_minute[current_minute]
    participants_for_statistics += participants
    price_distribution_in_percent = 0.0
    for participant in range(participants):
        prices_left_in_percent = ((prices_left * 100) / TOTAL_PRICES)
        time_left_in_percent = ((minutes_left * 100) / TOTAL_MINUTES)

        give_out_price = prices_left > 0

        if give_out_price:
            price_distribution_in_percent = get_percentage(np.count_nonzero(price_distribution), len(price_distribution))
            give_out_price = requests.get('http://10.11.12.110:5000?pricesLeftInPercent=' + str(prices_left_in_percent) + '&timePassedInPercent=' + str(100 - time_left_in_percent) + ' &pricesGiveOutTendencyInPercent=' + str(price_distribution_in_percent)).json()['give_out_price']

        if len(price_distribution) == 35:
            del price_distribution[0]

        price_distribution.append(1 if give_out_price else 0)

        if give_out_price:
            given_out_prices += 1
            prices_left -= 1

    if minutes_left % 50 == 0:
        print("{:.2f}".format(100 - time_left_in_percent) + '%;' + "{:.2f}".format(prices_left_in_percent) + '%;' + "{:.2f}".format(price_distribution_in_percent) + '%;' + str(participants_for_statistics) + ';' + str(given_out_prices) + ';')

        given_out_prices = 0
        participants_for_statistics = 0

    current_minute += 1
