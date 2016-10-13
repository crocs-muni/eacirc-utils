#!/usr/bin/python

# TODO: document here purpose of this experiment
# Tested functions: Big-testbed
# Settings: basic settings for CPU computations, used in many papers (as EACirc 2.0 paper)
# Purpose: baseline of EACirc 3, for future comparison with newer versions

# ReadMe:
# 1. fork this script and rewrite it for your purpose
# 2. document your purpose in the header, so others can easily get into your experiment
# Rewriting:
# a) choose functions and rounds in dictionaries estream and sha
# b) go trough text variables with actual configuration file
#   i) change constants in text, if your experiment doesn't need to variate them
#   ii) for variadic changes, create list/dict with your parameters and split surrrounding text parts; add for loop in main and print values, you are iterating trough; probably change directory tree generation


import os


estream_fun_names_id = {
    'ABC': 1,
    'Achterbahn': 2,
    'CryptMT': 3,
    'DECIM': 4,
    'DICING': 5,
    'Dragon': 6,
    'Edon80': 7,
    'F-FCSR': 8,
    'Fubuki': 9,
    'Grain': 10,
    'HC': 11,
    'Hermes': 12,
    'LEX': 13,
    'MAG': 14,
    'MICKEY': 15,
    'Mir-1': 16,
    'Pomaranch': 17,
    'Py': 18,
    'Rabbit': 19,
    'Salsa20': 20,
    'Sfinks': 21,
    'SOSEMANUK': 22,
    'TEA': 23,
    'Trivium': 24,
    'TSC-4': 25,
    'WG': 26,
    'Yamb': 27,
    'Zk-Crypt': 28
}

sha_fun_names_id = {
    'Abacus': 1,
    'ARIRANG': 2,
    'Aurora': 3,
    'Blake': 4,
    'Blender': 5,
    'Blue Midnight Wish': 6,
    'Boole': 7,
    'Cheetah': 8,
    'CHI': 9,
    'CRUNCH': 10,
    'CubeHash': 11,
    'DCH': 12,
    'Dynamic SHA': 13,
    'Dynamic SHA2': 14,
    'ECHO': 15,
    'ECOH': 16,
    'EDON': 17,
    'EnRUPT': 18,
    'ESSENCE': 19,
    'Fugue': 20,
    'Grostl': 21,
    'Hamsi': 22,
    'JH': 23,
    'Keccak': 24,
    'Khichidi': 25,
    'Lane': 26,
    'Lesamnta': 27,
    'Luffa': 28,
    'LUX': 29,
    'MCSSHA3': 30,
    'MD6': 31,
    'MeshHash': 32,
    'NaSHA': 33,
    'SANDstorm': 34,
    'Sarmal': 35,
    'Shabal': 36,
    'Shameta': 37,
    'SHAvite-3': 38,
    'SIMD': 39,
    'Skein': 40,
    'SpectralHash': 41,
    'StreamHash': 42,
    'SWIFFTX': 43,
    'Tangle': 44,
    'TIB3': 45,
    'Twister': 46,
    'Vortex': 47,
    'WaMM': 48,
    'Waterfall': 49
}

# used funs in batch
# USE exactly the string from estream_fun_names_id or worry about ID's of funs!
estream = {
    'DECIM': [5, 6, 7],
    'Fubuki': [1, 2, 3, 4],
    'Grain': [2, 3, 4],
    'Hermes': [0, 1, 2, 3],
    'LEX': [3, 4, 5],
    'Salsa20': [2, 3, 4],
    'TSC-4': [10, 11, 12, 13, 14]
}

sha = {
    'ARIRANG': [2, 3, 4],
    'Aurora': [2, 3, 4, 5],
    'Blake': [0, 1, 2, 3],
    'Cheetah': [4, 5, 6, 7],
    'CubeHash': [0, 1, 2, 3],
    'DCH': [1, 2, 3],
    'Dynamic SHA': [7, 8, 9, 10, 16],
    'Dynamic SHA2': [11, 12, 13, 14],
    'ECHO': [1, 2, 3, 4],
    'Grostl': [2, 3, 4, 5],
    'Hamsi': [0, 1, 2, 3],
    'JH': [6, 7, 8],
    'Lesamnta': [2, 3, 4, 5],
    'Luffa': [6, 7, 8],
    'MD6': [8, 9, 10, 11],
    'SIMD': [0, 1, 2, 3],
    'Tangle': [22, 23, 24, 25],
    'Twister': [6, 7, 8, 9]
}

header = """<?xml version="1.0" ?>
<EACIRC>
"""

# <NOTES>

