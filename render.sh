#!/bin/bash


set -e

slides="Masses"

manim render scene.py $slides --fps 30 -r "1280,720"
manim-slides convert $slides --to=html -cdata_uri=true scene.html
manim-slides present $slides
