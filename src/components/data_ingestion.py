import os
import sys
from pandas import DataFrame, read_csv
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import MyException
from src.logger import logging
from src.RemoteLikeStorage import RemoteStorage 
from src.data_access.proj1_data import Proj1Data

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data(self,)->DataFrame:
        """
        This function is  the placeholder function for exporting data from local storage RemoteLike/monogolike/
        """
        logging.info("data Collection started from RemoteLike Storage")
        
        storage = RemoteStorage(self.data_ingestion_config.Remote_Dir_path_Ingestion)
        
        df = storage.Retrieve_Data(self.data_ingestion_config.Remote_DB_Name)
        
        logging.info("Data Retrival Finished from RemoteLike Storage")
        
        return df
    
    def Export_Data(self,)-> DataFrame:
        """
        Takes help of Proj1Data class and returns data from mongodb atlas
        
        #also a Minimal example of Recursion Functions
        """

        storage = Proj1Data(self.data_ingestion_config.database_name)
        
        df = storage.Import_collection_as_dataframe(self.data_ingestion_config.collection_name, self.data_ingestion_config.database_name)
        
        if len(df) == 0:
            r = input("No data Found do you want to Repush the data to mongodb atlas (works only if you have mongodb_cluster configured ) (y/n): ")
            if r == 'y':
                data = read_csv(self.data_ingestion_config.Re_Push_data)
                storage.Export_collection_as_dataframe(data, self.data_ingestion_config.collection_name)
                return self.Export_Data() # Recursive entity
            else:
                raise MyException("No Collection found", sys)
                return None
            pass
        
        #df without _id column
        df.drop(df.columns[0], axis=1, inplace=True)
        return df



    def split_data_as_train_test(self,dataframe: DataFrame) ->None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:

            #Local storage
            dataframe = self.export_data() # to export data from RemoteLike local storage

            #MongoDb Atlas Storage.
            # dataframe = self.Export_Data()

            logging.info("Got the data from Remote Storage (MongoDB or MongoLike)")

            self.split_data_as_train_test(dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        