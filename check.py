import time
from methods import METHODS
import requests

def compare(store, url, **info):
	"""Compare given info to existing info, returning a dict {key: (old, new)} of changed values"""
	if url not in store.pagedata: return {}
	changes = {}
	thisdata = store.pagedata[url]
	for k, v in info.items():
		if k in thisdata and thisdata[k] != v:
			changes[k] = (thisdata[k], v)
	return changes

def update(store, url, **info):
	store.pagedata.setdefault(url, {}).update(info)
	store.save()

def do_storework(store, url, **info):
	"""Compare, update and generate alerts"""
	changes = compare(store, url, **info)
	if changes:
		changes.update(url=url, timestamp=time.time())
		store.alerts.append(changes)
	update(store, url, **info) # saves alerts too

def check_url(store, url, methods):
	resp = requests.get(url)
	info = {name : fn(resp) for name, fn in methods.items()}
	do_storework(store, url, **info)

def main(store, *urls, **kwargs):
	"""Takes additional kwarg: methods = comma-seperated list of method names to use"""
	if 'methods' in kwargs:
		methods = {name: METHODS[name] for name in kwargs.pop('methods').split(',')}
	else:
		methods = METHODS
	if kwargs: raise TypeError("Unknown keyword arguments")

	if not urls:
		urls = store.pagedata.keys()

	for url in urls:
		check_url(store, url, methods)

