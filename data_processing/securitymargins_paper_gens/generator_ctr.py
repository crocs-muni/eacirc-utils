#!/usr/bin/python3

import json
from copy import deepcopy
from generator_defaults import CfgDefaults, FunArgs


class GeneratorCfgCtr:
    cs_input_strategy_prefix = 'ctr'
    plaintext_target_stream = CfgDefaults.counter_stream

    # used funs in batch
    stream_cipher_funs = {}
    stream_cipher_default = {
        'type': 'stream_cipher',
        'generator': 'pcg32',
        'algorithm': None,
        'round': None,
        'block_size': None,
        'plaintext': plaintext_target_stream,
        'key_size': None,
        'key': CfgDefaults.random_stream,
        'iv_size': None,
        'iv': CfgDefaults.false_stream
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

        'KASUMI': FunArgs(8, 16, None, (1, 2, 3, 4, 5)),
        'MISTY1': FunArgs(8, 16, None, (1, 2, 3)),
        'KUZNYECHIK': FunArgs(16, 32, None, (1, 2, 3)),
        'NOEKEON': FunArgs(16, 16, None, (1, 2, 3, 4)),
        'SHACAL2': FunArgs(32, 64, None, (2, 3, 4, 5, 6, 7)),
        'XTEA': FunArgs(8, 16, None, (1, 2, 3, 4, 5)),
    }
    block_default = {
        'type': 'block',
        'init_frequency': 'only_once',
        'algorithm': None,
        'round': None,
        'block_size': 16,
        'plaintext': plaintext_target_stream,
        'key_size': 16,
        'key': CfgDefaults.random_stream,
        'iv_size': 16,
        'iv': CfgDefaults.false_stream
    }

    def prepare_cfg(self, project, fun, rounds, tv_size, tv_num, seed, name_prefix):
        cfg_name = '{}_{}_r{:02d}_b{}.json'.format(name_prefix, fun, rounds, tv_size)
        bin_name = '{}_{}_r{:02d}_b{}.bin'.format(name_prefix, fun, rounds, tv_size)

        with open(cfg_name, 'w') as f:

            current_cfg = deepcopy(CfgDefaults.config_base)
            current_cfg['seed'] = seed
            current_cfg['tv_size'] = tv_size
            current_cfg['tv_count'] = tv_num
            current_cfg['file_name'] = bin_name

            if project == "stream_cipher":
                stream = deepcopy(self.stream_cipher_default)
                stream['algorithm'] = fun
                stream['round'] = rounds
                stream['block_size'] = self.stream_cipher_funs[fun].block_size
                stream['key_size'] = self.stream_cipher_funs[fun].key_size
                stream['iv_size'] = self.stream_cipher_funs[fun].iv_size
                current_cfg['stream'] = stream

            elif project == "hash":
                stream = deepcopy(self.hash_default)
                stream['algorithm'] = fun
                stream['round'] = rounds
                stream['hash_size'] = self.hash_funs[fun].block_size
                stream['input_size'] = self.hash_funs[fun].block_size
                current_cfg['stream'] = stream

            elif project == "block":
                stream = deepcopy(self.block_default)
                stream['algorithm'] = fun
                stream['round'] = rounds
                stream['block_size'] = self.block_funs[fun].block_size
                stream['key_size'] = self.block_funs[fun].key_size
                current_cfg['stream'] = stream

            else:  # rnd
                stream = deepcopy(CfgDefaults.random_stream)
                stream['algorithm'] = fun
                stream['round'] = 0
                stream['block_size'] = 16
                current_cfg['stream'] = stream

            f.write(json.dumps(current_cfg))
            f.close()

        return cfg_name


