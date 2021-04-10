import json
import numpy as np
import pandas as pd
from sklearn import model_selection
from xgboost import XGBClassifier

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def lambda_handler(event, context):
    model = train_xgb_classifier()
    prediction = model.predict(np.array([[7.2, 3.2, 6.0, 1.8]]).reshape((1,-1)))
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Predicting Iris class for [6.4,2.9,4.3,1.3]: {}".format(prediction)
        })
    }

def train_xgb_classifier():
  url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
  names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
  dataset = pd.read_csv(url, names=names)

  # Split-out validation dataset
  array = dataset.values
  X = array[:,0:4]
  Y = array[:,4]
  validation_size = 0.20
  X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=7)

  m = XGBClassifier(max_depth=5, n_estimators=100, verbosity=0)
  m.fit(X_train, Y_train)

  return m