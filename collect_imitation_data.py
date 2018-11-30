import cPickle as pickle
import bz2
import os
import yaml
import datetime

from imitation_data_collector import ImitationDataCollector


# read the config
config_path = os.path.join(os.getcwd(), 'config/config.yml')
with open(config_path, 'r') as yml_file:
    config = yaml.load(yml_file)
    print('------------ Config ------------')
    print(yaml.dump(config))

config['openrave_rl']['challenging_trajectories_only'] = True
# params_file = None
# params_file = 'params_simple.pkl'
params_file = 'params_hard.pkl'

# number_of_trajectories = 8
# trajectories_per_file = 4
# threads = 2

number_of_trajectories = 100000
trajectories_per_file = 1000
threads = 100

data_collector = ImitationDataCollector(config, threads, params_file)
results_dir = 'imitation_data'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)
collected = 0
while collected < number_of_trajectories:
    a = datetime.datetime.now()
    current_buffer = data_collector.generate_samples(trajectories_per_file)
    b = datetime.datetime.now()
    print 'data collection took: {}'.format(b - a)
    dump_path = os.path.join(results_dir, 'temp_data_{}.path_pkl'.format(collected))
    compressed_file = bz2.BZ2File(dump_path, 'w')
    pickle.dump(current_buffer, compressed_file)
    compressed_file.close()
    collected += len(current_buffer)
data_collector.end()



