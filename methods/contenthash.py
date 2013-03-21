from sha import sha

def contenthash(resp):
	return sha(r.content).digest()
