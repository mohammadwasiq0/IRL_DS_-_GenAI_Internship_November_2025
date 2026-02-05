import streamlit as st
import nltk
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="AI Sentiment Intelligence with MLflow",
    page_icon="🧠",
    layout="wide"
)

# ======================================
# MLFLOW SETUP
# ======================================
@st.cache_resource
def init_mlflow():
    # Set MLflow tracking URI (use local or cloud)
    mlflow.set_tracking_uri("http://localhost:5000")  # Change to your MLflow server
    return MlflowClient()

client = init_mlflow()

# ======================================
# NLTK (CACHED)
# ======================================
@st.cache_resource
def download_nltk():
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)

download_nltk()

# ======================================
# DATA LOADING
# ======================================
@st.cache_data
def load_data():
    df = pd.read_csv("datanew.csv")
    
    # Safe imputation
    imputer_mean = SimpleImputer(strategy="mean")
    imputer_median = SimpleImputer(strategy="median")
    imputer_mode = SimpleImputer(strategy="most_frequent")
    
    if "Up Votes" in df.columns:
        df["Up Votes"] = imputer_mean.fit_transform(df[["Up Votes"]])
    if "Down Votes" in df.columns:
        df["Down Votes"] = imputer_median.fit_transform(df[["Down Votes"]])
    if "Place of Review" in df.columns:
        df["Place of Review"] = imputer_mode.fit_transform(df[["Place of Review"]]).flatten()
    
    df.fillna("", inplace=True)
    return df

df = load_data()

# ======================================
# PREPROCESSING FUNCTIONS
# ======================================
def infer_sentiment(rating):
    if rating >= 3.5:
        return 2  # Positive
    elif rating <= 2.5:
        return 0  # Negative
    return 1  # Neutral

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words and len(w) > 2]
    return " ".join(tokens)

# Apply preprocessing and sentiment labels
df["Sentiment"] = df["Ratings"].apply(infer_sentiment)
df["Processed Review"] = df["Review text"].apply(preprocess)

# ======================================
# MLFLOW TRAINING FUNCTION
# ======================================
def train_and_log_model(experiment_name="Sentiment-Analysis-v1"):
    # Create experiment if it doesn't exist
    try:
        experiment_id = client.create_experiment(experiment_name)
    except mlflow.exceptions.MlflowException:
        experiment = client.get_experiment_by_name(experiment_name)
        experiment_id = experiment.experiment_id
    
    with mlflow.start_run(experiment_id=experiment_id, run_name=f"RF-Sentiment-{experiment_name}") as run:
        run_id = run.info.run_id
        
        # Log parameters
        params = {
            "max_features": 1200,
            "n_estimators": 300,
            "random_state": 42
        }
        mlflow.log_params(params)
        
        # Vectorization
        vectorizer = TfidfVectorizer(max_features=1200)
        X = vectorizer.fit_transform(df["Processed Review"])
        y = df["Sentiment"]
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=params["n_estimators"],
            random_state=params["random_state"],
            n_jobs=-1
        )
        model.fit(X, y)
        
        # Predictions and metrics
        preds = model.predict(X)
        f1 = f1_score(y, preds, average="weighted")
        
        # Log metrics
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("train_accuracy", model.score(X, y))
        mlflow.log_metric("dataset_size", len(df))
        mlflow.log_metric("positive_ratio", (y==2).mean())
        
        # Log model
        mlflow.sklearn.log_model(model, "random_forest_model")
        mlflow.sklearn.log_model(vectorizer, "tfidf_vectorizer")
        
        # Log artifacts
        df.to_csv("processed_dataset.csv", index=False)
        mlflow.log_artifact("processed_dataset.csv")
        
        # Tag the run
        mlflow.set_tag("model_type", "RandomForest")
        mlflow.set_tag("task", "sentiment-analysis")
        mlflow.set_tag("version", "1.0")
        
        st.success(f"✅ Model trained and logged! Run ID: {run_id}")
        st.info(f"F1 Score: {f1:.4f}")
        
        return model, vectorizer, f1, run_id

