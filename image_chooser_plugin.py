from plugin import Plugin
from time import time, strftime, gmtime
from pyglui import ui
from audio import say
import logging
from zmq_tools import Msg_Receiver
from gui import start

logger = logging.getLogger(__name__)

class Image_Chooser(Plugin):

    def __init__(self, g_pool, example_param=1.0):
        super().__init__(g_pool)
        # persistent attribute
        self.example_param = example_param

    def init_ui(self):
        def close():
            self.alive = False

        self.add_menu()
        self.menu.label = 'Image Chooser'
        help_str = "After you press start the main application window appears."
        self.menu.append(ui.Info_Text(help_str))
        self.menu.append(ui.Button('Start', start, outer_label='Start the main application'))
        self.menu.append(ui.Button('Close', close, outer_label='Close the plugin'))

    def deinit_ui(self):
        self.remove_menu()