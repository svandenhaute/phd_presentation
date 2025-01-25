import glob
from functools import partial

import numpy as np

from manim import (
    Scene, VGroup, DrawBorderThenFill, Circumscribe, Create, PI, Group,
    Circle, Square, Text, SVGMobject, ImageMobject, Rectangle, CubicBezier, Tex,
    Line, Dot, NumberLine, ValueTracker, Vector, DashedLine, Arrow, StealthTip,
    RoundedRectangle, MathTex, DecimalNumber, Axes, CurvedArrow, ThreeDAxes,
    Sphere, DashedVMobject, ImageMobject, SurroundingRectangle, TexTemplate,
    FadeIn, Transform, FadeOut, AnimationGroup, Succession, Write, Uncreate,
    MoveToTarget, ReplacementTransform, Wait, AddTextLetterByLetter, Brace,
    MoveAlongPath, LaggedStart,
    f_always, linear, always,
    WHITE, BLACK, ManimColor, BLUE, RED, GRAY, DARK_GRAY,
    DOWN, LEFT, RIGHT, UP, ORIGIN, UL, UR, DR,
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
MESSAGE_COLORS = (
    ManimColor.from_rgb((245, 196, 0)),
    ManimColor.from_rgb((245, 86, 0)),
    ManimColor.from_rgb((245, 0, 45)),
)
BAD = ManimColor.from_rgb((235, 73, 52))
MID = ManimColor.from_rgb((196, 128, 10))
PRO = ManimColor.from_rgb((21, 148, 82))
tex_template = TexTemplate(preamble='\\usepackage{amsmath}\n\\usepackage{esvect}')

SLIDE_NUMBER_FONTSIZE = 25


class Title(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        title = ImageMobject('images/title_slide.png')
        self.add(title)
        self.wait()


class Particles(Slide):  # 1

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("1", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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


class PeriodicTable(Slide):  # 2

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
        self.add(Text("2", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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


class Masses(Slide):  # 3

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("3", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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

        raw_str = r"$$\vec{F} = m \vec{a}$$"
        classical_tex = Tex(raw_str, tex_template=tex_template).move_to(electrostatics.get_center()).set_color(WHITE)
        classical_tex.move_to(qm_tex.get_center() + 3 * DOWN)
        classical_tex[0][:2].set_color(color=QM_COLOR)
        self.play(ReplacementTransform(electrons_lines, hatch))
        self.play(Write(classical_tex), run_time=0.7)
        # self.play(Circumscribe(classical_tex[0][:2], color=QM_COLOR))
        self.next_slide()


class Dynamics(Slide):  # 4

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("4", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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


class OverviewPhysics(Slide):  # 5

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("5", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.3 * UP)
        self.add(table)

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
        self.add(physics)
        self.add(simulation)
        self.add(solution)
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


class TimeEvolution(Slide):  # 6

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("6", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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


class TimeScales(Slide):  # 7

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("7", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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


class Pareto(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        image = ImageMobject('test.png')
        self.add(image)
        self.play(Wait())
        self.next_slide()


class Overview(Slide):  # 8

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("8", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.3 * UP)
        self.add(table)
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
        self.add(physics)
        self.add(simulation)
        self.add(solution)
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

        newton = Tex(r"$\vec{F}=m\vec{a}$", color=WHITE, tex_template=tex_template)
        newton[0][:2].set_color(QM_COLOR)
        evaluations = Text(
            '# evaluations',
            font='Open Sans',
            font_size=250,
            color=WHITE,
        ).scale(0.1)
        challenges = VGroup(newton, evaluations).arrange(
            DOWN,
            buff=0.2,
        ).next_to(simulation, 0.5 * DOWN)
        self.play(FadeIn(challenges))
        self.next_slide()


class HydrogenRevisited(Slide):  # 9

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("9", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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


class Priors(Slide):  # 10

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("10", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
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

        arrow = Arrow(ORIGIN, 2 * DOWN).next_to(coordinates, DOWN)
        energy = Tex(r"\sffamily energy").next_to(arrow, DOWN)
        self.play(
            Create(arrow),
            Create(energy),
            run_time=0.5,
        )
        self.next_slide()


class Dimensionality(Slide):  # 11

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("11", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        title = Text(
            "the curse of dimensionality",
            font='Open Sans',
            font_size=350,
        ).scale(0.1).to_corner(UL)
        self.add(title)
        self.play(Wait())
        self.next_slide()

        axes = Axes((0.0, 8), (-1, 1), x_length=7).scale(0.7).shift(0.5 * LEFT)
        axes.shift(RIGHT)
        f = lambda x: potential(x / 1.5 * 0.74)
        graph = axes.plot(
            f,
            color=QM_COLOR,
            x_range=[0.6, 7],
        ).set_z_index(0)

        dots = [Dot() for i in range(10)]
        dots_f = [Dot() for i in range(10)]
        for dot, x in zip(dots, np.linspace(0.8, 5, 10)):
            dot.move_to(axes.c2p(x, 0))
        for dot, x in zip(dots_f, np.linspace(0.8, 5, 10)):
            dot.move_to(axes.c2p(x, f(x)))

        gdots = VGroup(*dots)
        gdots_f = VGroup(*dots_f)
        self.play(Create(graph), run_time=0.5)
        self.next_slide()

        self.play(Succession(*[FadeIn(d) for d in dots], lag_ratio=0.3), run_time=0.5)
        self.play(ReplacementTransform(gdots, gdots_f), run_time=1.0)
        self.next_slide()

        dots1 = VGroup(*[Dot() for i in range(10)]).arrange(RIGHT, buff=0.25).shift(RIGHT)
        self.play(FadeOut(graph, run_time=0.5))
        self.play(ReplacementTransform(gdots_f, dots1, run_time=0.5))
        self.next_slide()

        one_d = Text(
            "in 1D:",
            font='Open Sans',
            font_size=300,
            color=NUCLEUS_COLOR,
            weight="BOLD",
        ).scale(0.1).next_to(dots1, 8 * LEFT)
        one_count = Text(
            "10 points",
            font='Open Sans',
            font_size=350,
        ).scale(0.1).next_to(one_d, DOWN)
        # axis = Arrow(
        #     start=ORIGIN,
        #     end=7 * RIGHT,
        #     tip_shape=StealthTip,
        #     stroke_width=2.5,
        #     tip_length=0.2,
        # ).next_to(one_d, 5 * RIGHT, aligned_edge=LEFT)
        self.play(AddTextLetterByLetter(one_d), run_time=0.2)
        self.play(FadeIn(one_count), run_time=0.1)
        self.next_slide()

        dots2 = VGroup(*[Dot() for i in range(100)]).arrange_in_grid(10, 10, buff=0.25)
        dots2.move_to(dots1.get_center())
        two_d = Text(
            "in 2D:",
            font='Open Sans',
            font_size=300,
            color=NUCLEUS_COLOR,
            weight="BOLD",
        ).scale(0.1).move_to(one_d.get_center())
        two_count = Text(
            "100 points",
            font='Open Sans',
            font_size=350,
        ).scale(0.1).next_to(two_d, DOWN)
        self.play(
            ReplacementTransform(dots1, dots2),
            ReplacementTransform(one_d, two_d),
            ReplacementTransform(one_count, two_count),
            # axis.animate.move_to(VGroup(dots2[-10:]).get_center()),
            run_time=0.7,
        )
        self.next_slide()

        three_d = Text(
            "in 3D:",
            font='Open Sans',
            font_size=300,
            color=NUCLEUS_COLOR,
            weight="BOLD",
        ).scale(0.1).move_to(two_d.get_center())
        three_count = Text(
            "1000 points",
            font='Open Sans',
            font_size=350,
        ).scale(0.1).next_to(three_d, DOWN)
        self.play(
            FadeOut(dots2, run_time=0.5),
            ReplacementTransform(two_d, three_d),
            ReplacementTransform(two_count, three_count),
            run_time=0.5,
        )
        self.next_slide()

        equation = Tex(r"$E = E(x_1, y_1, z_1, x_2, y_2, z_2, ... )$").shift(2 * DOWN)
        brace = Brace(equation[0][4:-1], color=NUCLEUS_COLOR)
        self.play(Write(equation, run_time=0.5))
        self.play(Create(brace))
        self.next_slide()
        texts = []
        for number in [10, 100, 1000]:
            text = Text(
                str(number),
                font='Open Sans',
                font_size=300,
                color=NUCLEUS_COLOR,
            ).scale(0.1).next_to(brace, DOWN)
            texts.append(text)
        self.play(FadeIn(texts[0], run_time=0.5))
        self.play(ReplacementTransform(texts[0], texts[1]), run_time=0.5)
        self.play(ReplacementTransform(texts[1], texts[2]), run_time=0.5)
        self.next_slide()

        thousand_d = Text(
            "in 1000D:",
            font='Open Sans',
            font_size=300,
            color=NUCLEUS_COLOR,
            weight="BOLD",
        ).scale(0.1).move_to(two_d.get_center())
        thousand_count = Tex(r"$\infty$").next_to(three_d, DOWN).scale(1.3)
        self.play(
            ReplacementTransform(three_d, thousand_d),
            ReplacementTransform(three_count, thousand_count),
            run_time=0.5,
        )
        self.next_slide()


class Images(Slide):  # 12

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("12", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        title = Tex(r"\sffamily analogy: images")
        title.to_corner(UL)
        feynman = ImageMobject('images/feynman.jpg').scale(5).shift(3 * LEFT)
        dimensions = Tex(
            r"\sffamily 128 x 128 pixels; 10,000 dimensions",
            color=NUCLEUS_COLOR,
        ).next_to(feynman, DOWN)
        solved = Tex(
            r"\sffamily How? The manifold hypothesis",
            color=ELECTRON_COLOR,
        ).next_to(feynman, 2 * RIGHT, aligned_edge=LEFT).shift(2 * UP)
        self.add(title)
        self.play(Wait())
        self.next_slide()

        self.play(FadeIn(feynman, run_time=0.6))
        self.play(AddTextLetterByLetter(dimensions), run_time=0.5)
        self.next_slide()

        self.play(AddTextLetterByLetter(solved), run_time=0.5)
        self.next_slide()

        nimages = 10
        scale = 3
        images = np.random.randint(0, 256, size=(nimages, 128, 128)).astype(np.uint8)
        anims = []
        for image in images:
            mob = ImageMobject(image).move_to(feynman.get_center()).scale(5)
            mob.set_resampling_algorithm(4)  # 4 == box
            anims.append(FadeIn(mob, run_time=0.06))
            anims.append(Wait(0.2))

        self.play(Succession(*anims), run_time=5)
        self.next_slide()

        images = Tex(
            r"\sffamily images",
            color=WHITE,
        )
        audio = Tex(
            r"\sffamily audio (music)",
            color=WHITE,
        )
        text = Tex(
            r"\sffamily text (language)",
            color=WHITE,
        )
        atoms = Tex(
            r"\textbf{\sffamily atoms}",
            color=WHITE,
        )
        all_ = VGroup(images, audio, text, atoms).arrange(DOWN).next_to(solved, 3 * DOWN, aligned_edge=UP)

        self.play(AddTextLetterByLetter(images), run_time=0.5)
        self.next_slide()
        self.play(AddTextLetterByLetter(audio), run_time=0.5)
        self.next_slide()
        self.play(AddTextLetterByLetter(text), run_time=0.5)
        self.next_slide()

        self.play(AddTextLetterByLetter(atoms), run_time=0.5)
        self.next_slide()


class Network(Slide):  # 13

    def network(self, *sizes):
        layers = []
        for j, size in enumerate(sizes):
            kwargs = dict(
                radius=0.05,
                z_index=1,
                fill_color=BLACK,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=2,
            )
            dots = [Circle(**kwargs) for i in range(size)]
            VGroup(*dots).arrange(RIGHT, buff=0.3).shift(j * DOWN)
            layers.append(dots)

        weights = []
        # p = 0.2
        for i in range(1, len(layers)):
            layer = layers[i]
            other = layers[i - 1]
            per_layer_weights = []
            for k in range(len(layer)):
                for l in range(len(other)):
                    line = Line(
                        other[l].get_center(),
                        layer[k].get_center(),
                        stroke_width=1,
                        color=GRAY,
                        z_index=0,
                    )
                    per_layer_weights.append(line)
            weights.append(per_layer_weights)
        return layers, weights

    def construct(self):
        # "a systematic way of building complex functions"
        self.wait_time_between_slides = 0.05
        self.add(Text("13", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        title = Text(
            "neural networks",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        layers, weights = self.network(5, 10, 20, 8, 1)
        network = VGroup(*[m for mlist in weights + layers for m in mlist])
        network.center().shift(2 * LEFT + 0.5 * DOWN)
        top = VGroup(*layers[0]).get_center() + 0.5 * UP
        bottom = VGroup(*layers[-1]).get_center() + 0.5 * DOWN
        r = Tex(r"XYZ").move_to(top)
        qm = Square(1.5, fill_opacity=0.0, fill_color=WHITE).move_to((top + bottom) / 2)
        E = Tex(r"$E, \nabla E$").move_to(bottom)

        arrow = Arrow(r.get_bottom(), qm.get_top())
        arrow_ = arrow.copy().next_to(qm, DOWN, buff=0.3)
        label = Text(
            "QM",
            font='Open Sans',
            font_size=300,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).scale(0.1).move_to(qm.get_center())

        QM = VGroup(r, qm, arrow, arrow_, E, label)
        self.play(Create(QM), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(VGroup(arrow, arrow_, qm, label)), run_time=0.5)
        for layer, per_layer_weights in zip(layers[:-1], weights):
            anim_dots = LaggedStart(
                *[Create(d) for d in layer],
                lag_ratio=0.1,
                run_time=0.3,
            )
            anim_lines = LaggedStart(
                *[Create(d) for d in per_layer_weights],
                lag_ratio=0.1,
                run_time=0.3,
            )
            self.play(anim_dots, anim_lines)
        self.play(Create(layers[-1][0]), run_time=0.1)
        self.next_slide()

        learning = Text(
            "learns from examples",
            font='Open Sans',
            font_size=250,
            color=WHITE,
        ).scale(0.10).next_to(network).shift(UP + RIGHT)
        train = Tex(
            r"XYZ $\longrightarrow E, \nabla E$",
            color=NUCLEUS_COLOR,
        ).next_to(learning, DOWN)
        self.play(AddTextLetterByLetter(learning), run_time=0.5)
        self.play(Create(train), run_time=0.5)
        self.next_slide()
        all_weights = [w for weight in weights for w in weight]
        anims = [w.animate.set_color(NUCLEUS_COLOR).build() for w in all_weights]
        self.play(*anims)
        self.next_slide()


class GNN(Slide):  # 14

    def points(self):
        return np.array([
            [4, 2, 0],
            [2, 1, 0],
            [0, 0, 0],
            [-2, -1, 0],
            [-1, -1, 0],
            [-3, -2.5, 0],
            ])

    def dots(self, positions):
        return [Dot(radius=0.12, z_index=1).move_to(p) for p in positions]

    def feats(self, positions, blue=False, red=False):
        width, height = 0.3, 0.9
        rectangles = []
        for i, position in enumerate(positions):
            rectangle = Rectangle(
                width=width,
                height=height,
                color=WHITE,
                fill_color=WHITE,
                fill_opacity=0.0,
                stroke_width=1.5,
            ).move_to(position, aligned_edge=DOWN).shift(0.15 * UP)
            if i == 1:
                rectangle.shift(0.3 * LEFT)
            if i == 4:
                rectangle.shift(0.3 * RIGHT)
            rectangles.append(rectangle)
        return rectangles

    def bonds(self, positions):
        distances = np.linalg.norm(
            positions.reshape(1, 6, 3) - positions.reshape(6, 1, 3),
            axis=2
        )
        bonds = []
        for i in range(6):
            for j in range(i + 1, 6):
                if distances[i, j] < 4.0:
                    bond = Line(
                        positions[i],
                        positions[j],
                        z_index=0,
                        color=WHITE,
                    )
                    bonds.append(bond)
        return bonds

    def message(self, bonds, color=MESSAGE_COLORS[0]):
        messages = []
        for bond in bonds:
            for direction in [+1, -1]:
                m = Square(
                    0.3,
                    fill_color=color,
                    stroke_color=WHITE,
                    fill_opacity=1.0,
                    stroke_width=1.5,
                )
                if direction == -1:
                    bond = bond.copy().rotate(np.pi)
                message = Succession(
                    MoveAlongPath(m, bond),
                    FadeOut(m),
                    run_time=1.5,
                )
                messages.append(message)
        return messages

    def add_to_feats(self, feats, iteration=0, color=MESSAGE_COLORS[0]):
        blocks = []
        for feat in feats:
            m = Square(
                0.3,
                fill_color=color,
                stroke_color=WHITE,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            shift = (feat.height - m.side_length) / 2 - iteration * 0.3
            m.move_to(feat.get_center()).shift(shift * DOWN)
            blocks.append(m)
        return blocks

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("14", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        title = Text(
            "geometric graph neural networks",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)
        self.play(Wait())
        self.next_slide()

        # draw waters
        waters = []
        for i in range(2):
            atoms = [
                Circle(radius=0.8, color=OXYGEN_COLOR, fill_opacity=1.0, stroke_color=WHITE),
                Circle(radius=0.5, color=GRAY, fill_opacity=1.0, stroke_color=WHITE),
                Circle(radius=0.5, color=GRAY, fill_opacity=1.0, stroke_color=WHITE),
            ]
            for i, position in enumerate(1.2 * np.array([[0, 0], [-1, -1], [1, -1]])):
                atoms[i].move_to(np.array(list(position) + [0]))
            bonds = [
                Line(atoms[0].get_center(), atoms[1].get_center(), stroke_width=40),
                Line(atoms[0].get_center(), atoms[2].get_center(), stroke_width=40),
            ]
            for bond in bonds:
                bond.set_z_index(0)
            for atom in atoms:
                atom.set_z_index(1)
            waters.append((atoms, bonds))

        # shift and rotate one
        gwaters = [
            VGroup(*(waters[0][0] + waters[0][1])),
            VGroup(*(waters[1][0] + waters[1][1])),
        ]
        gwaters[0].rotate(np.pi / 4).shift(3 * LEFT)
        gwaters[1].rotate(np.pi / 2).shift(2 * RIGHT + 0.3 * UP)
        # for gwater in gwaters:
        #     gwater.shift(0.5 * DOWN)
        self.add(*gwaters)
        self.play(Wait())
        self.next_slide()

        atoms = [a for i in range(2) for a in waters[i][0]]
        bonds = [b for i in range(2) for b in waters[i][1]]
        anims = []
        dot_positions = np.zeros((6, 3))
        for i, atom in enumerate(atoms):
            dot_positions[i] = np.array(atom.get_center())
        dots = self.dots(dot_positions)
        for dot, atom in zip(dots, atoms):
            anims.append(ReplacementTransform(atom, dot))
        self.play(*[FadeOut(b) for b in bonds], run_time=0.2)
        self.play(*anims, run_time=0.5)
        self.next_slide()

        circle = Circle(
            radius=2.5,
            fill_color=WHITE,
            fill_opacity=0.0,
            color=WHITE,
            stroke_width=4,
        )
        circle = DashedVMobject(circle, dashed_ratio=0.3, num_dashes=40)
        circle.move_to(dot_positions[-1])
        self.play(Create(circle), run_time=0.5)
        self.next_slide()

        bonds = self.bonds(dot_positions)
        self.play(
            Create(bonds[-1]),
            Create(bonds[-2]),
            run_time=0.5,
        )
        self.play(FadeOut(circle), run_time=0.5)
        self.next_slide()

        self.play(*[Create(b) for b in bonds[:-2]], run_time=0.5)
        self.next_slide()

        feats = self.feats(dot_positions)
        self.play(*[Create(f) for f in feats], run_time=0.5)
        self.next_slide()

        self.play(*[FadeOut(b) for b in bonds], run_time=0.5)
        self.next_slide()

        messages = self.message(bonds)
        blocks0 = self.add_to_feats(feats)
        self.play(*messages)
        self.play(*[FadeIn(block) for block in blocks0])
        message_passing = Text(
            '"message passing"',
            font='Open Sans',
            font_size=250,
            color=NUCLEUS_COLOR,
        ).scale(0.1).next_to(title, DOWN).shift(DOWN)
        self.play(AddTextLetterByLetter(message_passing, run_time=0.3))
        self.next_slide()

        messages = self.message(bonds, color=MESSAGE_COLORS[1])
        blocks1 = self.add_to_feats(feats, iteration=1, color=MESSAGE_COLORS[1])
        self.play(*messages)
        self.play(*[FadeIn(block) for block in blocks1])
        self.next_slide()

        blocks2 = self.add_to_feats(feats, iteration=2, color=MESSAGE_COLORS[2])
        self.play(*[FadeIn(block) for block in blocks2])
        self.play(*[FadeIn(b) for b in bonds])
        self.play(*[FadeOut(f) for f in feats], run_time=0.1)
        self.next_slide()

        blocks_per_node = []
        for i in range(6):
            blocks_per_node.append(VGroup(blocks0[i], blocks1[i], blocks2[i]))

        everything = VGroup(*(dots + bonds + blocks_per_node))
        self.play(everything.animate.scale(0.5).shift(3 * LEFT), run_time=0.5)
        blocks = [block.copy() for block in blocks_per_node]
        self.play(VGroup(*blocks).animate.arrange(DOWN, buff=0.5).shift(3 * RIGHT))
        function = Tex(r"$f_{\text{\sffamily read}}(\qquad) = $")
        function.move_to(blocks[0].get_center())
        anims = []
        energy0 = Tex(r"$E_1$").next_to(function, RIGHT)
        self.play(
            FadeIn(function, run_time=0.5),
            FadeIn(energy0, run_time=0.5),
        )
        for i in range(1, 6):
            function_ = function.copy().move_to(blocks[i].get_center())
            energy = Tex("$E_" + str(i + 1) + "$").next_to(function_, RIGHT)
            self.play(Succession(
                ReplacementTransform(function, function_),
                FadeIn(energy, run_time=0.5),
                ),
                run_time=0.5,
            )
            function = function_
        readout = Tex(r"$f_{\text{\sffamily read}}$").next_to(function, LEFT)
        self.play(
            ReplacementTransform(function, readout, run_time=0.5),
        )
        self.next_slide()

        line = Line(ORIGIN, RIGHT).next_to(energy, DOWN)
        plus = Tex("$+$").next_to(line, RIGHT)
        E = Tex("$E$").next_to(line, DOWN)
        self.play(
            Create(line),
            Create(plus),
            Create(E),
            run_time=0.5,
        )
        self.next_slide()


class OverviewGNN(Slide):  # 15

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("15", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        boxes = generate_periodic_table()
        table = VGroup(*sum(boxes.values(), start=())).center().shift(1.3 * UP)
        self.add(table)
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
        self.add(physics)
        self.add(simulation)
        self.add(solution)
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

        newton = Tex(r"$\vec{F}=m\vec{a}$", color=WHITE, tex_template=tex_template)
        newton[0][:2].set_color(QM_COLOR)
        evaluations = Text(
            '# evaluations',
            font='Open Sans',
            font_size=250,
            color=WHITE,
        ).scale(0.1)
        challenges = VGroup(newton, evaluations).arrange(
            DOWN,
            buff=0.2,
        ).next_to(simulation, 0.4 * DOWN)
        self.play(FadeIn(challenges))
        self.next_slide()

        gnn = Text(
            'graph neural\n   networks',
            font='Open Sans',
            font_size=250,
            color=WHITE,
            weight="BOLD",
        ).scale(0.1).next_to(solution, DOWN)
        self.play(FadeIn(gnn))
        self.next_slide()


class Three(Slide):  # 16

    def gnn(self):
        message_passing = Text(
            "message passing:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1)
        from_xyz = Tex(r"$\text{\sffamily XYZ} \longrightarrow \quad$").next_to(message_passing, RIGHT)
        squares = []
        for color in MESSAGE_COLORS:
            square = Square(
                0.3,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            squares.append(square)
        feats = VGroup(*squares[::-1]).arrange(DOWN, buff=0).next_to(from_xyz, RIGHT)

        readout = Text(
            "readout:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1).next_to(message_passing, 3 * DOWN, aligned_edge=LEFT)
        f_read = Tex(r"$f_{\text{\sffamily read}}(\quad) = E_i$").next_to(readout, 2 * RIGHT)
        arg = feats.copy().move_to(f_read.get_center() + 0.14 * LEFT)

        content = VGroup(message_passing, from_xyz, feats, readout, f_read, arg)
        border = SurroundingRectangle(content, color=WHITE, buff=0.2)
        title = Text(
            "GNN",
            font='Open Sans',
            font_size=250,
            weight="BOLD",
        ).scale(0.1).next_to(border, 0.5 * UP, aligned_edge=LEFT)
        return content, border, title

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("16", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        title = Text(
            "so... the phd itself?",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)
        self.play(Wait())
        self.next_slide()

        content, border, title = self.gnn()
        gnn = VGroup(content, border, title).center()
        self.play(Create(title), Create(border), run_time=0.5)
        self.play(Create(content), run_time=0.7)
        self.next_slide()

        numbers = []
        for i in range(3):
            circle = Circle(
                radius=0.25,
                fill_color=WHITE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                z_index=0,
            )
            number = Text(
                str(i + 1),
                font="Open Sans",
                font_size=250,
                color=BLACK,
                z_index=1,
                weight="BOLD",
            ).scale(0.1)
            number.move_to(circle.get_center())
            if i == 0:
                number.shift(0.02 * LEFT)
            numbers.append(VGroup(number, circle))
        gnumbers = VGroup(*numbers).arrange(DOWN, buff=1.5).shift(6.5 * LEFT + 0.5 * DOWN)
        self.play(gnn.animate.scale(0.7).to_corner(UR), run_time=0.5)
        self.play(*[FadeIn(e) for n in numbers for e in n], run_time=0.5)
        self.next_slide()

        training = r"$\text{\sffamily GNN} \longleftarrow"
        training += r"\left\{\text{\sffamily XYZ}, E, \vec{F}\right\}$"
        training = Tex(training, tex_template=tex_template).next_to(numbers[0], RIGHT)
        self.play(Create(training.scale(0.9)), run_time=0.5)
        catch = Text(
            "on-the-fly learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(training, 0.5 * DOWN, aligned_edge=LEFT)
        self.play(AddTextLetterByLetter(catch), run_time=0.3)
        self.next_slide()

        no_F = Text(
            "most accurate QM methods can only do ",
            color=WHITE,
            font='Open Sans',
            font_size=200,
        ).scale(0.1 * 3 / 2).next_to(numbers[1], 2 * RIGHT)
        F = Tex(r"$\left\{\text{\sffamily XYZ}, E\right\}$", tex_template=tex_template).next_to(
            no_F,
            RIGHT,
        ).shift(0.0 * UP)
        transfer = Text(
            "transfer learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(no_F, 0.5 * DOWN, aligned_edge=LEFT)
        self.play(AddTextLetterByLetter(no_F, run_time=0.5))
        self.play(FadeIn(F), run_time=0.1)
        self.play(AddTextLetterByLetter(transfer, run_time=0.3))
        self.next_slide()

        texts = ['computational cost = ', '# steps ', ' x  (cost/step)']
        mtexts = []
        for text in texts:
            mtext = Text(
                text,
                font='Open Sans',
                font_size=200,
                fill_color=WHITE,
                fill_opacity=1.0,
            ).scale(0.1 * 3 / 2)
            mtexts.append(mtext)
        VGroup(*mtexts).arrange(RIGHT, buff=0.2).next_to(numbers[2], 2 * RIGHT)
        self.play(*[FadeIn(mtext) for mtext in mtexts], run_time=0.5)
        self.next_slide()

        to_gray = VGroup(mtexts[0], mtexts[2])
        self.play(to_gray.animate.set_color(DARK_GRAY))
        self.next_slide()

        sbc = Text(
            "classification (A|B)",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(mtexts[0], 0.5 * DOWN, aligned_edge=LEFT)
        target = Text(
            "targeted simulation: A to B",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(sbc, RIGHT, buff=1)
        self.play(AddTextLetterByLetter(sbc), run_time=0.5)
        self.next_slide()

        self.play(AddTextLetterByLetter(target), run_time=0.5)
        self.next_slide()

        feats = content[2].copy()
        feats_ = content[2].copy()
        self.play(
            feats.animate.set_y(no_F.get_y()),
            feats_.animate.set_y(mtexts[0].get_y()),
        )
        self.next_slide()


class Systems(Slide):  # 17

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("17", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        title = Text(
            "example: nanoporous materials",
            font="Open Sans",
            font_size=250,
            color=BLACK,
            z_index=1,
        ).scale(0.1 * 3 / 2).to_corner(UL)
        self.play(AddTextLetterByLetter(title, run_time=0.3))
        self.next_slide()

        blocks = ImageMobject('images/mofs/blocks.png').scale(0.22).shift(3 * LEFT + DOWN / 2)
        self.add(blocks)
        self.play(Wait())
        self.next_slide()

        mof = ImageMobject('images/mofs/mof5.png').scale(0.8).shift(3.5 * RIGHT + DOWN / 2)
        self.add(mof)
        self.play(Wait())
        self.next_slide()

        self.remove(mof)
        mof = ImageMobject('images/mofs/hkust1.png').scale(0.5).shift(4 * RIGHT + DOWN / 2)
        self.add(mof)
        self.play(Wait())
        self.next_slide()

        self.remove(mof)
        mof = ImageMobject('images/mofs/uio.png').scale(0.5).shift(4 * RIGHT + DOWN / 2)
        self.add(mof)
        self.play(Wait())
        self.next_slide()

        self.remove(mof)
        mof = ImageMobject('images/mofs/mil53.png').scale(0.3).shift(4 * RIGHT + DOWN / 2)
        self.add(mof)
        self.play(Wait())
        self.next_slide()


class QM(Slide):  # 18

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("18", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        title = Text(
            "QM is expensive",
            font="Open Sans",
            font_size=250,
            color=BLACK,
            z_index=1,
        ).scale(0.1 * 3 / 2).to_corner(UL)
        self.add(title)

        axes = Axes(
            (1.0, 3), (0, 30),
            axis_config={'stroke_color': BLACK, 'include_ticks': False},
        ).scale(0.7).shift(0.5 * DOWN)
        graph = axes.plot(
            lambda x: x ** 3,
            color=NUCLEUS_COLOR,
            x_range=[1, 3],
        ).set_z_index(4)
        ylabel = Text(
            "evaluation time",
            font='Open Sans',
            font_size=300,
            fill_color=BLACK,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_y_axis().get_end(), UP)
        xlabel = Text(
            "#atoms",
            font='Open Sans',
            font_size=300,
            fill_color=BLACK,
            fill_opacity=1.0,
        ).scale(0.1).next_to(axes.get_x_axis().get_end(), DOWN)

        self.play(Write(axes), run_time=0.4)
        self.play(AddTextLetterByLetter(xlabel), Write(ylabel), run_time=0.4)
        self.next_slide()

        self.play(Create(graph), run_time=0.5)
        self.next_slide()


class HPC(Slide):  # 19

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("19", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        axes = ImageMobject('images/top500_Layer_1.png')
        data = ImageMobject('images/top500_Layer_2.png')
        Group(axes, data).shift(0.5 * DOWN + 0.5 * RIGHT)
        self.add(axes)
        self.play(Wait())
        self.next_slide()
        self.add(data)
        self.play(Wait())
        self.next_slide()


class LUMI(Slide):  # 20

    def construct(self):
        self.wait_time_between_slides = 0.05
        image = ImageMobject('images/lumi.jpg').scale(0.5)
        self.add(image)
        self.play(Wait())
        self.next_slide()


class OnlineLearning(Slide):  # 21

    def new_walkers(self, nwalkers):
        walkers = VGroup(*[Dot(color=BLACK, z_index=1) for i in range(nwalkers)])
        walkers.arrange(DOWN, buff=0.09).to_edge(LEFT)
        walkers.shift(DOWN)
        return walkers

    def propagate(self, walkers, quality):
        lines = []
        start_list = [w.get_center() for w in walkers]
        offset = np.array([0.001, 0, 0])
        for i, walker in enumerate(walkers):
            line = Line(color=quality, z_index=0)

            def updater(m, index):
                start = start_list[index] - offset  # manim does not like zero-length lines
                end = walkers[index].get_center()
                m.put_start_and_end_on(
                    start,
                    end,
                )
            line.add_updater(partial(updater, index=i))
            lines.append(line)
        return lines

    def sample_data(self, walkers, quality):
        data = VGroup(*[w.copy() for w in walkers])
        self.play(data.animate.shift(4 * RIGHT), run_time=0.5)
        squares = []
        for i, dot in enumerate(data):
            square = Square(0.15, fill_color=quality, fill_opacity=1.0, stroke_opacity=0.0)
            squares.append(square)
            square.move_to(dot.get_center())
        squares = VGroup(*squares)
        self.play(ReplacementTransform(data, squares), run_time=0.5)
        self.next_slide()
        return squares

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("20", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        circle = Circle(
            radius=0.25,
            fill_color=BLACK,
            fill_opacity=1.0,
            stroke_color=BLACK,
            z_index=0,
        ).to_corner(UL)
        number = Text(
            "1",
            font="Open Sans",
            font_size=250,
            color=WHITE,
            z_index=1,
            weight="BOLD",
        ).scale(0.1)
        number.move_to(circle.get_center()).shift(0.02 * LEFT)
        self.add(number, circle)

        title = Text(
            "generating training data",
            font="Open Sans",
            font_size=250,
            color=BLACK,
            z_index=1,
        ).scale(0.1 * 3 / 2).next_to(circle, RIGHT)
        self.play(AddTextLetterByLetter(title, run_time=0.3))
        self.next_slide()

        basket = [
            Line(ORIGIN, DOWN, color=BLACK),
            Line(DOWN, DOWN + RIGHT, color=BLACK),
            Line(DOWN + RIGHT, RIGHT, color=BLACK),
        ]
        width = 2
        basket = VGroup(*basket).scale(width).set_x(6)
        data = Text("data", font='Open Sans', font_size=250, color=BLACK).scale(0.1)
        data.next_to(basket, DOWN)
        basket.add(data)
        self.play(*[Create(b) for b in basket], run_time=0.5)
        self.next_slide()

        model_quality = Text(
            'GNN quality: ',
            font='Open Sans',
            font_size=250,
            color=BLACK,
        ).scale(0.1).to_corner(UR).shift(2 * LEFT)
        bad = Text(
            'bad',
            font='Open Sans',
            font_size=250,
            color=BAD,
            weight="BOLD",
        ).scale(0.1).next_to(model_quality, RIGHT)
        self.play(AddTextLetterByLetter(model_quality), run_time=0.4)
        self.play(AddTextLetterByLetter(bad), run_time=0.1)
        self.next_slide()

        nwalkers = 20
        walkers = self.new_walkers(nwalkers)
        self.play(*[Create(w) for w in walkers], run_time=1.0)
        self.next_slide()

        lines = self.propagate(walkers, quality=BAD)
        self.add(*lines)
        self.play(*[w.animate.shift(RIGHT) for w in walkers], run_time=1)
        self.next_slide()

        squares = self.sample_data(walkers, BAD)
        final_BAD = VGroup(*[s.copy() for s in squares]).scale(0.8)
        final_BAD.arrange_in_grid(cols=10, buff=0.05).next_to(basket[1], UP)
        self.play(ReplacementTransform(squares, final_BAD), run_time=0.5)
        self.next_slide()

        x = walkers.get_x()
        walkers = self.new_walkers(nwalkers).set_x(x)
        self.play(*[w.animate.shift(0.3 * RIGHT) for w in walkers], run_time=0.3)
        self.next_slide()

        mid = Text(
            'mid',
            font='Open Sans',
            font_size=250,
            color=MID,
            weight="BOLD",
        ).scale(0.1).next_to(model_quality, RIGHT)
        self.play(ReplacementTransform(bad, mid))
        self.next_slide()

        lines = self.propagate(walkers, quality=MID)
        self.add(*lines)
        self.play(*[w.animate.shift(2 * RIGHT) for w in walkers], run_time=1)
        self.next_slide()

        squares = self.sample_data(walkers, MID)
        final_MID = VGroup(*[s.copy() for s in squares]).scale(0.8)
        final_MID.arrange_in_grid(cols=10, buff=0.05).next_to(final_BAD, UP)
        self.play(ReplacementTransform(squares, final_MID), run_time=0.5)
        self.next_slide()

        x = walkers.get_x()
        walkers = self.new_walkers(nwalkers).set_x(x)
        self.play(*[w.animate.shift(0.3 * RIGHT) for w in walkers], run_time=0.3)
        self.next_slide()

        pro = Text(
            'high',
            font='Open Sans',
            font_size=250,
            color=PRO,
            weight="BOLD",
        ).scale(0.1).next_to(model_quality, RIGHT)
        self.play(ReplacementTransform(mid, pro))
        self.next_slide()

        lines = self.propagate(walkers, quality=PRO)
        self.add(*lines)
        self.play(*[w.animate.shift(3 * RIGHT) for w in walkers], run_time=1)
        self.next_slide()

        squares = self.sample_data(walkers, PRO)
        final_PRO = VGroup(*[s.copy() for s in squares]).scale(0.8)
        final_PRO.arrange_in_grid(cols=10, buff=0.05).next_to(final_MID, UP)
        self.play(ReplacementTransform(squares, final_PRO), run_time=0.5)
        self.next_slide()


class Hardware(Slide):  # 22

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("22", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        title = Text(
            "... but on a supercomputer?",
            font="Open Sans",
            font_size=200,
            color=BLACK,
            z_index=1,
        ).scale(0.1 * 3 / 2).to_corner(UL)
        self.add(title)

        image = None
        for i in range(8):
            path = f'images/hardware/workflow_Layer_{i + 1}.png'
            # if image is not None:
            #     self.remove(image)
            image = ImageMobject(path).scale(0.6).shift(0.5 * DOWN)
            self.add(image)
            self.play(Wait())
            self.next_slide()


class Psiflow(Slide):  # 23

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("23", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        image = ImageMobject('images/logo_light.png').scale_to_fit_width(14)
        self.add(image)
        self.play(Wait())
        self.next_slide()


class ThreeReview(Slide):  # 24

    def gnn(self):
        message_passing = Text(
            "message passing:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1)
        from_xyz = Tex(r"$\text{\sffamily XYZ} \longrightarrow \quad$").next_to(message_passing, RIGHT)
        squares = []
        for color in MESSAGE_COLORS:
            square = Square(
                0.3,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            squares.append(square)
        feats = VGroup(*squares[::-1]).arrange(DOWN, buff=0).next_to(from_xyz, RIGHT)

        readout = Text(
            "readout:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1).next_to(message_passing, 3 * DOWN, aligned_edge=LEFT)
        f_read = Tex(r"$f_{\text{\sffamily read}}(\quad) = E_i$").next_to(readout, 2 * RIGHT)
        arg = feats.copy().move_to(f_read.get_center() + 0.14 * LEFT)

        content = VGroup(message_passing, from_xyz, feats, readout, f_read, arg)
        border = SurroundingRectangle(content, color=WHITE, buff=0.2)
        title = Text(
            "GNN",
            font='Open Sans',
            font_size=250,
            weight="BOLD",
        ).scale(0.1).next_to(border, 0.5 * UP, aligned_edge=LEFT)
        return content, border, title

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("24", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        title = Text(
            "so... the phd itself?",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        content, border, title = self.gnn()
        gnn = VGroup(content, border, title).center()
        self.add(content, gnn)

        numbers = []
        for i in range(3):
            circle = Circle(
                radius=0.25,
                fill_color=WHITE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                z_index=0,
            )
            number = Text(
                str(i + 1),
                font="Open Sans",
                font_size=250,
                color=BLACK,
                z_index=1,
                weight="BOLD",
            ).scale(0.1)
            number.move_to(circle.get_center())
            if i == 0:
                number.shift(0.02 * LEFT)
            numbers.append(VGroup(number, circle))
        gnumbers = VGroup(*numbers).arrange(DOWN, buff=1.5).shift(6.5 * LEFT + 0.5 * DOWN)
        gnn.scale(0.7).to_corner(UR)
        self.add(*[e for n in numbers for e in n])

        training = r"$\text{\sffamily GNN} \longleftarrow"
        training += r"\left\{\text{\sffamily XYZ}, E, \vec{F}\right\}$"
        training = Tex(training, tex_template=tex_template).next_to(numbers[0], RIGHT)
        self.add(training.scale(0.9))
        catch = Text(
            "on-the-fly learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(training, 0.5 * DOWN, aligned_edge=LEFT)
        self.add(catch)

        no_F = Text(
            "most accurate QM methods can only do ",
            color=WHITE,
            font='Open Sans',
            font_size=200,
        ).scale(0.1 * 3 / 2).next_to(numbers[1], 2 * RIGHT)
        F = Tex(r"$\left\{\text{\sffamily XYZ}, E\right\}$", tex_template=tex_template).next_to(
            no_F,
            RIGHT,
        ).shift(0.0 * UP)
        transfer = Text(
            "transfer learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(no_F, 0.5 * DOWN, aligned_edge=LEFT)
        self.add(no_F)
        self.add(F)
        # self.play(AddTextLetterByLetter(transfer, run_time=0.3))

        texts = ['computational cost = ', '# steps ', ' x  (cost/step)']
        mtexts = []
        for text in texts:
            mtext = Text(
                text,
                font='Open Sans',
                font_size=200,
                fill_color=WHITE,
                fill_opacity=1.0,
            ).scale(0.1 * 3 / 2)
            mtexts.append(mtext)
        VGroup(*mtexts).arrange(RIGHT, buff=0.2).next_to(numbers[2], 2 * RIGHT)
        self.add(*mtexts)

        to_gray = VGroup(mtexts[0], mtexts[2])
        to_gray.set_color(DARK_GRAY)
        self.play(Wait())
        self.next_slide()

        feats = content[2].copy()
        feats_ = content[2].copy()
        self.play(
            feats.animate.set_y(no_F.get_y()),
            feats_.animate.set_y(mtexts[0].get_y()),
        )
        self.next_slide()


class Movie(Slide):  # 25

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("25", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        self.play(Wait())
        self.next_slide()

        files = sorted(list(glob.glob('images/movie/frame_*.jpg')))
        block = 30
        for block_index in range(len(files) // block + 1):
            start = block_index * block
            stop = min((block_index + 1) * block, len(files))
            print(files[start:stop])
            images = [ImageMobject(file).scale(0.9) for file in files[start:stop]]
            anims = []
            for image in images:
                anims.append(FadeIn(image, run_time=0.001))
                anims.append(Wait(1 / 30))
            self.play(Succession(*anims), run_time=block / 20)  # somehow breaks at 30?
            for image in images[:-1]:  # keep last image to not have flashing white screen
                self.remove(image)
        self.next_slide()


class Features(Slide):  # 26

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("26", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        reaction = ImageMobject('images/zeo_isobutene.png').scale(0.6)
        reaction.to_corner(UL, buff=0.1)
        self.add(reaction)
        self.play(Wait())
        self.next_slide()

        for i in range(5):
            path = f'images/scatter_Layer_{i + 1}.png'
            image = ImageMobject(path).scale(0.7).to_corner(DR, buff=0.1)
            self.add(image)
            self.play(Wait())
            self.next_slide()


class DeltaLearning(Slide):  # 27

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("27", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        title = Text(
            "good = bad + (good - bad)",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        message_passing = Text(
            "message passing:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1)
        from_xyz = Tex(r"$\text{\sffamily XYZ} \longrightarrow \quad$").next_to(message_passing, RIGHT)
        squares = []
        for color in MESSAGE_COLORS:
            square = Square(
                0.3,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            squares.append(square)
        feats = VGroup(*squares[::-1]).arrange(DOWN, buff=0).next_to(from_xyz, RIGHT)

        readout = Text(
            "readout:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1).next_to(message_passing, 3 * DOWN, aligned_edge=LEFT)
        f_read = Tex(r"$f_{\text{\sffamily read}}(\quad) = E_i$").next_to(readout, 2 * RIGHT)
        arg = feats.copy().move_to(f_read.get_center() + 0.14 * LEFT)
        content = VGroup(message_passing, from_xyz, feats, readout, f_read, arg)
        content.center()
        self.add(content)
        self.play(Wait())
        self.next_slide()

        _99 = Text(
            '~99% of the weights',
            font='Open Sans',
            font_size=250,
            color=ELECTRON_COLOR,
        ).scale(0.1).next_to(message_passing, LEFT, buff=0.5)
        _1 = Text(
            '~1% of the weights',
            font='Open Sans',
            font_size=250,
            color=ELECTRON_COLOR,
        ).scale(0.1).next_to(readout, LEFT, buff=0.5)
        self.play(AddTextLetterByLetter(_99), run_time=0.4)
        self.play(AddTextLetterByLetter(_1), run_time=0.4)
        self.next_slide()

        delta = Text(
            "delta:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1).next_to(readout, 3 * DOWN, aligned_edge=LEFT)
        f_delta = Tex(r"$f_{\text{\sffamily delta}}(\quad) = \Delta E_i$").next_to(delta, 2 * RIGHT)
        arg = feats.copy().move_to(f_delta.get_center() + 0.27 * LEFT)
        gdelta = VGroup(delta, f_delta, arg)
        self.play(FadeIn(gdelta), run_time=0.5)
        self.next_slide()

        border = SurroundingRectangle(content + gdelta, color=WHITE, buff=0.2)
        title = Text(
            "augmented GNN",
            font='Open Sans',
            font_size=250,
            weight="BOLD",
        ).scale(0.1).next_to(border, 0.5 * UP, aligned_edge=LEFT)
        self.play(Create(border), FadeIn(title), run_time=0.5)
        self.next_slide()


class DeltaLearningFigure(Slide):  # 28

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("28", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        for i in range(4):
            path = f'images/delta_learning_Layer_{i + 1}.png'
            image = ImageMobject(path).scale(0.6)
            self.add(image)
            self.play(Wait())
            self.next_slide()


class IsobuteneProfile(Slide):  # 29

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("29", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        reaction = ImageMobject('images/zeo_isobutene_cation.png').scale(0.55).to_edge(LEFT)
        self.add(reaction)
        self.play(Wait())
        self.next_slide()

        profile = ImageMobject('images/reaction_profile/reaction_profile.png').scale(1.0)
        profile.to_edge(RIGHT, buff=0.1)
        self.add(profile)
        self.play(Wait())
        self.next_slide()


class ThreeFinal(Slide):  # 30

    def gnn(self):
        message_passing = Text(
            "message passing:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1)
        from_xyz = Tex(r"$\text{\sffamily XYZ} \longrightarrow \quad$").next_to(message_passing, RIGHT)
        squares = []
        for color in MESSAGE_COLORS:
            square = Square(
                0.3,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            squares.append(square)
        feats = VGroup(*squares[::-1]).arrange(DOWN, buff=0).next_to(from_xyz, RIGHT)

        readout = Text(
            "readout:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1).next_to(message_passing, 3 * DOWN, aligned_edge=LEFT)
        f_read = Tex(r"$f_{\text{\sffamily read}}(\quad) = E_i$").next_to(readout, 2 * RIGHT)
        arg = feats.copy().move_to(f_read.get_center() + 0.14 * LEFT)

        content = VGroup(message_passing, from_xyz, feats, readout, f_read, arg)
        border = SurroundingRectangle(content, color=WHITE, buff=0.2)
        title = Text(
            "GNN",
            font='Open Sans',
            font_size=250,
            weight="BOLD",
        ).scale(0.1).next_to(border, 0.5 * UP, aligned_edge=LEFT)
        return content, border, title

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("30", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        title = Text(
            "so... the phd itself?",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        content, border, title = self.gnn()
        gnn = VGroup(content, border, title).center()
        self.add(content, gnn)

        numbers = []
        for i in range(3):
            circle = Circle(
                radius=0.25,
                fill_color=WHITE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                z_index=0,
            )
            number = Text(
                str(i + 1),
                font="Open Sans",
                font_size=250,
                color=BLACK,
                z_index=1,
                weight="BOLD",
            ).scale(0.1)
            number.move_to(circle.get_center())
            if i == 0:
                number.shift(0.02 * LEFT)
            numbers.append(VGroup(number, circle))
        gnumbers = VGroup(*numbers).arrange(DOWN, buff=1.5).shift(6.5 * LEFT + 0.5 * DOWN)
        gnn.scale(0.7).to_corner(UR)
        self.add(*[e for n in numbers for e in n])

        training = r"$\text{\sffamily GNN} \longleftarrow"
        training += r"\left\{\text{\sffamily XYZ}, E, \vec{F}\right\}$"
        training = Tex(training, tex_template=tex_template).next_to(numbers[0], RIGHT)
        self.add(training.scale(0.9))
        catch = Text(
            "on-the-fly learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(training, 0.5 * DOWN, aligned_edge=LEFT)
        self.add(catch)

        no_F = Text(
            "most accurate QM methods can only do ",
            color=WHITE,
            font='Open Sans',
            font_size=200,
        ).scale(0.1 * 3 / 2).next_to(numbers[1], 2 * RIGHT)
        F = Tex(r"$\left\{\text{\sffamily XYZ}, E\right\}$", tex_template=tex_template).next_to(
            no_F,
            RIGHT,
        ).shift(0.0 * UP)
        transfer = Text(
            "transfer learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(no_F, 0.5 * DOWN, aligned_edge=LEFT)
        self.add(no_F)
        self.add(F)
        self.add(transfer)

        texts = ['computational cost = ', '# steps ', ' x  (cost/step)']
        mtexts = []
        for text in texts:
            mtext = Text(
                text,
                font='Open Sans',
                font_size=200,
                fill_color=WHITE,
                fill_opacity=1.0,
            ).scale(0.1 * 3 / 2)
            mtexts.append(mtext)
        VGroup(*mtexts).arrange(RIGHT, buff=0.2).next_to(numbers[2], 2 * RIGHT)
        self.add(*mtexts)

        to_gray = VGroup(mtexts[0], mtexts[2])
        to_gray.set_color(DARK_GRAY)
        feats = content[2].copy().set_y(no_F.get_y())
        feats_ = content[2].copy().set_y(mtexts[0].get_y())
        self.add(feats)
        self.add(feats_)

        self.play(Wait())
        self.next_slide()

        sbc = Text(
            "classification (A|B)",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(mtexts[0], 0.5 * DOWN, aligned_edge=LEFT)
        target = Text(
            "targeted simulation: A to B",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(sbc, RIGHT, buff=1)
        self.play(AddTextLetterByLetter(sbc), run_time=0.5)
        self.play(AddTextLetterByLetter(target), run_time=0.5)
        self.next_slide()


class IsobuteneBasins(Slide):  # 31

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("31", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        reaction = ImageMobject('images/zeo_isobutene_cation.png').scale(0.55).to_edge(LEFT)
        self.add(reaction)
        self.play(Wait())
        self.next_slide()

        for i in range(3):
            path = f'images/coordination_labeled_Layer_{i + 1}.png'
            image = ImageMobject(path).scale(0.65).to_edge(RIGHT, buff=0.1)
            self.add(image)
            self.play(Wait())
            self.next_slide()


class ManualLikelihood(Slide):  # 32

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("32", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        title = Text(
            "previously: based on human intuition",
            font='Open Sans',
            color=BLACK,
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)
        self.play(Wait())
        self.next_slide()

        image = ImageMobject('images/likelihood_manual.png').scale(0.8).shift(0.5 * DOWN)
        self.add(image)
        self.play(Wait())
        self.next_slide()


class PhaseLearningFigure(Slide):  # 33

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("33", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        title = Text(
            "train 'likelihood' functions!",
            font='Open Sans',
            color=BLACK,
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)
        self.play(Wait())
        self.next_slide()

        for i in range(4):
            path = f'images/logits_Layer_{i + 1}.png'
            image = ImageMobject(path).scale(0.6)
            self.add(image)
            self.play(Wait())
            self.next_slide()

        # preprint = Text(
        #     "arXiv:2404.03777 (April 2024)"
        # )


class LearnedLikelihood(Slide):  # 34

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("34", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        title = Text(
            "consider difference in (log) likelihood!",
            font='Open Sans',
            color=BLACK,
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        image = ImageMobject('images/likelihood_learned.png').scale(0.7).shift(0.5 * DOWN)
        self.add(image)
        self.play(Wait())
        self.next_slide()

        self.play(image.animate.scale(0.7).to_edge(LEFT, buff=0.1), run_time=0.4)
        manual = ImageMobject('images/likelihood_manual.png').scale(0.49)
        manual.set_y(image.get_y()).to_edge(RIGHT, buff=0.1)
        self.play(FadeIn(manual), run_time=0.2)
        self.next_slide()


class MIL53(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("34", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        title = Text(
            "not limited to chemical reactions!",
            font='Open Sans',
            color=BLACK,
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        mil = ImageMobject('images/mil53.png').scale(0.4).to_edge(LEFT, buff=0.1)
        self.add(mil)
        self.play(Wait())
        self.next_slide()

        scatter = ImageMobject('images/mil53_scatter.png').scale(0.5)
        scatter.to_edge(RIGHT, buff=0.1).set_y(mil.get_y())
        self.add(scatter)
        self.play(Wait())
        self.next_slide()


class Learning(Slide):  # 35

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("35", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        for i in range(5):
            path = f'images/learning_{i + 1}.png'
            image = ImageMobject(path).scale(0.6)
            self.add(image)
            self.play(Wait())
            self.next_slide()


class Performance(Slide):  # 36

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("36", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)

        items = [
            'additional computational cost ~ 0',
            '"end-to-end" from XYZ',
            'respects physical symmetries (!)',
            'reactive/solid-state/conformational',
            'data-efficient (exploits learned features)',
        ]
        texts = []
        for item in items:
            text = Text(
                item,
                font='Open Sans',
                font_size=200,
                color=NUCLEUS_COLOR,
            ).scale(0.1 * 3 / 2)
            texts.append(text)

        texts = VGroup(*texts).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(
            LEFT,
            buff=0.5,
        )
        self.play(FadeIn(texts), run_time=0.5)
        self.next_slide()

        image = ImageMobject('images/table.png').scale(0.5).to_edge(RIGHT, buff=0.1)
        self.play(FadeIn(image), run_time=0.5)
        self.next_slide()


class ThreeFinal(Slide):  # 37

    def gnn(self):
        message_passing = Text(
            "message passing:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1)
        from_xyz = Tex(r"$\text{\sffamily XYZ} \longrightarrow \quad$").next_to(message_passing, RIGHT)
        squares = []
        for color in MESSAGE_COLORS:
            square = Square(
                0.3,
                stroke_color=WHITE,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=1.5,
            )
            squares.append(square)
        feats = VGroup(*squares[::-1]).arrange(DOWN, buff=0).next_to(from_xyz, RIGHT)

        readout = Text(
            "readout:",
            font='Open Sans',
            font_size=250,
        ).scale(0.1).next_to(message_passing, 3 * DOWN, aligned_edge=LEFT)
        f_read = Tex(r"$f_{\text{\sffamily read}}(\quad) = E_i$").next_to(readout, 2 * RIGHT)
        arg = feats.copy().move_to(f_read.get_center() + 0.14 * LEFT)

        content = VGroup(message_passing, from_xyz, feats, readout, f_read, arg)
        border = SurroundingRectangle(content, color=WHITE, buff=0.2)
        title = Text(
            "GNN",
            font='Open Sans',
            font_size=250,
            weight="BOLD",
        ).scale(0.1).next_to(border, 0.5 * UP, aligned_edge=LEFT)
        return content, border, title

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("38", font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))
        title = Text(
            "so... the phd itself?",
            font='Open Sans',
            font_size=250,
        ).scale(0.13).to_corner(UL)
        self.add(title)

        content, border, title = self.gnn()
        gnn = VGroup(content, border, title).center()
        self.add(content, gnn)

        numbers = []
        for i in range(3):
            circle = Circle(
                radius=0.25,
                fill_color=WHITE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                z_index=0,
            )
            number = Text(
                str(i + 1),
                font="Open Sans",
                font_size=250,
                color=BLACK,
                z_index=1,
                weight="BOLD",
            ).scale(0.1)
            number.move_to(circle.get_center())
            if i == 0:
                number.shift(0.02 * LEFT)
            numbers.append(VGroup(number, circle))
        gnumbers = VGroup(*numbers).arrange(DOWN, buff=1.5).shift(6.5 * LEFT + 0.5 * DOWN)
        gnn.scale(0.7).to_corner(UR)
        self.add(*[e for n in numbers for e in n])

        training = r"$\text{\sffamily GNN} \longleftarrow"
        training += r"\left\{\text{\sffamily XYZ}, E, \vec{F}\right\}$"
        training = Tex(training, tex_template=tex_template).next_to(numbers[0], RIGHT)
        self.add(training.scale(0.9))
        catch = Text(
            "on-the-fly learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(training, 0.5 * DOWN, aligned_edge=LEFT)
        self.add(catch)

        no_F = Text(
            "most accurate QM methods can only do ",
            color=WHITE,
            font='Open Sans',
            font_size=200,
        ).scale(0.1 * 3 / 2).next_to(numbers[1], 2 * RIGHT)
        F = Tex(r"$\left\{\text{\sffamily XYZ}, E\right\}$", tex_template=tex_template).next_to(
            no_F,
            RIGHT,
        ).shift(0.0 * UP)
        transfer = Text(
            "transfer learning!",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(no_F, 0.5 * DOWN, aligned_edge=LEFT)
        self.add(no_F)
        self.add(F)
        self.add(transfer)

        texts = ['computational cost = ', '# steps ', ' x  (cost/step)']
        mtexts = []
        for text in texts:
            mtext = Text(
                text,
                font='Open Sans',
                font_size=200,
                fill_color=WHITE,
                fill_opacity=1.0,
            ).scale(0.1 * 3 / 2)
            mtexts.append(mtext)
        VGroup(*mtexts).arrange(RIGHT, buff=0.2).next_to(numbers[2], 2 * RIGHT)
        self.add(*mtexts)

        to_gray = VGroup(mtexts[0], mtexts[2])
        to_gray.set_color(DARK_GRAY)
        feats = content[2].copy().set_y(no_F.get_y())
        feats_ = content[2].copy().set_y(mtexts[0].get_y())
        self.add(feats)
        self.add(feats_)

        sbc = Text(
            "classification (A|B)",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(mtexts[0], 0.5 * DOWN, aligned_edge=LEFT)
        target = Text(
            "targeted simulation: A to B",
            color=ELECTRON_COLOR,
            font='Open Sans',
            font_size=300,
        ).scale(0.1).next_to(sbc, RIGHT, buff=1)
        self.play(AddTextLetterByLetter(sbc), run_time=0.5)
        self.play(AddTextLetterByLetter(target), run_time=0.5)
        self.play(Wait())
        self.next_slide()


class Acknowledgements(Slide):

    def construct(self):
        self.wait_time_between_slides = 0.05
        self.add(Text("35", color=BLACK, font_size=SLIDE_NUMBER_FONTSIZE).to_corner(DR))

        background = Square(15, fill_color=WHITE, fill_opacity=1.0, z_index=-1)
        self.add(background)
        group = ImageMobject('images/group_picture.jpg')
        self.add(group)
        self.play(Wait())
        self.next_slide()

        self.remove(group)
        self.play(Wait())
        self.next_slide()

        typst = ImageMobject('images/typst.png', z_index=2).scale(0.7)
        _3b1b  = ImageMobject('images/sanderson.jpeg', z_index=2).scale(2)
        Group(_3b1b, typst).arrange(RIGHT)
        text = Text(
            'Grant Sanderson',
            font='Open Sans',
            font_size=200,
            color=BLACK,
            z_index=3,
        ).scale(0.1 * 3 / 2).next_to(_3b1b, DOWN)
        self.play(FadeIn(_3b1b), FadeIn(text), run_time=0.5)
        self.next_slide()

        text = Text(
            'Typst',
            font='Open Sans',
            font_size=200,
            color=BLACK,
            z_index=3,
        ).scale(0.1 * 3 / 2).next_to(typst, DOWN)
        self.play(FadeIn(typst), FadeIn(text), run_time=0.5)
        self.next_slide()
