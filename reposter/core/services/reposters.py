import os
from instagrapi import Client


def instagram_repost(source_object):
    """ATTENTION. I recommend using official instagram graph API on the real projects"""
    try:
        client = Client()
        client.login(os.environ.get('INSTAGRAM_USERNAME'), os.environ.get('INSTAGRAM_PASSWORD'))
        client.album_upload(
            paths=[image.image.path for image in source_object.image_set.all()],
            caption=f'{source_object.name} - {source_object.description} | {source_object.price}$.\n'
                    f'Scan QR code for redirect to our website, more photos and information about the current ad'
        )
        client.logout()
        return True
    except Exception as e:
        print(e)
        return False
