# gcp-audio-transcribe
Uploads a folder of .flac files into Google Cloud Storage, transcribes audio using the Speech-to-Text API, and saves the transcript as a .docx file locally and in the Cloud Storage bucket.

## Before Running the Python Program
### gcp_storage_bucket.txt
Set the target bucket name here in Google Cloud Storage to store uploaded audio files.

The format to enter the bucekt name in `gcp_storage_bucket.txt` is `bucket_name='your_bucket_name'`.

### gcp_json_path.txt (optional)
Set the file pathway of the GCP .json to interface with the GCP API. Optionally, this can be skipped as the program will prompt for the file if not found.

The format to enter the .json file path in `gcp_json_path.txt` is `json_path='C:\Your\json\File\Path.json'`.

## Optional Features to Enhance Speech Recognition
In the function `transcribeRequest()` in `transcribe_audio.py`, speech recognition can be enhanced in transcriptions by using [speech adaptation][speech-adapt]. This uses `speech.SpeechContext()` and can be applied by uncommenting this section of code. For further refinement of speech recognition accuracy, [speech adaptation boost][speech-adapt-boost] can be applied to an enabled speech adaptation speech request by uncommenting `speech_contexts = [speechContexts]` in `transcribe_audio.py` and assigning phrases and weights. (Speech adaptation boost is a beta feature and requires beta access to use)

## Required Packages
Package versions listed were used to build the program on python 3.7. Newer versions should work, if not, match package versions here. Requires the [Google Cloud SDK][cloud-sdk] to be installed.
| Package | Version |
| ------- | ------- |
| [python-docx][pyDocx] | 0.8.11 |
| [google-cloud-speech][gcp-speech] | 2.5.0 |
| [google-cloud-storage][gcp-storage] | 1.41.1 |

  [pyDocx]: <https://python-docx.readthedocs.io/en/latest/>
  [gcp-speech]: <https://github.com/googleapis/python-speech>
  [gcp-storage]: <https://github.com/googleapis/python-storage>
  [speech-adapt]: <https://cloud.google.com/speech-to-text/docs/context-strength>
  [cloud-sdk]: <https://cloud.google.com/sdk/docs/install-sdk>
  [speech-adapt-boost]: <https://cloud.google.com/speech-to-text/docs/speech-adaptation#fine-tune_transcription_results_using_boost_beta>