main1 = """
    <MAIN>
        <CIRCUIT_REPRESENTATION>3</CIRCUIT_REPRESENTATION>
"""

# <PROJECT>

main2 = """
        <EVALUATOR>26</EVALUATOR>
        <EVALUATOR_PRECISION>8</EVALUATOR_PRECISION>
        <SIGNIFICANCE_LEVEL>5</SIGNIFICANCE_LEVEL>
        <RECOMMENCE_COMPUTATION>0</RECOMMENCE_COMPUTATION>
        <LOAD_INITIAL_POPULATION>0</LOAD_INITIAL_POPULATION>
        <NUM_GENERATIONS>30000</NUM_GENERATIONS>
        <SAVE_STATE_FREQ>100</SAVE_STATE_FREQ>
        <CIRCUIT_SIZE_INPUT>16</CIRCUIT_SIZE_INPUT>
        <CIRCUIT_SIZE_OUTPUT>1</CIRCUIT_SIZE_OUTPUT>
    </MAIN>
"""

outputs = """
    <OUTPUTS>
        <VERBOSITY>0</VERBOSITY>
        <INTERMEDIATE_CIRCUITS>0</INTERMEDIATE_CIRCUITS>
        <ALLOW_PRUNNING>0</ALLOW_PRUNNING>
        <SAVE_TEST_VECTORS>0</SAVE_TEST_VECTORS>
        <FRACTION_FILE>0</FRACTION_FILE>
    </OUTPUTS>
"""

random = """
    <RANDOM>
        <USE_FIXED_SEED>0</USE_FIXED_SEED>
        <SEED>145091104</SEED>
        <BIAS_RNDGEN_FACTOR>95</BIAS_RNDGEN_FACTOR>
        <LUT_HW>20000</LUT_HW>
        <USE_NET_SHARE>0</USE_NET_SHARE>
        <QRNG_PATH>../../../qrng/;../../../../qrng/;C:/qrng/;../qrng/</QRNG_PATH>
        <QRNG_MAX_INDEX>192</QRNG_MAX_INDEX>
    </RANDOM>
"""

cuda = """
    <CUDA>
        <ENABLED>0</ENABLED>
        <BLOCK_SIZE>512</BLOCK_SIZE>
    </CUDA>
"""

ga = """
    <GA>
        <EVOLUTION_OFF>0</EVOLUTION_OFF>
        <POPULATION_SIZE>1</POPULATION_SIZE>
        <REPLACEMENT_SIZE>1</REPLACEMENT_SIZE>
        <PROB_CROSSING>0.0</PROB_CROSSING>
        <PROB_MUTATION>0.05</PROB_MUTATION>
        <MUTATE_FUNCTIONS>1</MUTATE_FUNCTIONS>
        <MUTATE_CONNECTORS>1</MUTATE_CONNECTORS>
    </GA>
"""

gate_circuit = """
    <GATE_CIRCUIT>
        <NUM_LAYERS>5</NUM_LAYERS>
        <SIZE_LAYER>8</SIZE_LAYER>
        <NUM_CONNECTORS>4</NUM_CONNECTORS>
        <USE_MEMORY>0</USE_MEMORY>
        <SIZE_MEMORY>2</SIZE_MEMORY>
        <ALLOWED_FUNCTIONS>
            <FNC_NOP>1</FNC_NOP>
            <FNC_CONS>1</FNC_CONS>
            <FNC_AND>1</FNC_AND>
            <FNC_NAND>1</FNC_NAND>
            <FNC_OR>1</FNC_OR>
            <FNC_XOR>1</FNC_XOR>
            <FNC_NOR>1</FNC_NOR>
            <FNC_NOT>1</FNC_NOT>
            <FNC_SHIL>1</FNC_SHIL>
            <FNC_SHIR>1</FNC_SHIR>
            <FNC_ROTL>1</FNC_ROTL>
            <FNC_ROTR>1</FNC_ROTR>
            <FNC_EQ>0</FNC_EQ>
            <FNC_LT>0</FNC_LT>
            <FNC_GT>0</FNC_GT>
            <FNC_LEQ>0</FNC_LEQ>
            <FNC_GEQ>0</FNC_GEQ>
            <FNC_BSLC>1</FNC_BSLC>
            <FNC_READ>0</FNC_READ>
            <FNC_JVM>0</FNC_JVM>
        </ALLOWED_FUNCTIONS>
    </GATE_CIRCUIT>
"""

