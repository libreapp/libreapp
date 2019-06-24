import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options

LISTEN_PORT = 8000
LISTEN_ADDRESS = 'localhost'


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
    Handler that handles a websocket channel
    """
    @classmethod
    def urls(cls):
        return [
            (r'/api', cls, {}),  # Route/Handler/kwargs
        ]

    def initialize(self):
        self.channel = None

    def open(self):
        print('Channel open. ID of this handler: {}'.format(id(self)))

    def on_message(self, message):
        print('Message received:\n{}'.format(message))

    def on_close(self):
        print('Channel closed')

    def check_origin(self, origin: str):
        """Allow cross origin
        """
        if origin.startswith('http://localhost') or origin == 'https://libreapp.net':
            return True

        return False


def main():
    application = tornado.web.Application(WebSocketHandler.urls())
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(LISTEN_PORT, LISTEN_ADDRESS)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
