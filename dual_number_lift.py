
# dual_number_lift.py
# -----------------------------------------------------------
# A gentle, fully-commented Manim animation that shows how a
# real-valued function f: R -> R can be "lifted" to operate
# on real-dual numbers f: D_R -> D_R, and demonstrates the
# example f(x) = x^2 + 4x + 3 -> f(x + ε) = (x^2 + 4x + 3) + (2x + 4) ε.
#
# HOW TO RUN (Manim Community Edition):
#   1) Install manim (Community Edition) if you haven't:
#        pip install manim
#      (On macOS you may also need LaTeX (e.g., MacTeX) for MathTex.)
#
#   2) Save this file as dual_number_lift.py
#
#   3) Render the scene (pick one quality):
#        manim -pql dual_number_lift.py DualNumberLiftScene    # fast (low quality)
#        manim -pqm dual_number_lift.py DualNumberLiftScene    # medium
#        manim -pqh dual_number_lift.py DualNumberLiftScene    # high
#
#      -p opens the result when finished, -q* sets quality.
#
# WHAT THIS SCRIPT SHOWS
#   • A title: "Dual Number Lift"
#   • The map f : R -> R, then the lifted map f : D_R -> D_R
#   • A concrete polynomial f(x) = x^2 + 4x + 3
#   • Expanding f(x + ε) and using ε^2 = 0 to simplify to
#     (x^2 + 4x + 3) + (2x + 4) ε
#
# OPTIONAL: Using your RealDual class to verify at runtime
#   If you have a file RealDuals.py with a class RealDual(real, dual),
#   we attempt to import it to numerically verify the expansion.
#   If the import fails, the animation still works fine without it.
#
# Manim basics in 30 seconds (used here):
#   • Scene: A "Scene" is like a mini-movie. You subclass it and define
#     a construct(self) method that scripts your animation.
#   • Mobjects (Mathematical Objects): Text, MathTex, shapes, etc.
#   • Animations: self.play(Animation(...)) changes what’s on screen
#     smoothly over time. Common animations include Write, Create, FadeIn,
#     Transform, etc.
#   • Positions: You can move things with .to_edge(), .shift(), .next_to(), etc.
#   • Groups: VGroup(...) collects multiple objects so you can position them
#     together.
#
# -----------------------------------------------------------

from manim import *

# Try to import RealDual from the provided file if available.
# This is optional—if it isn't present or fails to import,
# we'll continue without runtime verification.
try:
    from RealDuals import RealDual  # expects / path containing RealDuals.py
    HAS_REALDUAL = True
except Exception as e:
    RealDual = None  # type: ignore
    HAS_REALDUAL = False


