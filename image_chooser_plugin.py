import sys
#sys.path.append('C:/')
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

logger = logging.getLogger(__name__)

class Image_Chooser(Plugin):

    def __init__(self, g_pool, store_duration=1.,history_length=0.2, onset_confidence_threshold=0.5, offset_confidence_threshold=0.5):
        super().__init__(g_pool)
        self.store_duration = store_duration 
        self.queue = []
        self.history_length = history_length  # unit: seconds
        self.onset_confidence_threshold = onset_confidence_threshold
        self.offset_confidence_threshold = offset_confidence_threshold
        self.history = deque()
        self.i = 0
        self.posx = 0
        self.posy = 0

    def init_ui(self):
        def close():
            self.alive = False

        self.add_menu()
        self.menu.label = 'Image Chooser'
        help_str = "After you press start the main application window appears."
        self.menu.append(ui.Info_Text(help_str))
        self.menu.append(ui.Button('Start', Thread(target=startApp, name="startApp", args=[self]).start, outer_label='Start the main application'))

    def deinit_ui(self):
        self.remove_menu()
        
    def getblinkpos(self):
        return [self.posx, self.posy]

    def recent_events(self, events={}):
        # add new gaze positions
        self.queue.extend(events['gaze_positions'])
        #print(events['gaze_positions'])

        now = self.g_pool.get_timestamp()
        # remove outdated gaze positions
        for idx, gp in enumerate(self.queue):
            if gp['timestamp'] < now - self.store_duration:
                del self.queue[:idx]
        
        data = self.queue.pop()
        gaze_pos = data['norm_pos']
        x = gaze_pos[0]
        y = gaze_pos[1]
        
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
        
        if blinked:
            print("x: ")
            self.posx = x
            print(x)
            print("y: ")
            self.posy = y
            print(y)
            
            self.i = self.i + 1
            blinked = False