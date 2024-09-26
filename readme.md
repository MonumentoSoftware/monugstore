# Monumento Gcloud Storage

This is project aims to provide some boilerplate code to handle actions using google cloud sotrage.

- [Monumento Gcloud Storage](#monumento-gcloud-storage)
- [Requirements](#requirements)
- [Install](#install)
- [Handling credentials](#handling-credentials)
  - [Local mode - Using a JSON file path](#local-mode---using-a-json-file-path)
    - [Hardcoding the path](#hardcoding-the-path)
    - [Using an environment variable](#using-an-environment-variable)
  - [Production mode - Converting the JSON file to a string](#production-mode---converting-the-json-file-to-a-string)
- [Usage](#usage)
  - [Creating a bucket](#creating-a-bucket)
  - [Uploading a file](#uploading-a-file)
  - [Listing files](#listing-files)
    - [listig files using prefix](#listig-files-using-prefix)
  - [Download a file](#download-a-file)
  - [Deleting a file](#deleting-a-file)
  - [Deleting a bucket](#deleting-a-bucket)
- [Author](#author)


# Requirements

- Google cloud account
- Activated google cloud storage API
- The credentials associated with the use of the service, generellay a JSON file.

# Install

To install the project, clone it, and run:
```
poetry install
```

# Handling credentials

To use the google cloud storage service, you need to provide the credentials associated with the service.
The most common and secure way to provide the credentials is using a JSON file.
While in development it is ok to have the credentials in a file, in production it is recommended to use environment variables.

## Local mode - Using a JSON file path

You can use the application with a path to a JSON file containing the credentials in different manners.

### Hardcoding the path
You can hardcode the path to the JSON file in the code.

```python
from monugstore import GCSManager

PATH_TO_CREDENTIALS = "/path/to/credentials.json"
gcs_manager = GCSManager.from_json_file(PATH_TO_CREDENTIALS)
```
### Using an environment variable
You can set an environment variable with the path to the JSON file.

```bash
export PATH_TO_CREDENTIALS=</path/to/credentials.json>
```

Or set the create a `.env` file with the following content:

```bash
PATH_TO_CREDENTIALS=</path/to/credentials.json>
```

And read the environment variable in the code.

```python
import os
from monugstore import GCSManager

PATH_TO_CREDENTIALS = os.getenv("PATH_TO_CREDENTIALS")
gcs_manager = GCSManager.from_json_file(PATH_TO_CREDENTIALS)
```

## Production mode - Converting the JSON file to a string

We have included a command to deal with the issue of storing the json file in production mode, where it is not recommended to store the file in the repository.
To convert the JSON file to a string, you can run the following command:

```bash
mgs-dump-key </path/to/credentials.json>
```
You will receive a string that you can use in the code with environment variables.
In your .env file, you can add the following line:

```bash
CREDENTIAL_STRING=<string>
```

and in the code, you can use the following code:

```python
import os
from monugstore import GCSManager

CREDENTIAL_STRING = os.getenv("CREDENTIAL_STRING")
gcs_manager = GCSManager.from_json_string(CREDENTIAL_STRING)
```

# Usage
After setting up the credentials, you can use the `GCSManager` class to interact with the google cloud storage service.
Without the steps mentioned above, you will not be able to use the service.
Let's say that you are using a hardcoded path to the JSON file.

```python
from monugstore import GCSManager

PATH_TO_CREDENTIALS = "/path/to/credentials.json"
gcs_manager = GCSManager.from_json_file(PATH_TO_CREDENTIALS)
```

## Creating a bucket
You have a instance of the `GCSManager` class, and you can use it to create a bucket.

```python
bucket_name = "my_bucket"
gcs_manager.create_bucket(bucket_name)
```

## Uploading a file
You can upload a file to the bucket using the `upload_file` method.
It will return a public url associated with the blob on the bucket

```python
bucket_name = "my-bucket"
path_to file = "path/to/file.jpg"

public_path = gcs_manager.upload_file(bucket_name, path_to_file)
```

## Listing files 
To list files on a bucket you can run the following method:

```python
bucket_name = "my-bucket"

public_path = gcs_manager.list_files(bucket_name)
```

### listig files using prefix
You can also list files using a prefix:

```python
bucket_name = "my-bucket"
prefix = "path/to/files" 

public_paths = gcs_manager.list_files(bucket_name, prefix)
```

## Download a file
You can download a file from the bucket using the `download_file` method.

```python
bucket_name = "my-bucket"
destination_path = "path/to/destination"

gcs_manager.download_file(bucket_name, "file.jpg", destination_path)
```

## Deleting a file
You can delete a file from the bucket using the `delete_file` method.

```python
bucket_name = "my-bucket"
file_name = "file.jpg"

gcs_manager.delete_file(bucket_name, file_name)
```

## Deleting a bucket
You can delete a bucket using the `delete_bucket` method.

```python
bucket_name = "my-bucket"

gcs_manager.delete_bucket(bucket_name)
```

# Author

This project was created by [Pedro Cavalcanti](https://github.com/pedroKpaxo)
You can contact at:

- [Linkedin](https://www.linkedin.com/in/pedrokpaxo/)
- **Email**: pedro@monumentosoftware.com.br