#!/usr/bin/env python3
import time
import sys
from threading import Thread
from multiprocessing import Process


from gpiozero import Device, OutputDevice

# These two lines are for testing on system without GPIO pins
# These lines will need to be removed / commented out when moved to production
from gpiozero.pins.mock import MockFactory
Device.pin_factory = MockFactory()

# Define GPIO output pins
HORN_RELAY_PIN = 16
LED_PIN = 17

# Delay flag duration in minutes
DELAY = 1

# Define horn intervals in minutes
START_SIGNALS = [
    {"WARNING": 0},
    {"PREPERATORY": 1},
    {"ONE_MINUTE": 4},
    {"START": 5}
]

class Horn():
    """
    Horn class
    """

    def __init__(self) -> None:
        """
        Initialize a new Horn object
        """
        self.relay = OutputDevice(pin=HORN_RELAY_PIN)

    # Trigger the horn relay for a full second
    def blast(self) -> None:
        """
        Trigger relay to emit horn sound
        """
        self.relay.on()
        time.sleep(1)
        self.relay.off()

class Race():
    """
    Race class
    """

    def __init__(self, starts: int) -> None:
        """
        Initialize new Race object
        """
        self.horn = Horn()
        self.starts = starts
        self.start_time = None

    def _start_timer(self) -> None:
        """
        Set start time attribute to epoch
        """
        self.start_time = time.time()

    def run_race(self) -> None:
        """
        Conduct a race by initiating and executing start sequence(s)
        """
        # First set the start_time
        self._start_timer()
        Thread(target = self.horn.blast).start()
        #print(time.strftime('%'))
        # Set the start time of the most recent start
        # This is used to determine intervals for subsequent starts
        last_start = self.start_time + (DELAY*60)

        while True:
            if time.time() >= last_start:
                break

        # Iterate through number of starts run sequence
        for start in range(self.starts):
            # Sound horn at each interval defined by global var START_SIGNALS
            for signal in START_SIGNALS:
                # Get the interval from the dict item
                for _, interval in signal.items():
                    # If multiple starts, ignore warning signal as preceding start signal is same
                    # as proceding warning signal
                    if start > 0 and interval == 0:
                        break
                    while True:
                        if time.time() - last_start >= interval*60:
                            elapsed = time.time() - self.start_time
                            print(f'{int(elapsed) // 60:02}:{int(elapsed) % 60:02}')
                            Thread(target = self.horn.blast).start()
                            break

            last_start = time.time()

def display_time() -> None:
    """
    Function placeholder to display time
    """
    pass

def main() -> None:
    """
    Main logic
    """
    race = Race(2)

    race_process = Process(target = race.run_race())
    race_process.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
