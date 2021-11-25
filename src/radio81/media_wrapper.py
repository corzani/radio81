from asyncio import sleep

from vlc import Meta, Media


class MediaWrapper:
    media: Media = None

    def get_media(self) -> Media:
        return self.media

    def set_media(self, media: Media):
        self.media = media


# This simulate the VLC real behaviour...
# This is awful :(
async def media_meta_changed(media_wrapper, callback_fn):
    while True:
        if media_wrapper.get_media() is not None:
            media = media_wrapper.get_media()
            title = media.get_meta(Meta.NowPlaying)
            callback_fn(title)
        sleep(2)

