import sys
from src.entity.config_entity import VehiclePredictorConfig
# from src.entity.s3_estimator import Proj1Estimator

from src.utils.main_utils import load_object
from src.RemoteLikeStorage import Proj1EstimatorLike

from src.exception import MyException
from src.logger import logging
from pandas import DataFrame


class VehicleData:
    def __init__(self,
                gender,
                age,
                bmi,
                smoker,
                children,
                region,                
                ):
        """
        Vehicle Data constructor
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

    def get_vehicle_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            return self.df_recieved
        
        except Exception as e:
            raise MyException(e, sys) from e


class VehicleDataClassifier:
    def __init__(self, Dataframe:DataFrame, prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
            self.dataframe = Dataframe
        except Exception as e:
            raise MyException(e, sys)

    def predict(self,) -> str:
        """
        This is the method of VehicleDataClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of VehicleDataClassifier class")
            # model = Proj1EstimatorLike(remote_model_path=self.prediction_pipeline_config.Remote_Like_Model_Path)
            # result =  model.predict(dataframe)

            #loading the processor
            model = load_object(file_path=self.prediction_pipeline_config.Remote_Like_Model_Path)
            result = model.predict(self.dataframe,)#  'here is my df recieved from GUI/user'
            
            return result
        
        except Exception as e:
            raise MyException(e, sys)