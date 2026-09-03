import unittest
from pathlib import Path


WIDGET = Path(__file__).resolve().parents[1] / "plugins" / "interactive-lecture" / "widget.mjs"
PROJECTOR_CONTROLS = Path(__file__).resolve().parents[1] / "plugins" / "interactive-python" / "projector-controls.mjs"
LECTURE_STYLES = Path(__file__).resolve().parents[1] / "assets" / "lecture-projector.css"
LECTURE_ONE = Path(__file__).resolve().parents[1] / "03-python" / "bootcamp-01-run-calculate-inspect.md"
LECTURE_TWO = Path(__file__).resolve().parents[1] / "03-python" / "bootcamp-02-procedures-decisions.md"
LECTURE_THREE = Path(__file__).resolve().parents[1] / "03-python" / "bootcamp-03-data-functions.md"
LECTURE_FOUR = Path(__file__).resolve().parents[1] / "03-python" / "bootcamp-04-arrays-figures.md"
GRADE_CALCULATOR_LAB = Path(__file__).resolve().parents[1] / "07-practice-labs" / "grade-calculator-design.md"
ND_ARRAY_ASSESSMENT = Path(__file__).resolve().parents[1] / "08-assessments" / "nd-array-evidence-check.md"
MYST_CONFIG = Path(__file__).resolve().parents[1] / "myst.yml"


