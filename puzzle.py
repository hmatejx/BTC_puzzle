#!/usr/bin/python3

"""
My attempt at solving the 0.025 BTC puzzle posted on Reddit:
    https://www.reddit.com/r/Bitcoin/comments/8krbd3/prize_inside_25mbtc_private_key_in_puzzle/

I was too late, but it was fun!
"""

from pycoin.key import Key
from pycoin.encoding import hash160, b2a_hashed_base58, hash160, b2a_base58, a2b_base58, double_sha256


def p2sh_address(key):
    """
    Function to convert the given private key to the P2SH key
    used to signify a SegWit address starting with '3'.

    This SegWit address is a <redeemScript>
    (https://bitcoincore.org/en/segwit_wallet_dev/#creation-of-p2sh-p2wpkh-address).

    It starts with a OP_0, followed by a canonical push of the keyhash 
    (i.e. 0x0014{20-byte keyhash}).
    """
    return b2a_hashed_base58(b'\5' + hash160(b'\x00\x14' + hash160(key.sec(use_uncompressed=False))))


# this is the final result, but below is the brute-force algorithm that shows how it was obtained
thekey = "L5fnrCYwxHsqbFKkfBVS2if1zwK6FyXV8Xet6FnmTG4W1eYgQDFq"

# key segments (letters only) that I'm sure of
k1 = "L"
k2 = "fnrCYwxHsqbFKkfZVS"
k3 = "if1zwK"
k4 = "FyXV"
k5 = "Xet"
k6 = "FnmTG"
k7 = "W"
k8 = "eYgQDFq"

# for the numbers I was not sure for all of them, so I just brute-forced the ones I was unsure of
longest_match = 0
for i1 in '4': # sure
    for i2 in '2': # sure
        for i3 in '6': # sure
            for i4 in '123456789': # NOT sure
                for i6 in '123456789': # NOT sure
                    for i7 in '123456789': # NOT sure

                        # make candidate private key
                        key = k1 + i1 + k2 + i2 + k3 + i3 + k4 + i4 + k5 + i3 + k6 + i6 + k7 + i7 + k8
                        print('Trying {}...\t'.format(key), end='')

                        # the private key encoded in base58 contains also a checksum at the end to check validity
                        # when a candidate key is made by concatenation as above it will most likely not be valid
                        # so we correct the checksum and compression byte of the candidate key
                        data = a2b_base58(key)
                        data, the_hash = data[:-4], data[-4:]
                        data = data[:-1] + b'\01'
                        fixed_key = b2a_base58(data + double_sha256(data)[:4])

                        # calculate the P2SH SegWit address for this private key
                        k = Key.from_text(fixed_key)
                        p2sh = p2sh_address(k)
                        print('{}\t'.format(p2sh), end='')

                        # compare with the published public key
                        if p2sh[0:7] == '37CSnmm':
                            print('Bingo!')
                            exit(0)
                        else:
                            i = 0
                            stars = ''
                            while p2sh[i] == '37CSnmm'[i]:
                                stars += '*'
                                i += 1
                            if i > longest_match:
                                longest_match = i
                            print('{} {}'.format(longest_match, stars))
