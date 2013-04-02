
def main(store, *urls, **kwargs):
	"""Takes aditional kwarg: -v, --verbose flag"""
	verbose = kwargs.pop('v', None) or kwargs.pop('verbose', None) or False
	if verbose not in {True, False}: raise TypeError("verbose flag should not be given a value")
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
		s = "{url}: Changes detected at {timestamp}: {changes}".format(changes=changes, **alert)
		print s