class InteractiveLectureWidgetTests(unittest.TestCase):
    def test_widget_is_self_contained_and_preserves_the_course_base_path(self):
        source = WIDGET.read_text()

        self.assertNotIn('from "./runtime.mjs"', source)
        self.assertIn('document.querySelector("base")?.href || new URL("./", location.href)', source)
        self.assertIn('new URL(`jupyterlite/lab/index.html#/tree/', source)

    def test_lecture_one_mermaid_classes_do_not_use_reserved_end_keyword(self):
        lecture = LECTURE_ONE.read_text()

        self.assertIn("classDef outcome", lecture)
        self.assertNotIn("classDef end", lecture)
        self.assertNotIn("class evidence,claim end", lecture)

    def test_lecture_two_through_line_is_static_and_does_not_require_the_mermaid_runtime(self):
        lecture = LECTURE_TWO.read_text()

        self.assertNotIn("```{mermaid}", lecture)
        for label in (
            "Scientific question",
            "Stated rule and assumptions",
            "Comparisons and branches",
            "Related observations",
            "Reusable function with a contract",
            "Many values with an array",
            "Inspectable result and a test",
        ):
            self.assertIn(label, lecture)

    def test_lecture_one_examples_are_self_contained_and_standard_library_first(self):
        lecture = LECTURE_ONE.read_text()

        self.assertIn("radius_km = 4.2", lecture)
        self.assertIn('importlib.util.find_spec("math")', lecture)
        self.assertIn("import math\n\npredicted_flux_erg_s_cm2", lecture)
        self.assertIn("import random", lecture)
        self.assertNotIn("import numpy as np", lecture)

    def test_lecture_one_explains_and_indexes_its_function_calls(self):
        lecture = LECTURE_ONE.read_text()

        self.assertIn("## How to read a function call", lecture)
        self.assertIn("## Reference · calls for ordinary Python work", lecture)
        self.assertIn("## Reference · environment and provenance calls", lecture)
        self.assertIn("## Reference · numerical calls and their arguments", lecture)
        self.assertIn("## Reference · stable and complex-number helpers", lecture)

    def test_lecture_one_links_to_official_docs_for_every_standard_library_module(self):
        lecture = LECTURE_ONE.read_text()

        for module in ("math", "sys", "pathlib", "random", "importlib", "cmath"):
            self.assertIn(f"https://docs.python.org/3/library/{module}.html", lecture)
        self.assertIn("https://docs.python.org/3/library/functions.html", lecture)

    def test_projector_code_uses_a_larger_readable_scale(self):
        styles = LECTURE_STYLES.read_text()

        self.assertIn("calc(1.18rem * var(--lecture-font-scale, 1))", styles)
        self.assertIn("calc(1.32rem * var(--lecture-font-scale, 1))", styles)
        self.assertIn("calc(2.1vw * var(--lecture-font-scale, 1))", styles)
        self.assertIn("calc(1.9rem * var(--lecture-font-scale, 1))", styles)
        self.assertIn("calc(1rem * var(--lecture-font-scale, 1))", styles)
        self.assertIn(".projector-lecture.projector-slide.lecture-scroll", styles)
        self.assertIn(".lecture-two-column", styles)
        self.assertIn("grid-template-columns: minmax(16rem, 0.8fr)", styles)
        self.assertIn(".projector-lecture .lecture-matrix", styles)
        self.assertIn("font-variant-numeric: tabular-nums", styles)

    def test_projector_controls_name_scrollable_blocks_as_sections(self):
        controls = PROJECTOR_CONTROLS.read_text()

        self.assertIn('slide.classList.contains("lecture-scroll")', controls)
        self.assertIn('const unit = sectionMode ? "section" : "slide"', controls)
        self.assertIn('sectionMode ? "Lecture section controls"', controls)

    def test_lecture_two_scaffolds_core_python_before_a_bounded_numpy_preview(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## I · Procedures and decisions",
            "## II · Store related observations deliberately",
            "## III · Package a calculation as a function",
            "## IV · First contact with NumPy",
        ):
            self.assertIn(heading, lecture)

        self.assertNotIn("## Exit check", lecture)

        self.assertIn(":::{projector-controls}", lecture)
        self.assertIn(":::{interactive-python}", lecture)
        self.assertIn("import numpy as np", lecture)
        self.assertIn("Week 2", lecture)
        self.assertIn("not yet learning", lecture)
        self.assertIn("03-python-control-flow.md", lecture)
        self.assertIn("04-python-data-structures.md", lecture)
        self.assertIn("05-python-functions-modules.md", lecture)
        self.assertIn("07-numpy-fundamentals.md", lecture)

        for heading in (
            "## More than two outcomes · `elif`",
            "## Combine conditions deliberately",
            "## Short-circuiting protects a calculation",
            "## `while` repeats until a stated condition changes",
            "## `for` loops: one procedure for every observation",
        ):
            self.assertIn(heading, lecture)

        self.assertLess(
            lecture.index("## Why programs need control flow"),
            lecture.index("## A Boolean expression chooses a branch"),
        )
        self.assertLess(
            lecture.index("## Loops apply one procedure repeatedly"),
            lecture.index("## `while` repeats until a stated condition changes"),
        )
        self.assertLess(
            lecture.index("## `while` repeats until a stated condition changes"),
            lecture.index("## `for` loops: one procedure for every observation"),
        )
        self.assertLess(
            lecture.index("## Write the rule before the code"),
            lecture.index("## A Boolean expression chooses a branch"),
        )
        self.assertLess(
            lecture.index("## `while` repeats until a stated condition changes"),
            lecture.index("## III · Package a calculation as a function"),
        )

    def test_lecture_two_has_worked_self_study_checks_and_a_numerically_sound_test(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("math.isclose(", lecture)
        self.assertNotIn("assert transit_depth(1.0, 10.0) == 0.01", lecture)
        self.assertIn("Example `or` policy", lecture)
        self.assertIn("**Read it:** `0.984` reaches the `0.990` branch.", lecture)
        self.assertIn("**Expected result:** no error; the body is skipped.", lecture)
        self.assertIn("**Expected result:** `stopped at step 3: residual = 0.010`.", lecture)
        self.assertIn("**Call contract:**", lecture)
        self.assertIn("`np.ones_like(time_days)` creates ones with the same shape", lecture)

    def test_lecture_two_uses_a_science_facing_elif_example_and_bounds_transit_domain(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("observation-triage example", lecture)
        self.assertNotIn("01-course-info/grading.md", lecture)
        self.assertIn("strong low-flux candidate", lecture)
        self.assertIn("radius_planet_cm > radius_star_cm", lecture)
        self.assertIn("full-overlap, uniform-brightness geometry", lecture)
        self.assertIn("Run this definition first", lecture)
        self.assertIn("strict software-test tolerance", lecture)

    def test_lecture_two_states_why_conditionals_and_loops_matter_before_syntax(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("A **conditional** is a fork in a procedure", lecture)
        self.assertIn("A `for` loop is the right default when a collection supplies", lecture)
        self.assertIn("A `while` loop is for work whose number of repeats is not known", lecture)

    def test_lecture_two_keeps_first_use_references_and_function_anatomy(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## Reference · conditionals and Boolean logic",
            "## Reference · loop patterns",
            "## Reference · collections and mutation",
            "## Anatomy of a function",
            "## Reference · functions and tests",
            "## Reference · NumPy essentials",
        ):
            self.assertIn(heading, lecture)

        self.assertLess(
            lecture.index("## Short-circuiting protects a calculation"),
            lecture.index("## Reference · conditionals and Boolean logic"),
        )
        self.assertLess(
            lecture.index("## Trace the loop; do not guess"),
            lecture.index("## Reference · loop patterns"),
        )
        self.assertLess(
            lecture.index("## Mutability is a bookkeeping choice"),
            lecture.index("## Reference · collections and mutation"),
        )
        self.assertLess(
            lecture.index("## Anatomy of a function"),
            lecture.index("## Reference · functions and tests"),
        )
        self.assertLess(
            lecture.index("## Run · make one simple numerical grid"),
            lecture.index("## Reference · NumPy essentials"),
        )

    def test_lecture_two_test_sequence_is_honest_and_fails_when_invalid_inputs_are_accepted(self):
        lecture = LECTURE_TWO.read_text()

        self.assertNotIn("Continuing from the preceding slide", lecture)
        self.assertIn("## Run the definition, then run its tests", lecture)
        self.assertIn('raise AssertionError("transit_depth accepted invalid geometry")', lecture)

    def test_lecture_two_covers_the_remaining_core_control_flow_data_and_function_topics(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## Stop, skip, or finish a loop deliberately",
            "## Nested loops: one procedure across two dimensions",
            "## List comprehensions: compact a simple loop",
            "## Tuples and sets express different relationships",
            "## Copying nested data needs an explicit decision",
            "## `return` makes a result reusable; `print` only displays it",
            "## Defaults and scope keep function behavior predictable",
            "## Never use a mutable object as a default argument",
            "## Modules are reusable boundaries",
            "## From a function contract to evidence",
        ):
            self.assertIn(heading, lecture)

        self.assertIn("break", lecture)
        self.assertIn("continue", lecture)
        self.assertIn("for ... else", lecture)
        self.assertIn("copy.deepcopy", lecture)
        self.assertIn("import math", lecture)
        self.assertIn("mutable default", lecture)

    def test_lecture_two_uses_one_consistent_transit_ratio_domain(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("0 < Rp <= Rstar", lecture)
        self.assertIn("0.0 < radius_ratio <= 1.0", lecture)
        self.assertNotIn("0.0 < radius_ratio < 1.0", lecture)
        self.assertLess(
            lecture.index("## From a function contract to evidence"),
            lecture.index("## Run the definition, then run its tests"),
        )

    def test_lecture_three_keeps_the_projector_structure_and_active_checks(self):
        lecture = LECTURE_THREE.read_text()

        self.assertIn("hide_toc: true", lecture)
        self.assertIn(":::{projector-controls}", lecture)
        self.assertIn("lecture-03-controls", lecture)
        self.assertGreaterEqual(lecture.count("projector-lecture projector-slide"), 12)
        self.assertIn("## The through-line", lecture)
        self.assertIn("## Today’s question", lecture)
        self.assertIn("## Predict", lecture)
        self.assertIn("## Exit check", lecture)
        self.assertIn(":::{interactive-python}", lecture)

    def test_lecture_four_keeps_scrollable_lecture_blocks_and_executable_cells(self):
        lecture = LECTURE_FOUR.read_text()

        self.assertIn("kernelspec:", lecture)
        self.assertIn("name: python3", lecture)
        self.assertGreaterEqual(lecture.count("```{code-cell} python"), 21)
        self.assertGreaterEqual(lecture.count("plt.show()"), 5)
        self.assertIn("hide_toc: true", lecture)
        self.assertIn(":::{projector-controls}", lecture)
        self.assertIn("lecture-04-controls", lecture)
        self.assertGreaterEqual(lecture.count("projector-lecture projector-slide"), 28)
        self.assertGreaterEqual(lecture.count("lecture-scroll"), 28)
        self.assertGreaterEqual(lecture.count("lecture-two-column"), 6)
        self.assertNotIn(":::{interactive-python}", lecture)
        self.assertNotIn(":class: lecture-prompt", lecture)
        self.assertNotIn("**Predict:**", lecture)
        for heading in (
            "## I · NumPy arrays: quantities, positions, and elementwise operations",
            "## II · Indexing, slicing, and Boolean selection",
            "## III · 2-D and ND arrays: matrices, axes, and shape",
            "## IV · Vectorized calculations and shape checks",
            "## V · Matplotlib: readable figures and bounded evidence",
            "## Reference · array creation and inspection",
            "## Reference · indexing and Boolean selection",
            "## Reference · ND arrays, axes, and broadcasting",
            "## Reference · vectorization and compatible shapes",
            "## Reference · a readable Matplotlib figure",
            "## Exit check",
            "## Carry forward",
        ):
            self.assertIn(heading, lecture)

    def test_week_two_extends_function_interfaces_before_array_work(self):
        lecture_three = LECTURE_THREE.read_text()
        lecture_four = LECTURE_FOUR.read_text()

        for topic in (
            "Keyword-only parameters protect consequential options",
            "Flexible calls need a narrow purpose",
            "*args",
            "**kwargs",
            "Unpacking lets a record meet a matching signature",
            "Return values should support the next question",
        ):
            self.assertIn(topic, lecture_three)

        self.assertIn("synthetic brightness measurements", lecture_four)
        self.assertNotIn("radioactive", lecture_four.lower())
        self.assertNotIn("Start Project 1", lecture_four)
        self.assertIn("def describe_series(values, *, label=", lecture_three)
        self.assertIn("def plot_series(ax, time_days, brightness, **plot_options)", lecture_three)
        self.assertNotIn("def describe_series(values, **metadata)", lecture_three)
        self.assertIn("observed_brightness", lecture_four)
        self.assertIn("reference_brightness", lecture_four)
        self.assertIn("brightness_by_source", lecture_four)
        self.assertIn("baseline_column", lecture_four)
        self.assertIn(
            "1.0 - dimming_depth * (1.0 + np.sin(phase)) / 2.0",
            lecture_four,
        )
        self.assertNotIn("amplitude * np.sin(phase) ** 2", lecture_four)

    def test_lecture_three_function_examples_state_and_enforce_their_contracts(self):
        lecture = LECTURE_THREE.read_text()

        self.assertIn(
            '"""Return phase in [0, 1) for time, period, and epoch in days."""',
            lecture,
        )
        self.assertIn('raise ValueError("period_days must be positive")', lecture)
        self.assertNotIn(
            "def phase_fraction(time_days, period_days, *, epoch_days=0.0):\n    ...",
            lecture,
        )
        self.assertIn("class FakeAxes:", lecture)
        self.assertIn('lable="synthetic observations"', lecture)
        self.assertIn("raises a `TypeError` before `FakeAxes.plot` is called", lecture)
        self.assertGreaterEqual(
            lecture.count('raise ValueError("flux_values must not be empty")'),
            3,
        )
        self.assertIn("rel_tol=0.0, abs_tol=1e-12", lecture)
        self.assertIn("| `return` one value |", lecture)
        self.assertIn("| `raise` an exception |", lecture)

    def test_week_two_teaches_the_published_grade_policy_with_a_realistic_timebox(self):
        lecture = LECTURE_THREE.read_text()
        lab = GRADE_CALCULATOR_LAB.read_text()

        self.assertIn("30 minutes", lecture)
        self.assertIn("final_course_letter(3.80)", lecture)
        self.assertIn("practice policy, not a grade system", lecture)
        self.assertIn("Two phases, two class meetings", lab)
        self.assertIn("30-minute implementation activity", lab)
        self.assertIn("| 23–30 min |", lab)
        self.assertIn("restart the kernel", lab)
        self.assertIn("checkpoint sentence", lab)
        self.assertIn("final_course_letter(3.80)", lab)
        self.assertIn("final_course_letter(3.79)", lab)
        self.assertIn("final_course_letter(4.30)", lab)

    def test_week_two_figure_design_names_orientation_threshold_and_noncolor_encoding(self):
        lecture = LECTURE_FOUR.read_text()

        self.assertIn("axes[1].invert_yaxis()", lecture)
        self.assertIn("axes[0].invert_xaxis()", lecture)
        self.assertIn('axes[1].set_xscale("log")', lecture)
        self.assertIn('axes[1].set_yscale("log")', lecture)
        self.assertIn("marker=", lecture)
        self.assertIn("linestyle=", lecture)
        self.assertIn("illustrative threshold", lecture)
        self.assertIn("even without color", lecture)
        self.assertIn("not a fit", lecture)

    def test_lecture_four_has_honest_array_contracts_and_documented_figure_workflow(self):
        lecture = LECTURE_FOUR.read_text()

        for phrase in (
            'raise ValueError("time_days must contain only finite values")',
            'raise ValueError("reference_period_days must be finite and positive")',
            'raise ValueError("dimming_depth must be finite and in [0, 1)")',
            "np.testing.assert_allclose(",
            "rtol=0.0,",
            "atol=1e-12,",
            "try:",
            'brightness_fig.savefig(',
            "Vectorization and Broadcasting Lab",
            "## Broadcasting: one operation across compatible shapes",
            "Broadcasting is NumPy’s shape-matching rule for elementwise",
            "NumPy aligns shapes from the right.",
            "## Apply the shape rule before the operation",
            "values_by_row_and_column = np.zeros((3, 5))",
            "per_row[:, np.newaxis]",
            "## Apply broadcasting to one baseline per source",
            "brightness_by_source.mean(axis=1)",
            "brightness_by_source.mean(axis=0)",
            "## Indexing starts at `0`; negative indices count from the end",
            "`values[0]` selects the first position",
            "`values[-1]` selects the last position",
            "observation_time_days[-1] == observation_time_days[len(observation_time_days) - 1]",
            "## A 2-D array can represent a labeled matrix",
            "`(number_of_rows, number_of_columns)`",
            "`brightness_by_source[1, 2]` is the bold entry",
            "`*` is elementwise multiplication for `ndarray` objects. `A @ B` is matrix",
            "## Matrix order and coordinate order are different conventions",
            "`image[y, x]`, not `image[x, y]`",
            "`(row, column)`, `(x, y)`, `(source, time)`",
            "## Shape and indexing use the same axis order",
            "`array.shape == (axis_0_length, axis_1_length, ...)`",
            "`array[axis_0_index, axis_1_index, ...]`",
            "`(row, column)`",
            "`brightness_by_source[source, time]`",
            "`(source, time, filter)`",
            "New NumPy arrays use C order by default, so the last index changes fastest in",
            "brightness_by_time_source = brightness_by_source.T",
            "## Use the docs for the full API",
            "np.arange(start, stop, step)",
            "np.linspace(start, stop, num)",
            "np.logspace(start, stop, num)",
            "np.zeros(shape)",
            "np.ones(shape)",
            "np.full(shape, fill_value)",
            "np.eye(N)",
            "Matplotlib Anatomy of a Figure",
            "https://numpy.org/doc/stable/user/index.html",
            "https://numpy.org/doc/stable/reference/index.html",
            "https://matplotlib.org/stable/index.html",
            "https://matplotlib.org/stable/api/index.html",
            "https://matplotlib.org/cheatsheets/",
            "https://matplotlib.org/stable/gallery/showcase/anatomy.html",
        ):
            self.assertIn(phrase, lecture)

        self.assertNotIn("brightness amplitude", lecture)
        self.assertNotIn("if observed_brightness < 0.985:\n    print", lecture)

        figure_section = lecture[
            lecture.index("## Add a threshold and complete the figure"):
            lecture.index("## Use figure anatomy as a checklist")
        ]
        self.assertLess(figure_section.index("ax.scatter("), figure_section.index("ax.legend()"))
        self.assertLess(figure_section.index("ax.legend()"), figure_section.index("plt.show()"))

        first_plot_section = lecture[
            lecture.index("## Run this: render the observations"):
            lecture.index("## Add a separately named reference curve")
        ]
        self.assertIn("ax.scatter(", first_plot_section)
        self.assertNotIn("ax.plot(", first_plot_section)
        self.assertIn("`plt.show()` displays a figure in a notebook.", lecture)
        self.assertIn(
            "../08-assessments/nd-array-evidence-check.md",
            lecture,
        )

        exit_check = lecture[
            lecture.index("## Exit check"):
            lecture.index("## Carry forward")
        ]
        self.assertIn("baseline_per_source[:, np.newaxis]", exit_check)
        self.assertIn("Why does their division fail?", exit_check)

    def test_lecture_four_renders_plot_files_with_alt_text_and_captions(self):
        lecture = LECTURE_FOUR.read_text()

        figures = (
            (
                "lecture-04-synthetic-observations.png",
                "fig:synthetic-observations",
                "Thirteen blue circular markers",
            ),
            (
                "lecture-04-observations-reference.png",
                "fig:observations-reference",
                "Thirteen blue circular observations are plotted",
            ),
            (
                "lecture-04-synthetic-brightness-figure.png",
                "fig:observations-reference-threshold",
                "A gray dashed horizontal line",
            ),
            (
                "lecture-04-scale-comparison.png",
                "fig:scale-comparison",
                "On linear axes the three farthest values cluster near zero",
            ),
            (
                "lecture-04-axis-direction.png",
                "fig:axis-direction",
                "detector row 1 at the top",
            ),
        )

        for filename, label, alt_text in figures:
            self.assertTrue((LECTURE_FOUR.parent / filename).is_file())
            self.assertIn(filename, lecture)
            self.assertIn(label, lecture)
            self.assertIn(alt_text, lecture)

        self.assertIn('export_path = Path("lecture-04-synthetic-brightness-figure.png")', lecture)
        self.assertIn('print(f"saved: {export_path} (exists: {export_path.exists()})")', lecture)

    def test_nd_array_evidence_check_is_individual_and_uses_the_course_grading_model(self):
        assessment = ND_ARRAY_ASSESSMENT.read_text()
        myst_config = MYST_CONFIG.read_text()

        for phrase in (
            "Individual graded assessment",
            "Scholarly Engagement",
            "nd_array_evidence_check.ipynb",
            "flux_by_target",
            "normalized_flux.shape == flux_by_target.shape",
            "normalized_flux[:, 0], 1.0",
            "axis `0`",
            "axis `1`",
            "Save the figure as a file and display it in the notebook.",
            "This is holistic letter feedback, not a point checklist.",
        ):
            self.assertIn(phrase, assessment)

        self.assertIn("08-assessments/nd-array-evidence-check.md", myst_config)


if __name__ == "__main__":
    unittest.main()
