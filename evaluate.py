#!/usr/bin/env python3
import time
import random
import math

# Import the required functions from your module rns
from rns import encode, decode, get_dynamic_range


# --- Helper functions for CRT ---

def extended_gcd(a, b):
    """Extended Euclidean algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    """Computes the multiplicative inverse of a modulo m."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Multiplicative inverse does not exist")
    return x % m


def decode_crt(code, moduli):
    """Decodes an RNS representation using the classical Chinese Remainder Theorem.
    Works only for pairwise coprime moduli."""
    M = 1
    for p in moduli:
        M *= p
    x = 0
    for a, p in zip(code, moduli):
        M_i = M // p
        y_i = modinv(M_i, p)
        x += a * M_i * y_i
    return x % M


# --- Benchmarking function for decoding ---

def benchmark_decode(decode_fn, moduli, num_iterations):
    """
    Generates num_iterations random numbers in the range [0, get_dynamic_range(moduli)),
    encodes them into RNS using the provided moduli, and measures the time required for decoding
    using the provided decode function.
    """
    dynamic_range = get_dynamic_range(moduli)
    numbers = [random.randrange(dynamic_range) for _ in range(num_iterations)]
    codes = [encode(n, moduli) for n in numbers]
    start = time.perf_counter()
    for code in codes:
        decode_fn(code, moduli)
    end = time.perf_counter()
    return end - start


def main():
    # Testing for pairwise coprime moduli (small set)
    iterations_small = 100000
    print("=== Testing with pairwise coprime moduli (small set) ===")
    coprime_moduli_small = [7, 11, 13]  # Dynamic range = 7 * 11 * 13 = 1001
    print("Moduli:", coprime_moduli_small)
    my_time_small = benchmark_decode(decode, coprime_moduli_small, iterations_small)
    crt_time_small = benchmark_decode(decode_crt, coprime_moduli_small, iterations_small)
    print(f"My (recursive) method time: {my_time_small:.6f} seconds")
    print(f"CRT method time: {crt_time_small:.6f} seconds")

    # Testing for pairwise coprime moduli (large set)
    iterations_large = 100000
    print("\n=== Testing with pairwise coprime moduli (large set) ===")
    coprime_moduli_large = [10007, 10009, 10037, 10039, 10061, 10067, 10069, 10079]
    print("Moduli:", coprime_moduli_large)
    my_time_large = benchmark_decode(decode, coprime_moduli_large, iterations_large)
    crt_time_large = benchmark_decode(decode_crt, coprime_moduli_large, iterations_large)
    print(f"My (recursive) method time: {my_time_large:.6f} seconds")
    print(f"CRT method time: {crt_time_large:.6f} seconds")

    # Testing for non-coprime moduli
    iterations_non = 100000
    print("\n=== Testing with non-coprime moduli ===")
    non_coprime_moduli = [7, 6, 5]  # Dynamic range = LCM(7,6,5) = 210
    print("Moduli:", non_coprime_moduli)
    my_time_non = benchmark_decode(decode, non_coprime_moduli, iterations_non)
    print(f"My method time (non-coprime): {my_time_non:.6f} seconds")
    print("CRT method is not applicable for non-coprime moduli.")

    # Testing for RSA-like case: only two very large prime numbers.
    # In real RSA, the primes are hundreds or thousands of bits long, but here we use smaller values for testing.
    iterations_rsa = 1000  # Fewer iterations due to larger numbers
    print("\n=== Testing RSA-like case (two large primes) ===")
    rsa_moduli = [1000003, 1000033]  # Two "large" primes (example values)
    print("Moduli:", rsa_moduli)
    my_time_rsa = benchmark_decode(decode, rsa_moduli, iterations_rsa)
    crt_time_rsa = benchmark_decode(decode_crt, rsa_moduli, iterations_rsa)
    print(f"My (recursive) method time: {my_time_rsa:.6f} seconds")
    print(f"CRT method time: {crt_time_rsa:.6f} seconds")


if __name__ == '__main__':
    main()
