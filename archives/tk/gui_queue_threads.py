#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 12:48:35
from __future__ import print_function

# cross threads queue
import Queue as queue
import sys

threadQueue = queue.Queue(maxsize=0)

# in main thread


def threadChecker(widget, delayMillis=100, perEvent=1):
    for i in range(perEvent):
        try:
            tmp = threadQueue.get(block=False)
            print(tmp)
            (callback, args) = tmp
        except queue.Empty:
            break
        else:
            callback(*args)
    widget.after(
        delayMillis, lambda: threadChecker(widget, delayMillis, perEvent))

import thread
# in new thread


def threaded(action, args, context, onExit, onFail, onProgress):
    try:
        if not onProgress:
            action(*args)
        else:
            def progress(*any):
                threadQueue.put((onProgress, any+context))
            action(progress=progress, *args)
    except:
        threadQueue.put((onFail, (sys.exc_info(),)+context))
    else:
        threadQueue.put((onExit, context))


def startThread(action, args, context, onExit, onFail, onProgress=None):
    thread.start_new_thread(
        threaded, (action, args, context, onExit, onFail, onProgress))

# thread-safe counter or flag


class ThreadCounter:

    def __init__(self):
        self.count = 0
        self.mutex = thread.allocate_lock()

    def incr(self):
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()

    def decr(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()

    def __len__(self):
        return self.count


def _test():
    import time
    from lib import ScrolledText

    def onEvent(i):
        myname = 'thread-%s' % i
        startThread(action=threadaction,
                    args=(i, 3),
                    context=(myname,),
                    onExit=threadexit,
                    onFail=threadfail,
                    onProgress=threadprogress)

    def threadaction(id, reps, progress):
        for i in range(reps):
            time.sleep(1)
            if progress:
                progress(i)
        if id % 2 == 1:
            raise Exception

    def threadexit(myname):
        text.insert('end', '%s\texit\n' % myname)
        text.see('end')

    def threadfail(exc_info, myname):
        text.insert('end', '%s\tfail\t%s\n' % (myname, exc_info[0]))
        text.see('end')

    def threadprogress(count, myname):
        text.insert('end', '%s\tprogress:\t%s\n' % (myname, count))
        text.see('end')
        text.update()

    text = ScrolledText()
    threadChecker(text)
    text.bind('<Button-1>', lambda event: list(map(onEvent, range(6))))
    text.mainloop()


if __name__ == '__main__':
    _test()
