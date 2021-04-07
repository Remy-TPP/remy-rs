# Set up a barebones Django project to use its ORM
import os
import sys

import django

sys.path.append('./remy_rs/data')
sys.dont_write_bytecode = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db.settings')

django.setup()

print('Django set up!')
