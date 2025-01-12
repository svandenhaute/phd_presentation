import numpy as np

from manim import (
    Scene, Create, VGroup,
    Circle, Square, Text, SVGMobject, ImageMobject, Rectangle, CubicBezier, Tex,
    Line, Dot, NumberLine, ValueTracker, Vector, DashedLine, Arrow, StealthTip,
    RoundedRectangle,
    FadeIn, Transform, FadeOut, Create, AnimationGroup, Succession, Write, Uncreate,
    MoveToTarget, ReplacementTransform,
    WHITE, BLACK, ManimColor, BLUE, RED, GRAY,
    DOWN, LEFT, RIGHT, UP, ORIGIN,
)
from manim_slides import Slide

from particles import create_circles, get_electron, get_nucleus, get_nucleus_text, \
    get_electron_text, get_atom
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


class Masses(Slide):

    def construct(self):
        positions = 2 * np.array([
            [-0.1, 0.3, 0],
            [0.7, 0.5, 0],
            [-0.2, 0.7, 0],
            [0.94, 0.1, 0],
        ])
        positions += np.array([-4, 1.0, 0])
        left = get_atom(label='H').scale(0.8).move_to(positions[2])
        right = get_atom(label='H').scale(0.8).move_to(positions[3])
        self.play(FadeIn(left), FadeIn(right))
        self.next_slide()

        electrons = [get_electron().move_to(p) for p in positions[:2]]
        nuclei = [get_nucleus().move_to(p).scale(0.7) for p in positions[2:]]
        kwargs = dict(
            fill_color=WHITE,
            stroke_color=WHITE,
            fill_opacity=0.0,
            stroke_opacity=1.0,
            stroke_width=2,
            radius=1.1,
        )
        circles = [Circle(**kwargs).move_to(n.get_center()) for n in nuclei]
        left_ = VGroup(nuclei[0], electrons[0], circles[0])
        right_ = VGroup(nuclei[1], electrons[1], circles[1])
        self.play(
            ReplacementTransform(left, left_),
            ReplacementTransform(right, right_),
        )
        self.play(*[FadeOut(c) for c in circles])
        self.next_slide()

        lines = []
        cover = 0.5
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                a = positions[i]
                b = positions[j]
                line = DashedLine(
                    a + 0.2 * (b - a),
                    b - 0.2 * (b - a),
                    stroke_color=WHITE,
                    stroke_width=1.0,
                )
                lines.append(line)

        at = np.mean(positions, axis=0) + 5 * RIGHT + 0.4 * UP
        coulomb = Text(
            "electrostatics",
            font='Open Sans',
            font_size=250,
            fill_color=WHITE,
            fill_opacity=1.0,
            weight="BOLD",
        ).scale(0.1).move_to(at)
        tex = Tex(r"$E_{\text{\sffamily Coulomb}} \sim \frac{1}{r}$").next_to(coulomb, DOWN)

        animation = AnimationGroup(
            FadeIn(coulomb, run_time=0.5),
            Write(tex, run_time=0.5),
        )
        self.play(animation)
        self.play(Succession([FadeIn(l) for l in lines]), run_time=1)
        self.next_slide()

        axis_mobjects = []
        axis_size = 13
        axis = Arrow(
            start=np.array([-axis_size / 2, -2, 0]),
            end=np.array([axis_size / 2, -2, 0]),
            tip_shape=StealthTip,
            stroke_width=2.5,
            tip_length=0.2,
        )
        label = Text(
            "mass",
            font='Open Sans',
            font_size=200,
            fill_color=WHITE,
            fill_opacity=1.0,
            weight="BOLD",
        ).scale(0.1).move_to(axis.get_end()).shift(0.5 * DOWN)
        self.play(Create(axis), FadeIn(label))
        self.next_slide()
        axis_mobjects += [axis, label]

        tick_animations = []
        length = np.linalg.norm(axis.get_start() - axis.get_end())
        scale = 0.90 * length / 32
        dot = Dot(np.array([0, 0, 0]) + axis.get_start())
        label = Text(
            "1 g",
            font='Open Sans',
            font_size=200,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1)
        label.next_to(dot, 0.5 * UP)
        droplet = SVGMobject('images/droplet.svg').move_to(axis.get_start() + 0.5 * DOWN)
        droplet.scale(0.3)
        anim = AnimationGroup(
            FadeIn(dot),
            FadeIn(droplet),
            Write(label),
        )
        self.play(anim)
        self.next_slide()
        axis_mobjects += [dot, droplet, label]

        dot = Dot(np.array([scale * 4, 0, 0]) + axis.get_start())
        label = Text(
            "0.1 mg",
            font='Open Sans',
            font_size=200,
            fill_color=WHITE,
            fill_opacity=1.0,
            # weight="BOLD",
        ).scale(0.1)
        label.next_to(dot, 0.5 * UP)
        salt = SVGMobject('images/salt.svg').scale(0.3).move_to(dot.get_center() + 0.5 * DOWN)
        anim = AnimationGroup(
            FadeIn(dot),
            FadeIn(salt),
            Write(label),
        )
        self.play(anim)
        self.next_slide()
        axis_mobjects += [dot, salt, label]

        dot = Dot(np.array([scale * 15, 0, 0]) + axis.get_start())
        label = Text(
            "0.5 fg",
            font='Open Sans',
            font_size=200,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1)
        label.next_to(dot, 0.5 * UP)
        covid = SVGMobject('images/covid.svg').scale(0.3).move_to(dot.get_center() + 0.5 * DOWN)
        anim = AnimationGroup(
            FadeIn(dot),
            FadeIn(covid),
            Write(label),
        )
        self.play(anim)
        self.next_slide()
        axis_mobjects += [dot, covid, label]

        highlight = RoundedRectangle(
            color=WHITE,
            fill_opacity=1.0,
            stroke_opacity=1.0,
            height=0.10,
            width=scale * 2,  # 2 powers
            corner_radius=0.05,
        ).move_to(np.array([scale * 24, 0, 0]) + axis.get_start())
        label = Tex(r"$\text{\sffamily 10}^{\text{\sffamily -" + str(24) +
                            r" }}\text{\sffamily g}$").next_to(highlight, 0.5 * UP).scale(0.7).shift(0.12 * RIGHT)
        nucleus = get_nucleus().next_to(highlight, 0.5 *
                                                           DOWN).scale(0.9)
        anim = AnimationGroup(
            FadeIn(highlight),
            FadeIn(nucleus),
            Write(label),
        )
        self.play(anim)
        self.next_slide()
        axis_mobjects += [highlight, nucleus, label]

        dot = Dot(np.array([scale * 28, 0, 0]) + axis.get_start())
        label = Tex(r"$\text{\sffamily 10}^{\text{\sffamily -" + str(28) +
                            r" }}\text{\sffamily g}$").next_to(dot, 0.5 * UP).scale(0.7).shift(0.12 * RIGHT)
        label.next_to(dot, 0.5 * UP)
        electron = get_electron().next_to(dot, 0.5 * DOWN)
        anim = AnimationGroup(
            FadeIn(dot),
            FadeIn(electron),
            Write(label),
        )
        self.play(anim)
        self.next_slide()
        axis_mobjects += [dot, electron, label]

        color = ManimColor.from_rgba((119, 247, 170, 1.0))
        line = Line(
            start=np.array([26.3 * scale, 1, 0]) + axis.get_start(),
            end=np.array([26.3 * scale, -3.5, 0]) + axis.get_start(),
            stroke_color=color,
            stroke_width=10.0,
        )
        arrow_left = Arrow(
            start=line.get_center(),
            end=line.get_center() + 4 * LEFT,
            tip_shape=StealthTip,
            stroke_width=2.5,
            tip_length=0.2,
            stroke_color=GRAY,
        )
        text_left = Text(
            "high school physics",
            font='Open Sans',
            font_size=240,
            fill_color=GRAY,
            fill_opacity=1.0,
        ).scale(0.1).next_to(arrow_left, 0.5 * DOWN)

        arrow_right = Arrow(
            start=line.get_center(),
            end=line.get_center() + 4 * RIGHT,
            tip_shape=StealthTip,
            stroke_width=2.5,
            tip_length=0.2,
            stroke_color=color,
        )
        text_right = Text(
            "quantum mechanics",
            font='Open Sans',
            font_size=240,
            fill_color=color,
            fill_opacity=1.0,
            weight="BOLD",
        ).scale(0.1).next_to(arrow_right, 0.5 * DOWN)
        anim = Succession(
            Create(line),
            AnimationGroup(Create(arrow_left), Create(arrow_right)),
            run_time=1.0,
        )
        self.play(anim)
        self.next_slide()
        axis_mobjects += [arrow_left, arrow_right, line, text_left, text_right]

        self.play(FadeIn(text_left), FadeIn(text_right), run_time=0.9)
        self.next_slide()

        entire_axis = VGroup(*axis_mobjects)
        entire_hydrogen = VGroup(*(nuclei + electrons + lines))
        electrostatics = VGroup(coulomb, tex)
        # qm = Text(  # create schrodinger equation
        #     "quantum mechanics",
        #     font='Open Sans',
        #     font_size=250,
        #     fill_color=color,
        #     fill_opacity=1.0,
        #     weight="BOLD",
        # ).scale(0.1).move_to(at + 1.5 * RIGHT)
        raw_str = r"$$i \hbar \frac{\displaystyle \partial \psi}{\displaystyle \partial t} = \hat{H} \psi$$"
        qm_tex = Tex(raw_str).move_to(at + 1.5 * RIGHT + 0.5 * DOWN).set_color(color)
        self.play(
            entire_axis.animate.shift(3.5 * DOWN),
            entire_hydrogen.animate.shift(1.5 * LEFT),
            electrostatics.animate.shift(2.5 * LEFT).set_color(GRAY),
        )
        self.play(
            Write(qm_tex, run_time=0.7),
        )
        self.next_slide()
