import json

class Torrent(object):
	def __init__(self, data):
                self.data = data 

        def __str__(self):
            return json.dumps(self.data)

        def __repr__(self):
            return json.dumps(self.data)
