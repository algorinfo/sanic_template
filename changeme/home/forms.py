from wtforms import Form, fields


class LoginForm(Form):
    username = fields.StringField("Username")
    password = fields.PasswordField("Password")
