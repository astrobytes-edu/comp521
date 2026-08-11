# COMP 521: Introduction to Scientific Computing and Data Science
## Course Outline - Balanced Foundations for Data Science & Numerical Methods

### Official Course Description (SDSU Catalog)
**Units: 3; Prerequisites: MATH 252; MATH 254 or 342A; or equivalent with instructor permission, or graduate standing**

Introduction to computational methods for scientific problem-solving and data analysis using Python. Students implement fundamental algorithms from first principles including numerical integrators, root-finders, optimization methods, and Monte Carlo samplers before utilizing professional libraries. Emphasizes software engineering practices, test-driven development, version control, documentation, and reproducible research. Topics include data wrangling with pandas, statistical analysis, visualization, regression methods, and performance optimization.

---

## Course Philosophy
*"Build algorithms from scratch, then leverage libraries for real data"*

This course provides balanced foundations in both numerical methods and practical data science. You'll implement core algorithms to understand how computational tools work, then apply them to real scientific datasets. Perfect preparation for both COMP 536 (advanced ML implementation) and industry data science roles.

---

## Assessment Structure

### Biweekly Projects (50% of grade)
Six comprehensive projects spanning two weeks each:
- **Week A**: Theory, implementation, basic validation
- **Week B**: Application to real data, comparison with libraries
- **Due**: Second Monday at 11:59 PM PT

### Additional Components
- **Growth Memos** (10%) - Reflection with each project
- **Final Project** (25%) - Data science pipeline
- **Technical Growth Synthesis** (5%) - Portfolio reflection
- **Participation** (10%) - Lab engagement

---

## PROJECT SEQUENCE - Scaffolded Learning Path

### Project 0: Python & Data Science Bootcamp (Week 1)
*Due before Week 2*
- Python environment setup (Jupyter, VS Code)
- NumPy arrays vs lists
- Pandas basics
- Matplotlib fundamentals
- Git/GitHub workflow

---

### Project 1: Scientific Programming & EDA (Weeks 1-3)
**Focus:** Python mastery, data structures, exploratory analysis

#### Week 1: Object-Oriented Programming
- **Topics:** Classes for scientific data
- **Lab:** Build `ScientificData` class with statistics methods
- **Data Skills:** Loading, cleaning, basic stats

#### Week 2: Exploratory Data Analysis - Sensor Array Dataset
- **Topics:** Pandas DataFrames, descriptive statistics
- **Dataset:** Gaia DR3 subset (20,000 "light sources")
- **Lab Activities:**
  - Load sensor array measurements
  - Handle missing values and quality flags  
  - Compute derived features (distance from parallax)
  - Discover natural patterns in brightness vs color
- **Visualizations:**
  - Distribution histograms for all features
  - 2D scatter: brightness vs color (HR diagram discovery)
  - Distance distributions from parallax
  - 3D position plots in sensor coordinates

#### Deliverables:
- OOP data analysis framework
- EDA report on sensor array patterns
- Discovery of brightness-color relationship
- Growth Memo: Pattern discovery process

---

### Project 2: Numerical Integration & Data Applications (Weeks 3-5)
**Focus:** Building integrators, applying to real problems

#### Week 3: Integration Methods
- **Topics:** Rectangle, trapezoid, Simpson's rule
- **Lab:** Implement from scratch
- **Application:** Start exoplanet transit function (HW2 Problem 1)

#### Week 4: Error Analysis & Real Data
- **Topics:** Adaptive quadrature, error estimation
- **Lab:** Compare methods, optimize performance
- **Data Application:** Integrate light curves, compute areas

#### Deliverables:
- Complete integration library
- **Exoplanet Transit Model** implementation
- Research Memo: When to use each method
- Growth Memo: Understanding numerical error

---

### Project 3: Root Finding & Optimization (Weeks 5-7)
**Focus:** Solving equations, finding optimal parameters

#### Week 5: Root Finding Methods
- **Topics:** Bisection, Newton-Raphson, secant
- **Lab:** Implement all three methods
- **Application:** Habitable zone calculations (HW4 Problem 2)

#### Week 6: Data Acquisition & Cleaning
- **Topics:** APIs, web scraping basics, data validation
- **Lab:** Download Kepler data using Lightkurve
- **Real Data:** Clean NaN values, identify outliers

#### Deliverables:
- Root finding library
- **Kepler Data Pipeline** - download, clean, identify transits
- Research Memo: Data quality assessment
- Growth Memo: From math to implementation

---

