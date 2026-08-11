# COMP 521: Problem Sets & Short Projects
## Introduction to Scientific Computing and Data Science

---

## Table of Contents

1. [Project 0: Python & Data Science Bootcamp](#project-0-python--data-science-bootcamp)
2. [Project 1: Scientific Programming & Exploratory Data Analysis](#project-1-scientific-programming--exploratory-data-analysis)
3. [Project 2: Numerical Integration & Transit Modeling](#project-2-numerical-integration--transit-modeling)
4. [Project 3: Root Finding & Data Acquisition](#project-3-root-finding--data-acquisition)
5. [Project 4: Linear Algebra & Statistical Model Fitting](#project-4-linear-algebra--statistical-model-fitting)
6. [Project 5: ODEs & Time Series Analysis](#project-5-odes--time-series-analysis)
7. [Project 6: Machine Learning Foundations](#project-6-machine-learning-foundations)
8. [Final Project: Complete Data Science Pipeline](#final-project-complete-data-science-pipeline)

---

## Project 0: Python & Data Science Bootcamp
**Due: Before Week 2 (Counts toward Participation)**

### Learning Outcomes
By completing this project, students will be able to:
- Set up a complete Python development environment
- Navigate Jupyter notebooks and VS Code effectively
- Use Git for version control
- Understand NumPy arrays vs Python lists performance differences
- Create basic visualizations with Matplotlib

### Assignment
1. Install Python environment with scientific stack (NumPy, SciPy, Pandas, Matplotlib)
2. Configure Git and create GitHub repository
3. Complete Python proficiency assessment:
   - Array operations benchmarking (lists vs NumPy)
   - Basic plotting exercise
   - DataFrame manipulation with Pandas
4. Write initial reflection (1 page): Prior programming experience and learning goals

---

## Project 1: Scientific Programming & Exploratory Data Analysis
**Due: End of Week 3 (Biweekly Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Design and implement object-oriented solutions for scientific data
- Perform comprehensive exploratory data analysis
- Create publication-quality visualizations
- Calculate and interpret descriptive statistics
- Identify patterns and outliers in real datasets

### Part A: Object-Oriented Programming for Science (Week 1)

#### Problem 1: Scientific Data Class
Create a `ScientificData` class that encapsulates data analysis functionality:

```python
class ScientificData:
    """Class for handling scientific measurements with uncertainties"""
    
    def __init__(self, data, errors=None, units=None):
        # Initialize with data array, optional errors, and units
        
    def statistics(self):
        # Return dict with mean, std, median, quartiles
        
    def clean_data(self, method='zscore', threshold=3):
        # Remove outliers using specified method
        
    def normalize(self):
        # Normalize data to [0,1] or z-scores
        
    def visualize(self, plot_type='histogram'):
        # Create various plot types
```

Test your class with synthetic data representing stellar magnitudes with measurement uncertainties.

### Part B: Exploratory Data Analysis (Week 2)

#### Problem 2: Real Data Analysis
Using the Gaia DR3 dataset (subset provided), perform comprehensive EDA:

1. **Data Loading & Inspection**
   - Load stellar catalog data
   - Check data types, missing values, distributions
   - Document data quality issues

2. **Statistical Analysis**
   - Calculate summary statistics for all numerical columns
   - Identify correlations between variables
   - Test for normality of distributions

3. **Visualization Suite**
   Create at least 6 different visualizations:
   - Histograms of key variables
   - Scatter plots with color-coding (e.g., HR diagram)
   - Correlation heatmap
   - Box plots for outlier detection
   - Pair plots for multivariate relationships

4. **Pattern Discovery**
   - Identify stellar populations
   - Find unusual objects
   - Document interesting patterns

### Deliverables
- Jupyter notebook with complete analysis
- `scientific_data.py` module with your class
- **Research Memo** (2-3 pages): EDA findings and their astronomical significance
- **Growth Memo** (1-2 pages): Reflection on OOP design choices and data exploration process

---

## Project 2: Numerical Integration & Transit Modeling
**Due: End of Week 5 (Biweekly Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Implement numerical integration methods from mathematical principles
- Analyze convergence and error propagation
- Model astrophysical phenomena computationally
- Compare computational efficiency of different algorithms
- Apply numerical methods to real scientific problems

### Part A: Integration Methods & Transit Model (Week 3)

#### Problem 1: Numerical Integration Suite
Create a module `numerical_integration.py` implementing:

a) **Rectangle Rule**:
$$\int_{x_0}^{x_N} f(x)dx \approx \sum_{i=0}^{N-1} f(x_i)\Delta x$$
where $\Delta x = (x_N - x_0)/N$ and $x_i = x_0 + i\Delta x$

b) **Trapezoidal Rule**:
$$\int_a^b f(x)dx \approx \frac{\Delta x}{2}\sum_{i=0}^{N-1}[f(x_i) + f(x_{i+1})]$$

c) **Simpson's Rule**:
$$\int_a^b f(x)dx \approx \frac{\Delta x}{3}\sum_{i=0}^{N/2-1}[f(x_{2i}) + 4f(x_{2i+1}) + f(x_{2i+2})]$$

Test with $\int_0^{\pi/2} \sin(x)dx$ for $N = 10, 10^2, 10^3, 10^4, 10^5$.

#### Problem 2: Exoplanet Transit Model
Implement the transit flux ratio for a planet crossing a star:

$$F(p, z) = 1 - \lambda(p, |z|)$$

where the obscured area function is:
$$\lambda(p, z) = \begin{cases}
0 & 1 + p < z \\
\frac{1}{\pi}\left[p^2\kappa_0 + \kappa_1 - \sqrt{\frac{4z^2-(1+z^2-p^2)^2}{4}}\right] & |1-p| < z \leq 1+p \\
p^2 & z \leq 1-p \\
1 & z \leq p-1
\end{cases}$$

with:
$$\kappa_0 = \cos^{-1}\left(\frac{p^2 + z^2 - 1}{2pz}\right)$$
$$\kappa_1 = \cos^{-1}\left(\frac{1 - p^2 + z^2}{2z}\right)$$

Parameters:
- $p = r_p/r_* =$ planet-to-star radius ratio
- $z = d/r_* =$ projected separation normalized by stellar radius

### Part B: Adaptive Methods & Limb Darkening (Week 4)

#### Problem 3: Adaptive Quadrature
Implement adaptive step size based on error tolerance:

```python
def adaptive_integrate(func, a, b, method='simpson', tol=1e-6):
    """
    Adaptively refine integration step size based on error estimate
    Returns: integral value, number of function evaluations
    """
```

#### Problem 4: Limb Darkening Effects
Extend transit model to include stellar limb darkening:

$$F(p, |z|) = \frac{\int_0^1 I(r)[1 - \delta(p, r, z)]2rdr}{\int_0^1 I(r)2rdr}$$

where $I(r) = 1 - u(1 - \sqrt{1-r^2})$ for linear limb darkening coefficient $u$.

### Deliverables
- `numerical_integration.py` module
- `exoplanet_transit.py` module  
- Convergence analysis plots
- **Research Memo** (2-3 pages): Comparison of integration methods and impact of limb darkening
- **Growth Memo** (1-2 pages): Challenges in handling numerical edge cases

---

## Project 3: Root Finding & Data Acquisition
**Due: End of Week 7 (Biweekly Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Implement and compare root-finding algorithms
- Access astronomical databases programmatically
- Clean and validate real observational data
- Identify features in time series data
- Apply numerical methods to astrophysical calculations

### Part A: Root Finding Methods (Week 5)

#### Problem 1: Root Finding Suite
Implement in `root_finders.py`:

a) **Bisection Method**:
```python
def bisection(func, a, b, tol=1e-6, max_iter=100):
    """Find root using bisection method"""
```

b) **Newton's Method**:
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

c) **Secant Method**:
$$x_{n+1} = x_n - f(x_n)\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

#### Problem 2: Habitable Zone Calculations
Find stellar temperature for habitable zone at specific distances:

$$d = \left(\frac{L/L_\odot}{S_{eff}}\right)^{1/2} \text{ AU}$$

where:
$$\frac{L}{L_\odot} = \left(\frac{T_{eff}}{5780\text{ K}}\right)^4$$

$$S_{eff} = S_{eff\odot} + aT_* + bT_*^2$$

with $T_* = T_{eff} - 5780$ K, and for inner edge: $S_{eff\odot} = 1.014$, $a = 8.177 \times 10^{-5}$, $b = 1.706 \times 10^{-9}$.

Find $T_{eff}$ for $d = 0.5$ AU using all three methods.

### Part B: Data Acquisition & Processing (Week 6)

#### Problem 3: Kepler Data Pipeline

```python
# Using Lightkurve package
import lightkurve as lk

# Download Kepler-7b data
lcs = lk.search_lightcurve("Kepler-7b", mission="Kepler", 
                          cadence="short").download_all()
```

Implement data cleaning pipeline:
1. Handle NaN values
2. Remove outliers (>3σ)
3. Normalize flux
4. Identify transits automatically

#### Problem 4: Transit Detection Algorithm
```python
def identify_transits(time, flux, flux_err, threshold=0.98):
    """
    Automatically identify transit events in light curve
    Returns: list of transit times and durations
    """
```

### Deliverables
- `root_finders.py` module
- `data_pipeline.py` with cleaning functions
- Comparison of root-finding convergence rates
- Plots of identified transits
- **Research Memo** (2-3 pages): Data quality assessment and transit detection reliability
- **Growth Memo** (1-2 pages): Challenges in working with real astronomical data

---

## Project 4: Linear Algebra & Statistical Model Fitting
**Due: End of Week 9 (Biweekly Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Solve linear systems computationally
- Implement least squares regression from first principles
- Perform statistical hypothesis testing
- Assess goodness of fit quantitatively
- Apply maximum likelihood estimation

### Part A: Linear Systems & Regression (Week 7)

#### Problem 1: Linear Algebra Methods
Implement in `linear_algebra.py`:

a) **Gaussian Elimination with Partial Pivoting**
b) **LU Decomposition**
c) **Normal Equations for Least Squares**:
$$\mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = \mathbf{X}^T\mathbf{y}$$

#### Problem 2: Multiple Linear Regression
Fit polynomial models to noisy data:
$$y = \beta_0 + \beta_1x + \beta_2x^2 + ... + \beta_nx^n + \epsilon$$

Compare your implementation with `numpy.polyfit` and `scipy.stats.linregress`.

### Part B: Statistical Model Fitting (Week 8)

#### Problem 3: Chi-Squared Fitting
Fit transit model to real Kepler data using chi-squared minimization:

$$\chi^2 = \sum_{i=1}^N \left(\frac{F_i - F(t_i; p, \tau, t_0)}{\sigma_{F,i}}\right)^2$$

where:
- $F_i$ = observed flux
- $F(t_i; p, \tau, t_0)$ = model flux
- $\sigma_{F,i}$ = flux uncertainty
- $z(t) = (t - t_0)/\tau$ for transit width $\tau$ and center time $t_0$

#### Problem 4: Statistical Validation
Calculate p-values using incomplete gamma function:
$$P(\chi^2 \geq \chi^2_{obs}) = \frac{\Gamma(\nu/2, \chi^2_{obs}/2)}{\Gamma(\nu/2)}$$

where $\nu = N - M$ degrees of freedom.

### Deliverables
- `linear_algebra.py` module
- `statistical_fitting.py` module
- Fitted transit parameters with uncertainties
- Goodness-of-fit assessment
- **Research Memo** (2-3 pages): Statistical analysis of transit fits
- **Growth Memo** (1-2 pages): Understanding parameter uncertainties

---

## Project 5: ODEs & Time Series Analysis
**Due: End of Week 11 (Biweekly Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Solve systems of coupled ODEs
- Analyze stability of numerical methods
- Detect periodicity in time series
- Apply Fourier analysis to real data
- Model physical systems computationally

### Part A: ODE Solvers (Week 9)

#### Problem 1: Runge-Kutta Methods
Implement in `ode_solvers.py`:

a) **Euler's Method**:
$$y_{n+1} = y_n + hf(t_n, y_n)$$

b) **RK4 Method**:
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
where:
- $k_1 = f(t_n, y_n)$
- $k_2 = f(t_n + h/2, y_n + hk_1/2)$
- $k_3 = f(t_n + h/2, y_n + hk_2/2)$
- $k_4 = f(t_n + h, y_n + hk_3)$

#### Problem 2: Planetary Structure (Simplified)
Solve hydrostatic equilibrium equations:

$$\frac{dP}{dr} = -\frac{Gm(r)\rho(r)}{r^2}$$
$$\frac{dm}{dr} = 4\pi\rho(r)r^2$$

with equation of state:
$$\rho(P) = \rho_0 + cP^n$$

### Part B: Time Series Analysis (Week 10)

#### Problem 3: Periodogram Analysis
Implement Lomb-Scargle periodogram for unevenly sampled data:

$$P(\omega) = \frac{1}{2}\left[\frac{(\sum_j X_j\cos\omega(t_j-\tau))^2}{\sum_j\cos^2\omega(t_j-\tau)} + \frac{(\sum_j X_j\sin\omega(t_j-\tau))^2}{\sum_j\sin^2\omega(t_j-\tau)}\right]$$

#### Problem 4: Variable Star Classification
Apply to variable star data:
- Detect primary period
- Find harmonics
- Classify variability type

### Deliverables
- `ode_solvers.py` module
- `time_series.py` module
- Planet mass-radius relationships
- Periodogram of variable stars
- **Research Memo** (2-3 pages): Stability analysis of ODE methods
- **Growth Memo** (1-2 pages): From differential equations to discrete solutions

---

## Project 6: Machine Learning Foundations
**Due: End of Week 13 (Biweekly Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Implement classification algorithms from scratch
- Apply clustering to discover patterns
- Perform dimensionality reduction
- Evaluate model performance properly
- Compare custom implementations with libraries

### Part A: Supervised Learning (Week 11)

#### Problem 1: k-Nearest Neighbors
```python
class KNN:
    def __init__(self, k=3):
        self.k = k
        
    def fit(self, X, y):
        """Store training data"""
        
    def predict(self, X):
        """Classify using k nearest neighbors"""
        
    def distance(self, x1, x2, metric='euclidean'):
        """Calculate distance between points"""
```

#### Problem 2: Decision Tree (Simplified)
Implement binary decision tree for stellar classification based on color and magnitude.

### Part B: Unsupervised Learning (Week 12-13)

#### Problem 3: k-Means Clustering
```python
class KMeans:
    def __init__(self, n_clusters=3, max_iter=100):
        self.n_clusters = n_clusters
        
    def fit(self, X):
        """Find cluster centers"""
        
    def predict(self, X):
        """Assign points to clusters"""
```

#### Problem 4: Principal Component Analysis
Implement PCA for dimensionality reduction:
1. Standardize data
2. Calculate covariance matrix
3. Find eigenvectors/eigenvalues
4. Project onto principal components

#### Problem 5: Exoplanet Candidate Classification
Apply all methods to classify Kepler Objects of Interest:
- Features: transit depth, duration, period, SNR
- Classes: planet, eclipsing binary, false positive
- Compare with scikit-learn implementations

### Deliverables
- `ml_algorithms.py` module
- Classification performance metrics
- Cluster visualization
- PCA explained variance plot
- **Research Memo** (2-3 pages): Algorithm comparison and performance analysis
- **Growth Memo** (1-2 pages): Understanding machine learning fundamentals

---

## Final Project: Complete Data Science Pipeline
**Due: End of Week 16 (4-Week Project)**

### Learning Outcomes
By completing this project, students will be able to:
- Design and implement a complete data science workflow
- Integrate multiple computational methods
- Validate results against known benchmarks
- Communicate findings effectively
- Demonstrate computational thinking skills

### Project Options

#### Option 1: Exoplanet Discovery Pipeline
Build an end-to-end system to find and validate exoplanets:

1. **Data Acquisition**
   - Download Kepler/TESS data for multiple stars
   - Implement robust data cleaning

2. **Transit Detection**
   - Apply matched filtering
   - Use periodogram for period finding
   - Implement box least squares (BLS)

3. **Model Fitting**
   - Fit physical transit models
   - MCMC for parameter uncertainties (simplified)
   - Validate against limb darkening models

4. **Statistical Validation**
   - Calculate false positive probability
   - Compare with known planets
   - Classify using ML methods

5. **Visualization Dashboard**
   - Interactive plots with Plotly
   - Parameter corner plots
   - Phase-folded light curves

#### Option 2: Custom Scientific Analysis
Choose a dataset from your field and apply learned methods:
- Minimum 5 different computational techniques
- Comparison with standard tools
- Novel analysis or visualization
- Publication-quality outputs

#### Option 3: Algorithm Comparison Study
Comprehensive analysis of algorithm performance:
- Implement 3+ versions of core algorithms
- Benchmark on various problem sizes
- Analyze computational complexity
- Create best practices guide

### Requirements
- Complete documentation with docstrings
- Unit tests for key functions
- Performance benchmarks
- Comparison with professional libraries
- Git repository with clean history

### Final Report Structure
1. **Abstract** (200 words)
2. **Introduction** (1 page)
   - Problem motivation
   - Previous work
   - Your approach
3. **Methods** (2-3 pages)
   - Algorithm descriptions
   - Implementation details
   - Validation approach
4. **Results** (2-3 pages)
   - Findings with figures
   - Performance metrics
   - Comparison with benchmarks
5. **Discussion** (1-2 pages)
   - Interpretation
   - Limitations
   - Future work
6. **Technical Growth Synthesis** (2-3 pages)
   - Learning journey reflection
   - Code evolution examples
   - Key breakthroughs

### Evaluation Criteria
- Technical correctness (25%)
- Code quality & documentation (25%)
- Analysis depth (25%)
- Communication clarity (25%)

---

## General Submission Guidelines

### For All Projects:
1. **Code**: Clean, documented, modular
2. **Notebooks**: Clear narrative with markdown cells
3. **Plots**: Publication quality with proper labels
4. **Research Memo**: LaTeX formatted, 2-3 pages
5. **Growth Memo**: Markdown or LaTeX, 1-2 pages

### GitHub Repository Structure:
```
comp521-assignments/
├── project1/
│   ├── code/
│   ├── data/
│   ├── notebooks/
│   ├── memos/
│   └── README.md
├── project2/
│   └── ...
└── final_project/
    └── ...
```

### AI Usage Disclosure:
Document all AI assistance in comments:
```python
# AI helped debug this indexing issue after 30 min struggle
# Verified correct by testing on known cases
```

---

## Grading Rubrics

### Projects (50% total)
- **Implementation** (40%): Correctness, efficiency
- **Documentation** (20%): Code comments, docstrings
- **Testing** (20%): Validation, edge cases
- **Extension** (20%): Beyond requirements

### Research Memos (part of project grade)
- **Technical Content** (40%): Accuracy, depth
- **Analysis** (30%): Insights, comparisons
- **Communication** (30%): Clarity, figures

### Growth Memos (10% total)
- **Reflection Depth** (50%): Honest assessment
- **Technical Growth** (30%): Skill development
- **Connections** (20%): Links to broader concepts

---

## Resources

### Required Installations:
```bash
conda install numpy scipy pandas matplotlib jupyter
pip install lightkurve astropy
```

### Key Documentation:
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Lightkurve Tutorials](https://docs.lightkurve.org/)

### LaTeX Templates:
Provided in course repository for research memos.

### Office Hours:
Available for project help - schedule on Canvas.
