import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
df=pd.read_csv("student-scores.csv")
# === 1. Charger et préparer les données ===
X = df[['part_time_job', 'absence_days', 'weekly_self_study_hours',
        'math_score', 'history_score', 'physics_score',
        'chemistry_score', 'biology_score', 'english_score']]
y = df['career_aspiration']

# === 2. Encodage des labels ===
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Sauvegarder l'encodeur
joblib.dump(le, 'label_encoder.pkl')

# === 3. Équilibrage des classes ===
df_combined = pd.concat([X, pd.Series(y_encoded, name='career')], axis=1)
max_count = df_combined['career'].value_counts().max()

df_resampled = pd.DataFrame()
for label in df_combined['career'].unique():
    df_class = df_combined[df_combined['career'] == label]
    df_upsampled = resample(df_class, replace=True, n_samples=max_count, random_state=42)
    df_resampled = pd.concat([df_resampled, df_upsampled])

X_balanced = df_resampled[X.columns]
y_balanced = df_resampled['career']

# === 4. Split des données ===
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, stratify=y_balanced, random_state=42)

# === 5. Entraînement du modèle ===
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# === 6. Évaluation ===
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# === 7. Sauvegarde du modèle et des colonnes ===
joblib.dump(model, 'modele_metier.pkl')
joblib.dump(X.columns.tolist(), 'colonnes_modele.pkl')
