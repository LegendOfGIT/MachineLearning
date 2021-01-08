"""
A parallel version of XOR using neat.parallel.

Since XOR is a simple experiment, a parallel version probably won't run any
faster than the single-process version, due to the overhead of
inter-process communication.

If your evaluation function is what's taking up most of your processing time
(and you should check by using a profiler while running single-process),
you should see a significant performance improvement by evaluating in parallel.

This example is only intended to show how to do a parallel experiment
in neat-python.  You can of course roll your own parallelism mechanism
or inherit from ParallelEvaluator if you need to do something more complicated.
"""

from __future__ import print_function

import math
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import regex as re
import random

import neat

import visualize

def get_percentage(current_amount, total_amount):
  if total_amount == 0:
    return 100

  return (current_amount * 100) / total_amount

def get_area_reward(time_left_in_percent, prices_left_in_percent):
    prices_won_in_percent = 100.0 - prices_left_in_percent

    no_multiplier = 0.2
    reward_multiplier = 1000

    if time_left_in_percent <= 98.0 and time_left_in_percent >= 92.2:
      if prices_left_in_percent >= 95.0:
        return no_multiplier

      if prices_left_in_percent <= 90.2:
        return no_multiplier

      return reward_multiplier

    if time_left_in_percent <= 92.0 and time_left_in_percent >= 88.2:
      if prices_left_in_percent >= 90.0:
        return no_multiplier

      if prices_left_in_percent <= 78.2:
        return no_multiplier

      return reward_multiplier

    if time_left_in_percent <= 56.0 and time_left_in_percent >= 49.5:
      if prices_left_in_percent >= 70.9:
        return no_multiplier

      if prices_left_in_percent <= 57.6:
        return no_multiplier

      return reward_multiplier

    if time_left_in_percent <= 39.5 and time_left_in_percent >= 42.0:
      if prices_left_in_percent >= 55.3:
        return no_multiplier

      if prices_left_in_percent <= 40.6:
        return no_multiplier

      return reward_multiplier * 8

    if time_left_in_percent <= 26.3 and time_left_in_percent >= 24.0:
      if prices_left_in_percent >= 43.3:
        return no_multiplier

      if prices_left_in_percent <= 31.2:
        return no_multiplier

      return reward_multiplier * 8

    if time_left_in_percent <= 10.5 and time_left_in_percent >= 8.0:
      if prices_left_in_percent >= 20.1:
        return no_multiplier

      if prices_left_in_percent <= 9.8:
        return no_multiplier

      return reward_multiplier * 25

    if time_left_in_percent <= 4.25 and time_left_in_percent >= 2.0:
      if prices_left_in_percent <= 8.1:
        return no_multiplier

      if prices_left_in_percent > 5.5:
        return no_multiplier

      return reward_multiplier * 100

    if time_left_in_percent <= 2.0 and time_left_in_percent >= 0.0:
      if prices_left_in_percent <= 3.2:
        return no_multiplier

      if prices_left_in_percent > 0.1:
        return no_multiplier

      return reward_multiplier * 200

    return no_multiplier

def get_price_distribution_reward(price_distribution):
    base_multiplier = 0.5

    if len(price_distribution) < 3:
      return 0

    prices_won_in_percent = get_percentage(np.count_nonzero(price_distribution), len(price_distribution))
    if prices_won_in_percent <= 15.0 or prices_won_in_percent >= 75.0:
      return 0

    return (75 - (prices_won_in_percent - 15.0)) * 25


