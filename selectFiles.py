
import glob
import tkinter
from tkinter import filedialog
import os
import shutil
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage

def userSelectedFiles():
    '''Prompts user for desired folder of .flac files in the folder directory
    Returns filePaths as a list of file pathways of .flac files in the selected folder;
            tempDir as the user selected folder pathway.'''

    root = tkinter.Tk()
    root.withdraw()

    currentDir = os.getcwd()
    tempDir = filedialog.askdirectory(parent = root,
                                      title = 'Please select the folder of the audio files'
                                      )

    if not tempDir:
        filePaths = tempDir
        return filePaths, tempDir

    fileLocation = os.path.join(tempDir, '*.flac')
    #adjust tkinter forward slash directory path
    fileLocation = os.path.normpath(fileLocation)

    filePaths = glob.glob(fileLocation)

    return filePaths, tempDir

def selectFolderFiles(fileExtension):
    '''Returns the list of files in the script folder directory that is the file extension provided in the argument.
    Accepts fileExtension as a string of the type of file to be found.
    Returns listOfFiles as a list of files of the provided file extension in the folder directory.'''

    currentDirectory = os.getcwd()
    listOfFiles = os.path.join(currentDirectory, fileExtension)
    listOfFiles = os.path.normpath(listOfFiles)
    listOfFiles = glob.glob(listOfFiles)

    return listOfFiles

def credentialManagement():
    '''Retrieves currently stored GCP json path and prompts user if it is to be used. If there is no stored/valid GCP json path,
    prompts user for GCP json file.
    Returns GCPCredentials as a string of the file path of the json file to be used.
            GCPCredentials as a boolean if the user chooses to quit in the input prompt.'''

    default_json_file_storage = 'gcp_json_path.txt'
    userSelectCondition = False
    allowableInputs = ['y', 'Y', 'n', 'N', 'q', 'Q']
    proceedInputs = allowableInputs[:2]
    changeInputs = allowableInputs[2:4]
    quitInputs = allowableInputs[4:]

    try:
        file = open(default_json_file_storage, 'r')
        firstLine = file.readline()
        firstLine = firstLine.strip()
        beginningIndex = firstLine.find('=') + 1

        GCPCredentials = firstLine[beginningIndex:]

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCPCredentials
        storageClient = storage.Client()
        buckets = storageClient.list_buckets()

        while not userSelectCondition:
            userSelect = input(f'The GCP credentials in the .json file \'{GCPCredentials}\' will be used with the GCP API.\nEnter \'y\' to confirm | Enter \'n\' to change | Enter \'q\' to quit\n')
            if isinstance(userSelect, str):
                if len(userSelect) == 1:
                    if userSelect in allowableInputs:
                        if userSelect in proceedInputs:
                            return GCPCredentials
                        elif userSelect in changeInputs:
                            GCPCredentials = userSelectJSON()
                            createGCPCredentialPath(default_json_file_storage, GCPCredentials)
                        elif userSelect in quitInputs:
                            GCPCredentials = False
                            return GCPCredentials
                        else:
                            print('The entered text is not valid.')
                    else:
                        print('The entered text is not valid.')
                else:
                    print('The entered text is not valid.')
            else:
                print('The entered text is not valid.')
                
    except DefaultCredentialsError:
        print(f'The \'{default_json_file_storage}\' storing the location of the GCP credentials .json file did not contain valid credentials. Please select a file with valid credentials.')
        GCPCredentials = userSelectJSON()
        print(f'The selected GCP credentials are in the file at: \'{GCPCredentials}\'')
        createGCPCredentialPath(default_json_file_storage, GCPCredentials)

        return GCPCredentials

    except FileNotFoundError:
        print(f'The \'{default_json_file_storage}\' storing the location of the GCP credentials could not be found. Please select the .json file containing the credentials.')
        GCPCredentials = userSelectJSON()
        print(f'The selected GCP credentials are in the file at: \'{GCPCredentials}\'')
        createGCPCredentialPath(default_json_file_storage, GCPCredentials)

        return GCPCredentials

def userSelectJSON():
    '''Prompts the user for the file of the .json file for google cloud credentials. 
    Returns jsonFilePath as the file path of the selected json file.'''

    root = tkinter.Tk()
    root.withdraw()

    userJsonFile = filedialog.askopenfilename(parent = root,
                                              title = 'Please select the Google Cloud .json file',
                                              filetypes=(('json files','*.json'), ('all files', '*.*'))
                                              )
    jsonFilePath = os.path.normpath(userJsonFile)

    return jsonFilePath

def openBucketName():
    '''Opens and reads the gcp_storage_bucket.txt file where the bucket name is stored,
    Returns theBucketName as the bucket name read from the txt file.'''

    file = open('gcp_storage_bucket.txt', 'r')
    firstLine = file.readline()
    firstLine = firstLine.strip()
    beginningIndex = firstLine.find('=') + 1

    theBucketName = firstLine[beginningIndex:]

    return theBucketName

print(openBucketName())

