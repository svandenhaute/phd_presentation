import numpy as np

from manim import (
    Scene, Create, VGroup,
    Circle, Square, Text, SVGMobject, ImageMobject, Rectangle,
    FadeIn, Transform, FadeOut, Create, AnimationGroup, Succession, Write,
    WHITE, BLACK, ManimColor,
    DOWN, LEFT, RIGHT, UP, ORIGIN,
)
from manim_slides import Slide

from particles import create_circles, get_electron, get_nucleus, get_nucleus_text, \
    get_electron_text
from periodic_table import generate_periodic_table, get_element


TITLE_FONT_SIZE = 14
ANIMATION_RUNTIME = 0.2


class Title(Slide):

    def construct(self):
        title = ImageMobject('images/title_slide.png')
        self.add(title)
        self.wait()


class Particles(Slide):

    def construct(self):
        globe = SVGMobject('images/globe_color.svg')
        globe.scale(2)

        equal = Text(
            '=',
            font='Open Sans',
            font_size=60,
            fill_color=WHITE,
            fill_opacity=1.0,
        )

        width = 5
        height = 3.5
        rectangle = Rectangle(
            height=height,
            width=width,
            stroke_color=WHITE,
            stroke_opacity=1.0,
        )
        circles = create_circles(
            num_particles=30,
            width=width,
            height=height,
            scale=0.9,
            offset=(
                rectangle.get_x() - width / 2,
                rectangle.get_y() - height / 2,
            ),
        )
        box = VGroup(rectangle, *circles)
        VGroup(globe, equal, box).arrange(buff=1.0)
        # description = Text(
        #     '"a collection of atoms"',
        #     font='Noto Sans',
        #     font_size=40,
        #     fill_color=WHITE,
        #     fill_opacity=1.0,
        # )
        # description.next_to(rectangle, UP, buff=0.5)
        equation = VGroup(globe, equal, box)

        self.play(FadeIn(globe, run_time=0.5))
        self.play(Create(equal))
        self.play(Create(rectangle))
        animations = []
        for circle in circles:
            animations.append(FadeIn(circle))
        self.play(Succession(animations, run_time=2))
        self.next_slide()

        self.play(equation.animate.scale(0.6).shift(2 * UP))

        atom = circles[-1]
        self.play(
            atom.animate.move_to(ORIGIN + 3 * LEFT + 2 * DOWN).scale(3),
            run_time=0.6,
        )

        empty = Circle(
            fill_color=WHITE,
            stroke_color=WHITE,
            fill_opacity=0.0,
            stroke_opacity=1.0,
            stroke_width=2,
            radius=1.3,
        )
        empty.set_x(atom.get_x())
        empty.set_y(atom.get_y())
        self.play(Transform(atom, empty), run_time=0.5)

        nucleus = get_nucleus(empty.get_center())
        electrons = []
        radii = np.random.uniform(0.55, 1.1, size=(7,))
        for i, radius in enumerate(radii):
            location = empty.get_center()
            location[0] += np.cos(2 * np.pi * i / len(radii)) * radius
            location[1] += np.sin(2 * np.pi * i / len(radii)) * radius
            electron = get_electron(location)
            electrons.append(electron)
        for particle in [nucleus, *electrons]:
            self.play(FadeIn(particle, run_time=0.15))
        self.next_slide()

        nucleus_text = get_nucleus_text(
            empty.get_center() + 4 * RIGHT + 1.2 * UP,
            scale=1.3,
        )
        electron_text = get_electron_text(
            empty.get_center() + 4 * RIGHT + 1.2 * DOWN,
            scale=1.3,
        )
        self.play(Write(nucleus_text), run_time=0.2)
        self.play(Write(electron_text), run_time=0.2)


class PeriodicTable(Slide):

    def highlight(self, elements, boxes):
        animations = []
        for element in elements:
            symbol, square = boxes[element]
            box_size = square.side_length
            inv_symbol, inv_square = get_element(element, box_size, invert=True)
            inv_symbol.shift(square.get_center())
            inv_square.shift(square.get_center())
            animation = AnimationGroup(
                Transform(square, inv_square),
                Transform(symbol, inv_symbol),
            )
            animations.append(animation)
        return animations

    def unhighlight(self, elements, boxes):
        animations = []
        for element in elements:
            symbol, square = boxes[element]
            box_size = square.side_length
            inv_symbol, inv_square = get_element(element, box_size, invert=False)
            inv_symbol.shift(square.get_center())
            inv_square.shift(square.get_center())
            animation = AnimationGroup(
                Transform(square, inv_square),
                Transform(symbol, inv_symbol),
            )
            animations.append(animation)
        return animations

    def construct(self):
        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.5 * UP)
        self.play(Create(table), run_time=1)
        self.next_slide()

        run_time = 0.6

        highlights = self.highlight(['H', 'O'], boxes)
        ice = SVGMobject('images/ice_cubes.svg').center().shift(2.8 * DOWN)
        self.play(FadeIn(ice), *highlights, run_time=run_time)
        self.next_slide()

        unhighlights = self.unhighlight(['H', 'O'], boxes)
        highlights = self.highlight(['H', 'O', 'N', 'C'], boxes)
        covid = SVGMobject('images/covid.svg').center().shift(2.8 * DOWN)
        self.play(FadeOut(ice), *unhighlights, run_time=run_time)
        self.play(FadeIn(covid), *highlights, run_time=run_time)
        self.next_slide()

        unhighlights = self.unhighlight(['H', 'O', 'N', 'C'], boxes)
        highlights = self.highlight(['Si'], boxes)
        solar = SVGMobject('images/solar_panel.svg').center().shift(2.8 * DOWN)
        self.play(FadeOut(covid), *unhighlights, run_time=run_time)
        self.play(FadeIn(solar), *highlights, run_time=run_time)
        self.next_slide()


class Second(Slide):

    def construct(self):
        square = Square()
        square.rotate(np.pi / 4)
        square.arrange(DOWN)

        self.play(Create(square))
        self.next_slide()
