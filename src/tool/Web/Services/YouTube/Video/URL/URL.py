from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Operations.Create.CreationItem import CreationItem

class URL(Object):
    embed: str = Field(default = 'https://www.youtube.com/embed/{0}?')
    base_url: str = Field(default = 'https://youtube.com/watch?v=')

    video_id: str = Field(default = None)
    playlist_id: str = Field(default = None)

    autoplay: bool = Field(default = False)
    mute: bool = Field(default = False)
    loop: bool = Field(default = False)
    controls: bool = Field(default = True)
    timecode: int | float = Field(default = None)
    si: str = Field(default = None)

    def set_url(self, url):
        if url.netloc == 'youtu.be':
            self.base_url = url.scheme + '://' + url.netloc
            self.video_id = url.path[1:]
        else:
            self.base_url = url.scheme + '://' + url.netloc + url.path

        for val in url.query.split('&'):
            keys = val.split('=')
            if keys[0] == 'v':
                self.video_id = keys[1]

            if keys[0] == 't':
                self.timecode = int(keys[1])

            if keys[0] == 'playlist_id':
                self.playlist_id = int(keys[1])

            if keys[0] == 'si':
                self.si = str(keys[1])

    def get_url(self):
        _url = self.base_url + '?v=' + self.video_id
        if self.timecode != None:
            _url += '&t=' + self.timecode

        return _url

    def get_embed_url(self):
        url = self.embed.format(self.video_id)
        # ???
        if self.playlist_id:
            url += '&playlist=' + self.playlist_id 
        if self.autoplay:
            url += '&autoplay=1'
        if self.mute:
            url += '&mute=1'
        if self.loop:
            url += '&loop=1'
        if self.controls == False:
            url += '&controls=0'
        if self.timecode:
            url += '&t=' + str(self.timecode)

        return url

    def get_width(self) -> float:
        if self.obj.width:
            return self.obj.width

        if self.local_obj.width:
            return self.local_obj.width

        return 500

    def get_height(self) -> float:
        if self.obj.height:
            return self.obj.height

        if self.local_obj.height:
            return self.local_obj.height

        return 300

    @classmethod
    def _creations(cls) -> list:
        return [
            CreationItem(
                name = 'YouTube URL',
                object_name = 'Web.Services.YouTube.Video.URL.URL',
                create = 'Web.Services.YouTube.Video.URL.Get',
            )
        ]
