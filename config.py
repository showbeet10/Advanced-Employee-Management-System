#It contains 
# configuration things like : URL, API, secrectKey, database url

class Config:

    SECRET_KEY = "sha256"

    SQLALCHEMY_DATABASE_URI = "sqlite:///employee.db"
    SQLALCHEMY_TRACK_MODIFICATION = False

    APP_NAME = "Employee Management System"
    UPLOAD_FOLDER = "uploads"
    API_KEY = "12341asdasd"
    DEBUG = True