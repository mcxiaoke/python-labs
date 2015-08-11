#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 12:00:11

from __future__ import print_function
import thread
import threading
import time
import Queue as queue

dataQueue = queue.Queue()


def producer(id):
    for i in range(5):
        print('put')
        time.sleep(0.1)
        dataQueue.put('[producer id=%d, count=%d]' % (id, i))


def consumer(root):
    try:
        # print('get')
        data = dataQueue.get(block=False)

    except queue.Empty:
        pass
    else:
        root.insert('end', 'consumer got => %s\n' % str(data))
        root.see('end')
    root.after(500, lambda: consumer(root))


def makethreads():
    print('make threads')
    for i in range(4):
        thread.start_new_thread(producer, (i,))


from Tkinter import Tk, Button
from lib import ScrolledText

# 线程与界面更新


def _test_queue():
    root = Tk()
    Button(root, text='Make Threads', command=makethreads).pack()
    st = ScrolledText(root)
    st.pack()
    consumer(st)
    root.mainloop()


class ThreadGui(ScrolledText):
    threadPerClick = 4

    def __init__(self, parent=None):
        ScrolledText.__init__(self, parent)
        self.pack()
        self.dataQueue = queue.Queue()
        self.bind('<Button-1>', self.makethreads)
        self.consumer()

    def producer(self, id):
        for i in range(10):
            time.sleep(0.5)
            self.dataQueue.put('[producer id=%d, count=%d]' % (id, i))

    def consumer(self):
        try:
            data = self.dataQueue.get(block=False)
            print('new data: %s' % data)
        except queue.Empty:
            pass
        else:
            self.insert('end', 'consumer got => %s\n' % str(data))
            self.see('end')
        self.after(100, self.consumer)

    def makethreads(self, event):
        for i in range(self.threadPerClick):
            threading.Thread(target=self.producer, args=(i,)).start()


if __name__ == '__main__':
    #_test_queue()
    ThreadGui().mainloop()
