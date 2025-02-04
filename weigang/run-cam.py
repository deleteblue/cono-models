#!/usr/bin/env python
# Simulate coevolutionary automata model
# John Miller, Ex Machina
# Appendix F. Testing

import sys
import cam # assume in the same directory
import argparse
import numpy as np

# Setup: arguments, parameters, and logging
parser = argparse.ArgumentParser(
    description="Simulate coevolutionary automata model (CAM) of John Miller")

parser.add_argument('-t', '--tag', default='test',
                    help='Prefix for output files. Default: "test"')

parser.add_argument('-s', '--rng_seed', type=int, default=None,
                    help='RNG seed to generate reproducible rng results. Default = None (i.e., unpredictable rng.')

parser.add_argument('-pop', '--pop_size', type=int, default=40,
                    help='Number of individuals in the population. Default = 40.')

parser.add_argument('-gen', '--generation', type=int, default=100,
                    help='Number of generations to evolve. Default = 100.')

parser.add_argument('-mut', '--mutation_rate', type=float, default=0.33,
                    help='Number of mutations per generation per haplotype, randomly selected by poisson distribution. '
                         'Default = 1/3')

parser.add_argument('-alg', '--algorithm', choices=['1', '2', '3'], default='1',
                    help='Evolutionary search algorithms. 1. Elite: select top 10 in each generation '
                         '2. Tournament: select best of two'
                         '3. Combo search: Combines fitness and novelty.')

parser.add_argument('-n', '--nearest_neighbors', type=int, default=10,
                    help='Number of nearest neighbors to use in novelty search. Default = 10.')
                    
parser.add_argument('-tsize', '--target_size', type=int, default=10,
                    help='Length of the target string. Default = 10.')

parser.add_argument('-asize', '--automata_size', type=int, default=2,
                    help='Number of states in a automata. Default = 2.')
                    
parser.add_argument('-arch', '--archive_method', choices=['1', '2'], default='1',
                    help='Method to use for selecting what to add to the archive. '
                         '1. Fixed size, random archive. 2. Adaptive threshold. Default = 1.')

parser.add_argument('-prob', '--prob_arch', type=float, default=0.1,
                    help='Probability for an individual to get randomly added to the archive during novelty '
                         'search method 1. Default = 0.1.')

parser.add_argument('-w', '--weight', type=float, default=0.5,
                    help='Weight for the combo search algorithm. Weight value is between 0 and 1. '
                         'Closer to 1 means more bias towards novelty. Default = 0.5.')

args = parser.parse_args()

rng = np.random.default_rng()

# problem target to match
target_str = ''.join([ rng.choice(['0', '1']) for i in range(args.target_size) ])
# start with a random input stream of n-1 length
input_str = ''.join([ rng.choice(['0', '1']) for i in range(args.target_size-1) ])

# Print simulation parameters
# print(f"Simulation parameters:\n\tTarget string: {target_str}\n\tInput stream: {input_str}\n\tPopulation size: {args.pop_size}\n\tSearch algorithm: {args.algorithm}")


# Initialize a population
p = cam.Population(pop_size = args.pop_size,
               machine_size = args.automata_size,
               target = target_str,
               in_stream = input_str,
               rng_seed=args.rng_seed
               )

#print(p.population)
#print(f"Starting machine: {p.population[0]}\n")

# Search by evolution
# print(f"Tag\tGen\ttop_elite\ttsize\tasize\n")

for n in range(args.generation):
#    print(f"{args.tag}\t{p.generation}\t{p.elite1[2]}\t{p.elite1[1]['output']}\t{p.avg_fit}\t{args.algorithm}")
    p.mutate(mut_rate=args.mutation_rate)
    if args.algorithm == '1':
        p.elite_selection()
    if args.algorithm == '2':
        p.tour_selection()

print(f"{args.tag}\t{args.target_size}\t{round(p.elite1[2],4)}\t{p.elite1[1]['output']}\t{p.avg_fit}\t{args.automata_size}\t{args.algorithm}")

