import simplejson as json
import os


class Store(object):
	def __init__(self, filename):
		self.filename = filename
		if os.path.exists(self.filename):
			self.data = json.loads(open(self.filename,'r').read())
		else:
			self.data = {'alerts': {}, 'pagedata': {}}

	@property
	def alerts(self):
		return self.data['alerts']

	@property
	def pagedata(self):
		return self.data[pagedata]

	def save(self):
		tmpfile = ".{}~".format(self.filename)

		try:
			f = open(tmpfile, 'w')
			f.write(dumps(self.data))
			f.close()
		except:
			os.remove(tmpfile)
			raise

		os.rename(tmpfile, self.filename)
