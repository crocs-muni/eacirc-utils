#!/usr/bin/python

# version 1.1
# constants fixed for EACirc 4


import os, sys # traveling trough files tree
import glob # glob for faster directory traversal
from time import gmtime, strftime # for logging
import argparse
from math import sqrt # in KS test

# Constants (change them properly for current EACirc):
eacirc_log_name = "01_eacirc.log"
rej_acc_keywords = "% interval"
uniformity_keyword = "uniformity hypothesis accepted"
nonuniformity_keyword = "uniformity hypothesis rejected"

statistics_keywords = "last p-value is:"


# Log both to file postprocessor.log and stdout
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("postprocessor.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()


# Kolmogorov-Smirnov test - one sample compared to uniform dist
# Are samples uniformly distributed?
# returns KS-statistics, critical val and if uniformity hypothesis should be rejected
def ks_uniform_test(samples):
    samples.sort()
    N = len(samples)

    max_dist = 0
    for i in range(N):
        temp = max(samples[i] - float(i)/float(N), float(i+1)/float(N) - samples[i])
        max_dist = max(temp, max_dist)

    critical_val = 1.628/sqrt(float(N))
    return (max_dist, critical_val, max_dist > critical_val)


# Statistics over final p-vals
# for rnd-rnd, p-vals should be uniform for whole experiment
def run_p_val_stat(p_vals):
    p_val, critical_val, rej = ks_uniform_test(p_vals)
    print("KS critical val = " + str(critical_val))
    if rej:
        print("KS of experiment p-vals is in 1% interval -> uniformity hypothesis rejected, ks-val = " + str(p_val))
    else:
        print("KS of experiment p-vals is not in 1% interval -> is uniform, KS-val = " + str(p_val))


#
def process_experiment(experiment_path):
    print("Processing experiment with path: " + str(experiment_path))

    # EACirc 2.0+ statistics
    accepted_count = 0
    rejected_count = 0
    others = 0

    # EACirc 4.0+ statistics
    p_vals = []

    for run, _, _ in os.walk(experiment_path):
        if run is experiment_path:
            continue
        log_path = run + "/" + eacirc_log_name
        try:
            log = open(log_path)
        except IOError:
            print("    Error: file " + log_path + " missing.")
            continue

        for line in log:
            if rej_acc_keywords in line:
                if nonuniformity_keyword in line:
                    rejected_count += 1
                elif uniformity_keyword in line:
                    accepted_count += 1
                else:
                    others += 1

            if statistics_keywords in line:
                # get p-val from end of the string (separated by ' ')
                # and convert it to float, inserting to p_vals
                p_vals.append(float(line.split()[-1]))

    if accepted_count + rejected_count > 0:
        print("    Results: rejected: " + str(rejected_count) + " of: " + str(accepted_count + rejected_count + others) + " ratio: " + str(rejected_count / float(accepted_count + rejected_count)))
    else:
        print("    Results: rejected: " + str(rejected_count) + " of: " + str(accepted_count + rejected_count + others))

    if len(p_vals) > 35: # we need more than 35 p-vals to run KS-test (but much more is recommended)
        run_p_val_stat(p_vals)
    print("") # newline


# 
def process_experiment_stdout(experiment_path):
    print("Processing experiment with path: " + str(experiment_path))

    # EACirc 2.0+ statistics
    accepted_count = 0
    rejected_count = 0
    others = 0

    # EACirc 4.0+ statistics
    p_vals = []

    for f in glob.glob(experiment_path + "/*.o*"):
        try:
            log = open(f)
        except IOError:
            print("    Error: file " + f + " missing.")
            continue

        for line in log:
            if rej_acc_keywords in line:
                if nonuniformity_keyword in line:
                    rejected_count += 1
                elif uniformity_keyword in line:
                    accepted_count += 1
                else:
                    others += 1

            if statistics_keywords in line:
                # get p-val from end of the string (separated by ' ')
                # and convert it to float, inserting to p_vals
                p_vals.append(float(line.split()[-1]))

    if accepted_count + rejected_count > 0:
        print("    Results: rejected: " + str(rejected_count) + " of: " + str(accepted_count + rejected_count + others) + " ratio: " + str(rejected_count / float(accepted_count + rejected_count)))
    else:
        print("    Results: rejected: " + str(rejected_count) + " of: " + str(accepted_count + rejected_count + others))

    if len(p_vals) > 35: # we need more than 35 p-vals to run KS-test (but much more is recommended)
        run_p_val_stat(p_vals)
    print("") # newline


# Traverse given subtree for experiments and analyse them
def process_all_exp_in_dir(root):
    for d, _, _ in os.walk(root):
        if d.endswith(".d"): # experiments ends with ".d"
            process_experiment(d)


if __name__ == "__main__":
    # arg parser
    parser = argparse.ArgumentParser(description='Process EACirc results (from e.g. metacentrum).',
        epilog='Prints and log (to ./postprocessor.log) ratio of experiments with rejected null hypothesis (~alpha (0.01) for rnd-rnd) and in case of experiments with last fitness also average of these fitnesses (~0.5 for rnd-rnd)')
    parser.add_argument('paths', metavar='PATH', type=str, nargs='+', help='path(s) for analysis')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--paths', dest='scan_paths', action='store_true', default=False, help='paths for analysis')
    group.add_argument('-s', '--stdout', dest='scan_stdout', action='store_true', default=False, help='paths with stdout *.o* files')
    group.add_argument('-r', '--root', dest='scan_root', action='store_true', default=False, help='root path where this start searching for experiments')

    if len(sys.argv) < 2:
        sys.argv.append("-h")
    args = parser.parse_args()

    # correct input
    if args.scan_paths:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": analyzing paths: " + str(args.paths))
        for p in args.paths:
            process_experiment(p)
    if args.scan_stdout:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": analyzing stdout in paths: " + str(args.paths))
        # os.chdir(experiment_path) # todo: analyze, if this is needed
        for p in args.paths:
            process_experiment_stdout(p)
    elif args.scan_root:
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": analyzing path: " + str(args.paths[0]))
        process_all_exp_in_dir(args.paths[0])
    exit(1)
