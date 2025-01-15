import xml.etree.ElementTree as ET
import re
import argparse
import os
from pathlib import Path
import cairosvg

def hide_all_layers(root):
    """Hide all layers in the SVG"""
    ns = {'svg': 'http://www.w3.org/2000/svg',
          'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}
    
    for elem in root.findall(".//*[@inkscape:groupmode='layer']", ns):
        style = elem.get('style', '')
        # Remove any existing display properties
        style = re.sub(r'display:\s*[^;]+;?', '', style)
        # Add display:none
        style = (style + ';display:none').lstrip(';')
        elem.set('style', style)

def show_layer(layer):
    """Show specific layer and ensure it's visible"""
    style = layer.get('style', '')
    # Remove any display:none
    style = re.sub(r'display:\s*none;?', '', style)
    # Add display:inline
    style = (style + ';display:inline').lstrip(';')
    layer.set('style', style)

def process_svg(input_file, output_dir, output_format='svg', dpi=300):
    """Process SVG and split layers"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Register namespaces
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('sodipodi', "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
    ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")
    
    # Parse the SVG file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Define namespace dictionary
    ns = {'svg': 'http://www.w3.org/2000/svg',
          'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}
    
    # Find all layers
    layers = root.findall(".//*[@inkscape:groupmode='layer']", ns)
    
    if not layers:
        print("No layers found - processing entire SVG")
        output_path = Path(output_dir) / f"{Path(input_file).stem}.{output_format}"
        if output_format.lower() == 'png':
            # Convert entire SVG to PNG
            cairosvg.svg2png(
                url=input_file,
                write_to=str(output_path),
                scale=dpi/96.0
            )
        else:
            # Copy SVG as-is
            tree.write(output_path, encoding='unicode', xml_declaration=True)
        return

    # Process each layer
    for layer in layers:
        # Get layer label
        label = layer.get(f'{{{ns["inkscape"]}}}label', '')
        safe_label = re.sub(r'[^a-zA-Z0-9_-]', '_', label or f'layer_{layers.index(layer)}')
        
        # Create new SVG for this layer
        new_root = ET.Element('svg')
        # Copy SVG attributes
        for attr, value in root.attrib.items():
            new_root.set(attr, value)
        
        # Copy any defs section
        defs = root.find('svg:defs', ns)
        if defs is not None:
            new_root.append(ET.fromstring(ET.tostring(defs)))
        
        # First hide all layers in the new SVG
        for other_layer in root.findall(".//*[@inkscape:groupmode='layer']", ns):
            layer_copy = ET.fromstring(ET.tostring(other_layer))
            style = layer_copy.get('style', '')
            style = re.sub(r'display:\s*[^;]+;?', '', style)
            style = (style + ';display:none').lstrip(';')
            layer_copy.set('style', style)
            new_root.append(layer_copy)
        
        # Show only the current layer
        current_layer = new_root.findall(".//*[@inkscape:groupmode='layer']", ns)[layers.index(layer)]
        show_layer(current_layer)
        
        # Create output filename
        output_path = Path(output_dir) / f"{Path(input_file).stem}_{safe_label}.{output_format}"
        
        if output_format.lower() == 'png':
            # Save temporary SVG
            temp_svg = output_path.with_suffix('.svg')
            ET.ElementTree(new_root).write(temp_svg, encoding='unicode', xml_declaration=True)
            
            # Convert to PNG
            cairosvg.svg2png(
                url=str(temp_svg),
                write_to=str(output_path),
                scale=dpi/96.0
            )
            
            # Remove temporary SVG
            os.remove(temp_svg)
        else:
            # Save as SVG
            ET.ElementTree(new_root).write(output_path, encoding='unicode', xml_declaration=True)
        
        print(f"Processed layer: {label}")

def main():
    parser = argparse.ArgumentParser(
        description='Split Inkscape SVG layers into separate files.'
    )
    parser.add_argument('input_file', help='Input SVG file to process')
    parser.add_argument(
        '-o', '--output-dir',
        default='output',
        help='Output directory for split files (default: output)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['svg', 'png'],
        default='svg',
        help='Output format (default: svg)'
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='DPI for PNG output (default: 300)'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        return 1
    
    try:
        process_svg(args.input_file, args.output_dir, args.format, args.dpi)
        return 0
    except Exception as e:
        print(f"Error processing file: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
