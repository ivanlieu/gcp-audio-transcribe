import os
from google.cloud import storage
from checkGCPBuckets import checkBuckets, listBlobs
from selectFiles import userSelectedFiles, getFileName, getFilePath
from checkDuplicatesGCPnLocal import checkDuplicates

def uploadBlobs(bucketName, sourceFileName, destinationBlobName, credentialPath):
	'''uploads files to the bucket using file pathway.
	Accepts bucketName as a string for the bucket to upload files to; 
			sourceFileName for the string/list of file path(s) to upload; 
			destinationBlobName as a string/list for the GCP storage name of the uploaded file in the bucket;
			credentialPath as a string for the file pathway of the json file to access GCP.'''

	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialPath

	storageClient = storage.Client()
	bucket = storageClient.bucket(bucketName)
	
	uploadedFiles = []
	count = 0

	if type(sourceFileName) is list:
		for files in sourceFileName:
			blob = bucket.blob(destinationBlobName[count])
			blob.upload_from_filename(files)
			uploadedFiles.append(files)
			print (f"File at '{files}' uploaded as '{destinationBlobName[count]}' to '{bucketName}' bucket.")

			count += 1
	elif type(sourceFileName) is str:
		blob = bucket.blob(destinationBlobName[count])
		blob.upload_from_filename(sourceFileName)
		uploadedFiles = sourceFileName
		print (f"File at '{sourceFileName}' uploaded as '{destinationBlobName}' to '{bucketName}' bucket.")
			
def verifyUploadedBlobs(bucketName, blobsToCheck, credentialPath):
	'''checks to see if storage objects are in the gcp storage bucket.
	Accepts bucketName as a string for the bucket to check objects in;
			blobsToCheck for the string/list of object(s) to be verified;
			credentialPath as a string for the file pathway of the json file to access GCP.
	Returns verifiedBlob as a string/list of object(s) from blobsToCheck present in the bucket;
			unverifiedBlob as a string/list of object(s) from blobsToCheck not present in the bucket;
			verifiedBlobStatus as a boolean thats True if all objects are true and false otherwise.'''

	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialPath

	storageClient = storage.Client()
	blobs = storageClient.list_blobs(bucketName)

	verifiedBlob = []
	unverifiedBlob = blobsToCheck

	if type(blobsToCheck) is list:
		for blob in blobs:
			for checkingBlobs in blobsToCheck:
				if blob.name == checkingBlobs:
					verifiedBlob.append(blob.name)
					unverifiedBlob.remove(blob.name)
	elif type(blobsToCheck) is str:
		for blob in blobs:
			if blob.name == checkingBlobs:
				verifiedBlob.append(blob.name)
				unverifiedBlob = []

	if unverifiedBlob == []:
		verifiedBlobStatus = True
	else:
		verifiedBlobStatus = False

	return verifiedBlob, unverifiedBlob, verifiedBlobStatus

def attemptReupload(correctBucketName, credentialPath, successfulUploads, unsuccessfulUploads):
	'''posts status of initial upload and attempts a re-upload of unsuccessful upload files.
	Accepts correctBucketName as a string for the bucket to upload files to;
			credentialPath as a string for the file pathway of the json file to access GCP;
			sucessfulUploads as the string/list of files successfully uploaded previously;
			unsuccessulUploads as the string/list of files unsuccessfully uploaded previously.'''

	print(f"The following files were uploaded successfully: {successfulUploads}")
	print(f"The following files were uploaded unsuccessfully: {unsuccessfulUploads}")
	print("Attempting to re-upload unsuccesful uploads.")

	unsuccessfulUploadsFilePaths = getFilePath(unsuccessfulUploads, newFilesToUpload)
	uploadBlobs(correctBucketName, unsuccessfulUploadsFilePaths, unsuccessfulUploads, credentialPath)
	successfulUploads2, unsuccessfulUploads2, uploadStatus2 = verifyUploadedBlobs(correctBucketName, unsuccessfulUploads, credentialPath)

	if uploadStatus2 == False:
		print(f"The following files were re-uploaded successfully: {successfulUploads2}")
		print(f"The following files were unable to be uploaded: {unsuccessfulUploads2}")
	else:
		print("All files successfully uploaded.")
