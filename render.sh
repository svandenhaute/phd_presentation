#!/bin/bash


set -e

# slides="Title Particles PeriodicTable Masses Dynamics OverviewPhysics TimeEvolution TimeScales Overview HydrogenRevisited Priors Dimensionality Images Network GNN OverviewGNN Three Systems QM HPC LUMI OnlineLearning Hardware Psiflow ThreeReview Movie Features DeltaLearning DeltaLearningFigure IsobuteneProfile"
slides="MIL53"

export PYTHONPATH=$(pwd):$PYTHONPATH
manim render --fps 30 -r "1280,720" scene.py $slides
# manim-slides convert $slides --to=pptx scene.pptx
manim-slides present --hide-info-window $slides
