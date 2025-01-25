#!/bin/sh
set -e

# Define slides as an array directly instead of a space-separated string
slides=(
    Title
    Particles
    PeriodicTable
    Masses
    Dynamics
    OverviewPhysics
    TimeEvolution
    TimeScales
    Overview
    HydrogenRevisited
    Priors
    Dimensionality
    Images
    Network
    GNN
    OverviewGNN
    Three
    Systems
    QM
    HPC
    LUMI
    OnlineLearning
    Hardware
    Psiflow
    ThreeReview
    Movie
    Features
    DeltaLearning
    DeltaLearningFigure
    IsobuteneProfile
    ThreeFinal
    IsobuteneBasins
    ManualLikelihood
    PhaseLearningFigure
    LearnedLikelihood
    MIL53
    Learning
    Performance
    ThreeFinal
    Acknowledgements
)
export PYTHONPATH=$(pwd):$PYTHONPATH

# Loop through array elements
for slide in "${slides[@]}"; do
    echo "Rendering slide: $slide"
    # manim render --fps 60 -r "1920,1080" scene.py "$slide"
done

# Pass array elements directly as arguments
manim-slides convert --to=HTML "${slides[@]}" scene.html
# manim-slides present --hide-mouse --hide-info-window "${slides[@]}"
