from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(FlaskForm):
    url = URLField('The URL for your bookmark:', validators=[DataRequired(), url(message="Please enter a valid url.")])
    description = StringField('Add an optional description:')

    def validate(self):
        if not self.url.data.startswith("http://") or\
            self.url.data.startswith("https://"):
            self.url.data = f"http://{self.url.data}"

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        return True