### Project 4: Linear Algebra & Statistical Methods (Weeks 7-9)
**Focus:** Matrix operations, statistical testing, regression

#### Week 7: Linear Systems & Least Squares
- **Topics:** Gaussian elimination, LU decomposition
- **Lab:** Solve linear systems from scratch
- **Stats:** Normal equations for regression

#### Week 8: Statistical Testing & Model Fitting
- **Topics:** Hypothesis testing, chi-squared, p-values
- **Lab:** Fit models to noisy data
- **Application:** **Fit transit model to Kepler data** (HW8)

#### Deliverables:
- Linear algebra toolkit
- Statistical model fitting to real transits
- Research Memo: Goodness of fit assessment
- Growth Memo: Statistical thinking

---

### Project 5: ODEs & Time Series Analysis (Weeks 9-11)
**Focus:** Differential equations, temporal data

#### Week 9: ODE Solvers
- **Topics:** Euler, RK2, RK4 methods
- **Lab:** Implement ODE suite
- **Application:** Planetary structure (simplified HW6)

#### Week 10: Time Series Methods
- **Topics:** Autocorrelation, periodograms, trend analysis
- **Lab:** Analyze periodic signals
- **Data:** Find periods in variable star data

#### Deliverables:
- ODE solver library
- Time series analysis of astronomical data
- Research Memo: Detecting periodicity
- Growth Memo: Dynamic systems thinking

---

### Project 6: Machine Learning Foundations (Weeks 11-13)
**Focus:** Basic ML algorithms, classification, clustering

#### Week 11: Supervised Learning Basics
- **Topics:** k-NN, decision trees, cross-validation
- **Lab:** Implement classifiers from scratch
- **Application:** Classify stellar types

#### Week 12: Unsupervised Learning
- **Topics:** k-means, hierarchical clustering, PCA
- **Lab:** Implement clustering algorithms
- **Data:** Apply to Gaia sensor array dataset from Project 1
- **Discovery:** Find natural groupings in brightness-color space

#### Week 13: Model Evaluation
- **Topics:** ROC curves, confusion matrices, feature importance
- **Lab:** Compare your implementations to scikit-learn
- **Integration:** Apply to exoplanet candidate classification

#### Deliverables:
- Basic ML library implementation
- Clustering analysis of Gaia sensor data
- Classification pipeline for Kepler candidates
- Research Memo: Algorithm comparison
- Growth Memo: Pattern recognition insights

---

### Final Project: Complete Data Science Pipeline (Weeks 14-16)
**Integrate Everything You've Learned**

#### Project Options:
1. **Exoplanet Discovery Pipeline**: 
   - Use all your tools to find planets in new Kepler data
   - Statistical validation of candidates
   - Comparison with known discoveries

2. **Custom Scientific Data Analysis**:
   - Choose dataset from your field
   - Apply numerical methods + ML
   - Publication-quality visualizations

3. **Algorithm Comparison Study**:
   - Implement vs library performance
   - Computational complexity analysis
   - Best practices guide

#### Requirements:
- Data acquisition and cleaning
- Exploratory analysis with visualizations  
- Statistical testing
- At least 2 numerical methods
- Basic ML application
- Comparison with library implementations
- Technical Growth Synthesis

---

## What Makes This Different from COMP 536

### COMP 521 (This Course):
- **Basic implementations**: Simple algorithms from scratch
- **Data focus**: EDA, cleaning, basic statistics
- **Simple ML**: k-NN, k-means, linear regression
- **Real data practice**: Working with messy datasets
- **Library comparison**: When to build vs use tools

### COMP 536 (Advanced):
- **Deep implementations**: N-body dynamics, MCRT
- **Advanced statistics**: Bayesian inference, MCMC
- **Advanced ML**: Neural networks from scratch, GPs
- **Framework development**: JAX ecosystem
- **Research-level problems**: Discovering new patterns

---

## Skills You'll Master

### Numerical Computing:
- Integration methods
- Root finding
- ODE solving
- Linear algebra operations
- Basic optimization

### Data Science:
- Pandas proficiency
- Data cleaning & validation
- Exploratory data analysis
- Statistical testing
- Time series analysis
- Basic machine learning
- Professional visualization

### Software Engineering:
- Object-oriented design
- Version control with Git
- Documentation
- Testing & validation
- Performance comparison

---

## The Scaffolded Exoplanet Project

Threading through the course:
1. **Project 2**: Build transit model equations
2. **Project 3**: Download and clean Kepler data
3. **Project 4**: Fit models to real transits
4. **Project 5**: Analyze time series for periods
5. **Project 6**: Classify planet candidates
6. **Final**: Complete discovery pipeline

This gives students a real scientific discovery experience while learning both numerical methods and data science!

---

## AI Integration Policy

### Phase 1 (Projects 1-2): Foundations
- Documentation and concepts only
- Build understanding from scratch

### Phase 2 (Projects 3-4): Debugging Support
- After 30 min documented effort
- Must understand all solutions

### Phase 3 (Projects 5-6): Strategic Use
- Boilerplate and optimization
- Focus on algorithm understanding

---

## Why This Balance Works

1. **Industry Ready**: Both numerical skills and data science
2. **Research Prepared**: Understanding before using libraries  
3. **Real Data Experience**: Messy data, real challenges
4. **Clear Progression**: Each project builds on previous
5. **Not Redundant**: Completely different from COMP 536's advanced topics

Students leave ready for:
- Data science internships
- COMP 536's advanced implementations
- Research projects requiring both analysis and computation
- Industry roles requiring numerical and data skills

---

## Instructor Implementation Notes (Workload Minimization)

### Lab Structure
- **Labs = Project Work Time**: No separate lab assignments or reports
- **Attendance/Participation Only**: Simple checkoff for being present and working
- **Peer Programming Required**: Students debug together, reducing office hour demands
- **No Additional Lab Deliverables**: Labs solely for implementation support

### Streamlined Grading Strategy

#### Automated Assessment
```python
# Provide test suites that auto-grade correctness
# Students must pass all tests before submission
def test_integration_suite():
    """Tests student implementations automatically"""
    assert abs(student.simpson_rule(np.sin, 0, np.pi/2, 100) - 1.0) < 1e-4
    assert abs(student.trap_rule(np.sin, 0, np.pi/2, 100) - 1.0) < 1e-2
    print("All tests passed!")
```

#### Biweekly Projects (Not Weekly)
- **6 projects total** instead of 10-12 = 40% less grading
- More time for quality implementations
- Fewer panic emails and extension requests

#### Growth Memos - Simple Rubric
- ✓+ Exceptional reflection (10%)
- ✓ Adequate reflection (85%)  
- ✓- Minimal effort (5%)
- **Time**: 30 seconds per memo

#### Research Memos - Structured Rubric
- Correct Methods (40%) - Did they use right approach?
- Clear Communication (30%) - Is it readable?
- Valid Results (30%) - Do numbers make sense?
- **Time**: 10 minutes per memo with rubric
- **Peer Review First**: Students review each other during lab

### Further Workload Reductions

#### GitHub Classroom Automation
- Auto-collects at deadline (no late submission confusion)
- Runs test suites automatically
- No Canvas duplicate submissions
- No "I emailed it" excuses

#### Reuse Existing Materials
- Projects adapted from ASTR 596 (already debugged)
- Solution code already written
- Test cases already validated
- Rubrics already created

#### Standard Requirements Only
- No "optional extensions" or "extra credit"
- Everyone completes identical base assignments
- No "choose your own adventure" options requiring unique grading

#### Single Submission Platform
- GitHub only (no Canvas uploads)
- Last commit before deadline = submission
- Clear timestamp trail

### Grading Time Estimates
Per project cycle (biweekly):
- Automated tests verify correctness: 0 hours
- Code quality review (with rubric): 5 min × 30 students = 2.5 hours
- Growth memos: 1 min × 30 students = 0.5 hours  
- Research memos: 10 min × 30 students = 5 hours
- **Total: ~8 hours per project cycle**

Final Project:
- Reuse ASTR 596 rubric exactly
- Peer presentations (students grade each other)
- **Total: ~15 hours at semester end**

### Communication Strategy
- **Single weekly announcement** with all information
- **No individual emails** - post answers to Canvas discussions
- **Office hours only** - no appointment meetings
- **Standard response**: "Discussed in class/lab, check recordings"

### Participation Grading
Simple weekly check:
- Present in lab? ✓
- Attempted work? ✓  
- Done for the week

No detailed tracking of "quality" of participation.

### Materials That Already Exist
From ASTR 596, just remove astronomy terminology:
- Project 2: Transit model → "Periodic signal model"
- Project 3: Kepler data → "Time series data"
- Project 4: Transit fitting → "Model fitting"
- Project 5: Planet structure → "Hydrostatic equilibrium"
- All solution code written and tested
- All rubrics created

This structure requires approximately **50% less grading time** than traditional weekly assignments while maintaining pedagogical integrity.
