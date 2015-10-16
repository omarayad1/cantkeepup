import urllib # pragma: no cover
from app.models import Command
class CommandProcessor:
	def __init__(self,command):
		self.command = command

	def parseCommand(self):
		pass
	
	def constructUrl(self):
		pass

	def processCommand(self):
		tokens = self.command.split(' ', 1)

		cmd_id = tokens[0]

		if len(tokens) > 1:
			commandText = tokens[1]
			commandText = urllib.quote(commandText.encode('utf8'), safe='')
		else:
			commandText = ""

		item = Command.query.filter_by(cmd_id=cmd_id).first()

		if item is None:
			self.command = urllib.quote(self.command.encode('utf8'), safe='')
			return 'http://www.google.com/search?q=%s' % self.command
		else:
			data = item.url
			return data.replace('%s', commandText)
