from manim import *
import math

class DerivativesScene(Scene):
    """
    Shows that the derivative equals the slope of the tangent line at a point.
    - Blue: original function f(x)
    - Orange: tangent line at x0
    - Yellow dot: point (x0, f(x0)) moving along the curve
    - Green: derivative curve f'(x) (numerically approximated)
    - Green dot: (x0, f'(x0))
    """

    def construct(self):
        self.derivative_showcase_0()
        # self.explore_dual_numbers_1()

    def derivative_showcase_0(self):
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-3, 3, 1],
            x_length=12,
            y_length=6,
            tips=False,
        ).to_edge(DOWN)

        x_label = axes.get_x_axis_label(MathTex("x").scale(0.8))
        y_label = axes.get_y_axis_label(MathTex("y").scale(0.8))

        x_min, x_max = -6, 6 # maximum and minimum values of x on axis
        delta = 0.6 # delta such that you're actually on the axes

        # The function
        def g(x: float) -> float:
            return 0.25 * x ** 3 - x + 1
        
        # Scaled version to look nicer
        def f(x: float) -> float:
            return g(x / 2)

        graph = axes.plot(f, x_range=[x_min + delta / 2, x_max - delta / 2], color=BLUE)

        self.play(
            Create(axes),
            FadeIn(x_label, y_label)
        )
        self.play(Create(graph))

        x0 = ValueTracker(x_min + delta)

        # Numerical derivative (central difference)
        def fprime_numeric(x: float, h: float = 1e-10) -> float:
            return (f(x + h) - f(x - h)) / (2 * h)

        dot = always_redraw(
            lambda: Dot(axes.c2p(x0.get_value(), f(x0.get_value())), color=YELLOW)
        )

        # This is the tangent line area
        def tangent_line_mobject():
            x_ = x0.get_value()
            m = fprime_numeric(x_)
            y_ = f(x_)
            x_delta = 1 / math.sqrt(1 + m ** 2)
            xa, xb = x_ - x_delta, x_ + x_delta
            p1 = axes.c2p(xa, y_ - m * x_delta)
            p2 = axes.c2p(xb, y_ + m * x_delta)
            return Line(p1, p2, color=ORANGE, stroke_width=6)

        tangent_line = always_redraw(tangent_line_mobject)

        # This is doing the shit on the top left
        slope_value = DecimalNumber(0, num_decimal_places=2)
        slope_label = VGroup(MathTex("f'(x_0)=").scale(0.9), slope_value).arrange(RIGHT, buff = 0.1)
        slope_label.add_updater(lambda m: m.to_corner(UL).to_corner(UL).shift(RIGHT*0.4 + DOWN*0.3))
        slope_value.add_updater(lambda d: d.set_value(fprime_numeric(x0.get_value())))
        
        self.play(
            FadeIn(tangent_line), 
            FadeIn(dot), 
            FadeIn(slope_label)
        )

        self.play(x0.animate.set_value(x_max - delta), 
                    run_time=6, 
                    rate_func=
                        lambda t: 
                            0.5 - 0.5 * math.cos(2 * PI * t) 
                                if t < 1 / 2 
                                else 0.75 - 0.25 * math.cos(2 * PI * t)
                    )
        self.play(
            FadeOut(tangent_line),
            FadeOut(dot), 
            FadeOut(slope_label),
            FadeOut(graph),
            FadeOut(axes),
            FadeOut(x_label, y_label)
        )
        self.wait(1)
    
    def explore_dual_numbers_1(self):
        varepsilon: MathTex = MathTex(r"\varepsilon")
        varepsilon_squared: MathTex = MathTex(r"\varepsilon^2")
        varepsilon_square_equals_0: MathTex = MathTex(r"\varepsilon^2 = 0")
        generalised_dual_number: MathTex = MathTex(r"a + b \cdot \varepsilon")

        self.play(
            FadeIn(varepsilon)
        )
        self.play(
            Transform(varepsilon, varepsilon_squared)
        )
        self.play(Transform(varepsilon_squared, varepsilon_square_equals_0))
        self.wait(0.5)
        self.play(
            Transform(varepsilon_square_equals_0, generalised_dual_number)
        )

