# Basic Crud Project - CMSC 447 Individual Project
By: Aqeel Mohamed

## Pre-Requirements
1. Latest version of python installed (3.x) <br>
2. Ability to execute scripts through command line. <br>
3. Python virtualenv library installed <br>
4. If you are not able to, run this code below...

```bash
Set-ExecutionPolicy RemoteSigned
```

## Installation
1. Navigate to the CMSC447-Indidividual Folder and open in terminal
```bash
cd CMSC447-Individual
```

2. Activate the virtual environment
Windows: 
```bash
.\venv\Scripts\activate
```

&emsp; &ensp;2a. If virtual environment is not working, delete the venv folder and create a new one, and activate the venv
```bash
python3 -m venv venv
.\venv\Scripts\activate
```

&emsp; &ensp;2b. Install the project requirements using pip
```bash
pip install -r requirements.txt
```

Installation is finished

## Running the project
1. To run the project and host locally, run the program through the command line using flask
```bash
flask run
```

This should pop up
```bash
(venv) PS C:\Users\[User]\...\...\CMSC447-Individual> flask run
 * Serving Flask app 'individualProject.py'
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

2. Click on the link provided, or type into your browser, http://127.0.0.1:5000/
3. Follow the directions provided on the home page of the website
4. A video demonstration is provided in the folder as well for convenience 
5. If the database needs to be reset, a file to reset it has been provided in the sql_commands folder named 'table_init.sql'