def getFileName(fileDirectories):
    '''extracts the file name from a Windows file pathway.
    Accepts fileDirectories as a string/list of file pathway(s).
    Returns fileNameStringForm as a string of the file name if fileDirectories is a string;
            fileNameListForm as a list of the file names if fileDirectories is a list'''

    reversedFilePath = ""
    fileNameListForm = []
    fileNameStringForm = ""

    if type(fileDirectories) is list:
        for filePath in fileDirectories:
            reversedFilePath = filePath[::-1]
            backslashIndex = reversedFilePath.find('\\')
            fileNameStartIndex = len(filePath) - backslashIndex
            tempFileName = filePath[fileNameStartIndex:]

            fileNameListForm.append(tempFileName)

        return fileNameListForm

    elif type(fileDirectories) is str:
        reversedFilePath = fileDirectories[::-1]
        backslashIndex = reversedFilePath.find('\\')
        fileNameStartIndex = len(fileDirectories) - backslashIndex
        tempFileName = fileDirectories[fileNameStartIndex:]

        fileNameStringForm = tempFileName

        return fileNameStringForm

def getFileNameGCSUri(gcsUri):
    '''extracts the file name without the file extension from a gcs uri.
    Accepts gcsUri as a string/list of gcs uri(s) for processing.
    Returns fileNameStringForm as a string of the file name if gcsUri is a string;
            fileNameListForm as a list of the file names if gcsUri is a list.'''

    reversedFilePath = ""
    fileNameListForm = []
    fileNameStringForm = ""
    
    if type(gcsUri) is list:
        for filePath in gcsUri:
            reversedFilePath = filePath[::-1]
            backslashIndex = reversedFilePath.find('/')
            periodIndex = reversedFilePath.find('.') + 1
            fileNameStartIndex = len(filePath) - backslashIndex
            fileNameEndIndex = len(filePath) - periodIndex
            tempFileName = filePath[fileNameStartIndex:fileNameEndIndex]

            fileNameListForm.append(tempFileName)

        return fileNameListForm

    elif type(gcsUri) is str:
        reversedFilePath = gcsUri[::-1]
        backslashIndex = reversedFilePath.find('/')
        periodIndex = reversedFilePath.find('.') + 1
        fileNameStartIndex = len(gcsUri) - backslashIndex
        fileNameEndIndex = len(gcsUri) - periodIndex
        tempFileName = gcsUri[fileNameStartIndex:fileNameEndIndex]

        fileNameStringForm = tempFileName

        return fileNameStringForm

def getFullFileNameGCSUri(gcsUri):
    '''extracts the file name with the file extension from a gcs uri.
    Accepts gcsUri as a string/list of gcs uri(s) for processing.
    Returns fileNameStringForm as a string of the file name if gcsUri is a string;
            fileNameListForm as a list of the file names if gcsUri is a list.'''

    reversedFilePath = ""
    fileNameListForm = []
    fileNameStringForm = ""
    
    if type(gcsUri) is list:
        for filePath in gcsUri:
            reversedFilePath = filePath[::-1]
            backslashIndex = reversedFilePath.find('/')
            fileNameStartIndex = len(filePath) - backslashIndex
            fileNameEndIndex = len(filePath)
            tempFileName = filePath[fileNameStartIndex:fileNameEndIndex]

            fileNameListForm.append(tempFileName)

        return fileNameListForm

    elif type(gcsUri) is str:
        reversedFilePath = gcsUri[::-1]
        backslashIndex = reversedFilePath.find('/')
        fileNameStartIndex = len(gcsUri) - backslashIndex
        fileNameEndIndex = len(gcsUri)
        tempFileName = gcsUri[fileNameStartIndex:fileNameEndIndex]

        fileNameStringForm = tempFileName

        return fileNameStringForm

def getFileSize(fileDirectories):
    '''obtains the local file's size in bytes.
    Accepts fileDirectories as a string/list of file pathway(s) for processing.
    Returns fileSizeString as a string of the file size if fileDirectories is a string;
            fileSizeList as a list of the file size if fileDirectories is a list.'''

    fileSizeList = []
    fileSizeString = ""

    if type(fileDirectories) is list:
        for filePaths in fileDirectories:
            fileSizeList.append(os.path.getsize(filePaths))

        return fileSizeList

    elif type(fileDirectories) is str:
        fileSizeString = os.path.getsize(fileDirectories)

        return fileSizeString

def getFilePath(fileNames, filePaths):
    '''returns the file path from a file name using a list of file pathways.
    Accepts fileNames as a string/list of file name(s);
            filePaths as a list of file pathways.
    Returns correspondingFilePath as a string/list of file pathways in the order provided from fileNames.'''
    #Potential for major logic errors by same name files if file pathways/names sourced from different folders!!

    if type(fileNames) is list:
        correspondingFilePath = []
        for fileNameItems in fileNames:
            for filePathItems in filePaths:
                if filePathItems.find(fileNameItems) != -1:
                    correspondingFilePath.append(filePathItems)

    elif type(fileNames) is str:
        correspondingFilePath = ''

        for filePathItems in filePaths:
            if filePathItems.find(fileNames) != -1:
                correspondingFilePath = filePathItems

    return correspondingFilePath

