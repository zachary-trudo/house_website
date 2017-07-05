# Household Website

This is a toy project for creating an internal website for my household server.

I'd like for it to have the following capabilities:

- Download torrents
- Notify users of torrent completion - Probably through slack.
  - This will require user logins and user support. 
- Display torrent status on webpage
- Allow for download.
- Allow for network playback, either using HTML5 or VLC.
- Scan for viruses


## Technologies used

- Flask for web server
- Slack for notifications
- Transmission for torrent download
- HTML5 or VLC for video playing


## Download Torrents

A user should be able to do the following:
  - Upload a torrent file
  - Point to a website address for a torrent file
Either of these actions should result in the torrent server downloading the
torrent.

## Notify users of torrent completion.

A user should get a notification through slack that their torrent has compelted.
This will require individual user support, and most likely user log-in. 

## Display torrent status on webpage

If transmissions internal webpage is insufficient, create one for displaying
information.

## Allow for download.

Allow users to download torrented files to their local machine. 

## Allow for network playback.

Network playback is important for being able to play videos on the playstations
throughout the house, it is also an added feature for users to be able to keep
their computers from beign jam-packed with videos. 

## Scan for viruses. 

Every file should be scanned for viruses prior to being released for
consumption.  
