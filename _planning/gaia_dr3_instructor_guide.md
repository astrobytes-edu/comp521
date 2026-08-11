# Gaia DR3 Instructor Guide for COMP 521
## Dataset Preparation and Assignment Integration

---

## Overview
This guide provides complete code for preparing Gaia DR3 data as a "sensor array dataset" for COMP 521. Students will analyze this data without knowing it's astronomical, discovering patterns like the HR diagram naturally through EDA.

---

## Dataset Specifications

### Target Size
- **Clean dataset:** 20,000 stars (manageable for student laptops)
- **Raw dataset:** 25,000 stars (includes messy data for cleaning practice)

### Renamed Columns (Hide Astronomy Context)
```python
COLUMN_MAPPING = {
    'ra': 'sensor_x',
    'dec': 'sensor_y', 
    'parallax': 'distance_indicator',
    'pmra': 'velocity_x',
    'pmdec': 'velocity_y',
    'phot_g_mean_mag': 'brightness',
    'bp_rp': 'color_index',
    'phot_bp_mean_mag': 'blue_sensor',
    'phot_rp_mean_mag': 'red_sensor',
    'parallax_error': 'distance_uncertainty',
    'ruwe': 'quality_flag',
    'radial_velocity': 'z_velocity'
}
```

---

## Complete Data Preparation Pipeline

### Step 1: Install Required Packages
```python
# Run once for setup
!pip install astroquery
!pip install astropy
!pip install pandas numpy matplotlib
```

### Step 2: Query and Download Gaia DR3 Data
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia
import warnings
warnings.filterwarnings('ignore')

def download_gaia_sample(n_stars=30000, save_raw=True):
    """
    Download sample of Gaia DR3 data for teaching purposes.
    Focuses on nearby, bright stars with good measurements.
    """
    
    # Configure Gaia query
    Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
    Gaia.ROW_LIMIT = n_stars
    
    # Query for nearby stars with good data
    # This query gets stars suitable for HR diagram discovery
    query = """
    SELECT TOP {n}
        ra, dec, parallax, parallax_error,
        pmra, pmdec,
        phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag,
        bp_rp, ruwe, radial_velocity,
        phot_g_mean_flux_over_error,
        phot_bp_mean_flux_over_error,
        phot_rp_mean_flux_over_error
    FROM gaiadr3.gaia_source
    WHERE parallax > 1                    -- Nearby stars (< 1000 pc)
        AND parallax_error < 0.1          -- Good parallax
        AND parallax/parallax_error > 10  -- High SNR
        AND phot_g_mean_mag < 16          -- Bright enough
        AND bp_rp IS NOT NULL              -- Has color
        AND ruwe < 2                       -- Good astrometric solution
        AND phot_g_mean_flux_over_error > 50
    ORDER BY random_index
    """.format(n=n_stars)
    
    print(f"Querying Gaia DR3 for {n_stars} stars...")
    job = Gaia.launch_job(query)
    results = job.get_results()
    
    # Convert to pandas
    df = results.to_pandas()
    print(f"Downloaded {len(df)} stars")
    
    if save_raw:
        df.to_csv('gaia_raw_astronomy.csv', index=False)
        print("Saved raw astronomical data to 'gaia_raw_astronomy.csv'")
    
    return df
