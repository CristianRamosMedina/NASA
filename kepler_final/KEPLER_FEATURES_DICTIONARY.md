# KEPLER - Selected Features Dictionary

## 20 Features Selected (Correlation >= 0.3, p < 0.05)

---

### 1. **koi_score** (Spearman: 0.750)
- **Description**: Confidence score in the KOI disposition (0-1 scale)
- **Units**: Dimensionless
- **Type**: Continuous
- **Interpretation**: Higher values indicate higher confidence that the object is a planet

### 2. **koi_fwm_stat_sig** (Spearman: 0.451)
- **Description**: Statistical significance of flux-weighted offset between in-transit and out-of-transit images
- **Units**: Percentage
- **Type**: Continuous
- **Interpretation**: Detects centroid shifts during transit (used to identify false positives)

### 3. **koi_srho_err2** (Spearman: 0.377)
- **Description**: Negative uncertainty for fitted stellar density
- **Units**: g/cm³
- **Type**: Continuous
- **Interpretation**: Error bar (lower bound) for stellar density measurement

### 4. **koi_dor_err2** (Spearman: 0.365)
- **Description**: Negative uncertainty for planet-star distance over star radius (a/R*)
- **Units**: Dimensionless
- **Type**: Continuous
- **Interpretation**: Error bar (lower bound) for orbital separation

### 5. **koi_dor_err1** (Spearman: 0.365)
- **Description**: Positive uncertainty for planet-star distance over star radius (a/R*)
- **Units**: Dimensionless
- **Type**: Continuous
- **Interpretation**: Error bar (upper bound) for orbital separation

### 6. **koi_incl** (Spearman: 0.362)
- **Description**: Orbital inclination angle (angle between plane of sky and orbital plane)
- **Units**: Degrees
- **Type**: Continuous
- **Interpretation**: ~90° indicates edge-on orbit (favorable for transit detection)

### 7. **koi_prad_err1** (Spearman: 0.351)
- **Description**: Positive uncertainty for planetary radius
- **Units**: Earth radii
- **Type**: Continuous
- **Interpretation**: Error bar (upper bound) for planet radius

### 8. **koi_count** (Chi-Square: 0.343)
- **Description**: Number of planet candidates identified in the same stellar system
- **Units**: Count
- **Type**: Categorical
- **Interpretation**: Multi-planet systems may have different validation rates

### 9. **koi_dor** (Spearman: 0.330)
- **Description**: Planet-star distance at mid-transit divided by stellar radius (a/R*)
- **Units**: Dimensionless
- **Type**: Continuous
- **Interpretation**: Larger values = farther from star

### 10. **koi_dikco_mdec_err** (Spearman: 0.328)
- **Description**: Uncertainty for angular offset in Declination from PRF (Pixel Response Function) centroids
- **Units**: Arcseconds
- **Type**: Continuous
- **Interpretation**: Measures centroid offset precision (false positive detection)

### 11. **koi_period_err1** (Spearman: 0.327)
- **Description**: Positive uncertainty for orbital period
- **Units**: Days
- **Type**: Continuous
- **Interpretation**: Error bar (upper bound) for orbital period

### 12. **koi_period_err2** (Spearman: 0.327)
- **Description**: Negative uncertainty for orbital period
- **Units**: Days
- **Type**: Continuous
- **Interpretation**: Error bar (lower bound) for orbital period

### 13. **koi_dikco_mra_err** (Spearman: 0.319)
- **Description**: Uncertainty for angular offset in Right Ascension from PRF centroids
- **Units**: Arcseconds
- **Type**: Continuous
- **Interpretation**: Measures centroid offset precision in RA direction

### 14. **koi_prad_err2** (Spearman: 0.316)
- **Description**: Negative uncertainty for planetary radius
- **Units**: Earth radii
- **Type**: Continuous
- **Interpretation**: Error bar (lower bound) for planet radius

### 15. **koi_dikco_msky_err** (Spearman: 0.315)
- **Description**: Uncertainty for sky offset from PRF centroids
- **Units**: Arcseconds
- **Type**: Continuous
- **Interpretation**: Combined centroid offset uncertainty

### 16. **koi_max_sngle_ev** (Spearman: 0.314)
- **Description**: Maximum single event statistic
- **Units**: Dimensionless
- **Type**: Continuous
- **Interpretation**: Depth of deepest single transit event

### 17. **koi_prad** (Spearman: 0.312)
- **Description**: Planetary radius
- **Units**: Earth radii (R⊕)
- **Type**: Continuous
- **Interpretation**: Size of the planet (1.0 = Earth-sized, >11 = Jupiter-sized)

### 18. **koi_dicco_mdec_err** (Spearman: 0.311)
- **Description**: Uncertainty for difference image control centroid offset in Declination
- **Units**: Arcseconds
- **Type**: Continuous
- **Interpretation**: Alternative centroid offset measurement

### 19. **koi_model_snr** (Spearman: 0.309)
- **Description**: Signal-to-Noise Ratio of the transit model fit
- **Units**: Dimensionless
- **Type**: Continuous
- **Interpretation**: Higher SNR = stronger/cleaner transit signal

### 20. **koi_dicco_mra_err** (Spearman: 0.301)
- **Description**: Uncertainty for difference image control centroid offset in Right Ascension
- **Units**: Arcseconds
- **Type**: Continuous
- **Interpretation**: Alternative centroid offset measurement in RA

---

## Feature Categories

### **Primary Discriminators (High Correlation)**
1. **koi_score** (0.750) - Disposition confidence
2. **koi_fwm_stat_sig** (0.451) - Centroid shift detection

### **Measurement Uncertainties**
- Planet radius errors: koi_prad_err1, koi_prad_err2
- Orbital distance errors: koi_dor_err1, koi_dor_err2
- Period errors: koi_period_err1, koi_period_err2
- Stellar density error: koi_srho_err2

### **Centroid Offset Measurements** (False Positive Detection)
- koi_dikco_mdec_err, koi_dikco_mra_err, koi_dikco_msky_err
- koi_dicco_mdec_err, koi_dicco_mra_err

### **Physical Properties**
- koi_prad (planetary radius)
- koi_dor (orbital distance)
- koi_incl (orbital inclination)

### **Signal Quality**
- koi_model_snr (signal-to-noise ratio)
- koi_max_sngle_ev (single event depth)

### **System Properties**
- koi_count (number of planets in system)

---

## Notes

- **err1** = positive/upper uncertainty
- **err2** = negative/lower uncertainty
- **dikco** = Difference Image KIC Control (centroid offset method)
- **dicco** = Difference Image Control Centroid (alternative method)
- **PRF** = Pixel Response Function
- **KOI** = Kepler Object of Interest
- **a/R*** = Semi-major axis / Stellar radius

---

## Target Variable

**koi_disposition** - 3 classes:
- **CONFIRMED**: Verified exoplanet
- **CANDIDATE**: Likely planet, pending confirmation
- **FALSE POSITIVE**: Not a planet (eclipsing binary, background star, etc.)

---

Generated: 2025-10-04
Source: NASA Exoplanet Archive
