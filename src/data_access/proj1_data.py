import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import MyException

class Proj1Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self, database_name:str,) -> None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=database_name)
            self.database_name = database_name
        except Exception as e:
            raise MyException(e, sys)

    def Import_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Import an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            # Convert collection data to DataFrame and preprocess
            print("Fetching data from mongoDB")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fecthed with len: {len(df)}")
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df

        except Exception as e:
            raise MyException(e, sys)
        
    
    def Export_collection_as_dataframe(self, data:pd.DataFrame, collection_name:str,):
    
        """
        data : pandas dataframe to be pused as list of dictionary
        collection_name : Name of the collection where data will(collectino) be pushed.
        database_name : Name of the Database where data(collection) will be pushed.

        # This Function exports the data(collection) to mongodb atlas 

        """
                
        data = data.to_dict(orient="records")
        try:
            collection = self.mongo_client.client[self.database_name][collection_name]
            collection.insert_many(data)
            print(f"Collection Pushed to MongoDb atlas cluster with db name {self.database_name} and collection name {collection_name}")
        except Exception as e:
            raise MyException(e, sys)
        