```

### Step 3: Create Teaching Datasets
```python
def prepare_teaching_datasets(df_raw, add_messiness=True):
    """
    Prepare clean and messy versions of the data for student exercises.
    Renames columns to hide astronomical nature.
    """
    
    # Start with copy
    df = df_raw.copy()
    
    # Compute derived features before renaming
    df['distance_pc'] = 1000.0 / df['parallax']  # Distance in parsecs
    df['abs_mag'] = df['phot_g_mean_mag'] + 5*np.log10(df['parallax']) - 10
    
    # Create quality metrics
    df['snr_distance'] = df['parallax'] / df['parallax_error']
    
    # === Create MESSY dataset for cleaning exercise ===
    if add_messiness:
        df_messy = df.copy()
        n_messy = len(df_messy)
        
        # Add some NaN values randomly (5% of data)
        nan_mask = np.random.random((n_messy, 3)) < 0.05
        df_messy.loc[nan_mask[:, 0], 'pmra'] = np.nan
        df_messy.loc[nan_mask[:, 1], 'pmdec'] = np.nan
        df_messy.loc[nan_mask[:, 2], 'radial_velocity'] = np.nan
        
        # Add some duplicates (2%)
        n_duplicates = int(0.02 * n_messy)
        duplicate_indices = np.random.choice(df_messy.index, n_duplicates)
        df_duplicates = df_messy.loc[duplicate_indices].copy()
        df_messy = pd.concat([df_messy, df_duplicates], ignore_index=True)
        
        # Add some outliers with bad measurements (1%)
        n_outliers = int(0.01 * len(df_messy))
        outlier_indices = np.random.choice(df_messy.index, n_outliers, replace=False)
        df_messy.loc[outlier_indices, 'parallax_error'] *= 10  # Bad uncertainties
        df_messy.loc[outlier_indices, 'ruwe'] = np.random.uniform(2, 5, n_outliers)
        
        # Shuffle rows
        df_messy = df_messy.sample(frac=1).reset_index(drop=True)
        
        # Rename columns to hide astronomy
        df_messy_renamed = df_messy.rename(columns=COLUMN_MAPPING)
        
        # Add computed features with generic names
        df_messy_renamed['computed_distance'] = df_messy['distance_pc']
        df_messy_renamed['absolute_brightness'] = df_messy['abs_mag']
        df_messy_renamed['measurement_quality'] = df_messy['snr_distance']
        
        # Save messy dataset
        df_messy_renamed.to_csv('sensor_data_raw.csv', index=False)
        print(f"Created messy dataset with {len(df_messy_renamed)} entries")
    
    # === Create CLEAN dataset for analysis ===
    # Remove poor quality data
    df_clean = df[
        (df['ruwe'] < 1.4) &                    # Good astrometric solution
        (df['parallax_error'] < 0.05) &         # Excellent parallax
        (df['parallax'] / df['parallax_error'] > 20) &  # High SNR
        (df['phot_g_mean_flux_over_error'] > 100)      # Good photometry
    ].copy()
    
    # Sample to exact size
    if len(df_clean) > 20000:
        df_clean = df_clean.sample(n=20000, random_state=42)
    
    # Rename columns
    df_clean_renamed = df_clean.rename(columns=COLUMN_MAPPING)
    
    # Add computed features
    df_clean_renamed['computed_distance'] = df_clean['distance_pc']
    df_clean_renamed['absolute_brightness'] = df_clean['abs_mag']
    df_clean_renamed['measurement_quality'] = df_clean['snr_distance']
    
    # Sort by brightness for consistent ordering
    df_clean_renamed = df_clean_renamed.sort_values('brightness').reset_index(drop=True)
    
    # Save clean dataset
    df_clean_renamed.to_csv('sensor_data_clean.csv', index=False)
    print(f"Created clean dataset with {len(df_clean_renamed)} entries")
    
    return df_clean_renamed, df_messy_renamed if add_messiness else None
```

### Step 4: Create Validation Plots (Instructor Only)
```python
def validate_datasets(df_clean, df_messy=None):
    """
    Create plots to verify the datasets show expected patterns.
    Students will discover these patterns on their own!
    """
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot 1: "HR Diagram" (students will discover this)
    ax = axes[0, 0]
    scatter = ax.scatter(df_clean['color_index'], 
                        df_clean['absolute_brightness'],
                        c=df_clean['color_index'], 
                        s=1, alpha=0.5, cmap='RdYlBu_r')
    ax.set_xlabel('Color Index')
    ax.set_ylabel('Absolute Brightness')
    ax.set_title('Check: Should show clear sequences')
    ax.invert_yaxis()
    plt.colorbar(scatter, ax=ax)
    
    # Plot 2: Distance distribution
    ax = axes[0, 1]
    ax.hist(df_clean['computed_distance'], bins=50, edgecolor='black')
    ax.set_xlabel('Distance (units)')
    ax.set_ylabel('Count')
    ax.set_title('Distance Distribution')
    ax.set_xlim(0, 1000)
    
    # Plot 3: Sky positions
    ax = axes[0, 2]
    ax.scatter(df_clean['sensor_x'], df_clean['sensor_y'], 
              s=1, alpha=0.3)
    ax.set_xlabel('Sensor X')
    ax.set_ylabel('Sensor Y')
    ax.set_title('Sensor Array Coverage')
    
    # Plot 4: Quality flag distribution
    ax = axes[1, 0]
    ax.hist(df_clean['quality_flag'], bins=30, edgecolor='black')
    ax.set_xlabel('Quality Flag')
    ax.set_ylabel('Count')
    ax.set_title('Data Quality Distribution')
    
    # Plot 5: Brightness distribution
    ax = axes[1, 1]
    ax.hist(df_clean['brightness'], bins=50, edgecolor='black')
    ax.set_xlabel('Brightness')
    ax.set_ylabel('Count')
    ax.set_title('Brightness Distribution')
    
    # Plot 6: Proper motion
    ax = axes[1, 2]
    ax.scatter(df_clean['velocity_x'], df_clean['velocity_y'],
              s=1, alpha=0.3)
    ax.set_xlabel('Velocity X')
    ax.set_ylabel('Velocity Y')
    ax.set_title('Velocity Distribution')
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    
    plt.tight_layout()
    plt.savefig('instructor_validation_plots.png', dpi=150)
    plt.show()
    
    print("\nDataset Statistics:")
    print(f"Total objects: {len(df_clean)}")
    print(f"Distance range: {df_clean['computed_distance'].min():.1f} - "
          f"{df_clean['computed_distance'].max():.1f}")
    print(f"Brightness range: {df_clean['brightness'].min():.1f} - "
          f"{df_clean['brightness'].max():.1f}")
    print(f"Color range: {df_clean['color_index'].min():.2f} - "
          f"{df_clean['color_index'].max():.2f}")
