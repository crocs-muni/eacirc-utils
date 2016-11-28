# eacirc-utils
Utils for experiment creation and result postprocessing

Running your jobs on metacentrum step-by-step:

1. Clone this repository to your home
2. Update accordingly to your experiment `./processors/preprocessor_big.py` (fork it for your experiment)
3. Run preprocessor in python in directory, where you want to do your computations
4. Optionals:
   * Update time and count of jobs in `./metacentrum/run_experiment.sh`
   * For very important experiments, that needs to be 100% valid: uncomment qrng settings in `./metacentrum/single_experiment.sh` -- you need to have folder `~/qrng` with random data for this.
5. Run `./metacentrum/run_experiment.sh` with paths for config files (usually: `./metacentrum/run_experiment.sh ~/path/to/experiment/rnd-rnd.json & ./metacentrum/run_experiment.sh ~/path/to/experiment/*/*.json`)
6. After computations are done, run `./processors/postprocessor.py` (usually: `python ./processors/postprocessor.py -s ~/path/with/results/*.d`)
7. Get the results on stdout or in log :)
