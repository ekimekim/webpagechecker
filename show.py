
def main(store, *urls, **kwargs):
	"""Takes aditional kwargs:
		-v, --verbose flag
		-q, --quiet flag
	"""
	verbose = kwargs.pop('v', None) or kwargs.pop('verbose', None)
	quiet = kwargs.pop('q', None) or kwargs.pop('quiet', None)
	if verbose and quiet: raise TypeError("Cannot specify both verbose and quiet.")
	if kwargs: raise TypeError("Unknown keyword arguments")

	for alert in store.alerts:
		if urls and alert['url'] not in urls: continue
		changes = {k:v for k, v in alert.items() if k not in {'timestamp', 'url'}}
		if verbose:
			changes = '\n' + '\n'.join(
				"\t{0}: {1!r} -> {2!r}".format(method, old, new)
				for method, (old, new) in changes.items())
		else:
			changes = ', '.join(changes)
		if quiet:
			s = alert['url']
		else:
			s = "{url}: Changes detected at {timestamp}: {changes}".format(changes=changes, **alert)
		print s
