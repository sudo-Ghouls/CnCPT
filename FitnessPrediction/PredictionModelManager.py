# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

from enum import Enum

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class PredictionModelManager:
    def __init__(self):
        self.models = self.initialize_models()

    def update_models(self, features, labels_class, labels_reg):
        self.update_classification_models(features, labels_class)
        self.update_regression_models(features, labels_reg)

    def update_classification_models(self, features, labels):
        for model in self.models["Classification"]:
            predictor = self.models["Classification"][model]["model"]
            self.models["Classification"][model]["scores"] = cross_val_score(predictor, features,
                                                                             labels, cv=5,
                                                                             scoring='accuracy')

    def update_regression_models(self, features, labels):
        for model in self.models["Regression"]:
            predictor = self.models["Regression"][model]["model"]
            self.models["Regression"][model]["scores"] = cross_val_score(predictor, features,
                                                                         labels, cv=5,
                                                                         scoring='neg_root_mean_squared_error')

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
            return PerformanceCategory.GREAT
        if result > 50:
            return PerformanceCategory.ACCEPTABLE
        if result > 25:
            return PerformanceCategory.POOR
        if result > 0:
            return PerformanceCategory.TERRIBLE


class PerformanceCategory(Enum):
    GREAT = 1
    ACCEPTABLE = 2
    POOR = 3
    TERRIBLE = 4
