import time


def measure_time(func):
    """
    Compute the execution time of a function. Adds a result (the time) to the return of the function
    :param func:
    :return: time
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper
