
from werkzeug.wrappers import Response
from sample.beaker import Resource


class Post(Resource):

    def query(self):
        return Response('Hello query')

    def save(self):
        return Response('Hello save')

    def get(self, post_id):
        return Response(post_id)

    def update(self, post_id):
        return Response('Hello update')

    def delete(self, post_id):
        return Response('Hello delete')

class Tag(Post):

    def query(self, post_id):
        return Response("Hello PostTag query"+post_id)

    def save(self, post_id):
        return Response("Hello PostTag save"+post_id)

    def get(self, tag_id):
        return Response(tag_id)
