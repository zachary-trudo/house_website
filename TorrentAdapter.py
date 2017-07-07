class TorrentAdapter(object):
  def __init__(self):
    pass
  
  def start_download(self, filename):
    """ Will interface with Sheyla's code on starting download.

    Args:
      filename (str): filename of the torrent file that will need to be downloaded.

    Returns:
      bool: indicates success or failure
    """
    return True

  def check_download(self, filename):
    """ Will interface with Sheyla's code on checking downloads.

    Args:
      filename (str): filename of the torrent that will be checked.

    Returns:
      tuple (bool, float): bool checking if it exists, float of percent complete. 
    """
    return (True, 0.5)

  def delete_download(self, filename):
    """ Will interface with Sheyla's code on deleting downloads.

    Args:
      filename (str): filename of the torrent that will be checked.

    Returns:
      bool: bool indicates success or failure.
    """
    return True