def eval_genome(genome, config):
    """
    This function will be run in parallel by ParallelEvaluator.  It takes two
    arguments (a single genome and the genome class configuration data) and
    should return one float (that genome's fitness).

    Note that this function needs to be in module scope for multiprocessing.Pool
    (which is what ParallelEvaluator uses) to find it.  Because of this, make
    sure you check for __main__ before executing any code (as we do here in the
    last few lines in the file), otherwise you'll have made a fork bomb
    instead of a neuroevolution demo. :)
    """

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    time_left = TOTAL_TIME
    prices_left = TOTAL_PRICES
    price_distribution = []

    current_time_left_in_percent = 100
    fitness = 0.0
    while time_left > 0:
      time_left -= 1
      prices_left_in_percent = get_percentage(prices_left, TOTAL_PRICES)
      time_left_in_percent = get_percentage(time_left, TOTAL_TIME)
      next_time_left_in_percent = math.floor(time_left_in_percent)
      time_passed_in_percent = 100 - time_left_in_percent

      output = net.activate((
         time_passed_in_percent / 100,
         prices_left_in_percent / 100,
         get_percentage(np.count_nonzero(price_distribution), len(price_distribution)) / 100
      ))

      give_out_price = output[0] > 0.5

      if len(price_distribution) == 50:
        del price_distribution[0]

      price_distribution.append(1 if give_out_price else 0)

      prices_left -= (1 if give_out_price else 0)
      if prices_left < 0:
        prices_left = 0

      prices_left_in_percent = get_percentage(prices_left, TOTAL_PRICES)

      if not current_time_left_in_percent == next_time_left_in_percent:
        fitness += (
            get_area_reward(time_left_in_percent, prices_left_in_percent) +
            get_price_distribution_reward(price_distribution)
        ) * time_passed_in_percent

      current_time_left_in_percent = next_time_left_in_percent

    fitness += (100 - prices_left_in_percent) * 1200

    return fitness

def evolute_for_x_generations(
    config,
    population,
    parallel_evolutor,
    stats,
    number_of_generations,
    current_generation
):
    winner = population.run(parallel_evolutor.evaluate, number_of_generations)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    time_left = TOTAL_TIME
    prices_left = TOTAL_PRICES

    time_passed_history = []
    prices_left_history = []
    price_distribution = []

    while time_left >= 0:
      time_left -= 1
      prices_left_in_percent = get_percentage(prices_left, TOTAL_PRICES)
      time_left_in_percent = get_percentage(time_left, TOTAL_TIME)
      time_passed_in_percent = 100 - time_left_in_percent


      output = winner_net.activate((
         time_passed_in_percent / 100,
         prices_left_in_percent / 100,
         get_percentage(np.count_nonzero(price_distribution), len(price_distribution)) / 100
      ))

      give_out_price = output[0] > 0.5
      if len(price_distribution) == 30:
        del price_distribution[0]

      price_distribution.append(1 if give_out_price else 0)

      prices_left -= (1 if give_out_price else 0)
      if prices_left < 0:
        prices_left = 0

      prices_left_in_percent = get_percentage(prices_left, TOTAL_PRICES)

      time_passed_history.append(time_passed_in_percent)
      prices_left_history.append(prices_left)

    node_names = {-1:'time_passed', -2: 'prices_left', -3: 'price_distribution', 0:'give out price'}
    visualize.draw_net(config, winner, True, node_names = node_names)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)

    print('total prices:')
    print(TOTAL_PRICES)

    print('prices left:')
    print(prices_left)

    handle, = plt.plot(time_passed_history, prices_left_history, Label = current_generation + len(stats.most_fit_genomes) + 1)

    return handle

def run(config_file, checkpoint_generation):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    if not checkpoint_generation is None:
      p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-' + str(checkpoint_generation))

      for f in os.listdir('.'):
        if re.search('neat-checkpoint', f) and not re.search('-' + str(checkpoint_generation), f):
          os.remove(os.path.join('.', f))

    else:
      p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    plot_handles = []
    pe = neat.ParallelEvaluator(10, eval_genome)
    for x in range(8):
      plot_handles.append(evolute_for_x_generations(
          config,
          p,
          pe,
          stats,
          5,
          0 if not checkpoint_generation else checkpoint_generation
      ))

    plt.legend(handles=plot_handles)