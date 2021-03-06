import re

from time import sleep
from pexpect import spawn as shell
from librescan.utils.camera import CameraDriver


class ChdkptpPT(CameraDriver):
    def __init__(self):
        self.cams = {}

    def detect(self, params):
        cameras = self.devices_list()
        for cam_info in cameras:
            self.connect(cam_info)

    def prepare(self, p_cam_config):
        zoom = p_cam_config.zoom
        self.rec_mode()
        self.set_quality()
        self.set_zoom(zoom)
        self.calibrate()

    def swap(self):
        cams = dict()
        cams['right'] = self.cams['left']
        cams['left'] = self.cams['right']
        self.cams = cams

    def set_zoom(self, p_zoom_level):
        zoom = p_zoom_level
        command = 'luar set_zoom({0})'.format(zoom)
        self._execute(command)

    def set_focus(self, p_focus_distance):
        self._execute('luar set_aflock(0)')
        self._cameras_wait()
        self._execute('luar set_focus({0})'.format(p_focus_distance))
        self._cameras_wait()
        self._execute('luar set_aflock(1)')

    def calibrate(self):
        if not self.cams:
            return -1
        self._execute('luar set_aflock(0)')
        sleep(0.25)
        self._execute("luar press('shoot_half')")
        sleep(1)
        self._execute("luar release('shoot_half')")
        sleep(0.5)
        self._execute("luar set_aflock(1)")
        return 1

    def devices_list(self):
        chdkptp = shell('chdkptp')
        chdkptp.sendline('list')
        chdkptp.expect("-1:.*", timeout=20)
        cams = chdkptp.after.decode()
        chdkptp.kill(0)
        return cams.split('\n')[:-1]

    def rec_mode(self):
        self._execute('rec')

    def shoot(self, p_save_path, p_pic_names):
        # remoteshoot /home/user/lsp00001 -tv=1/25 -sv=80
        cams = self.cams
        cams['right'].sendline('remoteshoot {0}{1} -tv=1/25 -sv={2}'.format(p_save_path, p_pic_names[0], str(80)))
        cams['left'].sendline('remoteshoot {0}{1} -tv=1/25 -sv={2}'.format(p_save_path, p_pic_names[1], str(80)))
        self._cameras_wait()

    def connect(self, p_orientation, p_cam_info):
        cam = shell('chdkptp')

        expression = r"(?P<bus>b=[0-9]+) (?P<dev>d=[0-9]+)"

        result = re.search(expression, p_cam_info)
        dev = result.group('dev')
        bus = result.group('bus')

        # Command connect to camera example: connect -b=001 -d=003
        cam.sendline('connect -{0} -{1}'.format(bus, dev))

        self.cams[p_orientation] = cam

    # Figure out why is affecting a2200
    # Make sure to have chdk full version running on the camera
    def set_quality(self):
        cams = self.cams
        command = ("luar props=require('propcase'); "
                   "set_prop(props.QUALITY, 0); "
                   "set_prop(props.RESOLUTION, 0); "
                   "set_nd_filter(2); "
                   "set_config_value(291, 0);")

        for cam in cams:
            cams[cam].sendline(command)
        self._cameras_wait()

    def _cameras_wait(self):
        cams = self.cams
        for cam in cams:
            cams[cam].expect('con .*> ', timeout=10)

    def _execute(self, command):
        cams = self.cams
        if not cams:
            raise Exception
        for cam in cams:
            cams[cam].sendline(command)
        self._cameras_wait()
