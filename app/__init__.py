from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from preferences import Config
from preferences import application_name

app: Flask = Flask(application_name, template_folder='app/templates')
app.config.from_object(Config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import API
from app.certificates.BirthCertificate import views
from app.certificates.DeathCertificate import views
from app.certificates.PerinatalDeathCertificate import views
from app.refbooks.DocumentType import views
from app.refbooks.MKB import views
from app.refbooks.ClientValidation import views
from app.refbooks.DocumentType import views
from app.refbooks.Organisation import views
from app.refbooks.Address import views
from app.refbooks.Client import views
from app.refbooks.Post import views
from app.refbooks.Speciality import views
from app.refbooks.UserPreferences import views
from app.refbooks.Counter import views
