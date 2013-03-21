import simplejson as json
import os
import gevent.lock


class Store(object):
	def __init__(self, filename):
		self.filename = filename
		self.save_lock = gevent.lock.Semaphore(1)
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
		with self.save_lock:
			tmpfile = ".{}~".format(self.filename)
			output = dumps(self.data)

			try:
				f = open(tmpfile, 'w')
				f.write(output)
				f.close()
			except:
				os.remove(tmpfile)
				raise

			os.rename(tmpfile, self.filename)
