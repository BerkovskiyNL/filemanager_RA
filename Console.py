import math

from typing import Tuple


def solve(a: float, b: float, c: float) -> Tuple[float, float] | float | None:
    d = b ** 2 - 4 * a * c

    return ((-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a),) \
        if (d > 0) else -b / (2 * a) if (d == 0) else None


if __name__ == '__main__':
    print(f'Solution: {solve(float(input("Enter a: ")), float(input("Enter b: ")), float(input("Enter c: ")))}')
