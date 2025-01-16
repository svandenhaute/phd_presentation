from functools import partial

import numpy as np

from manim import (
    Scene, VGroup, DrawBorderThenFill, Circumscribe, Create, PI, Group,
    Circle, Square, Text, SVGMobject, ImageMobject, Rectangle, CubicBezier, Tex,
    Line, Dot, NumberLine, ValueTracker, Vector, DashedLine, Arrow, StealthTip,
    RoundedRectangle, MathTex, DecimalNumber, Axes, CurvedArrow, ThreeDAxes,
    Sphere, DashedVMobject,
    FadeIn, Transform, FadeOut, AnimationGroup, Succession, Write, Uncreate,
    MoveToTarget, ReplacementTransform, Wait, AddTextLetterByLetter,
    f_always, linear, always,
    WHITE, BLACK, ManimColor, BLUE, RED, GRAY,
    DOWN, LEFT, RIGHT, UP, ORIGIN,
)
from manim.utils.rate_functions import ease_in_out_expo
from manim_slides import Slide, ThreeDSlide

from particles import create_circles, get_electron, get_nucleus, get_nucleus_text, \
    get_electron_text, get_atom, ELECTRON_COLOR, NUCLEUS_COLOR, create_atom
from periodic_table import generate_periodic_table, get_element
from quantum import generate_hatch_pattern
from hydrogen import potential, harmonic


TITLE_FONT_SIZE = 14
ANIMATION_RUNTIME = 0.2
QM_COLOR = ManimColor.from_rgba((119, 247, 170, 1.0))
OXYGEN_COLOR = ManimColor.from_rgb((242, 94, 68))


