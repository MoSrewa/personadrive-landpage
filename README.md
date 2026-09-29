# PersonaDrive project page

Project page for our paper
[PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation](https://arxiv.org/abs/2606.12616).

Live at https://pervasiveautonomylab.github.io/personadrive-landpage/

It's a plain static page (HTML + CSS, Bulma from a CDN), so there is nothing to build. GitHub Pages serves it
straight from `main`.

## Running it locally

```
python3 -m http.server 8000
```

then open http://localhost:8000.

## Making changes

All the text, tables and links are in `index.html`. Edit, commit and push; Pages picks up the new version
within a minute or two.

The Code and Dataset buttons are greyed out for now. When those are public, drop the `is-disabled` class and add
an `href`.

Videos and figures live in `static/`. Every clip is there as WebM and MP4, plus a `.jpg` poster. We generate them
from our demo-video renders with `make_assets.py`, which needs our `video_generation` folder next to this repo, so
it won't run from a fresh clone.

## Citation

```bibtex
@article{srewa2026personadrive,
  title   = {PersonaDrive: Human-Style Retrieval-Augmented VLA Agents for Closed-Loop Driving Simulation},
  author  = {Srewa, Mahmoud and Iddamsetty, Praneetsai Vasu and Al Faruque, Mohammad Abdullah and Elmalaki, Salma},
  journal = {arXiv preprint arXiv:2606.12616},
  year    = {2026}
}
```

The page layout is adapted from the [Nerfies](https://github.com/nerfies/nerfies.github.io) project page
(CC BY-SA 4.0).
