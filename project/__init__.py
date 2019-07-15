from flask import *

app = Flask(__name__)
app.secret_key='abc'

import project.com.controller
