from sha import sha

def contenthash(resp):
	return ''.join('%02x' % ord(c) for c in sha(resp.content).digest())
