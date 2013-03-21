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
			self.data = {'alerts': [], 'pagedata': {}}

	@property
	def alerts(self):
		return self.data['alerts']

	@property
	def pagedata(self):
		return self.data['pagedata']

	def save(self):
		with self.save_lock:
			tmpfile = ".{}~".format(os.path.basename(self.filename))
			tmpfile = os.path.join(os.path.dirname(self.filename), tmpfile)
			output = json.dumps(self.data, indent=4) + '\n'

			f = None
			try:
				f = open(tmpfile, 'w')
				f.write(output)
				f.close()
			except:
				if f: os.remove(tmpfile)
				raise

			os.rename(tmpfile, self.filename)
