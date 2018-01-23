# import json
import io
import mimetypes
import uuid

import falcon
import msgpack
import os


class Resource(object):
    _CHUNK_SIZE_BYTES = 4096

    # The resource object must now be initialised with a path used during POST
    def __init__(self, storage_path):
        self._storage_path = storage_path

    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        # Create a JSON representation of the resource
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK

        # resp.body = json.dumps(doc, ensure_ascii=False)

        # The following can be omitted since 200 is the default status returned by the framework, but it is included
        # here to illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        ext = mimetypes.guess_extension(req.content_type)
        name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=ext)
        image_path = os.path.join(self._storage_path, name)

        with io.open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name
