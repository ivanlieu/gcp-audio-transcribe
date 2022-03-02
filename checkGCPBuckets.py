'''Accesses the google cloud storage api to return bucket name and blob names within the bucket'''

import os
from google.cloud import storage

def checkBuckets(correctBucketName, credentialPath):
    '''lists all buckets in storage and checks if provided bucket name exists.
    Accepts correctBucketName as a string for the bucket to check;
            credentialPath as a string for the file pathway of the json file to access GCP.
    Returns myBucket as a boolean. If it exists value is True, otherwise value is False.'''

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialPath

    try:
        storageClient = storage.Client()
        buckets = storageClient.list_buckets()
    
        for bucket in buckets:
            #print(bucket.name)
            myBucket = False
            
            if bucket.name == correctBucketName:
                myBucket = True
                
                break
    except:
        myBucket = False

    return myBucket
    
def listBlobs(bucketName, credentialPath):
    '''lists all blobs in bucket
    Accepts bucketName as a string for the bucket to list objects;
            credentialPath as a string for the file pathway of the json file to access GCP.
    Returns myBlobs as a list of objects currently in the bucket.'''

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialPath

    storageClient = storage.Client()
    blobs = storageClient.list_blobs(bucketName)
    myBlobs = []
    

    for blob in blobs:
        #print(blob.name)

        myBlobs.append(blob.name)

    return myBlobs

