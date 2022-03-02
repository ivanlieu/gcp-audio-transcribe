# gcp-audio-transcribe
Uploads a folder of .flac files into Google Cloud Storage, transcribes audio using the Speech-to-Text API, and saves the transcript as a .docx file locally and in the Cloud Storage bucket.

## Before Running the Python Program
### gcp_storage_bucket.txt
Set the target bucket name here in Google Cloud Storage to store uploaded audio files.

### gcp_json_path.txt (optional)
Set the file pathway of the GCP .json to interface with the GCP API. Optionally, this can be skipped as the program will prompt for the file if not found.

