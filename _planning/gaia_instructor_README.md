# Gaia DR3 Teaching Dataset Preparation Guide
## COMP 521: Introduction to Scientific Computing and Data Science

---

## Quick Start

```bash
# Clone this repository
git clone [repository-url]
cd gaia-teaching-datasets

# Install requirements
pip install -r requirements.txt

# Generate all datasets (takes ~5-10 minutes)
python prepare_gaia_datasets.py
```

This creates all datasets needed for the semester. Students receive "sensor array" data without knowing it's astronomical.

---

## Purpose & Pedagogical Approach

### Why This Dataset?

The Gaia DR3 stellar catalog provides ideal teaching data because:
- **Natural clustering**: Students discover real patterns (HR diagram) without prompting
- **Multi-dimensional**: 10+ features for exploring relationships
- **Real messiness**: Missing values, outliers, quality issues
- **Scalable complexity**: Simple 2D patterns to complex multi-dimensional analysis
- **Unknown to students**: Even astronomy students won't recognize renamed columns

### Learning Goals

Students will:
1. **Project 1**: Discover fundamental patterns through EDA (Week 2)
2. **Project 6**: Apply clustering to find natural groupings (Week 12)
3. **Final Project**: Combine with Kepler data for complete pipeline

They achieve authentic scientific discovery without requiring domain knowledge.

---

## Prerequisites & Setup

### Required Software

```bash
# Python 3.8+ with packages:
pip install astroquery>=0.4.6
pip install astropy>=5.0
pip install pandas>=1.3.0
pip install numpy>=1.21.0
pip install matplotlib>=3.4.0
pip install seaborn>=0.11.0
```

### System Requirements
- **Internet connection** for Gaia archive query (~50MB download)
- **Storage**: ~100MB for all generated files
- **RAM**: 4GB minimum for data processing
- **Time**: 5-10 minutes for complete pipeline

### Directory Structure
```
comp521-datasets/
├── prepare_gaia_datasets.py      # Main preparation script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── data/
│   ├── sensor_data_clean.csv     # Main teaching dataset
│   ├── sensor_data_raw.csv       # Messy version for cleaning
│   ├── sensor_data_README.txt    # Student documentation
│   └── gaia_raw_astronomy.csv    # Backup (instructor only)
└── validation/
    └── instructor_plots.png       # Validation visualizations
```

---

## Detailed Dataset Preparation

### Step 1: Understanding the Data Pipeline

The script performs these transformations:
1. **Query Gaia Archive** → 30,000 nearby stars with good measurements
2. **Filter Quality** → Remove poor astrometric solutions
3. **Rename Columns** → Hide astronomical context
4. **Add Messiness** → Create realistic data cleaning challenges
5. **Sample Size** → 20,000 for clean, 25,000 for raw
6. **Generate Documentation** → Student-friendly descriptions

### Step 2: Running the Preparation Script

```python
# Full pipeline with all options
python prepare_gaia_datasets.py --all

# Or run interactively in Python:
from prepare_gaia_datasets import create_all_datasets
df_clean, df_messy = create_all_datasets()
```

### Step 3: Column Transformations

| Original (Astronomy) | Renamed (Generic) | Student Understanding |
|---------------------|-------------------|----------------------|
| ra, dec | sensor_x, sensor_y | Position coordinates |
| parallax | distance_indicator | Inverse distance measurement |
| pmra, pmdec | velocity_x, velocity_y | Motion across sensor |
| phot_g_mean_mag | brightness | Logarithmic brightness |
| bp_rp | color_index | Color measurement |
| ruwe | quality_flag | Data quality metric |
| parallax → 1000/parallax | computed_distance | Derived distance |
| M = m + 5log₁₀(π) - 10 | absolute_brightness | Distance-corrected brightness |

### Step 4: Data Quality Selections

**Clean Dataset Criteria:**
```python
# High-quality measurements only
parallax > 1                    # Within 1000 pc
parallax_error < 0.1            # Excellent parallax
parallax/parallax_error > 20    # High SNR
ruwe < 1.4                      # Good astrometric solution
phot_g_mean_flux_over_error > 100  # Good photometry
```

