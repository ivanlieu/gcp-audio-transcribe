'''This program prompts the user for the GCP .json file, the folder containing .flac audio files to transcribe, and saved GCP bucket name in a .txt file.
   It will then check for duplicates, upload non-duplicates files to the GCP Storage bucket, and transcribe using a call to the GCP speech-to-text API.
   The speech-to-text response is then parsed and saved as a .docx in the Transcripts folder and is uploaded to the GCP bucket.'''

from checkDuplicatesGCPnLocal import checkDuplicates
from checkGCPBuckets import checkBuckets, listBlobs
from selectFiles import userSelectedFiles, getGCSUri, getFileName, credentialManagement, openBucketName, verifyFolderExists, createFolder, moveTranscriptFiles, selectFolderFiles
from transcribe_audio import transcribeRequest, getTranscriptFileName
from uploadBlobsToBucket import uploadBlobs, verifyUploadedBlobs, attemptReupload


def main():
	# input for the file pathway to the gcp json file
	credentialPath = credentialManagement()
	if not credentialPath:
		return

	# input for the right bucket name to check objects and to compare with user files (.txt file saved to program directory)y
	correctBucketName = openBucketName()

	# input for the folder location to store transcripts
	transcriptFolder = 'Transcripts'

	# verify provided transcript folder location exists and create folder if it doesn't
	if not verifyFolderExists(transcriptFolder):
		createFolder(transcriptFolder)

	# verify bucket exists or access to bucket is available
	if not checkBuckets(correctBucketName, credentialPath):
		print(f"The provided bucket name: '{correctBucketName}' does not exist or insufficient permissions to access the bucket.")

		return

	# get the list of blobs currently in bucket
	bucketBlobObjects = listBlobs(correctBucketName, credentialPath)

	# get list of audio files to process 
	userFilesToUpload, audioFileFolder = userSelectedFiles()
	
	# check if audio files exist to be processed from the user selected folder
	if not userFilesToUpload:
		if not audioFileFolder:
			print('Selecting the folder for audio files was cancelled, this program will now end.')
		else:
			print(f'No .flac files were found in the folder \'{audioFileFolder}\'.\nThis program will now end.')

		return

	# check for duplicate files provided from user in userFilesToUpload with existing files in bucketBlobObjects
	newFilesToUpload, duplicateFiles = checkDuplicates(userFilesToUpload, bucketBlobObjects)
	print(f'The file(s): {duplicateFiles} already present in the bucket and will be skipped.')

	# check if no files need to be added because they are all duplicates
	if not newFilesToUpload:
		print(f'\nAll audio files from {audioFileFolder} already exist in the GCP bucket or have the same name.\nIf the files are not duplicates, please re-name them and try again.\nThis program will now end.')

		return

	# upload files to bucket in GCP storage
	fileNameInBucket = getFileName(newFilesToUpload)
	print("Initiating file uploads...")
	uploadBlobs(correctBucketName, newFilesToUpload, fileNameInBucket, credentialPath)

	# verify successful upload into bucket
	successfulUploads, unsuccessfulUploads, uploadStatus = verifyUploadedBlobs(correctBucketName, fileNameInBucket, credentialPath)
	if not uploadStatus:
		attemptReupload(correctBucketName, credentialPath, successfulUploads, unsuccessfulUploads)
	else:
		print("All files successfully uploaded.")

	# transcribe uploaded files, parse response, and save transcript as a .docx file
	gcsUrisToTranscribe = getGCSUri(correctBucketName, successfulUploads)
	transcribeRequest(gcsUrisToTranscribe, credentialPath)

	# check for duplicate transcript files in GCP bucket
	transcriptFiles = selectFolderFiles('*.docx')
	print(f'debug1:{transcriptFiles}')
	transcriptFilesToUpload, duplicateTranscriptFiles = checkDuplicates(transcriptFiles, bucketBlobObjects)
	print(f'The transcript file(s): {duplicateTranscriptFiles} already present in the bucket and will be skipped.')

	# upload trancript(s) to the gcp bucket
	transcriptFileNameInBucket = getFileName(transcriptFilesToUpload)
	print("Initiating transcript file uploads...")
	uploadBlobs(correctBucketName, transcriptFilesToUpload, transcriptFileNameInBucket, credentialPath)

	# verify successful trancript upload into bucket
	successfulTranscriptUploads, unsuccessfulTranscriptUploads, transcriptUploadStatus = verifyUploadedBlobs(correctBucketName, transcriptFileNameInBucket, credentialPath)
	if not transcriptUploadStatus:
		attemptReupload(correctBucketName, credentialPath, successfulTranscriptUploads, unsuccessfulTranscriptUploads)
	else:
		print("All files successfully uploaded.")
	
	# move transcript files to provided local folder
	moveTranscriptFiles(transcriptFiles, transcriptFolder)

	print('Operation completed.')

main()



