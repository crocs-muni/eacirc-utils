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
    'HC-128': 11,
    'Hermes': 12,
    'LEX': 13,
    'MAG': 14,
#    'MICKEY': 15, # cycles
    'Mir-1': 16,
    'Pomaranch': 17,
    'Py': 18,
    'Rabbit': 19,
    'Salsa20': 20,
    'SFINKS': 21,
    'SOSEMANUK': 22,
    'TEA': 23,
#    'Trivium': 24, # not working
    'TSC-4': 25,
    'WG': 26,
#    'Yamb': 27,
    'Zk-Crypt': 28
}

sha_fun_names_id = {
    'Abacus': 1,
    'ARIRANG': 2,
    'AURORA': 3,
    'BLAKE': 4,
    'Blender': 5,
    'BMW': 6,
    'Boole': 7,
    'Cheetah': 8,
    'CHI': 9,
    'CRUNCH': 10,
    'CubeHash': 11,
    'DCH': 12,
    'DynamicSHA': 13,
    'DynamicSHA2': 14,
    'ECHO': 15,
#    'ECOH': 16, # not working
    'EDON': 17,
#    'EnRUPT': 18,
    'ESSENCE': 19,
    'Fugue': 20,
    'Grostl': 21,
    'Hamsi': 22,
    'JH': 23,
    'Keccak': 24,
    'Khichidi': 25,
    'LANE': 26,
    'Lesamnta': 27,
    'Luffa': 28,
#    'LUX': 29,
    'MCSSHA3': 30,
    'MD6': 31,
    'MeshHash': 32,
    'NaSHA': 33,
#    'SANDstorm': 34,
    'Sarmal': 35,
    'Shabal': 36,
    'SHAMATA': 37,
    'SHAvite3': 38,
    'SIMD': 39,
    'Skein': 40,
    'SpectralHash': 41,
    'StreamHash': 42,
#    'SWIFFTX': 43,
    'Tangle': 44,
#    'TIB3': 45,
    'Twister': 46,
#    'Vortex': 47,
    'WaMM': 48,
    'Waterfall': 49,
    'Tangle2': 50
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
    'AURORA': [2, 3, 4, 5],
    'BLAKE': [0, 1, 2, 3],
    'Cheetah': [4, 5, 6, 7],
    'CubeHash': [0, 1, 2, 3],
    'DCH': [1, 2, 3],
    'DynamicSHA': [7, 8, 9, 10, 16],
    'DynamicSHA2': [11, 12, 13, 14],
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

header = """{
"""

# notes

main1 = """
    "seed" : null,

    "num-of-epochs" : 300,
    "significance-level" : 1,
    "tv-size" : 16,
    "tv-count" : 1000,
"""

# stream-a

streamB = """
    "stream-b" : {
        "type" : "pcg32-stream"
    },
"""

backend1 = """
    "backend" : {
        "type" : "circuit",
        "solver" : "global-search",

        "function-set" : [ "NOP", "CONS", "NOT",
                           "AND", "NAND", "OR", "XOR", "NOR",
                           "SHIL", "SHIR", "ROTL", "ROTR",
                           "MASK" ],
        "num-of-generations": 100,

        "initializer" : {
            "type" : "basic-initializer"
        },
        "mutator" : {
            "type" : "basic-mutator",
            "changes-of-functions" : 2,
            "changes-of-arguments" : 2,
            "changes-of-connectors" : 3
        },
        "evaluator" : {
            "type" : "categories-evaluator",
            "num-of-categories" : 8
        }
    }
 }
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
            f = open(fun_path + '/' + fun + '_r' + ("%02d" % r) + '.json', 'w')
            f.write(header)
            f.write('    \"notes\" : \"' + fun_path + '_r' + ("%02d" % r) + '\",')
            f.write(main1)

            # stream-a
            f.write('    \"stream-a\" : {\n')
            f.write('        \"type\" : \"estream\",\n')
            f.write('        \"generator\" : \"pcg32\",\n')
            f.write('        \"init-frequency\" : \"only-once\",\n')
            f.write('        \"algorithm\" : \"' + fun + '\",\n')
            f.write('        \"round\" : ' + str(r) + ',\n')
            f.write("""        "plaintext-type" : {
            "type" : "counter"
        },\n""")
            f.write('        \"key-type\" : \"random\",\n')
            f.write('        \"iv-type\" : \"zeros\"\n')
            f.write('    },')

            f.write(streamB)
            f.write(backend1)
            f.close()

    for fun, rounds in sha.items():
        fun_path = './sha/' + fun
        if not os.path.exists(fun_path):
            os.makedirs(fun_path)
        for r in rounds:
            f = open(fun_path + '/' + fun + '_r' + ("%02d" % r) + '.json', 'w')
            f.write(header)
            f.write('    \"notes\" : \"' + fun_path + '_r' + ("%02d" % r) + '\",')
            f.write(main1)

            # stream-a
            f.write('    \"stream-a\" : {\n')
            f.write('        \"type\" : \"sha3\",\n')
            f.write("""        "source" : {
            "type" : "counter"
        },\n""")
            f.write('        \"algorithm\" : \"' + fun + '\",\n')
            f.write('        \"round\" : ' + str(r) + ',\n')
            f.write('        \"hash-bitsize\" : 256\n')
            f.write('    },\n')

            f.write(streamB)
            f.write(backend1)
            f.close()

    # for rnd-rnd
    f = open('rnd_rnd.json', 'w')
    f.write(header)
    f.write('    \"notes\" : \"Big testbed: rnd-rnd\",')
    f.write(main1)

    # stream-a
    f.write('    \"stream-a\" : {\n')
    f.write('        \"type\" : \"pcg32-stream\"\n')
    f.write('    },')

    f.write(streamB)
    f.write(backend1)
    f.close()
