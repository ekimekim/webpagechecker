
from_header = lambda header: lambda resp: resp.headers.get(header, None)

etag = from_header('etag')
lastmodified = from_header('last-modified')
