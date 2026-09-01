import sys
from src.entity.config_entity import PremiumPredictorConfig
# from src.entity.s3_estimator import Proj1Estimator
from src.cloud_storage.aws_storage import SimpleStorageService

from src.utils.main_utils import load_object
from src.RemoteLikeStorage import Proj1EstimatorLike

from src.exception import MyException
from src.logger import logging
from pandas import DataFrame


class InsuranceDataRegressor:
    def __init__(self,
                gender,
                age,
                bmi,
                smoker,
                children,
                region,                
                prediction_pipeline_config: PremiumPredictorConfig = PremiumPredictorConfig(),
                ):
        """
        Insurance Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.sex = gender
            self.age = age
            self.region = region
            self.bmi = bmi
            self.smoker = smoker
            self.children = children

            self.df_recieved = DataFrame({"sex":[self.sex]*2, "age":[self.age]*2, "region":[self.region,]*2, "smoker":[self.smoker,]*2, "bmi":[self.bmi,]*2, "children":[self.children,]*2})

        except Exception as e:
            raise MyException(e, sys) from e

        self.prediction_pipeline_config = prediction_pipeline_config

    def get_insurance_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from InsuranceData class input
        """
        try:
            return self.df_recieved
        
        except Exception as e:
            raise MyException(e, sys) from e

    def predict(self,) -> str:
        
        
        try:

            #Production setup
            # logging.info("Entered predict method of InsuranceDataRegressor class")
            model_class = SimpleStorageService(self.prediction_pipeline_config.model_bucket_name, self.prediction_pipeline_config.model_file_path)
            model = model_class.load_model()
            result =  model.predict(self.get_insurance_input_data_frame(),)


            # local setup
            # logging.info("Entered predict method of InsuranceDataRegressor class")
            # model = load_object(file_path=self.prediction_pipeline_config.Remote_Like_Model_Path)
            # result = model.predict(self.df_recieved,)


            return result
        
        except Exception as e:
            raise MyException(e, sys)

