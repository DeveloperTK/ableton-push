import threading

from mido import Message


class ListenerThread(threading.Thread):

    def __init__(self, inport, outport, game_thread):
        threading.Thread.__init__(self)
        self.lastNote = 0
        self.inport = inport
        self.outport = outport
        self.game_thread = game_thread

    def run(self):
        while True:
            for msg in self.inport.iter_pending():
                self.handle_input(msg)
                print(msg)

    def handle_input(self, msg):
        if msg.type == 'control_change':
            self.handle_control(msg.channel, msg.control, msg.value, msg.time)
        elif msg.type == 'note_on':
            self.handle_note_on(msg.channel, msg.note, msg.velocity, msg.time)
        elif msg.type == 'note_off':
            self.handle_note_off(msg.channel, msg.note, msg.velocity, msg.time)
        elif msg.type == 'polytouch':
            self.handle_polytouch(msg.channel, msg.note, msg.velocity, msg.time)
        elif msg.type == 'aftertouch':
            self.handle_aftertouch(msg.channel, msg.value, msg.time)
        elif msg.type == 'pitchwheel':
            self.handle_pitchwheel(msg.channel, msg.pitch, msg.time)

    def handle_control(self, channel, control, value, time):
        if value > 0:
            self.game_thread.set_direction(control)
        else:
            pass
        pass

    def handle_note_on(self, channel, note, velocity, time):
        self.lastNote = note

    def handle_note_off(self, channel, note, velocity, time):
        pass

    def handle_polytouch(self, channel, note, velocity, time):
        pass

    def handle_aftertouch(self, channel, value, time):
        pass

    def handle_pitchwheel(self, channel, pitch, time):
        pass
