from django.core.cache import cache
import os

FIBONACCI_REDIS_KEY_PREFIX = os.environ.get('FIBONACCI_REDIS_KEY_PREFIX')
ACKERMANN_REDIS_KEY_PREFIX = os.environ.get('ACKERMANN_REDIS_KEY_PREFIX')
FACTORIAL_REDIS_KEY_PREFIX = os.environ.get('FACTORIAL_REDIS_KEY_PREFIX')


def get_nth_fibonacci(n):
    cache_keys = cache.keys(f'{FIBONACCI_REDIS_KEY_PREFIX}_*')
    current_cache_key = f'{FIBONACCI_REDIS_KEY_PREFIX}_{n}'
    if n <= 1:
        return 0
    if n in [2, 3]:
        return 1
    if current_cache_key in cache_keys:
        return cache.get(current_cache_key)
    else:
        current_value = get_nth_fibonacci(n - 1) + get_nth_fibonacci(n - 2)
        cache.set(current_cache_key, current_value, None)
        return current_value


def method2_fibo(number):
    if cache.get(f'{FIBONACCI_REDIS_KEY_PREFIX}_{number-1}') and cache.get(f'{FIBONACCI_REDIS_KEY_PREFIX}_{number-2}'):
        return cache.get(f'{FIBONACCI_REDIS_KEY_PREFIX}_{number-1}') + cache.get(f'{FIBONACCI_REDIS_KEY_PREFIX}_{number-2}')
    sorted_cache_keys = sorted([int(x.split("_")[-1]) for x in cache.keys(f'{FIBONACCI_REDIS_KEY_PREFIX}_*')])
    filtered_keys = [x for x in sorted_cache_keys if x < number]
    a = 1
    b = 1
    if len(filtered_keys) > 1:
        a = filtered_keys[-1]
        b = filtered_keys[-2]
    ctr = b
    if number == 0:
        return 0
    if number <= 2:
        return 1
    diff = number-len(filtered_keys)
    if diff == 0:
        return b
    for i in range(number-len(filtered_keys)):
        c = a + b
        a = b
        b = c
        ctr += 1
        cache.set(f'{FIBONACCI_REDIS_KEY_PREFIX}_{ctr}',c,None)

    return cache.get(f'{FIBONACCI_REDIS_KEY_PREFIX}_{number}')


def handle_fibonacci(number):
    redis_key = os.environ.get('FIBONACCI_REDIS_KEY_PREFIX')
    cached_value = cache.get(f'{redis_key}_number')
    if cached_value is not None:
        return cached_value
    else:
        # import sys
        # sys.setrecursionlimit(2000)
        return method2_fibo(number)


def handle_ackermann(number):
    pass


def handle_factorial(number):
    pass
