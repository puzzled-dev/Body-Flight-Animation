import csv
import sys

import colorama
import numpy as np
from manimlib import *

colorama.init(autoreset=True)
g = 9.80665


def read_data(filename):
    try:
        with open(filename, mode="r", encoding="utf-8") as input_file:
            data = list(csv.reader(input_file, delimiter=";"))[0]
            data = [int(elem) for elem in data]
        return data
    except FileNotFoundError:
        print(colorama.Fore.RED + "ERROR: No ", end="")
        print(colorama.Fore.CYAN + f"{filename} ", end="")
        print(colorama.Fore.RED + "found")
        sys.exit(0)


data = read_data("data.csv")


class FlyingBodySimulation(Scene):
    def construct(self):
        global data

        h, a, v = data
        a *= np.pi / 180

        max_l = ((np.sin(a) + np.sqrt(np.sin(a) ** 2 + (2 * g * h) /
                                      (v ** 2))) * v ** 2 * np.cos(a)) / g

        max_h = (v ** 2 * np.sin(a) ** 2) / (2 * g) + h

        tau = (v * np.sin(a) + np.sqrt(v ** 2 * np.sin(a) ** 2 + 2 * g * h)) / g

        axes = Axes((-1, max_l + 1), (-1, max_h + 1))
        axes.add_coordinate_labels(
            font_size=15,
        )
        self.add(axes)

        parabola_graph = axes.get_graph(
            lambda x: (-g / (2 * v ** 2 * np.cos(a) ** 2) * x ** 2 + np.tan(
                a) * x + h) if 0 <= x <= max_l else -100,
            discontinuities=[0, max_l],
            color=BLUE
        )

        self.play(ShowCreation(parabola_graph), run_time=3)

        function = Tex("-{g \\over 2v_0^2\\cos^2\\alpha} \\cdot x^2 + \\tan\\alpha\\cdot x + h_0",
                       font_size=30, isolate=["x"])
        function.set_color_by_tex_to_color_map(
            {"x": ORANGE,
             "-{g \\over 2v_0^2\\cos^2\\alpha}": BLUE,
             "\\tan\\alpha": TEAL,
             "h_0": GREEN
             }
        )
        function.move_to(3.2 * UP)
        self.play(Write(function), run_time=2)

        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(0, parabola_graph))
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))
        self.play(FadeIn(dot, scale=.5), ShowCreation(h_line), ShowCreation(v_line))
        x_tracker = ValueTracker(0)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola_graph)
        )
        self.play(x_tracker.animate.set_value(max_l), run_time=tau)
        self.play(FadeOut(h_line), FadeOut(v_line), run_time=0)

        self.wait()

        self.play(FadeOut(function), FadeOut(dot), FadeOut(parabola_graph), FadeOut(axes))
        sys.exit(0)

