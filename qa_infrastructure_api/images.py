# import json
import falcon

import msgpack

class Resource(object):

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
