# 🎧 What Makes a Spotify Track Popular?
*Predicting popularity using audio features, track metadata, and artist context*

Music streaming platforms have reshaped the modern music industry, creating an environment where millions of tracks compete for attention but only a small subset become widely popular. This project examines whether Spotify track popularity can be predicted using musical attributes, track metadata, and artist context at the track level.

## Project Structure
├── 01_data_wrangling.ipynb  
├── 02_exploratory_data_analysis.ipynb  
├── 03_modeling_and_preprocessing.ipynb (in progress)  
├── README.md  
├── requirements.txt

## Notebooks

**01_data_wrangling.ipynb**  
Cleans and restructures raw Spotify track and artist data, producing an enriched track-level dataset for analysis and modeling.

**02_exploratory_data_analysis.ipynb**  
Explores distributions, relationships, and statistical differences to understand which features are associated with track popularity.

**03_modeling_and_preprocessing.ipynb (in progress)**  
Performs model-specific preprocessing and builds predictive models to estimate Spotify track popularity.

## Project Status
- Data wrangling: complete  
- Exploratory data analysis: complete  
- Modeling and preprocessing: in progress  
- Documentation and presentation: planned

## Data
The data used in this project was sourced from public Spotify track and artist datasets available on Kaggle. Raw data files are not included in this repository due to size and licensing constraints. The notebooks assume access to local copies of these datasets.

## Tools
Python, pandas, numpy, seaborn, matplotlib, scipy
