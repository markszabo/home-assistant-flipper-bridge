import serial
import logging
import threading
import time
import re

_LOGGER = logging.getLogger(__name__)

ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

# Remove color codes from the CLI output
def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)

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
            baudrate=115200,
            timeout=0.5,
            write_timeout=1,
        )

        # === Flipper CLI wake-up sequence ===
        time.sleep(0.5)

        # Clear any startup noise
        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

        _LOGGER.debug("Flipper CLI initialization sequence complete")


    def close(self):
        if self._ser:
            self._ser.close()
            self._ser = None

    def send_command(self, command: str) -> str:
        with self._lock:
            self.connect()

            # Clear any old data
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()

            cmd = command.strip() + "\r\n"
            _LOGGER.debug("Sending CLI command: %s", cmd.strip())
            self._ser.write(cmd.encode())
            self._ser.flush()

            response_lines = []
            start = time.monotonic()
            got_anything = False

            # Wait up to 3 seconds total
            while time.monotonic() - start < 3.0:
                if self._ser.in_waiting > 0:
                    line = self._ser.readline()
                    if line:
                        got_anything = True
                        decoded = line.decode(errors="ignore").rstrip()
                        response_lines.append(decoded)
                        continue

                # If we already got some data, allow a short grace period
                if got_anything:
                    time.sleep(0.1)
                else:
                    time.sleep(0.2)

            response = "\n".join(response_lines)
            response = strip_ansi(response)
            response = response.replace("\r\n", "\n")

            if not response:
                _LOGGER.warning(
                    "No response received from Flipper for command: %s",
                    command,
                )
            else:
                _LOGGER.info("Flipper response:\n%s", response)

            return response

