import os
import sys

project=os.path.dirname(__file__)
app=os.path.dirname(project)

sys.path.append(project)
sys.path.append(app)
sys.path.append(os.path.join(app, "lib"))

# virtualenv lib
sys.path.append("/path/to/virtualenv/lib")

from app import app as application

