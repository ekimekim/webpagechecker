from headers import etag, lastmodified
from contenthash import contenthash

# {name: (function: requests Response object -> jsonable value)}
METHODS = dict(
	etag=etag,
	lastmodified=lastmodified,
	contenthash=contenthash,
)
