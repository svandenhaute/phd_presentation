#!/bin/env python

import argparse
import copy
import xml.etree.ElementTree as ET
import re
import cairosvg
import io
from PIL import Image
from pathlib import Path
from typing import Optional


def ensure_visibility(element):
    style = element.get('style', '')
    style = re.sub(r'display:\s*none;?', '', style).strip()
    if 'display:' not in style:
        style += ';display:inline' if style else 'display:inline'
    element.set('style', style)
    if 'display' in element.attrib:
        del element.attrib['display']


def parse_value(value):
    if value is None:
        return 0
    match = re.match(r"(-?[\d.]+)(\w*)", value)
    if match:
        number, unit = match.groups()
        number = float(number)
        # Convert to pixels (approximate)
        if unit == 'pt':
            return number * 1.33
        elif unit == 'pc':
            return number * 16
        elif unit == 'mm':
            return number * 3.779528
        elif unit == 'cm':
            return number * 37.79528
        elif unit == 'in':
            return number * 96
        else:
            return number
    return 0


def output_template(path_svg: Path, index: int, format: str) -> str:
    return path_svg.parent / (path_svg.stem + f'_{index}.{format}')


def split_svg_layers(path_svg: Path, dpi: int, separate: Optional[str] = None):
    tree = ET.parse(str(path_svg))
    root = tree.getroot()

    # Store original SVG attributes
    original_attrs = root.attrib.copy()

    # Find the main figure group
    figure_group = root.find(".//*[@id='figure_1']")
    if figure_group is None:
        print("Could not find the main figure group.")
        return

    # Find the axes group
    axes_group = figure_group.find(".//*[@id='axes_1']")
    if axes_group is None:
        print("Could not find the axes group.")
        return

    # Create background layer (everything except data layers)
    background_layer = copy.deepcopy(figure_group)
    bg_axes_group = background_layer.find(".//*[@id='axes_1']")

    # Identify and extract data layers
    data_layers = []
    for child in list(axes_group):
        if child.get('id', '').startswith('data_'):
            data_layer = ET.Element('g')
            data_layer.append(copy.deepcopy(child))
            data_layers.append(data_layer)
            bg_axes_group.remove(bg_axes_group.find(f".//*[@id='{child.get('id')}']"))

    # Prepare all layers
    all_layers = [background_layer] + data_layers

    for index, layer in enumerate(all_layers):
        # Create new SVG with original attributes
        new_svg = ET.Element('svg', original_attrs)
        new_svg.append(layer)

        # Ensure visibility of all elements
        for elem in new_svg.iter():
            ensure_visibility(elem)

        # Create SVG file
        new_tree = ET.ElementTree(new_svg)
        svg_output_path = output_template(path_svg, index=index + 1, format='svg')
        new_tree.write(str(svg_output_path), encoding='utf-8', xml_declaration=True)

        # Convert SVG to PNG
        png_output_path = output_template(path_svg, index=index + 1, format='png')
        cairosvg.svg2png(url=str(svg_output_path), write_to=str(png_output_path), dpi=dpi)

        # Process PNG to make white background transparent
        img = Image.open(png_output_path)
        img = img.convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        img.save(png_output_path, "PNG")
    print(f"Split and converted {len(all_layers)} layers from {path_svg}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--svg",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
    )
    parser.add_argument(
        "--separate",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    assert args.svg is not None

    split_svg_layers(
        Path(args.svg),
        dpi=args.dpi,
        separate=args.separate,
    )
