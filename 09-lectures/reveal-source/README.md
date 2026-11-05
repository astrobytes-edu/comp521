# Historical Lecture 10 source

This directory preserves the source of Lecture 10's existing export. All
lecture authoring and revisions use the MyST slides plug-in, as required by
the [lecture slide workflow](../README.md). Do not regenerate this Quarto deck;
an approved revision must move it to MyST.

This deck was adapted from the instructor's COMP 536
`lectures/python-fundamentals/slides/modular-design-oop.qmd` at commit
`252e03df388899b0042d199f33805bc528bf08bd`. The copied SCSS theme and
tokens are local, so the COMP 521 build does not depend on the COMP 536 checkout.

COMP 521 adaptations add the Rectangle method and attribute sequence, naming
conventions, inheritance, and composition. They also correct the notebook
workflow for Project 3 and direct the lab to Part 5. The Ariane 5 slide follows
the [ESA inquiry summary](https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report).

MyST copies `09-lectures/reveal` as a static folder; the regular site build
serves the committed HTML without running Quarto.
