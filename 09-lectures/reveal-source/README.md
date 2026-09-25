# Lecture 10 Reveal source

This deck was adapted from the instructor's COMP 536
`lectures/python-fundamentals/slides/modular-design-oop.qmd` at commit
`252e03df388899b0042d199f33805bc528bf08bd`. The copied SCSS theme and
tokens are local, so the COMP 521 build does not depend on the COMP 536 checkout.

COMP 521 adaptations add the Rectangle method and attribute sequence, naming
conventions, inheritance, and composition. They also correct the notebook
workflow for Project 3 and direct the lab to Part 5. The Ariane 5 slide follows
the [ESA inquiry summary](https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report).

The [lecture slide workflow](../README.md) is the authoring reference. To
regenerate this deck from the repository root:

```sh
python3 scripts/build_reveal_slides.py lecture-10-oop.qmd
```

MyST copies `09-lectures/reveal` as a static folder; the regular site build
serves the committed HTML without running Quarto.