```

### Step 5: Main Execution Script
```python
def create_all_datasets():
    """
    Complete pipeline to create all teaching datasets.
    Run this once at the beginning of the semester.
    """
    
    # Download from Gaia
    df_raw = download_gaia_sample(n_stars=30000)
    
    # Prepare teaching versions
    df_clean, df_messy = prepare_teaching_datasets(df_raw, add_messiness=True)
    
    # Validate (instructor only)
    print("\nValidating datasets...")
    validate_datasets(df_clean, df_messy)
    
    # Create metadata file for students
    create_student_readme()
    
    print("\n✓ All datasets created successfully!")
    print("Files created:")
    print("  - sensor_data_clean.csv (for Projects 1 & 6)")
    print("  - sensor_data_raw.csv (for data cleaning exercise)")
    print("  - sensor_data_README.txt (for students)")
    print("  - instructor_validation_plots.png (for you)")
    
    return df_clean, df_messy

def create_student_readme():
    """
    Create README file for students describing the dataset.
    """
    readme_text = """
Sensor Array Dataset
====================

This dataset contains measurements from a distributed sensor array monitoring
distant light sources. Each row represents one light source with various 
measurements collected over time.

Files:
------
- sensor_data_clean.csv: Pre-processed data ready for analysis
- sensor_data_raw.csv: Raw data requiring cleaning (contains duplicates, NaN values)

Column Descriptions:
--------------------
- sensor_x, sensor_y: Position coordinates in the sensor array
- distance_indicator: Measurement inversely related to distance (parallax)
- velocity_x, velocity_y: Apparent motion across the sensor plane
- brightness: Logarithmic brightness measurement (magnitude scale)
- color_index: Color measurement (blue minus red sensors)
- quality_flag: Data quality indicator (lower is better)
- computed_distance: Derived distance estimate
- absolute_brightness: Brightness corrected for distance

Data Characteristics:
---------------------
- ~20,000 measurements in clean dataset
- Distance range: 10-1000 units
- Some measurements may have missing values (especially in raw data)
- Quality flags > 1.5 may indicate unreliable measurements

Suggested Analyses:
-------------------
1. Explore relationships between brightness and color
2. Investigate distance distributions
3. Find natural groupings in the multi-dimensional space
4. Identify and remove outliers
5. Study the relationship between measured and absolute brightness

Note: This is real scientific data with natural patterns waiting to be discovered!
"""
    
    with open('sensor_data_README.txt', 'w') as f:
        f.write(readme_text)

# Run the complete pipeline
if __name__ == "__main__":
    df_clean, df_messy = create_all_datasets()
