import mido
import logging
from ListenerThread import ListenerThread
from GameThread import GameThread


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    logging.info("Opening MIDI out connection...")
    outport = mido.open_output('Ableton Push 2 Live Port')
    logging.info("Done!")

    logging.info("Opening MIDI in connection...")
    inport = mido.open_input('Ableton Push 2 Live Port')
    logging.info("Done!")

    game_thread = GameThread(inport, outport)
    listener_thread = ListenerThread(inport, outport, game_thread)

    logging.info("Starting listener thread")
    listener_thread.start()
    logging.info("Starting game thread")
    game_thread.start()
