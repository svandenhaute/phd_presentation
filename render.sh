#!/bin/bash


set -e

# slides="Title Particles PeriodicTable Masses Dynamics OverviewPhysics TimeEvolution TimeScales Overview HydrogenRevisited Priors Dimensionality Images GNN"
slides="OnlineLearning"

export PYTHONPATH=$(pwd):$PYTHONPATH
manim render --fps 30 -r "1280,720" scene.py $slides
# manim-slides convert $slides --to=html scene.html
manim-slides present --hide-info-window $slides
