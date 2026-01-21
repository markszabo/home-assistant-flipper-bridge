import serial
import logging
import threading
import time

_LOGGER = logging.getLogger(__name__)


class FlipperSerialClient:
    def __init__(self, port: str, baudrate: int):
        self._port = port
        self._baudrate = baudrate
        self._lock = threading.Lock()
        self._ser = None

    def connect(self):
        if self._ser and self._ser.is_open:
            return

        _LOGGER.info("Opening Flipper serial connection on %s", self._port)
        self._ser = serial.Serial(
            self._port,
            self._baudrate,
            timeout=0.5,
        )
        time.sleep(0.2)  # Flipper needs a moment

    def close(self):
        if self._ser:
            self._ser.close()
            self._ser = None

    def send_command(self, command: str) -> str:
        with self._lock:
            self.connect()

            cmd = command.strip() + "\n"
            _LOGGER.debug("Sending CLI command: %s", cmd.strip())
            self._ser.write(cmd.encode())

            response_lines = []
            start = time.monotonic()

            while time.monotonic() - start < 1.5:
                line = self._ser.readline()
                if not line:
                    break
                decoded = line.decode(errors="ignore").rstrip()
                response_lines.append(decoded)

            response = "\n".join(response_lines)
            if response:
                _LOGGER.info("Flipper response:\n%s", response)

            return response