def getGCSUri(bucketName, fileName):
    '''constructs the gcs uri using the bucket name and file name (with file extension). Assumes no folders in bucket.
    Accepts bucketName as a string for the name of the bucket;
            fileName as a string/list of the file(s) to get a gcs uri.
    Returns gcsUri as a string/list of the resulting gcs uri for the file(s) in the order provided in fileName.'''
    
    if type(fileName) is list:
        gcsUri = []
        for files in fileName:
            tempGCSUri = 'gs://' + bucketName + '/' + files
            gcsUri.append(tempGCSUri)
    elif type(fileName) is str:
        gcsUri = 'gs://' + bucketName + '/' + fileName

    return gcsUri

def moveTranscriptFiles(fileNames, destinationFolder):
    '''takes the provided file path and moves it to the specified folder. If duplicates file names are found, attempts 10 tries
       with ascending numbering until it ignores the file transfer.
    Accepts files as a string/list of files to be moved.
            destinationFolder as a string of the destination folder for the files.'''

    if type(fileNames) is list:
        for files in fileNames:
            try:
                shutil.move(files, destinationFolder)
                tempAdjustedFileName = files
            except shutil.Error as err:
                print(f'Warning: A transcript file already exists in folder: \'{destinationFolder}\' with the file name: \'{files}\'')
                oldFileName = files
                for attempt in range (1, 50):
                    try:
                        newFileName = addNumberToFileNameForDuplicate(files, attempt)
                        os.rename(oldFileName, newFileName)
                        shutil.move(newFileName, destinationFolder)
                    except shutil.Error as err:
                        print(f'Warning: A transcript file already exists in folder: \'{destinationFolder}\' with the file name: \'{newFileName}\'')
                        oldFileName = newFileName
                    else:
                        tempAdjustedFileName = newFileName
                        print(f'Transcript file: \'{files}\' has been renamed to \'{newFileName}\'.')
                        break
                else:
                    print(f'There are more than 50 files with the name: {files}. Attempts to rename and move the file have been reached. Rename or delete the unneeded files and try again.')
                    print(f'The transcript for {files} is located in the directory of this program: {os.getcwd()}')
                    os.rename(newFileName, oldFileName)

            print(f'Transcript file: \'{tempAdjustedFileName}\' successfully moved to the folder \'{destinationFolder}\'.')

    elif type(fileNames) is str:
        try:
            shutil.move(fileNames, destinationFolder)
            tempAdjustedFileName = fileNames
        except shutil.Error as err:
            print(f'Warning: A transcript file already exists in folder: \'{destinationFolder}\' with the file name: \'{fileNames}\'')
            oldFileName = fileNames
            for attempt in range (1, 50):
                try:
                    newFileName = addNumberToFileNameForDuplicate(fileNames, attempt)
                    os.rename(oldFileName, newFileName)
                    shutil.move(newFileName, destinationFolder)
                except shutil.Error as err:
                    print(f'Warning: A transcript file already exists in folder: \'{destinationFolder}\' with the file name: \'{newFileName}\'')
                    oldFileName = newFileName
                else:
                    tempAdjustedFileName = newFileName
                    print(f'Transcript file: \'{fileNames}\' has been renamed to \'{newFileName}\'.')
                    break
            else:
                print(f'There are more than 50 files with the name: {files}. Attempts to rename and move the file have been reached. Rename or delete the unneeded files and try again.')
                print(f'The transcript for {files} is located in the directory of this program: {os.getcwd()}')
                os.rename(newFileName, oldFileName)

        print(f'Transcript file: \'{tempAdjustedFileName}\' successfully moved to the foler \'{destinationFolder}\'')

def verifyFolderExists(folderName):
    '''takes the provided folder name, checks if it exists locally, and returns the folder status.
    Accepts folderName as a string of the folder name.
    Returns folderExists as a boolean of the folder's status.'''

    folderExists = os.path.exists(folderName)

    return folderExists

def createFolder(folderName):
    '''creates a new folder with the provided name in the default directory or given folder path.
    Accepts folderName as a string of the folder name or full folder path.'''

    os.makedirs(folderName)

def addNumberToFileNameForDuplicate(oldFileName, numberToAdd):
    '''This function adds variable numberToAdd, in brackets, to the end of the file name before the file extension of a provided file name
       and returns the new file name with (numberToAdd) inserted.
       Accepts oldFileName as a string of the file name to be processed;
               numberToAdd as an integer of the number to be added to the old file name.
       Returns newFileName as a string of the file name with numberToAdd in brackets added to the old file name.'''

    positionOfFileExtension = oldFileName.find('.')
    newFileName = oldFileName[:positionOfFileExtension] + '(' + str(numberToAdd) + ')' + oldFileName[positionOfFileExtension:]

    return newFileName

def createGCPCredentialPath(storageFileName, jsonFilePath):
    '''creates a .txt file that stores the file path of the .json file containing the GCP credentials.
    Accepts jsonFilePath as a string of the json file's filepath.
            storageFilePath as a string of the file name storing the .json file path'''

    credentialStorage = open(storageFileName, mode='w')
    stringToWrite = 'json_path=' + jsonFilePath
    credentialStorage.write(stringToWrite)
    credentialStorage.close()

