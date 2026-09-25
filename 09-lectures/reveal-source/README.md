# Lecture 10 Reveal source

This deck was adapted from the instructor's COMP 536 `lectures/python-fundamentals/slides/modular-design-oop.qmd` at commit `252e03df388899b0042d199f33805bc528bf08bd`. The copied SCSS theme and tokens are local so the COMP 521 build does not depend on the COMP 536 checkout.

COMP 521 adaptations add the Rectangle method/attribute sequence, naming conventions, inheritance and composition, correct the notebook workflow for Project 3, and change the lab connection to Part 5. The Ariane 5 slide now follows the [ESA inquiry summary](https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report).

To regenerate the committed self-contained slide deck (requires Quarto and a Python Jupyter kernel):

```sh
cd 09-lectures/reveal-source
quarto render lecture-10-oop.qmd --to revealjs
cp lecture-10-oop.html ../reveal/lecture-10-oop.html
python3 -c "from pathlib import Path; p=Path('../reveal/lecture-10-oop.html'); p.write_text('\n'.join(line.rstrip(' \t') for line in p.read_text().split('\n')))"
rm lecture-10-oop.html
```

MyST copies `09-lectures/reveal` as a static folder; the regular site build serves the committed HTML without running Quarto.
