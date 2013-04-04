import gevent.monkey
gevent.monkey.patch_all()

import sys, os

from scriptlib import with_argv

from data import Store
import check
import show


# We don't execute unless we must, to prevent needless reliance on HOME being in env
DEFAULT_FILENAME = lambda: os.path.join(os.environ['HOME'], ".webpagecheck.json")

@with_argv
def main(command, *urls, **kwargs):
	"""
	 check {URL}   - Check the given urls for changes, or all urls known if none given
	 show {URL}    - Print info on changes for the given urls (if any), or all if none given
	 query {URL}   - Exit non-zero if any changes for the given urls, or any if none given
	 clear {URL}   - Clear alerts for the given urls, or all if none given
	 forget {URL}  - Remove any given urls from the list of known urls
	 list          - List all known urls
	"""
	storefile = kwargs.pop('f', None) or kwargs.pop('filename', None) or DEFAULT_FILENAME()
	store = Store(storefile)

	submains = dict(check=check.main, show=show.main, query=query, clear=clear, forget=forget, list=list)
	if command not in submains: raise TypeError("Unknown sub-command")
	submains[command](store, *urls, **kwargs)


def query(store, *urls, **kwargs):
	if kwargs: raise TypeError("Unknown keyword arguments")
	if urls:
		found = [a for a in store.alerts if a['url'] in urls]
	else:
		found = store.alerts
	sys.exit(1 if found else 0)


def clear(store, *urls, **kwargs):
	if kwargs: raise TypeError("Unknown keyword arguments")
	if not urls:
		for a in store.alerts:
			store.alerts.remove(a)
	else:
		for a in store.alerts:
			if a['url'] in urls:
				store.alerts.remove(a)
	store.save()


def forget(store, *urls, **kwargs):
	if kwargs: raise TypeError("Unknown keyword arguments")
	for url in urls:
		if url in store.pagedata:
			del store.pagedata[url]
	store.save()


def list(store, v=None, verbose=None):
	"""Takes additional kwarg: -v --verbose flag"""
	verbose = verbose or v
	for url, data in store.pagedata.items():
		s = url
		if verbose:
			s += '\n' + '\n'.join('\t{0}: {1!r}'.format(*item) for item in data.items())
		print s


if __name__=='__main__':
	main()
