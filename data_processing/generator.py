#!/usr/bin/python3

import argparse
import json
import os
import subprocess
import sys
from copy import deepcopy

from joblib import Parallel, delayed

rtt_prefix = 'ctr_seed_1fe40505e131963c_'
# def confs
config_base = {
    'notes': 'generated by generator.py',
    'seed': '1fe40505e131963c',
    'tv-size': None,
    'tv-count': None
}
counter_stream = {
    'type': 'counter'
}
hw_stream = {
    'type': 'hw_counter',
    'hw': 4
}
random_stream = {
    'type': 'pcg32_stream'
}
false_stream = {
    'type': 'false_stream'
}
rnd_plt_ctx_stream = {
    'type': 'rnd_plt_ctx_stream',
    'source': None
}
sac_stream = {
    'type': 'sac'
}
plaintext_target_stream = counter_stream


class FunArgs:
    def __init__(self, block_size, key_size, iv_size=None, rounds=()):
        self.block_size = block_size
        self.key_size = key_size
        self.iv_size = iv_size
        self.rounds = rounds


# used funs in batch
stream_cipher_funs = { }
stream_cipher_default = {
    'type': 'stream_cipher',
    'generator': 'pcg32',
    'algorithm': None,
    'round': None,
    'block_size': None,
    'plaintext': plaintext_target_stream,
    'key_size': None,
    'key': random_stream,
    'iv_size': None,
    'iv': false_stream
}

hash_funs = {
    'BLAKE': FunArgs(32, None, None, (0, 1, 2, 3)),
    'Grostl': FunArgs(32, None, None, (1, 2, 3, 4)),
    'JH': FunArgs(32, None, None, (5, 6, 7, 8, 9)),
    'Keccak': FunArgs(32, None, None, (1, 2, 3, 4)),
    'MD6': FunArgs(32, None, None, (5, 6, 7, 8, 9, 10)),
    'Skein': FunArgs(32, None, None, (1, 2, 3, 4)),

    'Gost': FunArgs(32, None, None, (1, 2, 3)),
    'MD5': FunArgs(16, None, None, (6, 7, 8, 9, 10, 11)),
    'RIPEMD160': FunArgs(20, None, None, (7, 8, 9, 10)),
    'SHA1': FunArgs(20, None, None, (11, 12, 13, 14)),
    'SHA2': FunArgs(32, None, None, (5, 6, 7)),
    'Tiger': FunArgs(24, None, None, (1, 2)),
    'Whirlpool': FunArgs(64, None, None, (2, 4)),
}
hash_default = {
    'type': 'hash',
    'generator': 'pcg32',
    'algorithm': None,
    'round': None,
    'hash_size': None,
    'input_size': None,
    'source': plaintext_target_stream
}


block_funs = {
    'AES': FunArgs(16, 16, None, (1, 2, 3, 4)),
    'BLOWFISH': FunArgs(8, 32, None, (1, 2, 3, 4)),
    'MARS': FunArgs(16, 16, None, (0, 1)),
    'TWOFISH': FunArgs(16, 16, None, (1, 2, 3, 4)),
    'SERPENT': FunArgs(16, 16, None, (1, 2, 3, 4)),
    'RC6': FunArgs(16, 16, None, (2, 3, 4, 5)),

    'SIMON': FunArgs(16, 16, None, (13, 14, 15, 16, 17)),
    'SPECK': FunArgs(16, 16, None, (6, 7, 8, 9)),
    'SINGLE-DES': FunArgs(8, 7, None, (3, 4, 5, 6)),
    'TRIPLE-DES': FunArgs(8, 21, None, (1, 2, 3)),
    'TEA': FunArgs(8, 16, None, (2, 3, 4, 5)),
    'GOST': FunArgs(8, 32, None, (6, 7, 8, 9)),
    
    'ARIA': FunArgs(16, 16, None, (1, 2, 3)),
    'CAMELLIA': FunArgs(16, 16, None, (1, 2, 3, 4)),
    'CAST': FunArgs(8, 16, None, (1, 2, 3, 4, 5)),
    'IDEA': FunArgs(8, 16, None, (1, 2, 3)),
    'SEED': FunArgs(16, 16, None, (1, 2, 3, 4)),

    'KASUMI' : FunArgs(8, 16, None, (1, 2, 3, 4, 5)),
    'MISTY1' : FunArgs(8, 16, None, (1, 2, 3)),
    'KUZNYECHIK' : FunArgs(16, 32, None, (1, 2, 3)),
    'NOEKEON' : FunArgs(16, 16, None, (1, 2, 3, 4)),
    'SHACAL2' : FunArgs(32, 64, None, (2, 3, 4, 5, 6, 7)),
    'XTEA' : FunArgs(8, 16, None, (1, 2, 3, 4, 5)),
}
block_default = {
    'type': 'block',
    'init_frequency': 'only_once',
    'algorithm': None,
    'round': None,
    'block_size': 16,
    'plaintext': plaintext_target_stream,
    'key_size': 16,
    'key': random_stream,
    'iv_size': 16,
    'iv': false_stream
}


