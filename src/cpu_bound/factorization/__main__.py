from typing import List
import time
import math


DEFAULT_NUMBER: int = 1234567891011

def factorize(n: int) -> List[int]:
	factors: list = []

	for i in range(1, math.floor(math.sqrt(n)) + 1):
		if n % i == 0:
			factors.append(i)
			if n / i != i:
				factors.append(int(n / i))

	factors.sort()

	return factors

def main(params: dict) -> dict:
    try:
        number: int = int(params["number"])
        if number <= 0:
        	raise KeyError
    except (KeyError, ValueError):
        number: int = DEFAULT_NUMBER

    start = time.time()
    factors: List[int] = factorize(number)
    end = time.time()

    response: dict = {
    	"number": number,
    	"factors": factors,
    	"execution_time_ms": round((end - start) * 1000, 5),
    	"info": "cpu_bound"
    }
    if params.get("$scheduler") is not None:
        response["$scheduler"] = params["$scheduler"]

    return response


# if __name__ == '__main__':
# 	from json import dumps
# 	import sys
# 	print(dumps(main({
# 		"number": sys.argv[1]
# 	}), indent = 4))
# 
# 	# print(dumps(main({}), indent = 4))
