__author__ = 'ayelet'

from threading import Lock


class MRSW:

    def __init__(self):
        self.lock_reader = Lock()
        self.lock_writer = Lock()
        self.readers = 0

    def read_acquire(self):
        self.lock_reader.acquire()
        if self.readers == 0:
            self.lock_writer.acquire()
        self.readers += 1
        self.lock_reader.release()

    def read_release(self):
        self.lock_reader.acquire()
        if self.readers == 1:
            self.lock_writer.release()
        self.readers -= 1
        self.lock_reader.release()

    def write_acquire(self):
        self.lock_writer.acquire()

    def write_release(self):
        self.lock_writer.release()