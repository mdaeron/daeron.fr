#! /usr/bin/env python3

from flask import Flask, render_template, Blueprint
from flaskext.markdown import Markdown
import os, datetime

my_blueprint = Blueprint('my_blueprint', __name__, template_folder='templates', url_prefix='/daeron.fr')

app = Flask(__name__)

app.config.update(
	FREEZER_DESTINATION = 'freezer',
	)

Markdown(app, extensions = [
	'markdown.extensions.tables',
# 	'pymdownx.magiclink',
# 	'pymdownx.betterem',
	'pymdownx.highlight',
	'pymdownx.tilde',
	'pymdownx.caret',
# 	'pymdownx.emoji',
# 	'pymdownx.tasklist',
	'pymdownx.superfences'
	])

@my_blueprint.route('/')
@my_blueprint.route('/<page>/')
def main(page=''):
	if page == '':
		page = 'landing'
	file = f'{app.root_path}/pages/{page}.md'
	with open(file) as fid:
		md = fid.read()
	return render_template('main.html', md = md, page = page, now = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d %b %Y'))

app.register_blueprint(my_blueprint)
app.run(debug = True)

from flask_frozen import Freezer
freezer = Freezer(app)
freezer.freeze()

from pathlib import Path
import shutil
shutil.copytree(Path('freezer/daeron.fr'), Path('docs'), dirs_exist_ok = True)
shutil.copytree(Path('freezer/static'), Path('docs/static'), dirs_exist_ok = True)
shutil.copytree(Path('pages/biblio'), Path('docs/biblio'), dirs_exist_ok = True)
Path('docs/.nojekyll').touch()
