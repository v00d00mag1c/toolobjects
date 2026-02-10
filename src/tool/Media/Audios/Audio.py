from Media.Media import Media

class Audio(Media):
    mime_type = 'audio/mp3'
    default_name = 'audio.mp3'
    thumbnail_type = ['audio']
    extensions = ['mp3', 'aac']
