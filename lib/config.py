filename = './config.txt'

class Config():

	def __init__(self):
		self.token = self.getFromConfigFile('DISCORD_TOKEN')
		self.prefix = self.getFromConfigFile('COMMANDS_PREFIX')
		# self.guild

	def getFromConfigFile(self, var):
		with open(filename) as f:
			lines = f.read().splitlines()

		for line in lines:
			if line.startswith(var):
				return line.split('=')[1]