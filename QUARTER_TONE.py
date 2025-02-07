import pygame
import pygame.midi
import time
import numpy

sampleRate = 44100

pygame.midi.init()

pygame.mixer.init(44100, -16, 2, 512)

def list_devices():
    num_devices = pygame.midi.get_count()

    if num_devices < 2:
        print("Error, Less than 2 devices connected")
        return
    
    input_device_1 = pygame.midi.Input(0)
    input_device_2 = pygame.midi.Input(1)
    
    try:

        active_sounds = {}
        while True:
            if input_device_1.poll():
                midi_events_1 = input_device_1.read(10)
                for midi_event in midi_events_1:
                    status, note, velocity, _ = midi_event[0]

                    if status & 0xF0 == 0x90:
                        frequency = 440 * (2 ** ((note - 69) / 12))
                        print(frequency)
                        arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * frequency * x / sampleRate) for x in range(0, sampleRate)]).astype(numpy.int16)
                        arr2 = numpy.c_[arr, arr]
                        sound = pygame.sndarray.make_sound(arr2)
                        active_sounds[note] = sound.play(-1)
                    
                    elif status & 0xF0 == 0x80:
                        if note in active_sounds:
                            active_sounds[note].stop()
                            del active_sounds[note]

            if input_device_2.poll():
                midi_events_2 = input_device_2.read(10)
                for midi_event in midi_events_2:
                    status1, note1, velocity1, _ = midi_event[0]

                    if status1 & 0xF0 == 0x90:
                        frequency1 = (440 * (2 ** ((note1 - 69) / 12))) * (2**(50/1200))
                        print(frequency1)
                        arr3 = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * frequency1 * x / sampleRate) for x in range(0, sampleRate) ]).astype(numpy.int16)
                        arr4 = numpy.c_[arr3, arr3]
                        sound1 = pygame.sndarray.make_sound(arr4)
                        active_sounds[note1] = sound1.play(-1)

                    elif status1 & 0xF0 == 0x80:
                        if note1 in active_sounds:
                            active_sounds[note1].stop()
                            del active_sounds[note1]

    
    except KeyboardInterrupt:
        input_device_1.close()
        input_device_2.close()
        pygame.midi.quit()

list_devices()