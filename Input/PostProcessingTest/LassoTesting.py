import pickle

from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.model_selection._validation import cross_validate, check_scoring
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import cross_val_score

gen1 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_1_Results.pkl",
    "rb"))
gen2 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_2_Results.pkl",
    "rb"))
gen3 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_3_Results.pkl",
    "rb"))
gen4 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_4_Results.pkl",
    "rb"))
gen5 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_5_Results.pkl",
    "rb"))
gen6 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_6_Results.pkl",
    "rb"))
gen7 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_7_Results.pkl",
    "rb"))
gen8 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_8_Results.pkl",
    "rb"))
gen9 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_9_Results.pkl",
    "rb"))
gen10 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_10_Results.pkl",
    "rb"))
gen11 = pickle.load(open(
    r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\2021-06-24-135821\Generation_11_Results.pkl",
    "rb"))


def cross_val_score(estimator, X, y=None, groups=None, scoring=None, cv=5,
                    n_jobs=None, verbose=0, fit_params=None,
                    pre_dispatch='2*n_jobs', error_score='raise-deprecating',
                    return_estimator=True):
    scorer = check_scoring(estimator, scoring=scoring)
    try:
        cv_results = cross_validate(estimator=estimator, X=X, y=y, groups=groups,
                                    scoring={'score': scorer}, cv=cv,
                                    n_jobs=n_jobs, verbose=verbose,
                                    fit_params=fit_params,
                                    pre_dispatch=pre_dispatch,
                                    error_score=error_score,
                                    return_estimator=return_estimator,
                                    return_train_score=True)
        return cv_results['test_score'], cv_results['estimator']
    except ValueError:
        return None, None

predictor = Lasso()

X_train, X_test, y_train, y_test = train_test_split(gen11["model_features"], gen11["labels_reg"],
                                                    test_size=0.3,
                                                    random_state=0)
scaler = StandardScaler()
scaler.fit(X_train)
sel_ = SelectFromModel(Lasso())
sel_.fit(X_train, y_train)
sel_.get_support()
selected_feat = X_train[:,(sel_.get_support())]
print('total features: {}'.format((X_train.shape[1])))
print('selected features: {}'.format(len(selected_feat)))
print('features with coefficients shrank to zero: {}'.format(
      np.sum(sel_.estimator_.coef_ == 0)))
np.sum(sel_.estimator_.coef_ == 0)