import base64
import json
import requests
import torrent

class InvalidTransmissionQuery(Exception):
    """An exception thrown when a query is improperly structured when passed to the
    TransmissionClient
    """
    pass

class TransmissionClient(object):
        def _post_request(self, data):
            """Prepares the request to the Transmission client.

            Sets the authentication for the client, as well as the data to be requested.
            Resets the X-Transmission-Session-Id as needed.
            
            Args:
            data (json): A json representation of the data to be transmitted/requested.

            Returns:
            response (requests.Response): The response from the Transmission Daemon.
            """
            url = "http://{}:{}/transmission/rpc".format(self.host, self.port)
            # Post request
            response = requests.post(url, data=data, auth=(self.username, self.password), 
                    headers={ "X-Transmission-Session-Id": self.session_id })
            # Check if the session id needs to be renewed.
            if response.status_code == 409:
                self.session_id = response.headers["X-Transmission-Session-Id"]
                return requests.post(url, data=data, auth=(self.username, self.password),
                        headers={ "X-Transmission-Session-Id": self.session_id })
	    return response

        def __init__(self, host, port=9091, username="transmission", password="transmission"):
            """Initializes the client to communicate with the Transmission API over the network.
            
            Args:
            username (string): The username used for authentication with the Transmission Daemon.
            password (string): The password used for authentication with the Transmission Daemon.
            host (string): The hostname where the Transmission Daemon is located.
            port (int): The port where the Transmisison Daemon is serving.
            session_id (string): The X-Transmission-Session-Id currently being used to protect against XSRF attacks.
            """
	    self.username = username
	    self.password = password
            self.host = host
            self.port = port
            self.session_id = ""

        # Action Requests 
        def start_torrents(self, t_ids=[]):
            """Starts the torrent files of the associated ids passed in.

            Args:
            t_ids ([]int): The array of torrent ids to begin torrenting.

            Returns:
            isStarted (bool): True if the torrenting has begun, false otherwise.
            """
            data = {}
            if t_ids == []:
                data["arguments"] = {}
            else:
                data["arguments"] = { "ids": t_ids }
            data["method"] = "torrent-start"
            response = self._post_request(json.dumps(data))
            if json.loads(response.text)["result"] == "success":
                return True
            else:
                return False
        
        def stop_torrents(self, t_ids=[]):
            """Stops the torrent files of the associated ids passed in.

            Args:
            t_ids ([]int): The array of torrent ids to stop torrenting.

            Returns:
            isStopped (bool): True if the torrenting has halted, false otherwise.
            """
            data = {}
            if t_ids == []:
                data["arguments"] = {}
            else:
                data["arguments"] = { 
                        "ids": t_ids,
                }
            data["method"] = "torrent-stop"
            response = self._post_request(json.dumps(data))
            if json.loads(response.text)["result"] == "success":
                return True
            else:
                return False

        def get_torrent_id(self, filename):
            """Returns the id of the torrent with the assiciated filename.

            Args:
            filename (string): The filename of the torrent file. Omit the '.torrent' extension.
            """
	    torrents = self.get_torrents(fields=["id", "torrentFile"])
            for torrent in torrents:
                if filename in torrent.data["torrentFile"]:
                    return torrent.data["id"]
            return None

	def get_torrents(self, t_ids=[], fields=["id", "name", "totalSize"]):
            """Returns the specified torrent file(s). If none are specified, returns all.

            Args:
            t_ids ([]int): An array of torrent ids.
            fields ([]string): An array of strings indicating the desired attributes of a torrent file(s) to return. Must be of length greater than 1.
            
            Exceptions:
            Throws an exception if there is an insufficient number of fields specified.
            """
            if len(fields) < 1:
                raise InvalidTransmissionQuery("invalid 'torrent-get' query")
            
            data = {}
            if t_ids == []:
                data["arguments"] = { "fields": fields }
            else:
                data["arguments"] = { 
                        "fields": fields,
                        "ids": t_ids,
                }
            data["method"] = "torrent-get"

            json_data = json.dumps(data)
            response = self._post_request(json_data)
            torrents = []
            json_resp = json.loads(response.text)
            for torr in json_resp["arguments"]["torrents"]:
                torrents.append(torrent.Torrent(data=torr))
            return torrents

        def add_torrents(self, filenames, download_dir=""):
            """Adds torrent(s) to the torrent list on the Transmission client.
            
            Args:
            filenames ([]string): An array of filenames or URLs of the .torrent content.

            Returns:
            responses ([]string): An array of information, cooresponding to the filename indices 
                                  attempted to add, and the returned content of the query.
            """
            result = []
            for filename in filenames:
                result.append(self.add_torrent(filename))
            return result

	def add_torrent(self, filename, download_dir=""):
            """Adds a torrent to the torrent list on the Transmission client.
            
            Args:
            filename (string): The filename or URL of the .torrent content.
            
            Returns:
            response (string): The information returned about the file or url by Tramsmission.
            """
            data = {}
            data["arguments"] = { 
                    "filename": filename,
                    "paused": True,
                    "download-dir": download_dir,
            }
            data["method"] = "torrent-add"
            response = self._post_request(json.dumps(data))
            return response.text

	def delete_torrents(self, t_ids, delete_local_data=False):
            """Removes a torrent from the torrent list on the Transmission client.

            Args:
            t_ids ([]int): An array of torrent ids.
            delete-local-data (bool): Indicates whether the file should be deleted locally.

            Exceptions:
            Throws an exception if there is an insufficient number of torrent ids to delete.

            Returns:
            isDeleted (bool): True if the removal was successful, false otherwise.
            """
            if len(t_ids) < 1:
                raise InvalidTransmissionQuery("invalid 'torrent-remove' query")
           
            data = {}
            data["arguments"] = { 
                    "ids": t_ids,
                    "delete-local-data": delete_local_data,
            }
            data["method"] = "torrent-remove"
            response = self._post_request(json.dumps(data))
            if json.loads(response.text)["result"] == "success":
                return True
            else:
                return False
	