**Messy Dataset Additions:**
- 5% random NaN values in velocities
- 2% duplicate entries
- 1% bad measurements (high uncertainties)
- Shuffled row order

---

## Output Files Description

### Primary Files for Students

#### `sensor_data_clean.csv` (Main Dataset)
- **Size**: 20,000 rows × 12 columns
- **Use**: Projects 1 (EDA) and 6 (Clustering)
- **Quality**: Pre-filtered, no missing values
- **Key Feature**: Contains hidden HR diagram pattern

#### `sensor_data_raw.csv` (Cleaning Exercise)
- **Size**: ~25,000 rows × 12 columns
- **Use**: Data cleaning practice in Project 1
- **Issues**: NaNs, duplicates, outliers, bad quality flags
- **Purpose**: Teach real-world data preprocessing

#### `sensor_data_README.txt` (Student Documentation)
- Generic descriptions avoiding astronomy terminology
- Column explanations with units
- Suggested analyses (without giving away patterns)
- Data quality guidelines

### Instructor-Only Files

#### `gaia_raw_astronomy.csv` (Backup)
- Original column names preserved
- Full 30,000 star sample
- Use if re-generation needed

#### `instructor_validation_plots.png`
- HR diagram verification
- Distance distributions
- Quality checks
- Pattern confirmation

---

## Assignment Integration

### Project 1: Exploratory Data Analysis (Week 2)

**Student Prompt:**
> "Explore the sensor array dataset to understand its structure and discover patterns. Create at least 6 different visualizations exploring relationships between features. Pay special attention to brightness and color measurements."

**Expected Discoveries:**
- Clear sequences in brightness vs color plot (main sequence, red giants)
- Distance distribution biases
- Quality variations affect measurements
- Correlations between features

**Grading Checklist:**
- [ ] Found brightness-color relationship (the HR diagram)
- [ ] Identified at least 2 distinct groups
- [ ] Appropriate handling of outliers
- [ ] Statistical summaries computed
- [ ] Quality visualizations with proper labels

### Project 6: Machine Learning (Week 12)

**Student Prompt:**
> "Apply your clustering implementations to find natural groupings in the sensor data. Compare k-means, hierarchical clustering, and PCA. How many meaningful clusters exist?"

**Expected Results:**
- k-means: 2-3 clusters (main sequence, giants, possibly white dwarfs)
- Hierarchical: Sub-structure within main groups
- PCA: Most variance in first 2 components

**Assessment Points:**
- Correct implementation of algorithms
- Appropriate feature selection
- Cluster validation metrics
- Interpretation of results

---

## Common Issues & Solutions

### Problem: Gaia Query Timeout
```python
# Solution: Use smaller query or local backup
df = pd.read_csv('backup_data/gaia_raw_astronomy.csv')
```

### Problem: Memory Issues with Large Dataset
```python
# Solution: Use chunking or sampling
df = pd.read_csv('sensor_data_clean.csv', nrows=10000)
# Or
df = df.sample(n=10000, random_state=42)
```

### Problem: Students Recognize Astronomical Data
**Response**: "This is a generic sensor array dataset used in many fields. Focus on the patterns you discover rather than trying to identify the specific application."

### Problem: Missing Dependencies
```bash
# Complete environment setup
conda create -n comp521 python=3.9
conda activate comp521
pip install -r requirements.txt
```

---

## Advanced Modifications

### Adjusting Dataset Size

```python
# For smaller class or limited computers
def create_small_dataset(n_stars=5000):
    df = download_gaia_sample(n_stars=n_stars)
    return prepare_teaching_datasets(df)
```

### Adding More Features

```python
# Include additional measurements
EXTENDED_COLUMNS = {
    'phot_g_mean_flux': 'sensor_intensity',
    'astrometric_excess_noise': 'measurement_scatter',
    'visibility_periods_used': 'observation_count'
}
```

### Custom Selection Criteria

