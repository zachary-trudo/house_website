import urllib.request
import os
import json

class SlackMessager(object):
  def __init__(self, channel, webhook=None):
    """ Simple script for messaging slack.

    Will send messages to slack. Pretty simple and efficient. No error handling as of yet.

    Args:
      channel (str) = The channel you want to post too.
      webhook (str) = The webhook for the slack integration.
    """
    self.channel = channel
    self.webhook = webhook if webhook else self._get_webhook()
  
  def send_message(self, message):
    """ Sends a message to the slack webhook and default channel.

    Args:
      message (str) = The message you'd like to send.

    Returns:
      bool: Indicates success or failure.
    """
    retVal = False
    header = {'Content-type': 'application/json'}
    message = {"text": message, "channel": self.channel}
    req = urllib.request.Request(self.webhook, data=bytearray(json.dumps(message), 'utf-8'), headers=header)
    try:
      urllib.request.urlopen(req)
      retVal = True
    except:
      pass
    return retVal

  def send_message_to_alt_channel(self, message, channel):
    """ Sends a message to a designated channel. No error handling as of yet.

    Args:
      message (str): The message you'd like to send.
      channel (str): The channel you'd like it sent to.

    Returns:
      bool: Indicates success or failure
    """
    retVal = False
    default_channel = self.channel
    self.channel = channel
    try:
      retVal = self.send_message(message)
    except:
      pass
    self.channel = default_channel
    return retVal

  def _get_webhook(self):
    webhook_path = os.path.join("/", "website_auth", "slack_webhook")
    webhook = ""
    with open(webhook_path, "r") as wh:
      webhook = wh.read()
    print(webhook) 
    return webhook


def main():
  sm = SlackMessager("torrent_status")
  sm.send_message("Testing Channel switching")
  sm.send_message_to_alt_channel("Yeah New Cch annel", "random")
  sm.send_message("Back to old channel")


if __name__ == "__main__":
  main()


