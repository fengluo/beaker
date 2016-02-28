
from werkzeug.wrappers import Response
from sample.beaker import Resource


class Post(Resource):

    __resource__ = 'post'

    def index(self):
        return self.resp.json({'data': 'Hello index'})

    def create(self):
        return Response('Hello save')

    def show(self, post_id):
        return Response(post_id)

    def update(self, post_id):
        return Response('Hello update')

    def destroy(self, post_id):
        return Response('Hello delete')

class Tag(Post):

    def index(self, post_id):
        return Response("Hello PostTag query"+post_id)

    def create(self, post_id):
        return Response("Hello PostTag save"+post_id)

    def show(self, tag_id):
        return Response(tag_id)
