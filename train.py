# train.py — entrena y guarda el modelo dentro de src/ para que el Dockerfile lo copie
import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

X, y = load_iris(return_X_y=True)
model = LogisticRegression(max_iter=200).fit(X, y)
joblib.dump(model, "src/model.joblib")
