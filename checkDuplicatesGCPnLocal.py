'''This script compares blobs in GCP buckets for duplicates from the user folder and returns the list of non-duplicates and duplicates'''

from selectFiles import userSelectedFiles, getFileName

def checkDuplicates(filesFromUser, filesFromBucket):
	'''checks a provided string/list with objects in gcp bucket if there are duplicates.
	Accepts filesFromUser for the string/list of file paths for the files to check;
			filesFromBucket for the list of objects in the bucket to compare with.
	Returns newFilesPaths as a string/list of file paths of the files not in the bucket;
			duplicateFiles as a string/list of file names of duplicate objects already in the bucket.'''
	
	if type(filesFromUser) is list:
		duplicateFiles = []
		newFilesPaths = filesFromUser
		newFiles = getFileName(filesFromUser)

		blobs = filesFromBucket
		for blob in blobs:
			for files in filesFromUser:
				if blob == getFileName(files):
					duplicateFiles.append(blob)
					newFilesPaths.remove(files)
					newFiles.remove(blob)

	elif type(filesFromUser) is str:
		duplicateFiles = ''
		newFilesPaths = filesFromUser
		newFiles = getFileName(filesFromUser)

		blobs = filesFromBucket
		for blob in blobs:
			if blob == getFileName(filesFromUser):
				duplicateFiles = blob
				newFilesPaths = ''
				newFiles = getFileName(filesFromUser)

	print (f"Duplicate files in bucket: {duplicateFiles}")
	print (f"New files to add in bucket: {newFiles}")

	return newFilesPaths, duplicateFiles


