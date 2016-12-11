#!/usr/bin/python

# TODO: document here purpose of this experiment
# Tested functions: sha3 and estream finalists
# Settings: basic settings for CPU computations, used in many papers (as EACirc 2.0 paper)
# Purpose: finding rounds counts for usable testbed

# ReadMe:
# 1. fork this script and rewrite it for your purpose
# 2. document your purpose in the header, so others can easily get into your experiment
# Rewriting:
# a) choose functions and rounds in dictionaries estream and sha
# b) go trough text variables with actual configuration file
#   i) change constants in text, if your experiment doesn't need to variate them
#   ii) for variadic changes, create list/dict with your parameters and split surrrounding text parts; add for loop in main and print values, you are iterating trough; probably change directory tree generation


import os


# used funs in batch
# USE exactly the string from estream_fun_names_id or worry about ID's of funs!
estream = {
    'Grain': [2, 3, 4],
    'HC-128': [i for i in range(0, 5)],
#    'MICKEY': [i for i in range(0, 10)],
    'Rabbit': [i for i in range(0, 5)],
    'Salsa20': [2, 3, 4],
    'SOSEMANUK': [i for i in range(0, 5)]#,
#    'Trivium': [i for i in range(0, 10)]
}

sha = {
    'BLAKE': [0, 1, 2, 3],
    'Grostl': [2, 3, 4, 5],
    'JH': [6, 7, 8],
    'Keccak': [i for i in range(1, 10)],
    'MD6': [8, 9, 10, 11],
    'Skein': [0] # skein is not round based :(
}

class Fun_args:
    def __init__(self, rounds, block_size, key_size):
        self.rounds = rounds
        self.block_size = block_size
        self.key_size = key_size

block = {
    'TEA': Fun_args([3, 4, 5, 6], 8, 16), # 4 is max
    'AES': Fun_args([1, 2, 3, 4], 16, 16), # 2-3 is max
    'RC4': Fun_args([1], 16, 16), # RC4 is not round based :(
    'SINGLE-DES': Fun_args([i for i in range(0, 15)], 8, 8),
    'TRIPLE-DES': Fun_args([i for i in range(0, 15)], 24, 8)
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

    for fun, fun_args in block.items():
        fun_path = './block/' + fun
        if not os.path.exists(fun_path):
            os.makedirs(fun_path)
        for r in fun_args.rounds:
            f = open(fun_path + '/' + fun + '_r' + ("%02d" % r) + '.json', 'w')
            f.write(header)
            f.write('    \"notes\" : \"' + fun_path + '_r' + ("%02d" % r) + '\",')
            f.write(main1)

            # stream-a
            f.write('    \"stream-a\" : {\n')
            f.write('        \"type\" : \"block\",\n')
            f.write('        \"generator\" : \"pcg32\",\n')
            f.write('        \"init-frequency\" : \"only-once\",\n')
            f.write('        \"algorithm\" : \"' + fun + '\",\n')
            f.write('        \"round\" : ' + str(r) + ',\n')
            f.write('        \"block-size\" : ' + str(fun_args.block_size) + ',\n')
            f.write("""        "plaintext" : {
            "type" : "counter"
        },\n""")
            f.write('        \"key-size\" : ' + str(fun_args.key_size) + ',\n')
            f.write("""        "key" : {
            "type" : "pcg32-stream"
        },\n""")
            f.write('        \"mode\" : \"ECB\",\n')
            f.write("""        "iv" : {
            "type" : "false-stream"
        }\n""")
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
