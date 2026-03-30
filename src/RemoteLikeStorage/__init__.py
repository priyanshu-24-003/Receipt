from pandas import DataFrame, read_csv
import os

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
            try:
                

    


    
    