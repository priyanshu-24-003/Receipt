from pandas import DataFrame, read_csv
import os,sys
from src.exception import MyException
from src.utils.main_utils import load_object, save_object


class RemoteStorage():
    """
    A Class to Retrieve data From RemoteLike LocalStorage
    """

    def __init__(self, path:str):
        self.path = path
    
    def Retrieve_Data(self, filename:DataFrame)-> DataFrame :
        
        try:
            data_path = os.path.join(self.path, filename)
            
            data_frame = read_csv(data_path)

            return data_frame
        except Exception as e:
            raise MyException(e, sys) from e


class Proj1EstimatorLike():

    """
    A class to save & retrieve model from awslike storage
    """

    def __init__(self, remote_model_path):
        self.remote_model_path = remote_model_path
        self.model = None

    def does_model_exist(self,)-> bool:

        try:
            with open(self.remote_model_path, 'rb') as f:
                pass 
            return True
        except Exception as e:
            return False
    
    def Retreive_model(self,):
        
        return load_object(self.remote_model_path) if self.does_model_exist() else None

    def Push_model(self, obj):
        
        save_object(file_path=self.remote_model_path, obj=obj)

    
    