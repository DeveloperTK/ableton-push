import math
import queue
import time

from mido import Message
import threading


class GameThread(threading.Thread):
    BUTTON_OFFSET = 36

    pos_x = 0
    pos_y = 0

    def __init__(self, inport, outport):
        threading.Thread.__init__(self)
        self.inport = inport
        self.outport = outport
        self.parts = []
        self.parts.append((0, 0))
        self.max_len = 12
        self.key = 0

    def run(self):
        # Initialize the arrow-keys
        for i in [44, 46, 45, 47]:
            message = Message('control_change', channel=0, value=63, control=i, time=0)
            self.outport.send(message)
            print(str(i) + " on")

        self.clear()

        # Just display the dot
        while True:
            self.display()
            time.sleep(0.2)
            self.move_head(self.key)

    def display(self):
        self.clear()
        for i in range(0, len(self.parts)):
            color = 127
            if i == len(self.parts) - 1:
                color = 126
            self.outport.send(
                Message(type="note_on", channel=0, note=GameThread.xy_to_button(self.parts[i][0], self.parts[i][1]),
                        velocity=color, time=0))

    def clear(self):
        for i in range(36, 100):
            if not GameThread.button_to_xy(i) in self.parts:
                self.outport.send(
                    Message(type="note_on", channel=0, note=i,
                            velocity=33, time=0))
                # self.outport.send(Message(type="note_off", channel=0, note=i,
                #                          velocity=0, time=0))

    def set_direction(self, key):
        self.key = key

    def move_head(self, key):
        pos_x = self.parts[len(self.parts) - 1][0]
        pos_y = self.parts[len(self.parts) - 1][1]

        if key == 45:
            pos_x += 1
        elif key == 44:
            pos_x += -1
        elif key == 46:
            pos_y += 1
        elif key == 47:
            pos_y -= 1
        else:
            print("Unknown movement!")
            return
        pos_x %= 8
        pos_y %= 8

        if len(self.parts) + 1 > self.max_len:
            self.parts.pop(0)

        if (pos_x, pos_y) in self.parts:
            print("Game over lmao")
            quit(0)

        self.parts.append((pos_x, pos_y))

    @staticmethod
    def xy_to_button(x, y) -> int:
        return x + 8 * y + GameThread.BUTTON_OFFSET

    @staticmethod
    def button_to_xy(button):
        button = button - GameThread.BUTTON_OFFSET
        x = button % 8
        y = math.floor(button / 8)
        return x, y
