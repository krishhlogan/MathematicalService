import os
import logging
from .CacheManager import CacheRepository

FIBONACCI_REDIS_KEY_PREFIX = os.environ.get('FIBONACCI_REDIS_KEY_PREFIX')
ACKERMANN_REDIS_KEY_PREFIX = os.environ.get('ACKERMANN_REDIS_KEY_PREFIX')
FACTORIAL_REDIS_KEY_PREFIX = os.environ.get('FACTORIAL_REDIS_KEY_PREFIX')

INFINITY = 'infinity'

logger = logging.getLogger('django')


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
    elif cache_key == FACTORIAL_REDIS_KEY_PREFIX:
        infinity_limit = int(os.getenv('FACTORIAL_INFINITY_LIMIT'))
    else:
        infinity_limit_m = int(os.getenv('ACKERMANN_INFINITY_LIMIT_M'))
        infinity_limit_n = int(os.getenv('ACKERMANN_INFINITY_LIMIT_N'))
        if start > infinity_limit_m or end > infinity_limit_n:
            return True
        else:
            return False
    return True if end - start > infinity_limit else False


def get_last_two_numbers(keys):
    if len(keys) >= 2:
        return get_valid_cache_keys(keys)
    else:
        return []


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
        return int(cachedResult)

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
        logger.info(f"Input value: {number} is too large. Nearest fibonacci index is: {counter - 1}")
        return INFINITY

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


def get_last_number(keys):
    if len(keys) == 0:
        return 1, 1
    else:
        print(keys[-1])
        return int(keys[-1]), int(get_cache_repository().hget(FACTORIAL_REDIS_KEY_PREFIX, keys[-1]))


# def get_nth_factorial(number):
#     if number == 0:
#         return 0
#     cache_repo = get_cache_repository()
#     cache_result = cache_repo.hget(FACTORIAL_REDIS_KEY_PREFIX, number)
#     if cache_result:
#         return int(cache_result)
#     if number == 0 or number == 1:
#         cache_repo.hset(FACTORIAL_REDIS_KEY_PREFIX, number, 1)
#         return 1
#     else:
#         start_idx, fact = get_nearest_idx_from_cache(number, FACTORIAL_REDIS_KEY_PREFIX)
#         if return_infinity(start_idx, number, FACTORIAL_REDIS_KEY_PREFIX):
#             logger.info(f"Number: {number} too large to compute. Nearest factorial found is for number: ${start_idx}")
#             return INFINITY
#
#         for idx in range(start_idx + 1, number + 1):
#             fact *= idx
#             cache_repo.hset(FACTORIAL_REDIS_KEY_PREFIX, idx, fact)
#         return fact


def handle_fibonacci(number):
    return get_nth_fibonacci(number)


def get_non_starting_result(n, rows, cols, cache):
    r = rows - 1
    c = cache[rows][cols - 1]
    if r == 0:
        ans = c + 1
    elif c <= n:
        ans = cache[rows - 1][cache[rows][cols - 1]]
    else:
        ans = (c - n) * r + cache[r][n]
    return ans


def get_ackermann(m, n):
    cache_repo = get_cache_repository()
    cache_result = cache_repo.hget(ACKERMANN_REDIS_KEY_PREFIX, f"{m}-{n}")
    if cache_result:
        return int(cache_result)
    if return_infinity(m, n, ACKERMANN_REDIS_KEY_PREFIX):
        logger.info(f"Values(m={m},n={n}) passed are too large")
        return INFINITY
    cache = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for rows in range(m + 1):
        for cols in range(n + 1):
            if rows == 0:
                cache[rows][cols] = cols + 1
            elif cols == 0:
                cache[rows][cols] = cache[rows - 1][1]
            else:
                cache[rows][cols] = get_non_starting_result(n, rows, cols, cache)
    cache_repo.hset(ACKERMANN_REDIS_KEY_PREFIX, f"{m}-{n}", cache[m][n])
    return cache[m][n]


def handle_ackermann(m, n):
    return get_ackermann(m, n)


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
        if return_infinity(last_idx, number, FACTORIAL_REDIS_KEY_PREFIX):
            logger.info(f"Number: {number} too large to compute. Nearest factorial found is for number: ${last_idx}")
            return INFINITY

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
