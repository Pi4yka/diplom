#!/home/g/godfri4232/.flaskapp/bin/python
# -*- coding: UTF-8 -*-

from wsgiref.handlers import CGIHandler
from diplom import app

CGIHandler().run(app)