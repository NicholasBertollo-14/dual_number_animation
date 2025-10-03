from manim import *

def main():
    pass

class StartingScene(Scene):
    def construct(self):
        # square: Square = Square(2, fill_color = GREEN, stroke_color = BLUE)
        # self.play(Write(square, rate_func = lambda x: x ** 5, run_time=2))
        # self.wait(1)
        # dual_numbers: MathTex = MathTex(r"f: \mathbb{R} \to \mathbb{R}, f(x) = x^2 + 3x - 2").to_edge(UL, buff = 1)
        # self.play(Write(dual_numbers, rate_func=lambda t: t ** 5, run_time = 10)) 

        title: Tex = Tex("My Name is Nicholas")
        mathematics: MathTex = MathTex(r"\int_{\mathbb{R}}e^{-x^2} dx = \sqrt{\pi}", substrings_to_isolate=[r"x"])
        VGroup(title, mathematics).arrange(DOWN)
        self.play(
            Write(title, rate_func=lambda t: linear(t) if t < 1/2 else sigmoid(t)),
            Write(mathematics, rate_func=linear, run_time=1)
        ) 
        self.wait()

        more_things: Tex = Tex("This is some text")
        more_things.to_corner(UP + LEFT, buff = 1)

        mathematics.generate_target()
        mathematics.target.scale(1.2)
        mathematics.target.to_edge(UR, buff = 1)
        self.play(
            Transform(title, more_things), 
            MoveToTarget(mathematics)
        )
        mathematics.target.set_color_by_tex("x", PURPLE_A)
        self.play(
            LaggedStart(
                MoveToTarget(mathematics),
                lag_ratio=2
            )
        )
        self.wait(0.5)

        grid: NumberPlane = NumberPlane().add_coordinates(None)
        grid.set_z_index(-10, family=True)
        self.play(
            Write(grid),
            FadeOut(title, mathematics)
        )

        circle: Circle = Circle(2, PURPLE)
        square: Square = Square(2).set_color_by_gradient([PURPLE_A, PURPLE_E])
        self.play(Write(circle))
        self.play(Transform(circle, square))

if __name__ == "__main__":
    main()
