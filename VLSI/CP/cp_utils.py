import json
import sys

import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm


CIRCUIT_LINE_RE = re.compile(r'[0-9]* [0-9]*')
WINDOW_WIDTH = 500


def dump_statistics(statistics, status, fp=sys.stdout):
    """Dump pretty printed statistics from minizinc results.statistics."""
    statistics = {**statistics, 'status': str(status)}

    # Make time serializable
    time_keys = 'flatTime', 'time', 'solveTime', 'initTime', 'optTime'
    for key in time_keys:
        if key in statistics:
            statistics[key] = str(statistics[key])

    json.dump(statistics, fp, indent=4)


def show(width, height, n, circuits):
    """Show a window containing visual representation of an instance."""
    circuits_ratio = height / width
    fig, ax = plt.subplots(figsize=(WINDOW_WIDTH / 100, (WINDOW_WIDTH * circuits_ratio) / 100))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')

    # Create a colormap
    colormap = cm.get_cmap('hsv', len(circuits)+1)

    for i, circuit in enumerate(circuits):
        c_x = circuit['x']
        c_y = circuit['y']
        c_w = circuit['w']
        c_h = circuit['h']
        color = colormap(i)
        rect = patches.Rectangle((c_x, c_y), c_w, c_h, linewidth=1, edgecolor=color, facecolor=color)
        ax.add_patch(rect)
        # Add label with the same color as the rectangle
        ax.text(c_x + c_w / 2, c_y + c_h / 2, str(i), color=color, ha='center', va='center')

    plt.show()


def parse(data: str) -> list[dict]:
    """Parse a string containing output data and return it structured."""
    lines = data.splitlines()

    width, height = map(int, lines[0].split(' '))
    n = lines[1]

    # Filter away incorrect circuit lines
    circuit_lines = filter(CIRCUIT_LINE_RE.match, lines[2:])

    circuit_values = (map(int, line.split(' ')) for line in circuit_lines)
    circuits = [dict(zip(('w', 'h', 'x', 'y'), val)) for val in circuit_values]

    return width, height, n, circuits


def visualize_solution(filename):
    with open(filename) as fin:
        w, h, n, circuits = parse(fin.read())

    print(f'width: {w}, height: {h}, circuits: {n}')
    show(w, h, n, circuits)

