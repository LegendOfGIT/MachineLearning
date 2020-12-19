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

import neat

import visualize

# 2-input XOR inputs and expected outputs.
xor_inputs = [
              (0.98, 0.60),
              (0.30, 0.70),
              (0.79, 0.40),
              (0.30, 0.90),
              (0.90, 0.90)
              ]
xor_outputs = [
               (0.0,),
               (1.0,),
               (1.0,),
               (0.0,)
               ]


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

    total_time = 5000.0
    time_left = 5000.0
    total_prices = 2000.0
    prices_left = 2000.0

    fitness = 0.0
    while time_left > 0 and prices_left > 0:
      time_left -= 1
      prices_left_in_percent = (prices_left * 100) / total_prices
      time_left_in_percent = (time_left * 100) / total_time
      time_passed_in_percent = 100 - time_left_in_percent

      output = net.activate((time_passed_in_percent / 100, prices_left_in_percent / 100))

      give_out_price = output[0] > 0.8
      prices_left -= (1 if give_out_price else 0)
      prices_left_in_percent = (prices_left * 100) / total_prices

      multiplier = 1.0

      if time_passed_in_percent <= 2.0 and not give_out_price:
        multiplier += 1.0

      if time_passed_in_percent >= 50.0 and time_left_in_percent > 15.0 and prices_left_in_percent >= 20.0:
        multiplier += 1.0

      if time_left_in_percent <= 5.0 and prices_left_in_percent <= 5.0:
        multiplier += 1.0

      fitness += 1.0 * multiplier

    return fitness


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(4, eval_genome)
    winner = p.run(pe.evaluate, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi in xor_inputs:
        output = winner_net.activate(xi)
        print("input {!r}, got {!r}".format(xi, output))

    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True, node_names = node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(os.path.abspath("__file__"))
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
