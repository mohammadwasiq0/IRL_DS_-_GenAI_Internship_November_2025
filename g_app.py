import streamlit as st
import nltk
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="AI Sentiment + MLflow",
    page_icon="🧠",
    layout="wide"
)

# ======================================
# SETUP MLFLOW EXPERIMENT
# ======================================
# 
mlflow.set_experiment("Internship_Sentiment_Analysis")

# ======================================
# NLTK & PREPROCESSING
# ======================================
@st.cache_resource
def download_nltk():
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")

download_nltk()

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    if not isinstance(text, str): return ""
    text = re.sub(r"[^\w\s]", "", text.lower())
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)

# ======================================
# DATA LOADER (CACHED)
# ======================================
@st.cache_resource
def load_data():
    # Ensure you have your datanew.csv in the folder
    if not os.path.exists("datanew.csv"):
        st.error("dataset not found! Please upload 'datanew.csv'")
        return pd.DataFrame(), None, None
        
    df = pd.read_csv("datanew.csv")

    # ---- SAFE IMPUTATION ----
    if "Up Votes" in df:
        df["Up Votes"] = SimpleImputer(strategy="mean").fit_transform(df[["Up Votes"]])
    if "Down Votes" in df:
        df["Down Votes"] = SimpleImputer(strategy="median").fit_transform(df[["Down Votes"]])
    if "Place of Review" in df:
        df["Place of Review"] = SimpleImputer(strategy="most_frequent") \
                                     .fit_transform(df[["Place of Review"]]).flatten()
    
    df.fillna("", inplace=True)

    # ---- SENTIMENT LABEL ----
    def infer_sentiment(r):
        if r >= 3.5: return 2
        elif r <= 2.5: return 0
        return 1

    df["Sentiment"] = df["Ratings"].apply(infer_sentiment)
    df["Processed Review"] = df["Review text"].apply(preprocess)
    
    return df

# Initialize Data
df = load_data()

# ======================================
# HEADER
# ======================================
st.markdown("""
# 🧠 AI Sentiment Intelligence + MLflow MLOps
### Enterprise-Grade NLP Dashboard with Experiment Tracking
""")
st.markdown("---")

# ======================================
# TABS
# ======================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Prediction Engine", 
    "📊 Model Insights", 
    "🗃 Dataset Explorer",
    "⚙️ MLOps Training"
])

# GLOBAL VARIABLES (To hold model in memory for Tab 1 after training in Tab 4)
if 'model' not in st.session_state:
    st.session_state['model'] = None
if 'vectorizer' not in st.session_state:
    st.session_state['vectorizer'] = None

# ======================================
# TAB 4 — MLOPS (THE NEW INTERNSHIP PART)
# ======================================
with tab4:
    st.header("🧪 MLflow Experimentation Lab")
    st.markdown("Train models, log metrics, and visualize hyperparameters.")

    col_train, col_logs = st.columns([1, 2])
    
    with col_train:
        st.subheader("Hyperparameter Tuning")
        n_estimators_input = st.slider("Number of Trees (n_estimators)", 50, 500, 100, step=50)
        max_depth_input = st.select_slider("Max Depth", options=[None, 10, 20, 50])
        run_name_input = st.text_input("Run Name", value="Experimental_Run_v1")
        
        start_train = st.button("🚀 Train & Log to MLflow", type="primary")

    if start_train:
        with st.spinner("Training Model & Logging to MLflow..."):
            
            # 1. Prepare Data
            vectorizer = TfidfVectorizer(max_features=1200)
            X = vectorizer.fit_transform(df["Processed Review"])
            y = df["Sentiment"]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # 2. START MLFLOW RUN
            with mlflow.start_run(run_name=run_name_input) as run:
                
                # --- A. LOG PARAMETERS ---
                mlflow.log_param("n_estimators", n_estimators_input)
                mlflow.log_param("max_depth", str(max_depth_input))
                mlflow.log_param("vectorizer_max_features", 1200)

                # --- B. TRAIN MODEL ---
                model = RandomForestClassifier(
                    n_estimators=n_estimators_input,
                    max_depth=max_depth_input,
                    random_state=42
                )
                model.fit(X_train, y_train)
                
                # --- C. CALCULATE METRICS ---
                preds = model.predict(X_test)
                f1 = f1_score(y_test, preds, average="weighted")
                accuracy = model.score(X_test, y_test)

                # --- D. LOG METRICS ---
                mlflow.log_metric("f1_score", f1)
                mlflow.log_metric("accuracy", accuracy)

                # --- E. LOG ARTIFACTS (PLOTS) ---
                # 1. Feature Importance Plot
                importances = model.feature_importances_
                indices = np.argsort(importances)[-10:]
                features = np.array(vectorizer.get_feature_names_out())[indices]
                
                fig, ax = plt.subplots()
                ax.barh(features, importances[indices])
                ax.set_title("Top Words")
                plt.savefig("feature_importance.png") # Save locally first
                mlflow.log_artifact("feature_importance.png") # Log to MLflow
                
                # 2. Confusion Matrix
                fig_cm, ax_cm = plt.subplots()
                ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, ax=ax_cm, cmap='Blues')
                plt.savefig("confusion_matrix.png")
                mlflow.log_artifact("confusion_matrix.png")

                # --- F. REGISTER MODEL & TAGGING ---
                # Log the actual model object
                mlflow.sklearn.log_model(
                    sk_model=model, 
                    artifact_path="random_forest_model",
                    registered_model_name="Sentiment_RF_Prod" # Registers model in registry
                )
                
                # Set custom tags
                mlflow.set_tag("Developer", "Intern_Name")
                mlflow.set_tag("Stage", "Staging")

                # Save to Session State for Tab 1 usage
                st.session_state['model'] = model
                st.session_state['vectorizer'] = vectorizer

            st.success(f"✅ Run Completed! F1 Score: {round(f1, 4)}")
            st.info(f"Run ID: {run.info.run_id}")
            
            # Clean up local images
            os.remove("feature_importance.png")
            os.remove("confusion_matrix.png")

    with col_logs:
        st.info("💡 To view the MLflow UI, open your terminal and run:")
        st.code("mlflow ui", language="bash")
        st.markdown("**Check 'http://localhost:5000' in your browser.**")

# ======================================
# TAB 1 — PREDICTION (USES SESSION STATE MODEL)
# ======================================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        review = st.text_area("Enter Customer Review", height=150)
        
        if st.button("Analyze"):
            if st.session_state['model'] is None:
                st.warning("⚠️ Please train the model in the 'MLOps Training' tab first!")
            else:
                processed_text = preprocess(review)
                vec_text = st.session_state['vectorizer'].transform([processed_text])
                pred = st.session_state['model'].predict(vec_text)[0]
                
                label_map = {2: "Positive 😊", 1: "Neutral 😐", 0: "Negative ☹️"}
                st.success(f"Prediction: **{label_map[pred]}**")

# ======================================
# TAB 2 & 3 (Simplified for brevity)
# ======================================
with tab2:
    st.write("Train a model in Tab 4 to see insights in MLflow UI!")
with tab3:
    st.dataframe(df.head(50))