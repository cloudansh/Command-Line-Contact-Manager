
# Command Line Contact Manager

## Overview
The Command Line Contact Manager is a user-friendly tool designed for managing contacts directly from the command line. It features user authentication, JWT-based security, and seamless integration with a MongoDB database. The application also includes an automated MongoDB startup process, ensuring a smooth user experience.
## Features

- **User Authentication**: 
  - Secure registration and login functionality.
  - Passwords are hashed before storage.
  - JWT (JSON Web Tokens) used for session management and secure user identification.

- **MongoDB Integration**: 
  - Automatically starts MongoDB if it's not running.
  - Uses MongoDB for storing user credentials and contact information.

- **Contact Management**:
  - **Add Contacts**: Add new contacts with details like name, email, phone number.
  - **View Contacts**: View a list of all saved contacts.
  - **Update Contacts**: Edit existing contact details.
  - **Search Contacts**: Search contacts by name, phone number, or email.
  - **Delete Contacts**: Remove contacts from the database.

- **Exit and Clean Shutdown**:
  - Gracefully exits the application.
  - MongoDB



## Installation

Clone the repo
```bash
  git clone https://github.com/cloudansh/Command-Line-Contact-Manager/edit/main/README.md

```
Put the directory name into it
```bash
  cd <project dir>
```
Install the requirements
```bash
  pip install -r requirements.txt

```
Run the program
```bash
  python start.py
```


## Requirement

Python 3.10 or later
MongoDB installed and accessible

# Note
Executable might not work will be fixed soon :)
