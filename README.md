# Simulating Projection on Rotating Surface

<img src="https://github.com/ymilkessa/rotating-figures/blob/main/perspective_projection_demo.gif" width=500 />

## Summary
This codebase contains scripts that produce simple displays uing only ascii characters inside a gui.
Different characters represent different levels of illumination. The ones used are selected from `.,-~:;=!*#$@`,
which are taked from a more difficult projection by Andy Sloane [in this post](https://www.a1k0n.net/2011/07/20/donut-math.html).

The light source in all the scripts is somewhere to the left of the viewer. Some scripts use a parallel light source and are therefore simpler, whereas others use a point light source. Check the extended descriptions below on these two types of projection.

## Parallel Projection
In the "parallel projection" scripts, the incoming light has the same direction all over the surfaces. Furthermore, the images are produced by computing and rescaling the magnitude of light reflected toward a planar "viewing screen". Hence both the incoming light and the reflection are projected in parallel.

The result can be seen below. Notice that in each object, the character used is the same throughout during each snapshot.
<img src="https://github.com/ymilkessa/rotating-figures/blob/main/parallel_projection_demo.gif" width=550 />

## Point-Source Projection
In the "perspective projection" script, there is a fixed point light source, and a fixed point viewer. Hence the reflected magnitude is different across the surface. The clip at the very top shows the result of this script.

## How to run

First download the repo and cd into the main folder (duh).

For the first image above of the rotating disc with perspective projection:
```
python3 perspective_projection_disc.py
```

For the rotating disc and the square (with parallel projection):
```
python3 parallel_projection_figures.py
```

For just the rotating disc (without the square):
```
python3 parallel_projection_disc.py
```
