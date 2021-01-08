import neat

def eval_genome(genome, config):
    return 1000

def run_model(time_passed_in_percent, prices_left_in_percent, prices_give_out_tendency_in_percent):
    # Load configuration.
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        'neat-model.config'
    )

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Checkpointer.restore_checkpoint('neat-contest-winning-model.chk')
    pe = neat.ParallelEvaluator(6, eval_genome)
    winner = p.run(pe.evaluate, 1)
    net = neat.nn.FeedForwardNetwork.create(winner, config)

    output = net.activate((
        time_passed_in_percent / 100,
        prices_left_in_percent / 100,
        prices_give_out_tendency_in_percent / 100
    ))

    return output[0] > 0.5
