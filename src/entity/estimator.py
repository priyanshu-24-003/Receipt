import sys

import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.yes:int = 0
        self.no:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))

class MyModel:

    """
    
    This Class packages the Pipeline Transformer object and Trained model into on MyModel Object
    If there comes a new test_data MyModel can be used to both Transform the data and predict.

    """
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> DataFrame:
        """
        Function accepts preprocessed inputs (with all custom transformations already applied),
        applies scaling using preprocessing_object, and performs prediction on transformed features.
        """
        try:

            #step 1: feature Transformation using saved processor/transformer pipeline
            #after transformed converted the data into dataframe with columns name = model's columns name (it was trained so)

            X = pd.DataFrame(self.preprocessing_object.transform(dataframe),columns=self.trained_model_object.feature_names_in_)
            logging.info("Starting prediction process.")

            # Step 2: Perform prediction using the trained model
            logging.info("Using the trained model to get predictions")
            predictions = self.trained_model_object.predict(X)
            
            return predictions

        except Exception as e:
            logging.error("Error occurred in predict method", exc_info=True)
            raise MyException(e, sys) from e


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"