# ======================================
# HYPERPARAMETER TUNING FUNCTION
# ======================================
def hyperparameter_tuning():
    st.subheader("🔧 Hyperparameter Tuning with MLflow")
    
    # Get or create hyperparam experiment
    try:
        exp_id = client.create_experiment("Hyperparam-Tuning-v1")
    except mlflow.exceptions.MlflowException:
        exp = client.get_experiment_by_name("Hyperparam-Tuning-v1")
        exp_id = exp.experiment_id
    
    param_grid = {
        'n_estimators': [100, 300],
        'max_depth': [10, None]
    }
    
    vectorizer = TfidfVectorizer(max_features=1200)
    X = vectorizer.fit_transform(df["Processed Review"])
    y = df["Sentiment"]
    
    progress_bar = st.progress(0)
    total_runs = len(param_grid['n_estimators']) * len(param_grid['max_depth'])
    run_count = 0
    
    for n_est in param_grid['n_estimators']:
        for depth in param_grid['max_depth']:
            with mlflow.start_run(experiment_id=exp_id, run_name=f"RF-n{n_est}-d{depth}", nested=True):
                model = RandomForestClassifier(
                    n_estimators=n_est,
                    max_depth=depth,
                    random_state=42,
                    n_jobs=-1
                )
                model.fit(X, y)
                
                preds = model.predict(X)
                f1 = f1_score(y, preds, average="weighted")
                
                mlflow.log_params({
                    "n_estimators": n_est,
                    "max_depth": depth
                })
                mlflow.log_metric("f1_score", f1)
                
                mlflow.sklearn.log_model(model, f"model_n{n_est}_d{depth}")
                
                run_count += 1
                progress_bar.progress(run_count / total_runs)
                st.write(f"✅ n_estimators={n_est}, max_depth={depth} → F1: {f1:.4f}")

# ======================================
# MODEL REGISTRY FUNCTIONS
# ======================================
def register_best_model():
    st.subheader("🏷️ Model Registry")
    
    experiment = client.get_experiment_by_name("Sentiment-Analysis-v1")
    if not experiment:
        st.error("No Sentiment-Analysis-v1 experiment found. Train a model first!")
        return
    
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.f1_score DESC"], max_results=1)
    if runs:
        best_run = runs[0]
        model_uri = f"runs:/{best_run.info.run_id}/random_forest_model"
        
        model_name = "SentimentRFModel"
        
        try:
            # Register model
            model_version = mlflow.register_model(model_uri, model_name)
            
            # Tag the model version
            client.set_model_version_tag(
                name=model_name,
                version=model_version.version,
                key="production_ready",
                value="true"
            )
            client.set_model_version_tag(
                name=model_name,
                version=model_version.version,
                key="sentiment_type",
                value="3-class"
            )
            client.set_model_version_tag(
                name=model_name,
                version=model_version.version,
                key="f1_score",
                value=str(best_run.data.metrics["f1_score"])
            )
            
            st.success(f"✅ Model registered: {model_name} v{model_version.version}")
            st.json({
                "run_id": best_run.info.run_id,
                "f1_score": best_run.data.metrics["f1_score"],
                "version": model_version.version,
                "model_uri": model_version.model_uri
            })
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")

def list_mlflow_experiments():
    """Fixed function to list experiments"""
    try:
        experiments = []
        for exp in client.search_experiments():
            experiments.append({
                "name": exp.name,
                "id": exp.experiment_id,
                "artifact_location": exp.artifact_location,
                "lifecycle_stage": exp.lifecycle_stage
            })
        return experiments
    except:
        return []

# ======================================
# HEADER
# ======================================
st.markdown("""
# 🧠 AI Sentiment Intelligence with MLflow
### Enterprise ML Pipeline • Tracking • Registry • Hyperparams
**Streamlit 1.38+ Compatible**
""")
st.markdown("---")

