from wtforms import *


class loginVO:
    username = StringField
    password = StringField

class registerVO:
    name = StringField
    username = StringField
    start = StringField
    end = StringField
    assigned=StringField
    password = StringField
    c_password = StringField
