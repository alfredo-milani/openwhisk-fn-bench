from typing import List
import time
import math


DEFAULT_NUMBER: int = 10000000

def dynamic_allocation(n: int):
    memory_list = []

    for i in range(0, n):
        memory_list.append(i)

def main(params: dict) -> dict:
    try:
        number: int = int(params["number"])
        if number <= 0:
            raise KeyError
    except (KeyError, ValueError):
        number: int = DEFAULT_NUMBER

    start = time.time()
    dynamic_allocation(number)
    end = time.time()

    response: dict = {
        "number": number,
        "execution_time_ms": round((end - start) * 1000, 5),
        "info": "memory_bound"
    }
    if params.get("$scheduler") is not None:
        response["$scheduler"] = params["$scheduler"]

    return response


# if __name__ == '__main__':
#     from json import dumps
#     import sys
#     print(dumps(main({
#       "number": sys.argv[1]
#     }), indent = 4))
# 
#     # print(dumps(main({}), indent = 4))
