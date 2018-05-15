import sys
from plugin import Plugin
from time import time, strftime, gmtime
from pyglui import ui
from audio import say
import logging
from zmq_tools import Msg_Receiver
from MainWindow import*
from threading import Thread
import numpy as np
from collections import deque
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ChooserWindow import Ui_ChooserWindow
from PreviewWindow import Ui_PreviewWindow

logger = logging.getLogger(__name__)

class Image_Chooser(Plugin):
    """A plugin class that provides the main functionality"""
    def __init__(self, g_pool, store_duration=1.,history_length=0.2, onset_confidence_threshold=0.5, offset_confidence_threshold=0.5):
        """Initializes the plugin class"""
        super().__init__(g_pool)
        self.store_duration = store_duration    # time for which the gaze data will be stored 
        self.queue = []   # queue with gaze data
        self.history_length = history_length  # unit: seconds
        self.onset_confidence_threshold = onset_confidence_threshold    # threshold for confidence of onset blink
        self.offset_confidence_threshold = offset_confidence_threshold    # threshold for confidence of offset blink
        self.history = deque()    # history uf pupil
        self.mainWin = None   # object of main window

    def init_ui(self):
        """Initializes UI"""
        def close():
            """Exits the plugin, turns it of from the plugins list"""
            self.alive = False

        self.add_menu()
        self.menu.label = 'Image Chooser'
        help_str = "After you press start the main application window appears."
        self.menu.append(ui.Info_Text(help_str))
        self.menu.append(ui.Button('Start', self.startThread, outer_label='Start the main application'))
        self.menu.append(ui.Button('Close', close, outer_label='Closes the plugin'))

    def deinit_ui(self):
        """Deinitializes UI"""
        self.remove_menu()

    def recent_events(self, events={}):
        """Plugins function that runs without calling it, it stores recent gaze position
        and determines if the user blinked, parts were taken from pupils plugins"""
        if self.mainWin is None or not self.mainWin.isChooser():
            return
        
        # add new gaze positions
        self.queue.extend(events['gaze_positions'])
        #print(events['gaze_positions'])
        now = self.g_pool.get_timestamp()
        # remove outdated gaze positions
        for idx, gp in enumerate(self.queue):
            if gp['timestamp'] < now - self.store_duration:
                del self.queue[:idx]
        if len(self.queue) == 0:
            return
        data = self.queue.pop()
        gaze_pos = data['norm_pos']
        x = gaze_pos[0]
        y = gaze_pos[1]
        blinked = False
        
        self.history.extend(events.get('pupil_positions', []))

        try:  # use newest gaze point to determine age threshold
            age_threshold = self.history[-1]['timestamp'] - self.history_length
            while self.history[1]['timestamp'] < age_threshold:
                self.history.popleft()  # remove outdated gaze points
        except IndexError:
            pass

        filter_size = len(self.history)
        if filter_size < 2 or self.history[-1]['timestamp'] - self.history[0]['timestamp'] < self.history_length:
            return

        activity = np.fromiter((pp['confidence'] for pp in self.history), dtype=float)
        blink_filter = np.ones(filter_size) / filter_size
        blink_filter[filter_size // 2:] *= -1

        # The theoretical response maximum is +-0.5
        # Response of +-0.45 seems sufficient for a confidence of 1.
        filter_response = activity @ blink_filter / 0.45

        if -self.offset_confidence_threshold <= filter_response <= self.onset_confidence_threshold:
            return  # response cannot be classified as blink onset or offset
        elif filter_response > self.onset_confidence_threshold:
            blinked = True
        else:
            blinked = True

        confidence = min(abs(filter_response), 1.)  # clamp conf. value at 1.
        y = 1 - y   # because (0,0) is in the left bottom corner
        
        if (x < 0.7 and y < 0.7 and x >= 0.3 and y >= 0.3):
            self.calculateXY(x, y)
            
    def main(self, plugin):
        """Initializes PyQt application and starts the application"""
        app = QtWidgets.QApplication(sys.argv)
        self.mainWin = Ui_MainWindow(app, plugin)
        self.mainWin.show()        
        sys.exit(app.exec_()) 
        
    def startThread(self):
        """Starts the thread with the application"""
        if self.mainWin is None:
            t = Thread(target=self.main, args=[self])
            t.start()
            
    def setMainNone(self):
        """Sets main window object to type None"""
        self.mainWin = None
        
    def calculateXY(self, x, y):
        """Calculates which image should be highlighted and highlights it"""
        rows = self.mainWin.getChooser().getRows()
        cols = self.mainWin.getChooser().getCols()
        posx = ((x - 0.3)/(0.7-0.3))/(1/rows)
        posy = ((y - 0.3)/(0.7-0.3))/(1/cols)
        print("Pred")
        print(posx)
        print(posy)
        posx = int(posx)
        posy = int(posy)
        self.mainWin.getChooser().highlight(posx, posy)   # highlights image user is looking at
        