```python
# Modify query for different stellar populations
query_young_stars = """
SELECT TOP 10000 ...
WHERE parallax > 5  -- Very nearby
  AND bp_rp < 1      -- Blue (young) stars
  AND ...
"""
```

---

## Validation & Quality Checks

### Verify Pattern Visibility

```python
# Quick check that HR diagram is visible
df = pd.read_csv('sensor_data_clean.csv')
plt.scatter(df['color_index'], df['absolute_brightness'], 
            s=1, alpha=0.5)
plt.gca().invert_yaxis()
plt.xlabel('Color Index')
plt.ylabel('Absolute Brightness')
plt.title('Should show clear diagonal sequence + branch')
plt.show()
```

### Check Data Quality

```python
# Ensure no unexpected issues
assert df['quality_flag'].max() < 2.0
assert df['measurement_quality'].min() > 10
assert not df.isnull().any().any()  # No NaNs in clean
print(f"✓ Data quality verified: {len(df)} clean samples")
```

---

## Student Support Materials

### Starter Code Template

```python
"""Project 1 Starter: Sensor Array Analysis"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('sensor_data_clean.csv')

# Your exploration begins here!
# Hint 1: Check data types and ranges
# Hint 2: Look for relationships between features
# Hint 3: Some features might need log scaling for visualization
```

### Common Student Questions

**Q: Why is brightness on a backward scale?**  
A: "Logarithmic sensor measurements often use inverse scales. Focus on relative values."

**Q: What patterns should we look for?**  
A: "Let the data guide you. Start with pairwise relationships and see what emerges."

**Q: How many clusters should we find?**  
A: "Use metrics like silhouette score to determine optimal cluster count."

---

## Teaching Tips

### Week 2 (Project 1 Lab)
1. Have students start with basic statistics
2. Guide toward scatter plots without specifying which
3. When someone finds brightness-color pattern, have them share
4. Celebrate the "discovery" without revealing it's the HR diagram

### Week 12 (Project 6 Lab)
1. Students should use same data from Project 1
2. Start with 2D clustering on brightness-color
3. Expand to higher dimensions
4. Compare with their Project 1 visual discoveries

### Revealing the Truth (Optional, End of Semester)
Consider revealing this is real stellar data after final projects. Students are often amazed they discovered a fundamental astronomical relationship without any physics knowledge.

---

## Troubleshooting Guide

### If Gaia Archive is Down
```bash
# Use provided backup
cp backups/gaia_30k_backup.csv gaia_raw_astronomy.csv
python prepare_datasets.py --from-backup
```

### For Different Class Sizes
- Small class (< 20): Use full 20k dataset
- Large class (> 50): Consider 10k for faster processing
- Online course: Provide pre-generated CSVs only

### Performance Optimization
```python
# For slow computers, use dtype optimization
dtypes = {
    'sensor_x': np.float32,
    'sensor_y': np.float32,
    'brightness': np.float32
}
df = pd.read_csv('sensor_data_clean.csv', dtype=dtypes)
```

---

## License & Attribution

This teaching dataset is derived from:
- **Source**: ESA Gaia Data Release 3 (2022)
- **License**: CC BY-SA 3.0 IGO
- **Citation** (for instructors only): Gaia Collaboration et al. (2022)

Students should NOT be informed of the astronomical source until after projects are complete.

---

## Support & Contact

For issues or questions:
1. Check this README first
2. See troubleshooting section
3. Review validation plots
4. Contact course coordinator

---

## Version History

- **v1.0** (2024): Initial version for COMP 521
- Based on Gaia DR3 (2022 release)
- Tested with Python 3.8-3.11

---

## Final Checklist

Before semester starts:
- [ ] Run `prepare_gaia_datasets.py`
- [ ] Verify all CSV files created
- [ ] Check validation plots
- [ ] Test student starter code
- [ ] Upload files to course LMS
- [ ] Remove astronomy references from student materials
- [ ] Prepare grading rubrics

Ready to teach data science with authentic discovery! 🚀
