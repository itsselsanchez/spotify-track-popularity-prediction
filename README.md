# 🎧 Hit or Miss? Predicting Hit Songs on Spotify with Machine Learning
*Predicting hit status using audio features, track metadata, and artist context*

Music streaming platforms have reshaped the modern music industry. Millions of tracks compete for attention, but only a small fraction become hits.

This project asks a simple question:

**Can we predict a hit using only what we know about a track and who made it?**

## 🔑 Key Findings
**Short answer:** Yes.
The final XGBoost model achieved a **PR-AUC of 0.812**, well above the **0.205 random baseline**.

**Long answer**: Yes, but not in the way you might expect.

- 🎯 **It doesn’t learn what makes a song sound good.**  
  It learns **when** the song was released and **who** made it.
- 📈 **It excels at modern music.**  
  The model correctly identifies **89.4% of hits from 2010–2021**.
- 📉 **It struggles with older tracks.**  
  Hit detection drops to **9.5% for songs from 1950–1979**.
- 🎶 **Audio features matter less than you’d think.**  
  Danceability, energy, and tempo had minimal impact.
- 🌍 **Context drives performance.**  
  Release year, artist popularity, and genre carried the model.

💡 **Takeaway**:  
**The sound matters, but the story behind a song matters more.**

## 🗂️ Project Structure
```
|- notebooks/
  |- 01_data_wrangling.ipynb
  |- 02_exploratory_data_analysis.ipynb
  |- 03_modeling_and_preprocessing.ipynb
|- assets/
  |- spotify_popularity_analysis_static.pdf
  |- spotify_hit_prediction_report.pdf
  |- xgb_v2_model_metrics.pdf
|- game/
  |- .streamlit/
    |- config.toml
  |- app.py
  |- spotify_game_dataset.csv
  |- robot.png
  |- human.png
  |- game_hit_or_miss_header.png
|- README.md
|- requirements.txt
```
## 📓 Notebooks

**01_data_wrangling.ipynb**  
Cleans and restructures raw Spotify track and artist data, producing an enriched track-level dataset for analysis and modeling.

**02_exploratory_data_analysis.ipynb**  
Explores distributions, relationships, and statistical differences to understand which features are associated with hit status.

**03_modeling_and_preprocessing.ipynb**  
Performs model-specific preprocessing and trains six classification models: Dummy Classifier, Logistic Regression, Random Forest, XGBoost, MLP, and TabNet, with hyperparameter tuning, threshold tuning, and full model interpretation.

## 📁 Assets
**spotify_popularity_analysis_static.pdf**  
Visual presentation of key findings and model results

**spotify_hit_prediction_report.pdf**  
Full technical report covering data preparation, modeling, and evaluation

**xgb_v2_model_metrics.pdf**  
Detailed performance metrics for the final XGBoost model

## 📊 Data
The data used in this project was sourced from the [Spotify Dataset (1921–2021, 600k+ tracks)](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks) on Kaggle, containing both track-level and artist-level data. Raw data files are not included in this repository due to size and licensing constraints. The notebooks assume access to local copies of these datasets.

## 🧰 Tools
Python, pandas, numpy, scikit-learn, XGBoost, PyTorch, TabNet, Optuna, MLflow, SHAP, seaborn, matplotlib, scipy, joblib