polynomial_circuit = """
    <POLYNOMIAL_CIRCUIT>
        <NUM_POLYNOMIALS>1</NUM_POLYNOMIALS>
        <MAX_NUM_TERMS>50</MAX_NUM_TERMS>
        <MUTATE_TERM_STRATEGY>1</MUTATE_TERM_STRATEGY>
        <TERM_COUNT_PROB>1.00</TERM_COUNT_PROB>
        <TERM_VAR_PROB>0.60</TERM_VAR_PROB>
        <ADD_TERM_PROB>0.05</ADD_TERM_PROB>
        <ADD_TERM_STRATEGY>0</ADD_TERM_STRATEGY>
        <RM_TERM_PROB>0.05</RM_TERM_PROB>
        <RM_TERM_STRATEGY>0</RM_TERM_STRATEGY>
        <CROSSOVER_RANDOMIZE_POLY>1</CROSSOVER_RANDOMIZE_POLY>
        <CROSSOVER_TERM_PROB>0.05</CROSSOVER_TERM_PROB>
    </POLYNOMIAL_CIRCUIT>
"""

test_vectors = """
    <TEST_VECTORS>
        <GENERATOR>1</GENERATOR>
        <INPUT_LENGTH>16</INPUT_LENGTH>
        <OUTPUT_LENGTH>1</OUTPUT_LENGTH>
        <SET_SIZE>1000</SET_SIZE>
        <SET_CHANGE_FREQ>100</SET_CHANGE_FREQ>
        <EVALUATE_BEFORE_TEST_VECTOR_CHANGE>0</EVALUATE_BEFORE_TEST_VECTOR_CHANGE>
        <EVALUATE_EVERY_STEP>0</EVALUATE_EVERY_STEP>
    </TEST_VECTORS>
"""

estream1 = """
    <ESTREAM>
        <GENERATOR_FOR_RAND_STREAM>1</GENERATOR_FOR_RAND_STREAM>
        <USAGE_TYPE>101</USAGE_TYPE>
        <CIPHER_INIT_FREQ>0</CIPHER_INIT_FREQ>
"""

# <ESTREAM/ALGORITHM_1>

estream2 = """
        <ALGORITHM_2>99</ALGORITHM_2>
        <BALLANCED_TEST_VECTORS>1</BALLANCED_TEST_VECTORS>
        <LIMIT_NUM_OF_ROUNDS>1</LIMIT_NUM_OF_ROUNDS>
"""

# <ESTREAM/ROUNDS_ALG_1>

estream3 = """
        <ROUNDS_ALG_2>0</ROUNDS_ALG_2>
        <PLAINTEXT_TYPE>0</PLAINTEXT_TYPE>
        <KEY_TYPE>2</KEY_TYPE>
        <IV_TYPE>0</IV_TYPE>
        <GENERATE_STREAM>0</GENERATE_STREAM>
        <STREAM_SIZE>5242880</STREAM_SIZE>
    </ESTREAM>
"""

sha1 = """
    <SHA3>
        <USAGE_TYPE>201</USAGE_TYPE>
        <PLAINTEXT_TYPE>210</PLAINTEXT_TYPE>
        <USE_FIXED_SEED>0</USE_FIXED_SEED>
        <SEED>145091104</SEED>
"""

# <SHA3/ALGORITHM_1>

sha2 = """
        <ALGORITHM_2>99</ALGORITHM_2>
        <HASHLENGTH_ALG_1>256</HASHLENGTH_ALG_1>
        <HASHLENGTH_ALG_2>256</HASHLENGTH_ALG_2>
        <BALLANCED_TEST_VECTORS>1</BALLANCED_TEST_VECTORS>
        <LIMIT_NUM_OF_ROUNDS>1</LIMIT_NUM_OF_ROUNDS>
"""

# <SHA3/ROUNDS_ALG_1>

sha3 = """
        <ROUNDS_ALG_2>0</ROUNDS_ALG_2>
        <GENERATE_STREAM>0</GENERATE_STREAM>
        <STREAM_SIZE>5242880</STREAM_SIZE>
    </SHA3>
"""

caesar = """
    <CAESAR>
        <USAGE_TYPE>301</USAGE_TYPE>
        <ALGORITHM>1</ALGORITHM>
        <LIMIT_NUM_OF_ROUNDS>0</LIMIT_NUM_OF_ROUNDS>
        <ALGORITHM_ROUNDS>0</ALGORITHM_ROUNDS>
        <PLAINTEXT_LENGTH>16</PLAINTEXT_LENGTH>
        <AD_LENGTH>2</AD_LENGTH>
        <PLAINTEXT_TYPE>2</PLAINTEXT_TYPE>
        <KEY_TYPE>1</KEY_TYPE>
        <AD_TYPE>0</AD_TYPE>
        <SMN_TYPE>0</SMN_TYPE>
        <PMN_TYPE>0</PMN_TYPE>
        <GENERATE_STREAM>0</GENERATE_STREAM>
        <STREAM_SIZE>5242880</STREAM_SIZE>
    </CAESAR>
"""

