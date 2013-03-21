from data import Store
import sys, os
import check
import show

USAGE = """
%s check {URL}   - Check the given urls for changes, or all urls known if none given
%s show {URL}    - Print info on changes for the given urls (if any), or all if none given
%s query {URL}   - Exit non-zero if any changes for the given urls, or any if none given
%s clear {URL}   - Clear alerts for the given urls, or all if none given
"""

# We don't execute unless we must, to prevent needless reliance on HOME being in env
DEFAULT_FILENAME = lambda: os.path.join(os.env['HOME'], ".webpagecheck.json")

def main(command, *urls, **kwargs):
	storefile = kwargs.pop('f', None) or kwargs.pop('filename', None) or DEFAULT_FILENAME()
	store = Store(storefile)

	submains = dict(check=check.main, show=show.main, query=query, clear=clear)
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
			del store.alerts[a]
	else:
		for a in store.alerts:
			if a['url'] in urls:
				del store.alerts[a]
	store.save()