# ======================================
# SIDEBAR - MLflow Controls
# ======================================
with st.sidebar:
    st.header("⚙️ MLflow Controls")
    
    if st.button("🚀 Train & Log Model", type="primary"):
        with st.spinner("Training model and logging to MLflow..."):
            model, vectorizer, f1, run_id = train_and_log_model()
            st.session_state.model = model
            st.session_state.vectorizer = vectorizer
            st.session_state.f1 = f1
            st.session_state.run_id = run_id
            st.rerun()
    
    st.button("🔧 Run Hyperparameter Tuning")
    
    st.button("🏷️ Register Best Model")
    
    st.markdown("---")
    if st.button("📊 Open MLflow UI"):
        st.info("Open http://localhost:5000")
    
    st.markdown("---")
    st.caption("**MLflow Server:**\n`mlflow ui`")

# ======================================
# TABS
# ======================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Prediction", "📊 Insights", "🗃 Dataset", "📈 MLflow"
])

# ======================================
# TAB 1 — PREDICTION ENGINE
# ======================================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'model' not in st.session_state:
            st.warning("👈 Use sidebar to train model first!")
        else:
            review = st.text_area("Enter Review", height=160)
            
            if st.button("🚀 Analyze", type="primary") and review.strip():
                cleaned = preprocess(review)
                vect = st.session_state.vectorizer.transform([cleaned])
                
                pred = st.session_state.model.predict(vect)[0]
                probs = st.session_state.model.predict_proba(vect)[0]
                
                label_map = {2: "Positive 😊", 1: "Neutral 😐", 0: "Negative ☹️"}
                st.success(f"### **{label_map[pred]}**")
                
                st.metric("Confidence", f"{np.max(probs):.1%}")
                
                st.json({
                    "Negative": f"{probs[0]:.1%}",
                    "Neutral": f"{probs[1]:.1%}", 
                    "Positive": f"{probs[2]:.1%}"
                })
    
    with col2:
        if 'f1' in st.session_state:
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("F1 Score", f"{st.session_state.f1:.4f}")
            with col_b: st.metric("Reviews", len(df))
            with col_c: st.metric("Vocab", len(st.session_state.vectorizer.vocabulary_))

# ======================================
# TAB 2 — MODEL INSIGHTS
# ======================================
with tab2:
    if 'model' in st.session_state:
        importances = st.session_state.model.feature_importances_
        indices = np.argsort(importances)[-20:]
        features = np.array(st.session_state.vectorizer.get_feature_names_out())[indices]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(len(features)), importances[indices])
        ax.set_yticks(range(len(features)))
        ax.set_yticklabels(features)
        ax.set_xlabel("Importance")
        st.pyplot(fig)
    
    st.bar_chart(df["Sentiment"].value_counts().sort_index())

# ======================================
# TAB 3 — DATASET
# ======================================
with tab3:
    st.dataframe(df.head(100), use_container_width=True)

# ======================================
# TAB 4 — MLFLOW EXPERIMENTS
# ======================================
with tab4:
    experiments = list_mlflow_experiments()
    
    if experiments:
        for exp in experiments[:5]:  # Show top 5
            with st.expander(f"📁 {exp['name']}"):
                runs = client.search_runs(exp['id'], max_results=5)
                if runs:
                    run_data = []
                    for run in runs:
                        run_data.append({
                            "Run": run.info.run_id[:8],
                            "F1": f"{run.data.metrics.get('f1_score', 0):.4f}",
                            "Params": f"n_est={run.data.params.get('n_estimators', 'N/A')}",
                            "Status": run.info.status
                        })
                    st.dataframe(pd.DataFrame(run_data), hide_index=True)
    else:
        st.info("🚀 No experiments yet. Train a model!")

# ======================================
# FOOTER
# ======================================
with st.expander("📋 Setup Commands"):
    st.code("""
pip install -U streamlit mlflow scikit-learn nltk pandas numpy matplotlib

# Terminal 1
mlflow ui --host 0.0.0.0 --port 5000

# Terminal 2  
streamlit run app.py
    """)