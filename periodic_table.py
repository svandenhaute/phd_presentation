from manim import Square, Text, WHITE, VGroup, BLACK

from particles import ELECTRON_COLOR


elements = {
    'H': (1, 1, 1), 'He': (2, 1, 18),
    'Li': (3, 2, 1), 'Be': (4, 2, 2), 'B': (5, 2, 13), 'C': (6, 2, 14),
    'N': (7, 2, 15), 'O': (8, 2, 16), 'F': (9, 2, 17), 'Ne': (10, 2, 18),
    'Na': (11, 3, 1), 'Mg': (12, 3, 2), 'Al': (13, 3, 13), 'Si': (14, 3, 14),
    'P': (15, 3, 15), 'S': (16, 3, 16), 'Cl': (17, 3, 17), 'Ar': (18, 3, 18),
    'K': (19, 4, 1), 'Ca': (20, 4, 2), 'Sc': (21, 4, 3), 'Ti': (22, 4, 4),
    'V': (23, 4, 5), 'Cr': (24, 4, 6), 'Mn': (25, 4, 7), 'Fe': (26, 4, 8),
    'Co': (27, 4, 9), 'Ni': (28, 4, 10), 'Cu': (29, 4, 11), 'Zn': (30, 4, 12),
    'Ga': (31, 4, 13), 'Ge': (32, 4, 14), 'As': (33, 4, 15), 'Se': (34, 4, 16),
    'Br': (35, 4, 17), 'Kr': (36, 4, 18),
    'Rb': (37, 5, 1), 'Sr': (38, 5, 2), 'Y': (39, 5, 3), 'Zr': (40, 5, 4),
    'Nb': (41, 5, 5), 'Mo': (42, 5, 6), 'Tc': (43, 5, 7), 'Ru': (44, 5, 8),
    'Rh': (45, 5, 9), 'Pd': (46, 5, 10), 'Ag': (47, 5, 11), 'Cd': (48, 5, 12),
    'In': (49, 5, 13), 'Sn': (50, 5, 14), 'Sb': (51, 5, 15), 'Te': (52, 5, 16),
    'I': (53, 5, 17), 'Xe': (54, 5, 18),
    'Cs': (55, 6, 1), 'Ba': (56, 6, 2), 'Hf': (72, 6, 4), 'Ta': (73, 6, 5),
    'W': (74, 6, 6), 'Re': (75, 6, 7), 'Os': (76, 6, 8), 'Ir': (77, 6, 9),
    'Pt': (78, 6, 10), 'Au': (79, 6, 11), 'Hg': (80, 6, 12), 'Tl': (81, 6, 13),
    'Pb': (82, 6, 14), 'Bi': (83, 6, 15), 'Po': (84, 6, 16), 'At': (85, 6, 17),
    'Rn': (86, 6, 18),
    'Fr': (87, 7, 1), 'Ra': (88, 7, 2), 'Rf': (104, 7, 4), 'Db': (105, 7, 5),
    'Sg': (106, 7, 6), 'Bh': (107, 7, 7), 'Hs': (108, 7, 8), 'Mt': (109, 7, 9),
    'Ds': (110, 7, 10), 'Rg': (111, 7, 11), 'Cn': (112, 7, 12), 'Nh': (113, 7, 13),
    'Fl': (114, 7, 14), 'Mc': (115, 7, 15), 'Lv': (116, 7, 16), 'Ts': (117, 7, 17),
    'Og': (118, 7, 18)
}


def get_element(
    element,
    box_size,
    invert=False,
    use_number=False,
):
    if not invert:
        kwargs = dict(
            fill_color=WHITE,
            fill_opacity=0.0,
            stroke_color=WHITE,
            stroke_opacity=1.0,
            stroke_width=2.0
        )
    else:
        kwargs = dict(
            fill_color=WHITE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_opacity=1.0,
            stroke_width=2.0
        )
    square = Square(
        side_length=box_size,
        **kwargs,
    )
    if not invert:
        kwargs = dict(
            fill_color=WHITE,
            fill_opacity=1.0,
        )
    else:
        kwargs = dict(
            fill_color=BLACK,
            fill_opacity=1.0,
        )
    if not use_number:
        text = element
    else:
        assert not invert
        text = str(elements[element][0])
        kwargs['fill_color'] = ELECTRON_COLOR
    symbol = Text(
        text,
        font='Open Sans',
        font_size=250,
        **kwargs,
    ).scale(0.1).move_to(square.get_center())
    return symbol, square


def generate_periodic_table(**kwargs):
    boxes = {}
    box_size = 0.65
    for element, (atomic_num, row, col) in elements.items():
        x = (col - 1) * box_size
        y = (-1.0) * (row - 1) * box_size
        symbol, square = get_element(element, box_size, **kwargs)
        box = VGroup(symbol, square)
        box.move_to((x, y, 1))
        boxes[element] = (symbol, square)
    return boxes
