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
        self.explore_dual_numbers_1()
        self.finding_derivative_2()
        self.exercise_3()

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
        self.play(Transform(varepsilon, varepsilon_square_equals_0))
        self.wait(0.5)
        self.play(
            Transform(varepsilon, generalised_dual_number)
        )
        self.wait(1)
        self.play(FadeOut(varepsilon))
        self.wait(1)
        
        title_mul = Tex("Multiplication").to_corner(UL).scale(0.9)
        expr0 = MathTex(r"(3 + 4 \varepsilon)\cdot(2 + 1 \varepsilon)").scale(1.2)
        self.play(Write(title_mul), Write(expr0))

        expr1 = MathTex(
            r"(3 + 4 \varepsilon)\cdot(2 + 1 \varepsilon)",
            r"=",
            r"3\cdot 2",
            r"+",
            r"3\cdot 1\varepsilon",
            r"+",
            r"4\varepsilon\cdot 2",
            r"+",
            r"4\varepsilon\cdot 1\varepsilon",
        ).move_to(expr0)
        self.play(TransformMatchingTex(expr0, expr1, path_arc=0.2))
        self.wait(0.2)

        expr2 = MathTex(
            r"(3 + 4 \varepsilon)\cdot(2 + 1 \varepsilon)",
            r"=",
            r"6",
            r"+",
            r"3\varepsilon",
            r"+",
            r"8\varepsilon",
            r"+",
            r"4\varepsilon^2",
        ).move_to(expr1)
        self.play(TransformMatchingTex(expr1, expr2, path_arc=0.15))
        self.wait(0.2)

        expr3 = MathTex(
            r"(3 + 4 \varepsilon)\cdot(2 + 1 \varepsilon)",
            r"=",
            r"6",
            r"+",
            r"11\varepsilon",
            r"+",
            r"4\varepsilon^2",
        ).move_to(expr2)
        self.play(TransformMatchingTex(expr2, expr3, path_arc=0.1))
        self.wait(0.2)

        bad_term = expr3.get_part_by_tex(r"4\varepsilon^2")
        cross = Cross(bad_term, color=RED, stroke_width=8).scale(1.10)
        self.play(Create(cross))
        self.wait(0.2)

        expr4 = MathTex(
            r"(3 + 4 \varepsilon)\cdot(2 + 1 \varepsilon)",
            r"=",
            r"6 + 11\varepsilon",
        ).move_to(expr3)
        self.play(
            TransformMatchingTex(expr3, expr4, path_arc=0.1),
            FadeOut(cross)
        )
        self.wait(0.6)

        self.play(FadeOut(expr4), FadeOut(title_mul))
        title_div = Tex("Division").to_corner(UL).scale(0.9)
        div0 = MathTex(r"\frac{1}{a + b \varepsilon}").scale(1.2)
        self.play(Write(title_div), Write(div0))

        div1 = MathTex(
            r"\frac{1}{a + b \varepsilon}",
            r"=",
            r"\frac{1}{a + b \varepsilon}\cdot\frac{a - b \varepsilon}{a - b \varepsilon}",
        ).move_to(div0)
        self.play(TransformMatchingTex(div0, div1, path_arc=0.15))

        div2 = MathTex(
            r"\frac{1}{a + b \varepsilon}",
            r"=",
            r"\frac{a - b \varepsilon}{a^2 - (b \varepsilon)^2}",
        ).move_to(div1)
        self.play(TransformMatchingTex(div1, div2, path_arc=0.15))

        div3 = MathTex(
            r"\frac{1}{a + b \varepsilon}",
            r"=",
            r"\frac{a - b \varepsilon}{a^2}",
        ).move_to(div2)
        self.play(TransformMatchingTex(div2, div3, path_arc=0.12))

        note = Tex(r"valid only if $a\neq 0$").scale(0.8).next_to(div3, DOWN)
        self.play(FadeIn(note, shift=UP*0.2))

        bad_frac = MathTex(r"\frac{1}{b \varepsilon}").next_to(div3, DOWN, buff=1.1)
        self.play(Write(bad_frac))
        cross2 = Cross(bad_frac, color=RED, stroke_width=8).scale(1.05)
        self.play(Create(cross2))
        caption = Tex(r"cannot divide by $b\varepsilon$ (since $\varepsilon^2=0$)").scale(0.7)
        caption.next_to(bad_frac, DOWN, buff=0.25)
        self.play(FadeIn(caption, shift=UP*0.2))
        self.wait(1.2)
        self.play(
            FadeOut(title_div),
            FadeOut(div3),
            FadeOut(note),
            FadeOut(bad_frac),
            FadeOut(cross2),
            FadeOut(caption)
        )
        self.wait(2)


    def finding_derivative_2(self):
        d_def = MathTex(
            r"\mathbb{D} = \{ a + b \varepsilon \mid a, b \in \mathbb{R} \} = \{ \text{Dual numbers} \}"
        ).scale(0.9)
        self.play(Write(d_def))
        self.wait(0.6)
        self.play(FadeOut(d_def))

        f_real = MathTex(
            r"f : \mathbb{R} \to \mathbb{R}, \,", r"f(x) = x^2 + 3x + 5"
        ).to_edge(DOWN, buff=3.0)
        self.play(Write(f_real))

        f_dual = MathTex(
            r"f : \mathbb{D} \to \mathbb{D}, \,", r"f(u) = u^2 + 3u + 5"
        ).to_edge(UP, buff=3.0)
        self.play(Transform(f_real, f_dual))
        self.wait(0.3)

        self.play(
            FadeOut(f_real[0]),
            f_real[1].animate.move_to(ORIGIN)
        )
        self.wait(0.2)
        equation = f_real[1]

        f_input = MathTex(
            r"f(x + \varepsilon) = ", r"(x + \varepsilon)^2 + 3(x + \varepsilon) + 5"
        ).move_to(equation)
        self.play(Transform(equation, f_input, path_arc=0.2))
        self.wait(0.2)

        expand = MathTex(
            r"f(x + \varepsilon) = ", r"x^2 + 2x\varepsilon + \varepsilon^2 + 3x + 3\varepsilon + 5"
        ).move_to(f_input)
        self.play(Transform(equation, expand, path_arc=0.15))
        self.wait(0.2)

        group_terms = MathTex(
            r"f(x + \varepsilon) = ", r"(x^2 + 3x + 5) + (2x + 3)\cdot \varepsilon + \varepsilon^2"
        ).move_to(equation)
        self.play(Transform(equation, group_terms, path_arc=0.12))
        self.wait(0.2)

        simplified = MathTex(
            r"f(x + \varepsilon) =", r"(x^2 + 3x + 5) + (2x + 3)\cdot \varepsilon"
        ).move_to(group_terms)
        self.play(Transform(equation, simplified, path_arc=0.1))
        self.wait(0.3)

        final = MathTex(
            r"f(x + \varepsilon) =", r"f(x) + f^\prime(x)\,\varepsilon"
        ).move_to(simplified)
        self.play(Transform(equation, final, path_arc=0.12))
        self.wait(1.0)
        self.play(FadeOut(equation))
        self.wait(0.5)


    def exercise_3(self):
        exercise = VGroup(
            Tex(r"Exercise").scale(0.9).set_color(YELLOW),
            Tex(r"Show that for any polynomial"),
            MathTex(r"p(x) &= \sum_{i=0}^n a_i \, x^i"),
            Tex(r"We have that"),
            MathTex(r"p(x + \varepsilon) &= p(x) + p'(x)\,\varepsilon")
        ).arrange(DOWN).to_edge(UP)
        self.play(FadeIn(exercise, aligned_edge=LEFT, shift=DOWN))
        self.wait(4.0) 

        self.play(
            FadeOut(exercise)
        )
        proof_title = Tex("Proof").to_corner(UL).scale(0.9)
        self.play(Write(proof_title))

        s1 = MathTex(
            r"p(x + \varepsilon)", r"=", r"\sum_{i = 0}^n a_i\,(x + \varepsilon)^i"
        ).scale(1.0).to_edge(UP, buff=2.0)
        self.play(Write(s1))
        self.wait(0.25)

        s2 = MathTex(
            r"p(x + \varepsilon)", r"=",
            r"\sum_{i = 0}^n a_i \sum_{k = 0}^{i} \binom{i}{k} x^{\,i-k}\varepsilon^{k}"
        ).move_to(s1)
        self.play(TransformMatchingTex(s1, s2, path_arc=0.2))
        self.wait(0.25)

        note = Tex(r"$\varepsilon^2 = 0\ \Rightarrow\ k\ge 2 \text{ terms vanish}$").scale(0.7)
        note.next_to(s2, DOWN, buff=0.25)
        self.play(FadeIn(note, shift=UP*0.2))
        self.play(Circumscribe(s2, color=YELLOW, time_width=0.6))
        self.wait(0.2)

        s3 = MathTex(
            r"p(x + \varepsilon)", r"=",
            r"\sum_{i = 0}^n a_i \Big(x^i + i\,x^{\,i-1}\varepsilon\Big)"
        ).move_to(s2)
        self.play(TransformMatchingTex(s2, s3, path_arc=0.15), FadeOut(note))
        self.wait(0.25)

        s4 = MathTex(
            r"p(x + \varepsilon)", r"=",
            r"\sum_{i=0}^n a_i x^i",
            r"+",
            r"\varepsilon \sum_{i=0}^n i\,a_i\,x^{\,i-1}"
        ).move_to(s3)
        self.play(TransformMatchingTex(s3, s4, path_arc=0.12))
        self.wait(0.25)

        s5 = MathTex(
            r"p(x+\varepsilon)", r"=", r"p(x)", r"+", r"p'(x)\,\varepsilon"
        ).move_to(s4)
        self.play(TransformMatchingTex(s4, s5, path_arc=0.12))
        self.play(Indicate(s5[-3], color=BLUE), Indicate(s5[-1], color=BLUE))
        self.wait(0.8)

        qedsym = MathTex(r"\square").scale(0.9).next_to(s5, RIGHT, buff=0.3)
        self.play(FadeIn(qedsym, shift=RIGHT*0.2))
        self.wait(0.8)
        self.play(FadeOut(s5), FadeOut(proof_title), FadeOut(qedsym))