# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

import warnings
from copy import deepcopy
from enum import Enum

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.model_selection._validation import cross_validate, check_scoring
# from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore", category=DeprecationWarning)


class PredictionModelManager:
    def __init__(self):
        self.models = self.initialize_models()
        self.aggregate_data = {}

    def update_models(self, generation, population_sample, sample_results, features, labels_class, labels_reg):
        self.aggregate_data[generation] = {"Architectures": population_sample,
                                           "Results": sample_results}

        self.update_classification_models(features, labels_class, generation)
        self.update_regression_models(features, labels_reg, generation)

    def update_classification_models(self, features, labels, generation):
        for model in self.models["Classification"]:
            predictor = self.models["Classification"][model]["model"]
            self.models["Classification"][model]["scores"], \
            self.models["Classification"][model]["estimators"] = cross_val_score(predictor, features,
                                                                                 labels, cv=5,
                                                                                 return_estimator=True,
                                                                                 scoring='accuracy')
        self.aggregate_data[generation]["Models"] = {"Classification": deepcopy(self.models["Classification"])}

    def update_regression_models(self, features, labels, generation):
        for model in self.models["Regression"]:
            predictor = self.models["Regression"][model]["model"]
            self.models["Regression"][model]["scores"], \
            self.models["Regression"][model]["estimators"] = cross_val_score(predictor, features,
                                                                             labels, cv=5,
                                                                             return_estimator=True,
                                                                             scoring='r2')
        self.aggregate_data[generation]["Models"] = {"Regression": deepcopy(self.models["Regression"])}

    @staticmethod
    def initialize_models():
        models = {"Classification": {},
                  "Regression": {}}
        # Initialize All Classification Models
        models['Classification']["LogisticRegression"] = {"model": LogisticRegression()}
        models['Classification']["LinearDiscriminantAnalysis"] = {"model": LinearDiscriminantAnalysis()}
        models['Classification']["KNeighborsClassifier"] = {"model": KNeighborsClassifier()}
        models['Classification']["GaussianNB"] = {"model": GaussianNB()}
        models['Classification']["DecisionTreeClassifier"] = {"model": DecisionTreeClassifier()}
        models['Classification']["SVC"] = {"model": SVC()}

        # Initialize All Regression Models
        models['Regression']["LinearRegression"] = {"model": LinearRegression()}
        models['Regression']["Ridge"] = {"model": Ridge()}
        models['Regression']["Lasso"] = {"model": Lasso()}
        models['Regression']["ElasticNet"] = {"model": ElasticNet()}
        models['Regression']["MLPRegressor"] = {"model": MLPRegressor()}
        return models

    @staticmethod
    def determineResultCategory(result):
        if result > 75:
            return PerformanceCategory.GREAT.value
        if result > 50:
            return PerformanceCategory.ACCEPTABLE.value
        if result > 25:
            return PerformanceCategory.POOR.value
        if result > 0:
            return PerformanceCategory.TERRIBLE.value


class PerformanceCategory(Enum):
    GREAT = 1
    ACCEPTABLE = 2
    POOR = 3
    TERRIBLE = 4


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