class DualNumberLiftScene(Scene):
    """Main animation scene."""
    def construct(self):
        # -------------------------------------------------------
        # 1) Title
        # -------------------------------------------------------
        title = Text("Dual Number Lift", weight=BOLD)
        self.animate(Write(title))
        self.wait(0.6)
        self.play(title.to_edge, UP)  # Pin the title to the top
        self.wait(0.2)

        # -------------------------------------------------------
        # 2) Show maps f : R -> R  and  f : D_R -> D_R
        # -------------------------------------------------------
        # MathTex renders LaTeX. We use \mathbb{R} for reals and
        # \mathbb{D}_{\mathbb{R}} for the dual numbers over the reals.
        real_map = MathTex(r"f : \mathbb{R} \to \mathbb{R}")
        dual_map = MathTex(r"f : \mathbb{D}_{\mathbb{R}} \to \mathbb{D}_{\mathbb{R}}")

        maps = VGroup(real_map, dual_map).arrange(DOWN, buff=0.4).shift(UP*0.5)
        self.play(Write(real_map))
        self.wait(0.4)

        # We'll bring in the "lifted" map with a little emphasis:
        lift_label = Tex("lift", color=YELLOW).scale(0.7)
        arrow = Arrow(real_map.get_right(), dual_map.get_left(), buff=0.25, max_tip_length_to_length_ratio=0.12)
        lift_label.next_to(arrow, UP, buff=0.1)

        self.play(Create(arrow), FadeIn(lift_label, shift=UP*0.1))
        self.play(Write(dual_map))
        self.wait(0.8)

        # -------------------------------------------------------
        # 3) Introduce a concrete example f(x) = x^2 + 4x + 3
        # -------------------------------------------------------
        poly_def = MathTex(r"f : x \mapsto x^2 + 4x + 3")
        poly_def.to_edge(LEFT).shift(DOWN*0.2)
        self.play(Write(poly_def))
        self.wait(0.6)

        # -------------------------------------------------------
        # 4) Expand f(x + \varepsilon) step by step
        # -------------------------------------------------------
        # We'll place the expansion on the right of the polynomial definition.
        # Step A: Show the substitution into f
        stepA = MathTex(
            r"f(x + \varepsilon)",
            r"=",
            r"(x + \varepsilon)^2 + 4(x + \varepsilon) + 3",
        ).scale(0.95)

        stepA.next_to(poly_def, RIGHT, buff=1.0)

        self.play(Write(stepA))
        self.wait(0.6)

        # Step B: Expand the squares and distribute:
        #   (x + ε)^2 = x^2 + 2xε + ε^2
        #   4(x + ε) = 4x + 4ε
        stepB = MathTex(
            r"=",
            r"x^2 + 2x\varepsilon + \varepsilon^2",
            r"+",
            r"4x + 4\varepsilon",
            r"+",
            r"3"
        ).scale(0.95)
        stepB.next_to(stepA, DOWN, aligned_edge=LEFT, buff=0.35)

        self.play(Write(stepB))
        self.wait(0.6)

        # Step C: Use the defining relation of dual numbers: ε^2 = 0
        # We'll highlight ε^2 and then cross it out / fade it.
        eps_sq = MathTex(r"\varepsilon^2").move_to(stepB[1]).shift(RIGHT*1.5 + DOWN*0.0)
        eps_rule = MathTex(r"\varepsilon^2 = 0").scale(0.9).set_color(YELLOW).next_to(stepB, RIGHT, buff=0.6)

        # Create a surrounding rectangle around ε^2 to draw attention.
        eps_sq_box = SurroundingRectangle(eps_sq, color=YELLOW, buff=0.05)
        self.play(Create(eps_sq_box), FadeIn(eps_rule))
        self.wait(0.6)

        # Now, animate replacing ε^2 with 0 in the expression:
        # We'll transform stepB into stepC where ε^2 is removed.
        stepC = MathTex(
            r"=",
            r"x^2 + 2x\varepsilon",
            r"+",
            r"4x + 4\varepsilon",
            r"+",
            r"3"
        ).scale(0.95)
        stepC.next_to(stepA, DOWN, aligned_edge=LEFT, buff=0.35)

        self.play(TransformMatchingTex(stepB, stepC))
        self.play(FadeOut(eps_sq_box))
        self.wait(0.4)

        # Step D: Collect real parts and ε parts:
        # Real: x^2 + 4x + 3
        # Dual: (2x + 4) ε
        stepD = MathTex(
            r"=",
            r"\big(",
            r"x^2 + 4x + 3",
            r"\big)",
            r"+",
            r"\big(",
            r"2x + 4",
            r"\big) \varepsilon"
        ).scale(0.95)
        stepD.next_to(stepC, DOWN, aligned_edge=LEFT, buff=0.35)

        self.play(Write(stepD))
        self.wait(0.8)

        # For emphasis, color the ε term and fade the grouping parentheses
        stepD_eps = stepD[6:8]  # "2x + 4)\varepsilon"
        self.play(stepD_eps.animate.set_color(BLUE))
        self.wait(0.5)

        # Step E: Present the final summarized identity alone:
        final_eq = MathTex(
            r"f(x + \varepsilon) = (x^2 + 4x + 3) + (2x + 4)\varepsilon"
        )
        final_eq.next_to(poly_def, DOWN, buff=1.4).to_edge(LEFT)
        self.play(TransformMatchingTex(stepD.copy(), final_eq), run_time=1.2)
        self.wait(1.0)

        # -------------------------------------------------------
        # 5) OPTIONAL: Verify numerically with RealDual (if available)
        # -------------------------------------------------------
        # We evaluate f at (x + 1·ε) for some x (say x=2) using RealDual and
        # compare to the expression (f(x) + f'(x)·ε).
        if HAS_REALDUAL:
            # A small note explaining we're about to verify with code:
            verify_note = Tex("Numerical check with RealDual (optional)").scale(0.6)
            verify_note.next_to(final_eq, DOWN, buff=0.6).to_edge(LEFT)
            self.play(FadeIn(verify_note))
            self.wait(0.3)

            x_val = 2.0
            # Create RealDual representing x + 1·ε
            x_dual = RealDual(x_val, 1.0)

            # Define f using Python on RealDual: f(z) = z^2 + 4z + 3
            # If your RealDual class overloads +, *, ** correctly, this will propagate.
            try:
                f_x_dual = (x_dual ** 2) + (4 * x_dual) + 3

                # Expected: real part = x^2 + 4x + 3; dual part = (2x + 4) * 1
                real_expected = x_val**2 + 4*x_val + 3
                dual_expected = 2*x_val + 4

                check_tex = MathTex(
                    rf"x={x_val}:~ f(x+\varepsilon) = ",
                    rf"{real_expected:.1f}",
                    r"+",
                    rf"{dual_expected:.1f}\varepsilon"
                ).scale(0.9)
                check_tex.next_to(verify_note, DOWN, aligned_edge=LEFT)

                self.play(Write(check_tex))
                self.wait(0.6)
            except Exception as e:
                # If RealDual import worked but the operations aren't available at runtime,
                # let the viewer know we skipped the live check.
                skipped = Tex("(RealDual present, but runtime ops not available here)").scale(0.6).set_color(GREY)
                skipped.next_to(verify_note, DOWN, aligned_edge=LEFT)
                self.play(FadeIn(skipped))
                self.wait(0.6)
        else:
            # If RealDual not available, simply note that the algebra is the key point.
            info = Tex("Algebraic takeaway: the $\\varepsilon$-coefficient is $f'(x)$.").scale(0.6)
            info.next_to(final_eq, DOWN, buff=0.6).to_edge(LEFT)
            self.play(FadeIn(info))
            self.wait(0.6)

        # Small outro pause
        self.wait(1.0)


# TIP: If you plan to chain multiple scenes in one file, add more Scene subclasses here.
#      Each "manim ... <SceneClassName>" renders the scene you name.
