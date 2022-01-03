import logging
import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
import os
import datetime

class syncnow:

    def __init__(self, cloud_1_provider,cloud_1_bucket,cloud_1_secrets_file,
                cloud_2_provider,cloud_2_bucket ):
        
        self.providera = cloud_1_provider
        self.providerb = cloud_2_provider

        self.bucketa = cloud_1_bucket
        self.bucketb = cloud_2_bucket

        self.secrets_file_a = cloud_1_secrets_file
        

        self.storage_client = storage.Client.from_service_account_json(
            self.secrets_file_a)
        self.bucket = self.storage_client.bucket(self.bucketa)
        self.s3 = boto3.client('s3')

    def download_file(self,file,provider):
        message = 'downloading {} from {}'.format(file,provider)
        path, filename = os.path.split(file)
        if provider == 'GC':
            print(message)
            
            blob = self.bucket.blob(file)
            blob.download_to_filename(filename)

        elif provider == 'S3':
            print(message)
            
            self.s3.download_file(self.bucketb, file, filename)


    def upload_file(self,file,provider):
        message = 'uploading {} from {}'.format(file,provider)
        path, filename = os.path.split(file)
        if provider == 'GC':
            print(message)
            blob = self.bucketa.blob(file)
            blob.upload_from_filename(filename)
        elif provider == 'S3':
            print(message)
            self.s3.upload_file(filename,self.bucketb,file)

    def tidy_temp_file(self,file):
        message = 'removing temp file {}'.format(file)
        path, filename = os.path.split(file)
        os.remove(filename)
        print(message)
        
    def get_files_list(self,provider):
        #establish the provider and build the connection
        filelist = []
        if provider == 'GC':
            print('Google Cloud')
            blobs = self.storage_client.list_blobs(self.bucketa)
            for blob in blobs:
                filelist.append(blob.name)
                


        elif provider == 'S3':
            print('S3')
            s3  = boto3.client('s3')
            
            for key in s3.list_objects(Bucket=self.bucketb)['Contents']:
                
                filelist.append(key['Key'])
        return filelist

    def compare_files_lists(self,list1,list2):
        print('comparing file lists')
        set_difference = set(list1).symmetric_difference(set(list2))
        list_difference = list(set_difference)

        return list_difference

    def sync_files(self,providera,providerb,list_difference,list1,list2):
        changes = []
        for file in list_difference:
            if file in list1:
                message = 'copy {} to {}'.format(file,providerb)
                self.download_file(file,providera)
                self.upload_file(file,providerb)
                self.tidy_temp_file(file)
                pass
            elif file in list2:
                message = 'copy {} to {}'.format(file,providera)
                print(message)
                self.download_file(file,providerb)
                self.upload_file(file,providera)
                self.tidy_temp_file(file)
            else:
                message = 'file {} does not exist anywhere'.format(file)
                print(message)
                pass



    

        return changes

