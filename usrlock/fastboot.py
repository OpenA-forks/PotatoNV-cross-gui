from time import sleep
import traceback
from . import ui
from fastbootpy import FastbootDevice, FastbootManager

def handle_exception(e: Exception, message: str):
    ui.error(message)
    traceback.print_exc()
    exit(1)


class Fastboot:
    def connect(self):
        ui.info("Waiting for fastboot device")
        while True:
            devices = FastbootManager.devices()
            if len(devices) == 1:
                for attempt in range(10):
                    try:
                        self.fb_dev = FastbootDevice.connect(devices[0])
                        ui.info(f"Connected to device {devices[0]}")
                        return
                    except Exception as e:
                        if attempt < 9:
                            ui.info(f"USB busy, retrying in 2s... ({attempt+1}/10)")
                            sleep(2)
                        else:
                            raise
                break
            elif len(devices) > 1:
                ui.error("More than one fastboot device is connected!")

    def write_nvme(self, prop: str, data: bytes):
        cmd = f"getvar:nve:{prop}@".encode('UTF-8')
        cmd += data
        ui.debug(f"Sending command: {cmd}")
        ui.info(f"Writing {prop}")
        for attempt in range(10):
            try:
                result = self.fb_dev.send(cmd)
                if not "set nv ok" in result:
                    ui.error(f"Failed to write {prop}: {result}", critical=True)
                return
            except Exception as e:
                if attempt < 9:
                    ui.info(f"USB busy on write, retrying in 2s... ({attempt+1}/10)")
                    sleep(2)
                    # Reconnect
                    try:
                        devices = FastbootManager.devices()
                        if devices:
                            self.fb_dev = FastbootDevice.connect(devices[0])
                    except:
                        pass
                else:
                    raise

    def erase(self, partition: str):
        cmd = f"erase:{partition}".encode('UTF-8')
        ui.info(f"Erasing {partition}")
        for attempt in range(10):
            try:
                result = self.fb_dev.send(cmd)
                ui.success(f"Erased {partition}: {result}")
                return True
            except Exception as e:
                if attempt < 9:
                    ui.info(f"USB busy on erase, retrying in 2s... ({attempt+1}/10)")
                    sleep(2)
                    try:
                        devices = FastbootManager.devices()
                        if devices:
                            self.fb_dev = FastbootDevice.connect(devices[0])
                    except:
                        pass
                else:
                    ui.error(f"Failed to erase {partition}: {e}")
                    return False

    def oem_unlock(self, key: str):
        cmd = f"oem unlock {key}".encode('UTF-8')
        ui.info(f"Sending OEM unlock")
        for attempt in range(10):
            try:
                result = self.fb_dev.send(cmd)
                ui.success(f"OEM unlock result: {result}")
                return True
            except Exception as e:
                if attempt < 9:
                    ui.info(f"USB busy on unlock, retrying in 2s... ({attempt+1}/10)")
                    sleep(2)
                    try:
                        devices = FastbootManager.devices()
                        if devices:
                            self.fb_dev = FastbootDevice.connect(devices[0])
                    except:
                        pass
                else:
                    ui.error(f"Failed to unlock: {e}")
                    return False

    def reboot(self):
        result = self.fb_dev.reboot()
        ui.info(f"Reboot result: {result}")
    
    def reboot_bootloader(self):
        result = self.fb_dev.reboot_bootloader()
        ui.info(f"Reboot bootloader result: {result}")
    
