# -*- coding: utf-8 -*-
from app import db
from app.models import *
from app.core.helpers import getGroupId, getUserId
# create the db and the db table
db.create_all()

# insert data

## groups
db.session.add(Group("global", "Global Group"))

## users
db.session.add(User("ghooo", "Mohamed", "Ghoneim", "ghooo", \
		"ghooo@cantkeepup.com"))
db.session.add(User("omarayad1", "Omar", "Ayad", "omarayad1", \
		"omarayad1@cantkeepup.com"))

## commands
### global commands
db.session.add(Command( \
		"s", \
		"http://www.google.com/search?q=%s", \
		"Google Search", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

db.session.add(Command( \
		"g", \
		"http://www.google.com/search?q=%s", \
		"Google Search", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

db.session.add(Command( \
		"t", \
		"https://translate.google.com/#en/ar/%s", \
		"Google Translate", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

db.session.add(Command( \
		"p", \
		"https://pastie.org", \
		"Pastie", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

db.session.add(Command( \
		"ulib", \
		"http://aucegypt.summon.serialssolutions.com/search?utf8=✓&s.q=%s", \
		"University Library", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

db.session.add(Command( \
		"shorten", \
		"https://api-ssl.bitly.com/v3/shorten?access_token=9c15127ed875236ed5a6d91bf158dceeb66cf73a&longUrl=%s&format=txt", \
		"URL Shortner", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

db.session.add(Command( \
		"map", \
		"https://www.google.com.eg/maps/search/%s", \
		"Google Maps", \
		getGroupId("global"), \
		getUserId("ghooo") \
		))

### ghooo's commands
db.session.add(Command( \
		"ocvs", \
		"https://github.com/Itseez/opencv/search?utf8=✓&q=\"%s\"", \
		"OpenCV Codebase", \
		getUserId("ghooo"), \
		getUserId("ghooo") \
		))

### omarayad1's commands
db.session.add(Command( \
		"batee5", \
		"http://www.theuselessweb.com/", \
		"Batee5", \
		getUserId("omarayad1"), \
		getUserId("omarayad1") \
		))

# commit the changes
db.session.commit()
