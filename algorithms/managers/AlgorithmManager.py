import logging
import os
from .CacheManager import CacheRepository

FIBONACCI_REDIS_KEY_PREFIX = os.environ.get('FIBONACCI_REDIS_KEY_PREFIX')
ACKERMANN_REDIS_KEY_PREFIX = os.environ.get('ACKERMANN_REDIS_KEY_PREFIX')
FACTORIAL_REDIS_KEY_PREFIX = os.environ.get('FACTORIAL_REDIS_KEY_PREFIX')


def get_cache_repository():
    return CacheRepository()

def get_nth_fibonacci(n):
    cacheRepo = get_cache_repository()
    cachedResult = cacheRepo.connection.hget(FIBONACCI_REDIS_KEY_PREFIX, n)
    if cachedResult:
        return cachedResult

    last_two = [0, 1]
    counter = 3

    while counter <= n:
        next_fib = last_two[0] + last_two[1]
        last_two[0] = last_two[1]
        last_two[1] = next_fib
        counter += 1

    if n > 1:
        cacheRepo.connection.hset(FIBONACCI_REDIS_KEY_PREFIX,n,last_two[1])
        return last_two[1]
    else:
        cacheRepo.connection.hset(FIBONACCI_REDIS_KEY_PREFIX, n, last_two[0])
        return last_two[0]


def handle_fibonacci(number):
    return get_nth_fibonacci(number)


def handle_ackermann(number):
    pass


def handle_factorial(number):
    pass
