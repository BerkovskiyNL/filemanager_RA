import re
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from collections import deque
from typing import Sequence, Tuple


class PingParser(object):
    __pattern = r'^64 bytes from (.*): icmp_seq=(\d+) ttl=\d+ time=(\d+.\d) ms$'
    __results = deque(maxlen=50)

    host = str()

    @classmethod
    def parse(cls) -> Sequence[Tuple[int, float]]:
        while True:
            line = sys.stdin.readline()
            sys.stdout.write(line)

            match = re.search(cls.__pattern, line.strip())

            if match:
                cls.host = match.group(1)

                package = int(match.group(2))
                time = float(match.group(3))
                cls.__results.append((package, time))

                return cls.__results


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)


    def animate(_):
        xs = []
        ys = []

        data = PingParser.parse()

        for x, y in data:
            xs.append(x)
            ys.append(y)

        ax.clear()
        ax.plot(xs, ys)

        plt.title(PingParser.host)
        plt.xlabel('Package')
        plt.ylabel('Time (ms)')

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
