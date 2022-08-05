import sys

import pyaudio


class StreamReader:
    def __init__(self, device=None, rate=None):
        self.device = device
        self.rate = rate
        self.pa = pyaudio.PyAudio()

        self.info = self.pa.get_device_info_by_index(self.device)
        self.update_window_n_frames = None

    def check_devices(self):
        """
        Checks for openable devices for microphone input.
        :return: first valid devices
        """
        devices = []
        for device in range(self.pa.get_device_count()):
            if self.test_device(device):
                devices.append(device)

        if len(devices) == 0:
            print("No working microphone devices found!")
            sys.exit()

        print("Found %d working microphone device(s): " % len(devices))
        for device in devices:
            self.print_device_info(device)

        return devices[0]

    def test_device(self, device, rate=None):
        """
        Checks if a given device with rate is usable.
        :param device: device which is going to be tested
        :param rate: sample rate of device
        :return: validity of the device
        """
        try:
            self.info = self.pa.get_device_info_by_index(device)
            if not self.info["maxInputChannels"] > 0:
                return False

            if rate is None:
                rate = int(self.info["defaultSampleRate"])

            stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                input_device_index=device,
                frames_per_buffer=self.update_window_n_frames,
                rate=rate,
                input=True
            )
            stream.close()
            return True
        except Exception as e:
            print(e)
            return False

    def print_device_info(self, device):
        """
        Prints information about a given device.
        :param device:
        :return: None
        """
        device_info = self.pa.get_device_info_by_index(device)
        print('\nDevice %s:' % (str(device)))
        for key, value in sorted(device_info.items()):
            print("%s: %s" % (key, value))
