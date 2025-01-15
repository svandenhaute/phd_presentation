from functools import partial

import numpy as np

from manim import Circle, Square, WHITE, Text, VGroup, DOWN, BLACK, ManimColor


NUCLEUS_COLOR = ManimColor.from_rgb((237, 105, 52))
ELECTRON_COLOR = ManimColor.from_rgb((37, 161, 219))


def get_text(
    title,
    bullets,
    title_color=WHITE,
    scale=1.0,
):
    # avoid weird kerning by using very large font with downscaling
    first = Text(
        title,
        font='Open Sans',
        font_size=250,
        fill_color=title_color,
        fill_opacity=1.0,
        weight="BOLD",
    ).scale(0.1)
    items = []
    for bullet in bullets:
        item = Text(
            bullet,
            font='Open Sans',
            font_size=200,
            fill_color=title_color,
            fill_opacity=1.0,
            weight="BOOK",
        ).scale(0.1)
        items.append(item)
    all_text = VGroup(first, *items)
    all_text.scale(scale)
    all_text.arrange_in_grid(
        rows=1 + len(bullets),
        columns=1,
        col_alignments='l',
        buff=0.2,
    )
    return all_text


get_nucleus_text = partial(
    get_text,
    title="nucleus",
    bullets=["positively charged", "heavy"],
    title_color=NUCLEUS_COLOR,
)
get_electron_text = partial(
    get_text,
    title="electron",
    bullets=["negatively charged", "lightweight"],
    title_color=ELECTRON_COLOR,
)


def create_atom(
    num_electrons,
    radius,
    label=None,
    scale=0.9,
):
    circle = Circle(
        fill_color=WHITE,
        fill_opacity=0.0,
        stroke_color=WHITE,
        radius=radius,
        stroke_width=2.0,
    )
    particles = [get_nucleus()]
    positions = np.zeros((num_electrons + 1, 3))
    while len(particles) < num_electrons + 1:
        pos = np.random.uniform(
            low=(-scale * radius, -scale * radius, 0),
            high=(scale * radius, scale * radius, 0),
            size=(3,),
        ).reshape((1, 3))
        distances = np.linalg.norm(positions - pos, axis=1)
        if np.any(np.linalg.norm(positions - pos, axis=1) < 0.4):
            continue
        if np.linalg.norm(pos) > radius:
            continue
        if np.linalg.norm(pos) < 0.5:
            continue
        positions[len(particles), :] = pos[0]
        particles.append(get_electron())

    for i, particle in enumerate(particles):
        particle.move_to(positions[i])

    atom = VGroup(
        circle,
        *particles,
    )
    return atom


def create_circles(
    num_particles,
    width,
    height,
    scale,
    offset,
) -> list:
    circles = []
    positions = np.zeros((num_particles, 2))
    positions[:] = np.nan

    length_scale = np.sqrt(width * height / num_particles)
    print(length_scale)

    colors = [NUCLEUS_COLOR, ELECTRON_COLOR]
    while len(circles) < num_particles:
        color = colors[len(circles) % len(colors)]
        radius = 0.1

        start = (1 - scale) / 2
        stop = scale + (1 - scale) / 2

        pos = np.random.uniform(
            low=(start * width, start * height),
            high=(stop * width, stop * height),
            size=(2,),
        ).reshape(1, 2)
        if np.any(np.linalg.norm(positions - pos, axis=1) < 0.5 * length_scale):
            continue
        positions[len(circles), :] = pos[0]
        circle = Circle(
            fill_color=color,
            fill_opacity=1.0,
            radius=radius,
            stroke_opacity=0.0,
        )
        circle.set_x(pos[0, 0] + offset[0])
        circle.set_y(pos[0, 1] + offset[1])
        circles.append(circle)
    return circles


def get_particle(
    label,
    color,
    text_color,
    radius=1.0,
    scale=1.0,
):
    circle = Circle(
        fill_color=color,
        fill_opacity=1.0,
        radius=radius,
        stroke_opacity=0.0,
    )
    text = Text(
        label,
        font="Noto Sans",
        font_size=500,
        fill_color=text_color,
        fill_opacity=1.0,
    ).scale(0.1)
    text.move_to(circle.get_center())
    particle = VGroup(circle, text)
    particle.scale(scale)
    return particle


get_electron = partial(
    get_particle,
    label='-',
    color=ELECTRON_COLOR,
    text_color=WHITE,
    radius=0.17,
    scale=0.8
)

get_nucleus = partial(
    get_particle,
    label='+',
    color=NUCLEUS_COLOR,
    text_color=WHITE,
    radius=0.3,
)

get_atom = partial(
    get_particle,
    color=WHITE,
    text_color=BLACK,
    radius=0.5,
)


if __name__ == '__main__':
    pass
