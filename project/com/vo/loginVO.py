from wtforms import *


class loginVO:
    username = StringField
    password = StringField

class registerVO:
    name = StringField
    username = StringField
    start = StringField
    end = StringField
    password = StringField
    c_password = StringField