def prepare_cfg(project, fun, rounds, tv_size, tv_num):
    cfg_name = '{}_r{:02d}_b{}.json'.format(fun, rounds, tv_size)
    bin_name = '{}_r{:02d}_b{}.bin'.format(fun, rounds, tv_size)

    with open(cfg_name, 'w') as f:

        current_cfg = deepcopy(config_base)
        current_cfg['tv_size'] = tv_size
        current_cfg['tv_count'] = tv_num
        current_cfg['file_name'] = bin_name

        if project == "stream_cipher":
            stream = deepcopy(stream_cipher_default)
            stream['algorithm'] = fun
            stream['round'] = rounds
            stream['block_size'] = stream_cipher_funs[fun].block_size
            stream['key_size'] = stream_cipher_funs[fun].key_size
            stream['iv_size'] = stream_cipher_funs[fun].iv_size
            current_cfg['stream'] = stream

        elif project == "hash":
            stream = deepcopy(hash_default)
            stream['algorithm'] = fun
            stream['round'] = rounds
            stream['hash_size'] = hash_funs[fun].block_size
            stream['input_size'] = hash_funs[fun].block_size
            current_cfg['stream'] = stream

        elif project == "block":
            stream = deepcopy(block_default)
            stream['algorithm'] = fun
            stream['round'] = rounds
            stream['block_size'] = block_funs[fun].block_size
            stream['key_size'] = block_funs[fun].key_size
            current_cfg['stream'] = stream

        else:  # rnd
            stream = deepcopy(random_stream)
            stream['algorithm'] = fun
            stream['round'] = 0
            stream['block_size'] = 16
            current_cfg['stream'] = stream

        f.write(json.dumps(current_cfg))
        f.close()

    return cfg_name