class Title(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        title = ImageMobject('images/title_slide.png')
        self.add(title)
        self.wait()


class Particles(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
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
            num_particles=60,
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
        equation = VGroup(globe, equal, box).shift(2 * UP).scale(0.8)

        self.play(FadeIn(globe, run_time=0.5))
        self.play(Write(equal), DrawBorderThenFill(rectangle), run_time=0.5)
        animations = []
        for circle in circles:
            animations.append(FadeIn(circle))
        self.play(Succession(animations, run_time=1.0))
        self.next_slide()

        atom = create_atom(num_electrons=1, radius=1.0).scale(0.8)
        atom.shift(2 * DOWN + 4 * LEFT)
        detached = VGroup(*circles[-2:])

        nucleus_text = get_nucleus_text(
            scale=1.3,
        ).move_to(equation.get_center() + 4 * DOWN)
        electron_text = get_electron_text(
            scale=1.3,
        ).move_to(equation.get_center() + 4 * DOWN + 4 * RIGHT)
        self.play(Write(nucleus_text), run_time=0.2)
        self.play(Write(electron_text), run_time=0.2)
        self.next_slide()

        self.play(ReplacementTransform(detached, atom))
        self.next_slide()

        carbon = create_atom(8, 1.2).move_to(atom.get_center())
        self.play(ReplacementTransform(atom, carbon))
        self.next_slide()

        gold = create_atom(22, 1.8).move_to(atom.get_center())
        self.play(ReplacementTransform(carbon, gold))
        self.next_slide()


class PeriodicTable(Slide):

    def highlight(self, elements, boxes):
        self.wait_time_between_slides = 0.05
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
        self.wait_time_between_slides = 0.05
        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.3 * UP)
        self.play(Create(table), run_time=1)
        self.next_slide()

        run_time = 0.4

        highlights = self.highlight(['H', 'O'], boxes)
        ice = SVGMobject('images/ice_cubes.svg').center().shift(2.5 * DOWN)
        self.play(FadeIn(ice), *highlights, run_time=run_time)
        self.next_slide()

        unhighlights = self.unhighlight(['H', 'O'], boxes)
        highlights = self.highlight(['H', 'O', 'N', 'C'], boxes)
        covid = SVGMobject('images/covid.svg').center().shift(2.5 * DOWN)
        self.play(FadeOut(ice), *unhighlights, run_time=run_time)
        self.play(FadeIn(covid), *highlights, run_time=run_time)
        self.next_slide()

        unhighlights = self.unhighlight(['H', 'O', 'N', 'C'], boxes)
        highlights = self.highlight(['Si'], boxes)
        solar = SVGMobject('images/solar_panel.svg').center().shift(2.5 * DOWN)
        self.play(FadeOut(covid), *unhighlights, run_time=run_time)
        self.play(FadeIn(solar), *highlights, run_time=run_time)
        self.next_slide()

        unhighlights = self.unhighlight(['Si'], boxes)
        self.play(FadeOut(solar), *unhighlights, run_time=run_time)
        self.next_slide()

        physics = Text(
            'laws of physics?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        simulation = Text(
            'challenges?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        solution = Text(
            'solution?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        goals = VGroup(physics, simulation, solution).arrange(RIGHT, buff=2.5)
        goals.shift(2 * DOWN)
        self.play(Write(physics), run_time=0.5)
        self.next_slide()
        self.play(Write(simulation), run_time=0.5)
        self.next_slide()
        self.play(Write(solution), run_time=0.5)
        self.next_slide()


class Masses(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        positions = 2 * np.array([
            [-0.1, 0.3, 0],
            [0.7, 0.5, 0],
            [-0.2, 0.7, 0],
            [0.94, 0.1, 0],
        ])
        positions += np.array([-2, 1.0, 0])
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

        at = np.mean(positions, axis=0) + 4 * RIGHT + 0.4 * UP
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
        self.play(DrawBorderThenFill(axis), FadeIn(label))
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

        line = Line(
            start=np.array([26.3 * scale, 1, 0]) + axis.get_start(),
            end=np.array([26.3 * scale, -3.5, 0]) + axis.get_start(),
            stroke_color=QM_COLOR,
            stroke_width=10.0,
        )
        arrow_left = Arrow(
            start=line.get_center(),
            end=line.get_center() + 4 * LEFT,
            tip_shape=StealthTip,
            stroke_width=2.5,
            tip_length=0.1,
            stroke_color=GRAY,
        )
        text_left = Text(
            "classical physics",
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
            tip_length=0.1,
            stroke_color=QM_COLOR,
        )
        text_right = Text(
            "quantum mechanics",
            font='Open Sans',
            font_size=240,
            fill_color=QM_COLOR,
            fill_opacity=1.0,
            weight="BOLD",
        ).scale(0.1).next_to(arrow_right, 0.5 * DOWN)
        anim = Succession(
            DrawBorderThenFill(line),
            AnimationGroup(DrawBorderThenFill(arrow_left), DrawBorderThenFill(arrow_right)),
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
        qm_tex = Tex(raw_str).move_to(electrostatics.get_center()).set_color(QM_COLOR)
        self.play(
            # entire_axis.animate.shift(3.5 * DOWN),
            # entire_hydrogen.animate.shift(1.5 * LEFT),
            # electrostatics.animate.shift(2.5 * LEFT).set_color(GRAY),
            ReplacementTransform(electrostatics, qm_tex, run_time=0.7),
        )
        self.next_slide()

        hatch_lines = []
        for (start, end) in generate_hatch_pattern(4, 2.5, 40, 0.2):
            line = Line(
                np.array(start + (-1,)),
                np.array(end + (-1,)),
                stroke_width=2,
                stroke_color=ELECTRON_COLOR,
                z_index=0,
            )
            hatch_lines.append(line)
        hatch = VGroup(*hatch_lines)
        _nuclei = [get_nucleus().move_to(p).scale(0.7) for p in positions[2:]]
        _electrons = [get_electron().move_to(p) for p in positions[:2]]
        classical_hydrogen = VGroup(*(_nuclei + _electrons))
        classical_hydrogen.shift(2 * DOWN)
        hatch.move_to(classical_hydrogen.get_center())

        electrons_lines = VGroup(*_electrons)
        text_top = Text(
            "exact",
            font='Open Sans',
            font_size=240,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).move_to(entire_hydrogen.get_center() + 4 * LEFT)
        self.play(FadeIn(text_top))

        text_bottom = Text(
            "approximate",
            font='Open Sans',
            font_size=240,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).move_to(entire_hydrogen.get_center() + 2 * DOWN + 4 * LEFT)

        self.play(
            text_top.animate.shift(UP),
            entire_hydrogen.animate.shift(UP),
            qm_tex.animate.shift(UP),
            entire_axis.animate.scale(0.6),
            FadeIn(text_bottom),
        )
        self.next_slide()

        self.play(FadeIn(classical_hydrogen))
        for nucleus in _nuclei:
            nucleus.set_z_index(1)
        self.next_slide()

        raw_str = r"$$F = m a$$"
        classical_tex = Tex(raw_str).move_to(electrostatics.get_center()).set_color(WHITE)
        classical_tex.move_to(qm_tex.get_center() + 3 * DOWN)
        classical_tex[0][0].set_color(color=QM_COLOR)
        self.play(ReplacementTransform(electrons_lines, hatch))
        self.play(Write(classical_tex), run_time=0.7)
        # self.play(Circumscribe(classical_tex[0][:2], color=QM_COLOR))
        self.next_slide()


class Dynamics(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        equilibrium_distance = 1.5
        positions = np.array([
            [equilibrium_distance / 2, 0, 0],
            [-equilibrium_distance / 2, 0, 0],
        ])
        atoms = [get_atom('H').move_to(p).scale(0.7) for p in positions]
        for atom in atoms:
            atom.set_x_index(1)
        bond = Line(
            atoms[0].get_center(),
            atoms[1].get_center(),
            stroke_width=20,
            color=WHITE,
            z_index=0,
        )
        molecule = VGroup(bond, *atoms).shift(3 * UP)
        self.play(FadeIn(molecule), run_time=0.3)
        self.next_slide()

        time = ValueTracker(0)
        self.add(time)
        frequency = 119e12 * 1e-15  # period ~ 8 fs

        def separation():
            return equilibrium_distance + 0.35 * np.sin(2 * np.pi * frequency * time.get_value())

        distance = DecimalNumber(
            equilibrium_distance / 2 * 0.74,
            num_decimal_places=2,
        )
        unit = Text(
            "Å",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(distance, RIGHT, aligned_edge=DOWN)
        distance.add_updater(lambda x: x.set_value(separation() / equilibrium_distance * 0.74))
        d_label = VGroup(distance, unit)

        def oscillation(index, positive):
            if positive:
                direction = 1.0
            else:
                direction = -1.0
            return bond.get_center()[0] + separation() * direction / 2

        f_always(atoms[0].set_x, partial(oscillation, index=0, positive=True))
        f_always(atoms[1].set_x, partial(oscillation, index=1, positive=False))
        #self.play(time.animate.set_value(80), rate_func=linear, run_time=3)
        #self.next_slide()

        axes = Axes((0.0, 8), (-1, 1)).scale(0.7)
        xlabel = Text(
            "interatomic\n  distance",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_x_axis().get_end(), DOWN)
        ylabel = Text(
            "energy",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_y_axis().get_end(), LEFT)
        f = lambda x: potential(x / equilibrium_distance * 0.74)
        graph = axes.plot(
            f,
            color=QM_COLOR,
            x_range=[0.6, 7],
            stroke_width=5,
        ).set_z_index(0)
        graph_label = axes.get_graph_label(graph, 'E(r)')
        graph_label.next_to(graph.get_start(), RIGHT)

        self.play(AddTextLetterByLetter(axes.get_x_axis()), Write(xlabel, run_time=0.6))
        self.next_slide()

        def get_dot_x():
            return axes.c2p(separation(), 0)  # always on x-axis

        dot_x = Dot(ORIGIN, z_index=1).move_to(get_dot_x())
        f_always(dot_x.move_to, get_dot_x)
        # f_always(d_label.move_to, lambda: dot_x.get_center() + 0.5 * (UP + RIGHT))
        d_label.move_to(axes.c2p(equilibrium_distance + 1, 0.3))
        self.play(FadeIn(dot_x), FadeIn(d_label))
        self.next_slide()

        self.play(time.animate.set_value(27), rate_func=linear, run_time=2)
        self.next_slide()

        self.play(
            Write(axes.get_y_axis(), lag_ratio=0.01, run_time=0.5),
            Write(ylabel, run_time=0.6),
        )
        self.play(Create(graph, run_time=0.5), Write(graph_label, run_time=0.5))
        self.next_slide()

        def get_dot():
            s = separation()
            return axes.c2p(s, f(s))
        dot = Dot(z_index=1).move_to(get_dot())
        f_always(dot.move_to, get_dot)

        self.play(ReplacementTransform(dot_x, dot), run_time=0.5)
        self.next_slide()

        force = Arrow(
            ORIGIN,
            LEFT,
            z_index=3,
            max_stroke_width_to_length_ratio=200,
            max_tip_length_to_length_ratio=0.5,
            stroke_width=5,
            color=NUCLEUS_COLOR,
        )
        force.put_start_and_end_on(
            dot.get_center(),
            dot.get_center() + 0.5 * DOWN + 0.5 * LEFT,
        )
        self.play(Write(force), run_time=0.3)
        self.next_slide()

        force_ = force.copy()
        self.add(force_)
        anim0 = Transform(
            force,
            force.copy().put_start_and_end_on(
                atoms[0].get_center() + 0.5 * DOWN,
                atoms[0].get_center() + 0.5 * DOWN + LEFT / np.sqrt(2),
            )
        )
        anim1 = Transform(
            force_,
            force_.copy().put_start_and_end_on(
                atoms[1].get_center() + 0.5 * DOWN,
                atoms[1].get_center() + 0.5 * DOWN + RIGHT / np.sqrt(2),
            )
        )
        self.play(anim0, anim1)
        self.next_slide()

        self.play(Uncreate(force_), Uncreate(force), run_time=0.1)
        self.play(time.animate.set_value(54), run_time=6, rate_func=linear)
        self.next_slide()


class OverviewPhysics(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05

        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.3 * UP)
        self.play(Create(table), run_time=1)

        physics = Text(
            'laws of physics?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        simulation = Text(
            'challenges?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        solution = Text(
            'solution?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        goals = VGroup(physics, simulation, solution).arrange(
            RIGHT,
            buff=2.5,
            aligned_edge=UP,
        )
        goals.shift(2 * DOWN)
        self.play(AddTextLetterByLetter(physics), run_time=0.5)
        self.play(AddTextLetterByLetter(simulation), run_time=0.5)
        self.play(AddTextLetterByLetter(solution), run_time=0.5)
        self.next_slide()

        nuclei = Text(
            'classical (nuclei)',
            font='Open Sans',
            font_size=250,
            color=NUCLEUS_COLOR,
        ).scale(0.1)
        electrons = Text(
            'quantum (electrons)',
            font='Open Sans',
            font_size=250,
            color=QM_COLOR,
        ).scale(0.1)
        laws = VGroup(nuclei, electrons).arrange(
            DOWN,
            buff=0.2,
            # aligned_edge=LEFT,
        ).next_to(physics, DOWN)
        self.play(FadeIn(laws), run_time=0.4)
        self.next_slide()

        # newton = Tex(r"$F=ma$", color=WHITE)
        # newton[0][0].set_color(QM_COLOR)
        # evaluations = Text(
        #     '# evaluations',
        #     font='Open Sans',
        #     font_size=250,
        #     color=WHITE,
        # ).scale(0.1)
        # challenges = VGroup(newton, evaluations).arrange(
        #     DOWN,
        #     buff=0.2,
        # ).next_to(simulation, DOWN)
        # self.play(FadeIn(challenges))
        # self.next_slide()


class TimeEvolution(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        frequency = 119e12 * 1e-15  # period ~ 8 fs
        time_offset = 2

        def distance(t):
            return 0.74 + 0.35 * np.sin(2 * np.pi * frequency * (t - time_offset))

        axes = Axes(
            (0.0, 16), (0, 1.5),
            y_axis_config={'include_ticks': False},
        ).scale(0.7).shift(UP)
        graph = axes.plot(
            distance,
            color=WHITE,
            x_range=[0, 16],
        ).set_z_index(0)
        mean = axes.plot(
            lambda x: 0.74,
            color=WHITE,
            stroke_width=2,
        )
        mean = DashedVMobject(mean, dashed_ratio=0.3, num_dashes=60)
        ylabel = Text(
            "interatomic\n  distance",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_y_axis().get_end(), LEFT)
        xlabel = Text(
            "time",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_x_axis().get_end(), DOWN)
        tick = Text(
            "0.74 Å",
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).move_to(axes.c2p(0, 0.74) + LEFT)

        self.play(Write(axes), run_time=0.4)
        self.play(AddTextLetterByLetter(xlabel), Write(ylabel), run_time=0.4)
        self.next_slide()

        self.play(Write(graph))
        self.play(Write(mean, run_time=0.5), Write(tick, run_time=0.5))
        self.next_slide()

        dt = 1.0
        dots = []
        molecules = []
        for i in range(17):
            dot = Dot(
                axes.c2p(i * dt, distance(i * dt)),
                color=NUCLEUS_COLOR,
                radius=0.1,
            )
            dots.append(dot)

            # offset = np.array([0, 0, 0])
            d = 1.0 * distance(i * dt)
            atoms = [
                get_atom('H').scale(0.7).move_to(np.array([+d, 0, 0])),
                get_atom('H').scale(0.7).move_to(np.array([-d, 0, 0])),
            ]
            for atom in atoms:
                atom.set_z_index(1)
            bond = Line(
                atoms[0].get_center(),
                atoms[1].get_center(),
                stroke_width=20,
                color=WHITE,
                z_index=0,
            )
            mol = VGroup(bond, *atoms).shift(3 * UP + 3 * RIGHT)
            molecules.append(mol)

        self.play(
            Create(dots[0], run_time=0.1),
            FadeIn(molecules[0], run_time=0.1),
        )
        self.next_slide()
        self.play(
            Create(dots[1], run_time=0.1),
            ReplacementTransform(molecules[0], molecules[1], run_time=0.1),
        )
        self.next_slide()
        for i in range(2, 6):
            self.play(
                Create(dots[i], run_time=0.1),
                ReplacementTransform(molecules[i - 1], molecules[i], run_time=0.1),
            )
            self.next_slide()

        for i in range(6, 17):
            self.play(
                Create(dots[i], run_time=0.1),
                ReplacementTransform(molecules[i - 1], molecules[i], run_time=0.1),
            )
        self.next_slide()

        md = Text(
            "molecular dynamics",
            font='Open Sans',
            font_size=300,
            fill_color=NUCLEUS_COLOR,
            fill_opacity=1.0,
            weight="BOLD",
        ).scale(0.1).next_to(molecules[-1], 1.5 * LEFT)
        self.play(AddTextLetterByLetter(md, run_time=0.5))
        self.next_slide()

        cost = Text(
            "computational cost?",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
            weight="BOLD",
        ).scale(0.1)
        steps = Text(
            "(# steps)  x  (cost/step)",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1)
        # per_step = Text(
        #     "cost per step",
        #     font='Open Sans',
        #     font_size=300,
        #     fill_color=WHITE,
        #     fill_opacity=1.0,
        # ).scale(0.1)
        total = VGroup(
            cost,
            steps,
        ).arrange(RIGHT, buff=2).move_to(2.5 * DOWN)
        self.play(AddTextLetterByLetter(cost), run_time=0.5)
        self.next_slide()
        self.play(AddTextLetterByLetter(steps), run_time=0.5)
        self.next_slide()
        values = Text(
            "    ~30        x  ~1 second",
            font='Open Sans',
            font_size=300,
            fill_color=ELECTRON_COLOR,
            fill_opacity=1.0,
        ).scale(0.1).next_to(steps, DOWN).shift(0.2 * RIGHT)
        self.play(AddTextLetterByLetter(values), run_time=0.5)
        self.next_slide()


class TimeScales(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        files = [f'images/timescales/timescales_Layer_{i + 2}.png' for i in range(4)]
        parts = Group(*[ImageMobject(file).center().scale(0.5) for file in files])
        parts.scale(0.8).shift(UP)

        amino = Text(
            'amino acid',
            font='Open Sans',
            font_size=250,
            color=WHITE,
        ).scale(0.1).next_to(parts, DOWN).shift(3 * LEFT)
        # primary = Text(
        #     'primary structure',
        #     font='Open Sans',
        #     font_size=250,
        #     color=WHITE,
        # ).scale(0.1).move_to(parts.next_to(parts.get_corner(DOWN + LEFT)))

        labels = [amino]

        for i, part in enumerate(parts):
            self.add(part)
            self.play(Wait())
            self.next_slide()

        axis_size = 13
        axis = Arrow(
            start=np.array([-axis_size / 2, 0, 0]),
            end=np.array([axis_size / 2, 0, 0]),
            tip_shape=StealthTip,
            stroke_width=2.5,
            tip_length=0.2,
        ).shift(2 * DOWN)
        axis_label = Text(
            'time scale [s]',
            font='Open Sans',
            font_size=250,
        ).scale(0.1).move_to(axis.get_end() + 0.4 * DOWN + 0.5 * RIGHT, RIGHT)

        powers = list(range(-15, 3, 3))
        #labels = [r'$10^{' + str(i) + r'}$' for i in powers]

        femtosecond = Text(
            '~10 femtoseconds',
            font='Open Sans',
            font_size=300,
            color=NUCLEUS_COLOR,
        ).scale(0.1).move_to(axis.get_start(), UP).shift(2 * RIGHT + UP)
        microsecond = Text(
            '~1 millisecond!',
            font='Open Sans',
            font_size=300,
            color=NUCLEUS_COLOR,
        ).scale(0.1).move_to(axis.get_end() + 0.5 * UP + 2 * LEFT, RIGHT)

        self.play(Create(axis), AddTextLetterByLetter(axis_label), run_time=0.5)
        self.next_slide()

        self.play(AddTextLetterByLetter(femtosecond), run_time=0.5)
        self.next_slide()
        self.play(AddTextLetterByLetter(microsecond), run_time=0.5)
        self.next_slide()

        milliseconds = Text(
            "1 millisecond",
            font='Open Sans',
            font_size=300,
            fill_color=ELECTRON_COLOR,
            fill_opacity=1.0,
        ).scale(0.1)
        evals = Text(
            "~  2,000,000,000 force evaluations",
            font='Open Sans',
            font_size=150,
            fill_color=ELECTRON_COLOR,
            fill_opacity=1.0,
        ).scale(0.2)
        scale = VGroup(milliseconds, evals).arrange(
            RIGHT,
            buff=0.3,
        )
        scale.move_to(3 * DOWN)
        self.play(AddTextLetterByLetter(milliseconds), run_time=0.5)
        self.play(AddTextLetterByLetter(evals), run_time=0.5)
        self.next_slide()

        time = Text(
            "~  83 years of simulation ...",
            font='Open Sans',
            font_size=150,
            fill_color=ELECTRON_COLOR,
            fill_opacity=1.0,
        ).scale(0.2).next_to(evals, DOWN, aligned_edge=LEFT)
        self.play(AddTextLetterByLetter(time), run_time=0.5)
        self.next_slide()


class Overview(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05

        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.3 * UP)
        self.play(Create(table), run_time=1)
        self.next_slide()

        physics = Text(
            'laws of physics?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        simulation = Text(
            'challenges?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        solution = Text(
            'solution?',
            font='Open Sans',
            font_size=300,
        ).scale(0.1)
        goals = VGroup(physics, simulation, solution).arrange(
            RIGHT,
            buff=2.5,
            aligned_edge=UP,
        )
        goals.shift(2 * DOWN)
        self.play(AddTextLetterByLetter(physics), run_time=0.5)
        self.play(AddTextLetterByLetter(simulation), run_time=0.5)
        self.play(AddTextLetterByLetter(solution), run_time=0.5)
        self.next_slide()

        nuclei = Text(
            'classical (nuclei)',
            font='Open Sans',
            font_size=250,
            color=NUCLEUS_COLOR,
        ).scale(0.1)
        electrons = Text(
            'quantum (electrons)',
            font='Open Sans',
            font_size=250,
            color=QM_COLOR,
        ).scale(0.1)
        laws = VGroup(nuclei, electrons).arrange(
            DOWN,
            buff=0.2,
            # aligned_edge=LEFT,
        ).next_to(physics, DOWN)
        self.play(FadeIn(laws), run_time=0.4)
        self.next_slide()

        newton = Tex(r"$F=ma$", color=WHITE)
        newton[0][0].set_color(QM_COLOR)
        evaluations = Text(
            '# evaluations',
            font='Open Sans',
            font_size=250,
            color=WHITE,
        ).scale(0.1)
        challenges = VGroup(newton, evaluations).arrange(
            DOWN,
            buff=0.2,
        ).next_to(simulation, DOWN)
        self.play(FadeIn(challenges))
        self.next_slide()


class HydrogenRevisited(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        axes = Axes((0.0, 8), (-1, 1), x_length=7).scale(0.7).shift(0.5 * LEFT)
        axes.shift(3.0 * LEFT)
        xlabel = Text(
            "interatomic\n  distance",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_x_axis().get_end(), DOWN)
        ylabel = Text(
            "energy",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_y_axis().get_end(), UP)
        f = lambda x: potential(x / 1.5 * 0.74)
        graph = axes.plot(
            f,
            color=QM_COLOR,
            x_range=[0.6, 7],
        ).set_z_index(0)
        graph_label = axes.get_graph_label(graph, 'E(r)')
        graph_label.next_to(graph.get_start(), RIGHT)

        self.play(Create(axes), run_time=0.6)
        self.play(
            Create(graph),
            AddTextLetterByLetter(ylabel),
            AddTextLetterByLetter(xlabel),
            run_time=0.6,
        )
        self.play(Write(graph_label), run_time=0.6)
        self.next_slide()

        dots = []
        for r in np.array([0.8, 0.9, 1.11, 1.3, 1.64, 1.91, 2.29, 2.66]):
            dot = Dot(axes.c2p(r, f(r)), z_index=1)
            dots.append(dot)
        dots = VGroup(*dots)
        self.play(Create(dots))
        self.next_slide()

        r = Tex(r"XYZ").shift(3 * RIGHT + 3 * UP)
        qm = Square(1.5, fill_opacity=0.0, fill_color=WHITE).next_to(r, DOWN)
        qm.shift(DOWN)
        arrow = Arrow(r.get_center(), qm.get_top())
        arrow_ = arrow.copy().next_to(qm, DOWN, buff=0.3)
        E = Tex(r"$E, \nabla E$", color=QM_COLOR).next_to(arrow_.get_end(), DOWN)
        label = Text(
            "QM",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).move_to(qm.get_center())
        self.play(Succession(
            Create(r),
            Create(arrow),
            Create(qm),
            Create(arrow_),
            Create(E),
        ), run_time=0.6)
        self.play(AddTextLetterByLetter(label), run_time=0.1)
        self.next_slide()

        clock = SVGMobject('images/clock.svg').move_to(label.get_center()).scale(0.5)
        self.play(Transform(label, clock))
        self.next_slide()

        motto = Text(
            'can we not just learn E(r) "from the data"?',
            font='Open Sans',
            font_size=150,
            fill_color=ELECTRON_COLOR,
            fill_opacity=1.0,
        ).scale(0.2).center().shift(3 * DOWN)
        self.play(FadeOut(graph))
        self.play(AddTextLetterByLetter(motto), run_time=0.5)
        self.next_slide()

        graph = axes.plot(
            lambda x: harmonic(x / 1.5 * 0.74),
            color=ELECTRON_COLOR,
            x_range=[0.6, 3],
            stroke_width=6.0,
        ).set_z_index(5)
        self.play(Create(graph))
        self.next_slide()
        curved = CurvedArrow(
            r.get_center(),
            E.get_center(),
            angle=-2 * np.pi / 3,
        ).shift(RIGHT).set_color(ELECTRON_COLOR)
        self.play(Create(curved))
        self.next_slide()


class Priors(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        title = Tex(
            r"\sffamily learning a mapping: XYZ $\longrightarrow$ energy",
        ).to_corner(UP + LEFT)
        self.add(title)
        positions = np.array([
            [0, 0],
            [-1, -1],
            [1, -1],
        ])
        axes = Axes(
            x_range=(0, 2),
            y_range=(0, 2),
            x_length=2,
            y_length=2,
            x_axis_config={'include_ticks': False},
            y_axis_config={'include_ticks': False},
        ).shift(5 * LEFT + 0.3 * DOWN)
        xlabel = Tex(
            "$x$",
        ).next_to(axes.get_x_axis().get_end(), DOWN)
        ylabel = Tex(
            "$y$",
        ).next_to(axes.get_y_axis().get_end(), RIGHT)

        circles = [
            Circle(radius=0.8, color=OXYGEN_COLOR, fill_opacity=1.0, stroke_color=WHITE),
            Circle(radius=0.5, color=GRAY, fill_opacity=1.0, stroke_color=WHITE),
            Circle(radius=0.5, color=GRAY, fill_opacity=1.0, stroke_color=WHITE),
        ]

        angle = ValueTracker(0.0)
        self.add(angle)

        def update_circle(index=0):
            a = angle.get_value()
            rotation = np.array([
                [np.cos(a), np.sin(a)],
                [-np.sin(a), np.cos(a)],
                ])
            new_pos = np.hstack((positions @ rotation, np.zeros((3, 1))))
            return new_pos[index] + np.array([-1, 0, 0])

        bonds = []
        for i in range(2):
            bond = Line(
                circles[0].get_center(),
                circles[i + 1].get_center(),
                z_index=0,
                stroke_width=40,
            )
            f_always(
                bond.set_points_by_ends,
                partial(update_circle, index=0),
                partial(update_circle, index=i + 1),
            )
            bonds.append(bond)

        for i, circle in enumerate(circles):
            circle.move_to(update_circle(i))  # initialize
            circle.set_z_index(1)
            f_always(circle.move_to, partial(update_circle, index=i))

        values = []
        for i in range(3):
            for j in range(2):
                value = DecimalNumber(
                    positions[i, j],
                    include_sign=True,
                    mob_class=Tex,
                    color=WHITE,
                )
                def updater(m, i, j):
                    a = angle.get_value()
                    rotation = np.array([
                        [np.cos(a), np.sin(a)],
                        [-np.sin(a), np.cos(a)],
                        ])
                    new_pos = positions @ rotation
                    m.set_value(new_pos[i, j])
                value.add_updater(partial(updater, i=i, j=j))
                values.append(value)

        self.add(*circles)
        self.play(
            Create(axes),
            AddTextLetterByLetter(xlabel),
            AddTextLetterByLetter(ylabel),
            Create(VGroup(*(circles + bonds))),
            run_time=0.5,
        )
        self.next_slide()

        x, y = Tex(r"$x$"), Tex(r"$y$")
        table = [
            Tex(), x, y,
            Tex("O", color=OXYGEN_COLOR), values[0], values[1],
            Tex("H", color=GRAY), values[2], values[3],
            Tex("H", color=GRAY), values[4], values[5],
        ]
        coordinates = VGroup(*table).arrange_in_grid(
            rows=4,
            columns=3,
            buff=0.5,
        )
        coordinates.shift(4.5 * RIGHT)
        self.play(*[FadeIn(v) for v in table], run_time=0.06)
        self.next_slide()

        self.play(angle.animate.set_value(np.pi / 2), run_time=3)
        self.next_slide()

        linear_coord = coordinates.copy().arrange(RIGHT, buff=0.2)
        linear_coord.center().shift(2 * DOWN)
        self.play(
            ReplacementTransform(coordinates, linear_coord),
        )
        self.next_slide()
