from io import StringIO
from typing import Union,List
import os,sys
from src.logger import logging
from src.exception import MyException
from pandas import DataFrame,read_csv
import pickle



from botocore.exceptions import ClientError
import boto3
from src.configuration.aws_connection import S3Client
from mypy_boto3_s3.service_resource import Bucket
from src.entity.estimator import MyModel


class SimpleStorageService(MyModel):
    """
    A class for interacting with AWS S3 storage, providing methods for file management, 
    data uploads, and data retrieval in S3 buckets.

    Inherits MyModel to enable prediction.
    """

    def __init__(self, bucket_name, model_path):
        """
        Initializes the SimpleStorageService instance with S3 resource and client
        from the S3Client class.
        """
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

        self.bucket_name = bucket_name
        self.model_path = model_path

    def is_model_present(self,) -> bool:
        """
        Checks if a specified S3 key path (file path) is available in the specified bucket.

        """
        try:
            bucket = self.get_bucket(self.bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=self.model_path)]
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Reads the specified S3 object with optional decoding and formatting.
        """

        # logging.info("Entered the read_object method of SimpleStorageService class")
        try:
            # Read and decode the object content if decode=True
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode else object_name.get()["Body"].read()
            )
            # Convert to StringIO if make_readable=True
            conv_func = lambda: StringIO(func()) if make_readable else func()
            # logging.info("Exited the read_object method of SimpleStorageService class")
            return conv_func()
        except Exception as e:
            raise MyException(e, sys) from e

    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        Retrieves the S3 bucket object based on the provided bucket name.
        """

        logging.info("Entered the get_bucket method of SimpleStorageService class")
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of SimpleStorageService class")
            return bucket
        except Exception as e:
            raise MyException(e, sys) from e

    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        """
        Retrieves the file object(s) from the specified bucket based on the filename.
        """

        logging.info("Entered the get_file_object method of SimpleStorageService class")
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(file_objects)
            logging.info("Exited the get_file_object method of SimpleStorageService class")
            return file_objs
        except Exception as e:
            raise MyException(e, sys) from e

    def load_model(self, model_dir: str = None) -> object:
        """
        Loads a serialized model from the specified S3 bucket.
        """

        try:
            model_file = model_dir + "/" + self.model_path if model_dir else self.model_path
            file_object = self.get_file_object(model_file, self.bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = pickle.loads(model_obj)


            logging.info("Expossing the Preprocessor that was used to train the model and the model itself.")
            self.preprocessing_object = model.preprocessing_object
            self.trained_model_object = model.trained_model_object

            logging.info("Production model loaded from S3 bucket.")
            return model
        except Exception as e:
            raise MyException(e, sys) from e


    def save_model(self, from_filename: str, remove: bool = True):
        """
        Uploads a local file to the specified S3 bucket with an optional file deletion.
        """
        
        logging.info("Entered the upload_file method of SimpleStorageService class")
        try:
            logging.info(f"Uploading {from_filename} to {self.model_path} in {self.bucket_name}")
            self.s3_resource.meta.client.upload_file(from_filename, self.bucket_name, self.model_path)
            logging.info(f"Uploaded {from_filename} to {self.model_path} in {self.bucket_name}")

            # Delete the local file if remove is True
            if remove:
                os.remove(from_filename)
                logging.info(f"Removed local file {from_filename} after upload")
            logging.info("Exited the upload_file method of SimpleStorageService class")
        except Exception as e:
            raise MyException(e, sys) from e

