import os
import sys

project=os.path.dirname(__file__)
app=os.path.join(project, "app")

sys.path.append(project)
sys.path.append(os.path.join(app, "lib"))

# virtualenv lib
import site
site.addsitedir(os.path.join(project, "lib/python2.7/site-packages"))

from app import app as application