def run_single(args):
    project, fun, rounds, tv_size, data, num_tv, generator_binary = args
    cfg_name = prepare_cfg(project, fun, rounds, tv_size, num_tv)
    cmd = '{} -c={}'.format(generator_binary, cfg_name)
    print("Executing: " + cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    binfile_name = cfg_name.split('.')[0] + '.bin'

    cfg_size = ['1MB.json', '10MB.json', '100MB.json', '1000MB.json', 'default-8GB.json']
    if 1000000 <= data < 10000000:
        cfg = cfg_size[0]
    elif 10000000 <= data < 100000000:
        cfg = cfg_size[1]
    elif 100000000 <= data < 1000000000:
        cfg = cfg_size[2]
    elif 1000000000 <= data < 8000000000:
        cfg = cfg_size[3]
    elif 8000000000 <= data:
        cfg = cfg_size[4]
    else:
        exit("Too small data for testing.")
        return None
    cmd = 'submit_experiment --all_batteries -c {0} -f {1} -n {2}{1}'.format(cfg, binfile_name, rtt_prefix)
    print("Executing: " + cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    cmd = 'rm {0}'.format(binfile_name)
    print("Executing: " + cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()


def single_setup_generator(generator_binary, data=None, num_tv=None):
    def _yield_single_setup(funs, project):
        for fun in funs:
            args = funs[fun]
            for rounds_count in args.rounds:
                if data:
                    data_out = data
                    num_tv_out = data // args.block_size
                else:
                    data_out = num_tv * args.block_size
                    num_tv_out = num_tv
                yield [project, fun, rounds_count, args.block_size, data_out, num_tv_out, generator_binary]

    yield from _yield_single_setup(stream_cipher_funs, 'stream_cipher')
    yield from _yield_single_setup(hash_funs, 'hash')
    yield from _yield_single_setup(block_funs, 'block')


def run_all(binary, data=None, num_tv=None):
    Parallel(n_jobs=-1)(delayed(run_single)(single_setup)
                        for single_setup in single_setup_generator(binary, data, num_tv))


def get_tv_size(main_args):
    if main_args.stream_type == "stream_cipher":
        return stream_cipher_funs[main_args.fun].block_size
    if main_args.stream_type == "hash":
        return hash_funs[main_args.fun].block_size
    if main_args.stream_type == "block":
        return block[main_args.fun].block_size
    return 16


def main_args_to_fnc(main_args):
    project = main_args.stream_type
    fun = main_args.fun
    rounds = main_args.rounds

    tv_size = get_tv_size(main_args)
    tv_num = (main_args.num // tv_size) if main_args.data else main_args.num

    prepare_cfg(project, fun, rounds, tv_size, tv_num)


def main():
    parser = argparse.ArgumentParser()
    single_execution_args(parser)
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        default=False,
        help='Whether we should execute all experiments, or just single one'
    )
    parser.add_argument(
        '-p',
        '--path_to_generator_binary',
        type=str,
        default='./generator',
        help='Path to the binary of generator (or newly called eacirc_streams binary)'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-n',
        '--num_tv',
        action='store_true',
        default=False,
        help='Number of test vectors generated'
    )
    group.add_argument(
        '-d',
        '--data',
        action='store_true',
        default=False,
        help='Number of generated bytes'
    )
    parser.add_argument(
        'num',
        metavar='N',
        type=int,
        default=1000000,
        help='the number of TV or data')
    main_args, _ = parser.parse_known_args()

    if main_args.num_tv == main_args.data:
        sys.exit('Choose EITHER --num_tv or --data')

    if main_args.all:
        print('Running all experiments')
        data = main_args.num if main_args.data else None
        num_tv = main_args.num if main_args.num_tv else None
        run_all(main_args.path_to_generator_binary, data=data, num_tv=num_tv)
    else:
        single_execution_parse(main_args)
        main_args_to_fnc(main_args)
        os.system(main_args.path_to_generator_binary)


def single_execution_parse(main_args):
    if main_args.stream_type == '':
        if main_args.fun in stream_cipher_funs:
            main_args.stream_type = 'stream_cipher'
        elif main_args.fun in hash_funs:
            main_args.stream_type = 'hash'
        elif main_args.fun in block_funs:
            main_args.stream_type = 'block'
        else:
            sys.exit('Unknown function and unspecified stream. Set -s! Function was: ' + main_args.fun)
    else:
        if main_args.fun in stream_cipher_funs and main_args.stream_type != 'stream-cipher':
            sys.exit('Mismatch arguments: function '
                     + main_args.fun
                     + ' is from stream-cipher, your stream_type is '
                     + main_args.stream_type)
        elif main_args.fun in hash_funs and main_args.stream_type != 'hash':
            sys.exit('Mismatch arguments: function '
                     + main_args.fun
                     + ' is from hash, your stream_type is '
                     + main_args.stream_type)
        elif main_args.fun in block_funs and main_args.stream_type != 'block':
            sys.exit('Mismatch arguments: function '
                     + main_args.fun
                     + ' is from block, your stream_type is '
                     + main_args.stream_type)
    print('generator.py: preparing config for function '
          + main_args.fun
          + ' from '
          + main_args.stream_type
          + ' reduced to '
          + str(main_args.rounds)
          + ' rounds.')


def single_execution_args(parser):
    parser.add_argument(
        '-s',
        '--stream_type',
        type=str,
        default='',
        help='Stream: for AES, DES... = block, Salsa... = stream-cipher, Keccak... = hash'
    )
    parser.add_argument(
        '-f',
        '--fun',
        type=str,
        default='PRNG',
        help='Function used for data generation'
    )
    parser.add_argument(
        '-r',
        '--rounds',
        type=int,
        default=1,
        help='Function is reduced to --rounds'
    )


if __name__ == '__main__':
    main()
