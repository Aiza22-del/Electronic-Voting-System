Electronic Voting System

A secure and efficient online voting platform designed to streamline the election process. Built using Python (Flask), MySQL, HTML/CSS, and JavaScript, this system ensures robust security through secret key mechanisms and provides real-time result tracking.

Features

- Secure voter authentication using a secret key
- Email notifications for vote confirmation
- Real-time results tracking and updates
- Role-based login (Admin, Voter)
- Responsive and user-friendly UI
- Encrypted vote storage for enhanced security

Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python with Flask
- **Database:** MySQL
- **Security:** Secret key mechanism, email validation

How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Aiza22-del/Electronic-Voting-System.git
cd Electronic-Voting-System
````

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

* Create a MySQL database named `evoting`
* Update the database configuration in the project (e.g., `config.py` or directly in the app file)

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your-username'
app.config['MYSQL_PASSWORD'] = 'your-password'
app.config['MYSQL_DB'] = 'evoting'
```

### 5. Run the Application

```bash
python app.py
```

### 6. Open in Browser

Visit: `http://localhost:5000`

## 📂 Folder Structure

```
├── static/
├── templates/
├── app.py
├── config.py
├── requirements.txt
└── README.md
```
