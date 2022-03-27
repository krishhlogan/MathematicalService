import logging
import os
from .CacheManager import CacheRepository
import math

FIBONACCI_REDIS_KEY_PREFIX = os.environ.get('FIBONACCI_REDIS_KEY_PREFIX')
ACKERMANN_REDIS_KEY_PREFIX = os.environ.get('ACKERMANN_REDIS_KEY_PREFIX')
FACTORIAL_REDIS_KEY_PREFIX = os.environ.get('FACTORIAL_REDIS_KEY_PREFIX')


def get_cache_repository():
    return CacheRepository()


def validate_input(number, min_value):
    if number is None:
        raise ValueError("Number Argument is missing")
    if type(number) == 'str' and not number.isdigit():
        raise TypeError("Number Should be a positive integer")
    if int(number) < min_value:
        raise ValueError(f"Number Should be a larger than {min_value - 1}")
    return True


def get_filtered_keys(number, keys):
    return list(filter(lambda x: True if int(x) < number else False, keys))


def get_valid_cache_keys(keys):
    found = False
    idx = len(keys) - 1
    while not found:
        if abs(int(keys[int(idx)]) - int(keys[int(idx) - 1])) != 1:
            idx -= 1
        else:
            found = True
    return [keys[int(idx) - 1], keys[int(idx)]]


def return_infinity(start, end, cache_key):
    if cache_key == FIBONACCI_REDIS_KEY_PREFIX:
        infinity_limit = int(os.getenv('FIBONACCI_INFINITY_LIMIT'))
    elif cache_key == FIBONACCI_REDIS_KEY_PREFIX:
        infinity_limit = int(os.getenv('FACTORIAL_INFINITY_LIMIT'))
    else:
        infinity_limit = int(os.getenv('ACKERMANN_INFINITY_LIMIT'))
    return True if end - start > infinity_limit else False


def get_last_two_numbers(keys):
    if len(keys) >= 2:
        return get_valid_cache_keys(keys)
    else:
        return []


def get_last_number(keys):
    if len(keys) == 0:
        return 1, 1
    else:
        print(keys[-1])
        return int(keys[-1]), int(get_cache_repository().hget(FACTORIAL_REDIS_KEY_PREFIX, keys[-1]))


def get_nearest_idx_from_cache(number, cache_name):
    cache_repo = get_cache_repository()
    filtered_keys = get_filtered_keys(number, cache_repo.hkeys(cache_name, natural_sort=True))
    if cache_name == FIBONACCI_REDIS_KEY_PREFIX:
        return get_last_two_numbers(list(filtered_keys))
    elif cache_name == FACTORIAL_REDIS_KEY_PREFIX:
        return get_last_number(list(filtered_keys))
    else:
        return


def get_nth_fibonacci(number):
    cacheRepo = get_cache_repository()
    cachedResult = cacheRepo.hget(FIBONACCI_REDIS_KEY_PREFIX, number)

    if cachedResult:
        return cachedResult

    nearest_keys = get_nearest_idx_from_cache(number, FIBONACCI_REDIS_KEY_PREFIX)

    if nearest_keys:
        first = int(cacheRepo.hget(FIBONACCI_REDIS_KEY_PREFIX, nearest_keys[0]))
        second = int(cacheRepo.hget(FIBONACCI_REDIS_KEY_PREFIX, nearest_keys[1]))
        last_two = [first, second]
        counter = int(nearest_keys[1]) + 1
    else:
        last_two = [0, 1]
        counter = 3
    if return_infinity(counter, number, FIBONACCI_REDIS_KEY_PREFIX):
        return 'infinity'

    while counter <= number:
        next_fib = last_two[0] + last_two[1]
        last_two[0] = last_two[1]
        last_two[1] = next_fib
        cacheRepo.hset(FIBONACCI_REDIS_KEY_PREFIX, counter, last_two[1])
        counter += 1

    if number > 1:
        return last_two[1]
    else:
        return last_two[0]


def get_nth_factorial(number):
    if number == 0:
        return 0
    cache_repo = get_cache_repository()
    cache_result = cache_repo.hget(FACTORIAL_REDIS_KEY_PREFIX, number)
    if cache_result:
        return int(cache_result)
    if number == 0 or number == 1:
        cache_repo.hset(FACTORIAL_REDIS_KEY_PREFIX, number, 1)
        return 1
    else:
        start_idx, fact = get_nearest_idx_from_cache(number, FACTORIAL_REDIS_KEY_PREFIX)
        if return_infinity(start_idx, number, FACTORIAL_REDIS_KEY_PREFIX):
            return 'infinity'

        for idx in range(start_idx + 1, number + 1):
            fact *= idx
            cache_repo.hset(FACTORIAL_REDIS_KEY_PREFIX, idx, fact)
        return fact


def handle_fibonacci(number):
    return get_nth_fibonacci(number)


def handle_ackermann(number):
    pass


def get_factorial(number):
    cache_repo = get_cache_repository()
    cache_result = cache_repo.hget(FACTORIAL_REDIS_KEY_PREFIX, number)
    if cache_result:
        return int(cache_result)
    if number == 0 or number == 1:
        cache_repo.hset(FACTORIAL_REDIS_KEY_PREFIX, number, 1)
        return 1
    else:
        last_idx, factorialSoFar = get_nearest_idx_from_cache(number, FACTORIAL_REDIS_KEY_PREFIX)
        left = last_idx
        right = number
        fact = factorialSoFar
        while left <= right:
            if left == right:
                fact *= left
            else:
                fact *= left
                fact *= right
            left += 1
            right -= 1
    cache_repo.hset(FACTORIAL_REDIS_KEY_PREFIX, number, fact)
    return fact


def handle_factorial(number):
    return get_factorial(number)