files = """
    <FILES>
        <USAGE_TYPE>401</USAGE_TYPE>
        <FILENAME_1>../../../qrng/Random000.bin</FILENAME_1>
        <FILENAME_2>../../../qrng/Random001.bin</FILENAME_2>
        <BALLANCED_TEST_VECTORS>1</BALLANCED_TEST_VECTORS>
        <USE_FIXED_INITIAL_OFFSET>1</USE_FIXED_INITIAL_OFFSET>
        <INITIAL_OFFSET_1>0</INITIAL_OFFSET_1>
        <INITIAL_OFFSET_2>0</INITIAL_OFFSET_2>
    </FILES>
</EACIRC>
"""


if __name__ == "__main__":

    # mkdirs estream, sha (from current dir - run from target dir)
    if not os.path.exists("./estream"):
        os.makedirs("./estream")

    if not os.path.exists("./sha"):
        os.makedirs("./sha")

    # for estream
    for fun, rounds in estream.items():
        fun_path = './estream/' + fun
        if not os.path.exists(fun_path):
            os.makedirs(fun_path)
        for r in rounds:
            f = open(fun_path + '/' + fun + 'r' + ("%02d" % r) + '.xml', 'w')
            f.write(header)
            f.write('    <NOTES>Big testbed: ' + fun_path + 'r' + ("%02d" % r) + '</NOTES>')
            f.write(main1)
            f.write('        <PROJECT>100</PROJECT>')  # eStream
            f.write(main2 + outputs + random + cuda + ga + gate_circuit + polynomial_circuit + test_vectors + estream1)
            f.write('        <ALGORITHM_1>' + str(estream_fun_names_id[fun]) + '</ALGORITHM_1>')
            f.write(estream2)
            f.write('        <ROUNDS_ALG_1>' + str(r) + '</ROUNDS_ALG_1>')
            f.write(estream3 + sha1)
            f.write('        <ALGORITHM_1>99</ALGORITHM_1>')  # unimportant
            f.write(sha2)
            f.write('        <ROUNDS_ALG_1>0</ROUNDS_ALG_1>')  # unimportant
            f.write(sha3 + caesar + files)
            f.close()

    # for sha
    for fun, rounds in sha.items():
        fun_path = './sha/' + fun
        if not os.path.exists(fun_path):
            os.makedirs(fun_path)
        for r in rounds:
            f = open(fun_path + '/' + fun + 'r' + ("%02d" % r) + '.xml', 'w')
            f.write(header)
            f.write('    <NOTES>Big testbed: ' + fun_path + 'r' + ("%02d" % r) + '</NOTES>')
            f.write(main1)
            f.write('        <PROJECT>200</PROJECT>')  # SHA3
            f.write(main2 + outputs + random + cuda + ga + gate_circuit + polynomial_circuit + test_vectors + estream1)
            f.write('        <ALGORITHM_1>99</ALGORITHM_1>')  # unimportant
            f.write(estream2)
            f.write('        <ROUNDS_ALG_1>0</ROUNDS_ALG_1>')  # unimportant
            f.write(estream3 + sha1)
            f.write('        <ALGORITHM_1>' + str(sha_fun_names_id[fun]) + '</ALGORITHM_1>')
            f.write(sha2)
            f.write('        <ROUNDS_ALG_1>' + str(r) + '</ROUNDS_ALG_1>')
            f.write(sha3 + caesar + files)
            f.close()

    # for rnd-rnd
    f = open('rnd_rnd.xml', 'w')
    f.write(header)
    f.write('    <NOTES>Big testbed: rnd-rnd</NOTES>')
    f.write(main1)
    f.write('        <PROJECT>100</PROJECT>')  # eStream
    f.write(main2 + outputs + random + cuda + ga + gate_circuit + polynomial_circuit + test_vectors + estream1)
    f.write('        <ALGORITHM_1>99</ALGORITHM_1>')
    f.write(estream2)
    f.write('        <ROUNDS_ALG_1>0</ROUNDS_ALG_1>')  # unimportant
    f.write(estream3 + sha1)
    f.write('        <ALGORITHM_1>99</ALGORITHM_1>')  # unimportant
    f.write(sha2)
    f.write('        <ROUNDS_ALG_1>0</ROUNDS_ALG_1>')  # unimportant
    f.write(sha3 + caesar + files)
    f.close()
