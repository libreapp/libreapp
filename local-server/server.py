from __future__ import annotations

from pathlib import Path
from typing import Union, Set
import asyncio

import watchdog.observers
import watchdog.events

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options
import tornado.gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())


LISTEN_PORT = 29285
LISTEN_ADDRESS = '127.0.0.1'

DATA_DIR = Path.home().joinpath('LibreApp')
DATA_DIR.mkdir(exist_ok=True)

CreatedEvent = Union[watchdog.events.FileCreatedEvent,
                     watchdog.events.DirCreatedEvent]


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """Websocket channel
    """
    open_sockets: Set[WebSocketHandler] = set()  # noqa pylint: disable=undefined-variable

    @classmethod
    def urls(cls):
        return [
            (r'/api', cls, {}),  # Route/Handler/kwargs
        ]

    def initialize(self):
        self.channel = None
        # self.subscription = outbound_message.subscribe(self.write_message)

    def open(self):
        print('Channel open. ID of this handler is: {}'.format(id(self)))
        type(self).open_sockets.add(self)

    def on_message(self, message):
        print('Message received:\n{}'.format(message))

    def on_close(self):
        print('Channel closed. ID of this handler was: {}'.format(id(self)))
        type(self).open_sockets.remove(self)
        # self.subscription.dispose()

    def check_origin(self, origin: str):
        """Allow cross origin
        """
        if (
                origin == 'http://localhost:3000' or
                origin == 'https://localhost:3000' or
                origin == 'https://libreapp.net'):
            return True

        return False


class FileSystemEventHandler(watchdog.events.FileSystemEventHandler):
    """Handles files system events
    """

    def on_created(self, event: CreatedEvent):
        with open(event.src_path, 'rb') as a_file:
            data = a_file.read()

        for socket in WebSocketHandler.open_sockets:
            socket.write_message(data, binary=True)


def main():
    urls = [
        (r'/api', WebSocketHandler, {})
    ]

    application = tornado.web.Application(urls)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(LISTEN_PORT, LISTEN_ADDRESS)

    file_system_event_handler = FileSystemEventHandler()
    observer = watchdog.observers.Observer()
    observer.schedule(file_system_event_handler, str(DATA_DIR), recursive=True)
    observer.start()

    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == '__main__':
    main()
