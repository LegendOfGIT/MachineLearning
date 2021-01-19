import gzip
import neat
import pickle

def load_net():
    with gzip.open('contest-winning.net') as f:
        obj = pickle.load(f)
        return obj

def run_model(time_passed_in_percent, prices_left_in_percent, prices_give_out_tendency_in_percent):
    net = load_net()

    output = net.activate((
        time_passed_in_percent / 100,
        prices_left_in_percent / 100,
        prices_give_out_tendency_in_percent / 100
    ))

    return output[0] > 0.5
