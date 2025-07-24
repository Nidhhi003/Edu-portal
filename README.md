# Edu-portal
ScribbleSpace is a clean and user-friendly web application designed to simplify academic file sharing among students and educators. 
Built using Python (Flask) and SQLite for the backend and HTML/CSS, Javascript for the frontend.
The app supports uploading, downloading, and deleting study materials like notes, assignments, projects, and more. 
Feature:
1. Upload and organize educational files.
2. Download resources instantly.
3. Delete outdated or unwanted files.
4. SQLite database for lightweight and efficient storage.
5. Fully responsive and modern UI.
6. Secure file handling with confirmation prompts


** How to Run Locally**

#### 1. Clone the Repository

Open terminal or command prompt and run:

```
git clone https://github.com/your-username/edu_portal.git
cd edu_portal
```

#### 2. Set Up Virtual Environment (Recommended)

```
python -m venv venv
```

Then activate it:

* **On Windows**:
  `venv\Scripts\activate`

* **On macOS/Linux**:
  `source venv/bin/activate`

#### 3. Install Dependencies

```
pip install -r requirements.txt
```

#### 4. Run the App

```
python app.py
```
```
python -m flask run
```

Now visit in browser:
`http://127.0.0.1:5000`


### The uploads folder in ./static is where app saves the files that users upload.


