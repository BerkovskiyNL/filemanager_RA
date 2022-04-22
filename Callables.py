from typing import Any, Callable, Iterable, List


# Декоратор, добавляющий отладочную информацию о вызове функции.
# Принимает оригинальную функцию, возвращает декорированную.
def debug(func: Callable) -> Callable:

    # создаём функцию-обёртку, которую потом и вернём
    def wrapper(*args, **kwargs):
        # внедряем вывод отладочной информации
        print(f'Call: {func} with {len(args) + len(kwargs)} args')

        # вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper


# обычная функция - Callable
def f_sum(a: float, b: float) -> float:
    return a + b

# λ-функция (анонимная однострочная функция) - Callable
l_sum = lambda a, b: a + b


class Sum(object):
    def __call__(self, a: float, b: float) -> float:
        return a + b

# объект класс с переопределённым методом __call__() - Callable
o_sum = Sum()


# Частично применяет функцию func (фиксируем первый аргумент как x, возвращаем функцию f(x0..xn-1) вместо f(x0..xn))
def partial_apply(x: Any, func: Callable) -> Callable:
    return lambda args, kwargs: func(x, *args, **kwargs)


# Callable c сохранением истории вызовов
class Sqr(object):
    def __init__(self):
        self.__calls_history = []

    @property
    def calls_history(self) -> List[str]:
        return self.__calls_history

    def __call__(self, x: float) -> float:
        result = x ** 2

        self.__calls_history.append(f'{x} ** 2 = {result}')

        return result


# Пример функции высшего порядка (может принимать и/или возвращает другие функции)
def for_each(iterable: Iterable, func):
    for value in iterable:
        func(value)

    return func


if __name__ == '__main__':
    sqr_with_history: Sqr = for_each(range(10), Sqr())
    print(sqr_with_history.calls_history)
