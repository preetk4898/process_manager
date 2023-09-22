# Process Manager Tool

Written by Preet Kaur 
Sources used: 
- FASTApi Docs: https://fastapi.tiangolo.com/
- Uvicorn Docs: https://www.uvicorn.org/
- Pytest Docs: https://docs.pytest.org/en/7.1.x/contents.html
- StackOverflow

## Overview

The Process Manager is a Python class designed to handle process IDs. It allows adding, returning, and retrieving processes. The class uses a pandas DataFrame to store process information, including process IDs, process names, and the status of each process (either 'in use' or 'available'). 

The Process Manager class also uses thread-safe operations to support concurrent modifications. It uses Python's `threading` module to implement reentrant locks, which allow a thread to acquire the same lock multiple times without blocking. This is crucial for avoiding race conditions where two threads might try to modify the same data concurrently.

## Logic Behind the Process Manager

The Process Manager class is used to manage process IDs. It has the following methods:

- add_process(process_name, user_id): Adds a process with the given name and returns its ID. Raises an exception if the maximum number of processes is reached.
- return_process(process_id, user_id, process_name): Returns a process with the given ID, making it available for reuse. Raises an exception if the process ID does not exist, if it's not in use, if it's not associated with the user, or if the process name does not match.
- get_process(process_id, user_id): Gets a process with the given process ID and user ID. Raises a ValueError if no such process exists.

## API Endpoints

The tool provides the following API endpoints:

- POST /processes/: Adds a process. The request body should be a JSON object with two properties: process_name and user_id. Returns a JSON object with the process ID. If the process name or user ID is empty, it returns a 400 status code. If the maximum number of processes is reached, it returns a 403 status code.
- PUT /processes/{pid}/{user_id}/{process_name}: Returns a process. The process ID, user ID, and process name should be specified in the URL. Returns a JSON object with a success message. If the process ID does not exist, is not in use, is not associated with the user, or if the process name does not match, it returns a 400 status code.
- GET /processes/{pid}/{user_id}: Gets a process. The process ID and user ID should be specified in the URL. Returns a JSON object with the process ID and process name. If no such process exists, it returns a 404 status code.

## Edge Cases

The tool handles several edge cases:

- If the process name or user ID is empty when trying to add a process, the /processes/ endpoint returns a 400 status code with an error message.
- If the maximum number of processes is reached when trying to add a process, the /processes/ endpoint returns a 403 status code with an error message.
- If a non-existent process ID, a process ID that's not in use, a process ID that's not associated with the user, or a mismatched process name is provided when trying to return a process, the /processes/{pid}/{user_id}/{process_name} endpoint returns a 400 status code with an error message.
- If a non-existent process ID is provided when trying to get a process, the /processes/{pid}/{user_id} endpoint returns a 404 status code with an error message.

## Installation

Requirements
To use the tool, you need to have the following packages installed:

1. pandas
2. FastAPI
3. Uvicorn

You can install these packages using pip:

```bash
pip install pandas fastapi uvicorn
```

3. Download the `process_id.py` file and save it in your project directory.

## Usage

The Process Manager can be used in a Python script or through an API.

### Python Script

Here's an example of how to use the Process Manager in a Python script:

```python
from process_id_tool.process_id import ProcessManager

# Initialize ProcessManager
pm = ProcessManager()

# Add a process
process_id = pm.add_process('test_process', 'test_user')

# Return a process
pm.return_process(process_id, 'test_user', 'test_process')

# Get a process
process = pm.get_process(process_id, 'test_user')
```

### API

You can use the ProcessManager class with the FastAPI application and Uvicorn as follows:

1. Save the FastAPI application in a Python script, for example main.py.
2. Run the FastAPI application with Uvicorn:

```bash
python uvicorn script_name:app --reload
```

3. Interacting with the FastAPI application: After running the FastAPI application, users can interact with it using HTTP requests. These requests can be made using Python's requests library.

- To add a process, users can make a POST request to the /processes/ endpoint. The process name and user ID must be included in the request body as JSON. Here's an example:

```python
import requests
import json

url = 'http://localhost:8000/processes/'
headers = {'Content-Type': 'application/json'}
data = {'process_name': 'process1', 'user_id': 'user1'}
response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())
```

- To return a process, users can make a PUT request to the /processes/{pid}/{user_id}/{process_name} endpoint, replacing {pid}, {user_id}, and {process_name} with the process ID, user ID, and process name, respectively. Here's an example:

```python
import requests

url = 'http://localhost:8000/processes/1/user1/process1'
response = requests.put(url)

print(response.json())
```

- To get a process, users can make a GET request to the /processes/{pid}/{user_id} endpoint, replacing {pid} and {user_id} with the process ID and user ID, respectively. Here's an example:

```python 
import requests

url = 'http://localhost:8000/processes/1/user1'
response = requests.get(url)

print(response.json())
```