```

---

## Student-Facing Starter Code

### For Project 1: EDA Starter
```python
"""
Project 1: Exploratory Data Analysis
Starter code for analyzing sensor array data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class SensorDataAnalyzer:
    """Class for analyzing sensor array measurements"""
    
    def __init__(self, filepath):
        """Load and prepare data"""
        self.data = pd.read_csv(filepath)
        self.clean_data = None
        
    def basic_info(self):
        """Display basic information about the dataset"""
        print(f"Dataset shape: {self.data.shape}")
        print(f"\nColumn types:\n{self.data.dtypes}")
        print(f"\nMissing values:\n{self.data.isnull().sum()}")
        print(f"\nBasic statistics:\n{self.data.describe()}")
        
    def clean_dataset(self):
        """Remove outliers and handle missing values"""
        # TODO: Implement cleaning logic
        # Consider quality_flag values
        # Handle NaN values appropriately
        pass
    
    def plot_distributions(self):
        """Create distribution plots for all features"""
        # TODO: Create histograms for each feature
        pass
    
    def plot_relationships(self):
        """Explore relationships between variables"""
        # TODO: Create scatter plots
        # Hint: Try brightness vs color_index
        # Hint: Try distance vs brightness
        pass
    
    def find_patterns(self):
        """Look for natural groupings in the data"""
        # TODO: Explore 2D relationships
        # What patterns emerge?
        pass

# Load the data
analyzer = SensorDataAnalyzer('sensor_data_clean.csv')
analyzer.basic_info()

# Your analysis starts here!
```

### For Project 6: Clustering Starter
```python
"""
Project 6: Clustering Analysis
Apply your clustering algorithms to find groups in sensor data
"""

import pandas as pd
import numpy as np
from your_ml_module import KMeans, PCA  # Your implementations

# Load the same data from Project 1
data = pd.read_csv('sensor_data_clean.csv')

# Select features for clustering
# Hint: brightness-color space shows interesting patterns
features = ['color_index', 'absolute_brightness']
X = data[features].values

# Apply your clustering algorithm
# How many clusters do you find?
# What characterizes each cluster?
```

---

## Assignment Integration

### Project 1 (Week 2): EDA Discovery
**Student Instructions:**
"Analyze the sensor array dataset to discover natural patterns. Pay special attention to relationships between brightness and color. What groupings do you see?"

**What Students Should Discover:**
- Clear sequences in brightness vs color (main sequence, giants)
- Distance distribution (selection effects)
- Quality variations in measurements
- Natural clustering in feature space

**Grading Hints:**
- Check if they found the brightness-color relationship
- Did they handle outliers appropriately?
- Quality of visualizations
- Depth of statistical analysis

### Project 6 (Week 12): Clustering Application  
**Student Instructions:**
"Apply your clustering implementations to the sensor data. How many natural groups exist? What features best separate them?"

**Expected Outcomes:**
- k-means should find 2-3 main groups (main sequence, giants, maybe white dwarfs)
- PCA should show most variance in first 2-3 components
- Hierarchical clustering reveals sub-structure

---

## Instructor Notes

### What Students Don't Need to Know:
- This is Gaia DR3 stellar data
- They're discovering the Hertzsprung-Russell diagram
- The clusters are different stellar populations
- Parallax is being used for distance

### Common Student Questions:
**Q: "Why is brightness measured on a negative/backward scale?"**
A: "This is a logarithmic scale where brighter objects have lower values - common in sensor measurements."

**Q: "What does 'absolute brightness' mean?"**
A: "It's brightness corrected for distance - what the brightness would be at a standard distance."

**Q: "What are these patterns in brightness vs color?"**
A: "Great discovery! You've found natural groupings in the data. This is exactly the kind of pattern we're looking for."

### Troubleshooting:
- If Gaia query fails: Use the backup CSV files provided
- If students need more data: The query can be modified for up to 100k stars
- For faster queries: Add more restrictive parallax cuts

### Extensions for Advanced Students:
- Add proper motion analysis
- Include radial velocity where available
- 3D position reconstruction
- Time series from Gaia epochs (if available)

---

## Quick Reference

### File Outputs:
```
sensor_data_clean.csv     # Main dataset for Projects 1 & 6
sensor_data_raw.csv       # Messy data for cleaning exercise
sensor_data_README.txt    # Student documentation
gaia_raw_astronomy.csv    # Backup (instructor only)
instructor_validation_plots.png  # Verification plots
```

### Key Patterns Students Should Find:
1. Main sequence (diagonal line in brightness-color)
2. Red giant branch (bright, red objects)
3. White dwarfs (if included - faint, blue objects)
4. Distance limits from selection effects
5. Quality variations affect measurements

### Grading Rubric Hints:
- **Excellent**: Finds and explains main sequence pattern
- **Good**: Identifies multiple groupings, good visualizations
- **Adequate**: Basic EDA, some pattern recognition
- **Needs Work**: Minimal exploration, missed obvious patterns

---

## One-Line Execution

To create all datasets at once:
```python
# Just run this!
exec(open('prepare_gaia_datasets.py').read())
```

This will download, process, and create all necessary files for the semester.
