import os
import time
import rospy

from FlightLib import FlightLib
from FlightLib import LedLib

import client
import messaging_lib as messaging
import play_animation

def

class CopterClient(client.Client):
    def load_config(self):
        super(CopterClient, self).load_config()
        self.FRAME_ID = self.config.get('COPTERS', 'frame_id')  # TODO in play_animation
        self.TAKEOFF_HEIGHT = self.config.getfloat('COPTERS', 'takeoff_height')
        self.TAKEOFF_TIME = self.config.getfloat('COPTERS', 'takeoff_time')
        self.RFP_TIME = self.config.getfloat('COPTERS', 'reach_first_point_time')
        self.SAFE_TAKEOFF = self.config.getboolean('COPTERS', 'safe_takeoff')

        self.X0_COMMON = self.config.getfloat('COPTERS', 'x0_common')
        self.Y0_COMMON = self.config.getfloat('COPTERS', 'y0_common')
        self.X0 = self.config.getfloat('PRIVATE', 'x0')
        self.Y0 = self.config.getfloat('PRIVATE', 'y0')

        self.USE_LEDS = self.config.getboolean('PRIVATE', 'use_leds')
        play_animation.USE_LEDS = self.USE_LEDS

    def start(self):
        super(CopterClient, self).start()
        rospy.init_node('Swarm_client', anonymous=True)
        if self.USE_LEDS:
            LedLib.init_led()


@messaging.request_callback("selfcheck")
def _response_selfcheck():
    return FlightLib.selfcheck()

@messaging.request_callback("batt_voltage")
def _response_batt():
    return FlightLib.get_telemetry('body').voltage

@messaging.request_callback("cell_voltage")
def _response_cell():
    return FlightLib.get_telemetry('body').cell_voltage

@messaging.message_callback("service_restart")
def _message_service_restart(*args, **kwargs):
    os.system("systemctl restart"+kwargs["name"])

@messaging.message_callback("led_test")
def _command_config_write(*args, **kwargs):
    LedLib.chase(255, 255, 255)
    time.sleep(2)
    LedLib.off()



if __name__ == "__main__":
    copter_client = CopterClient()
    copter_client.start()
