import pygame
import pygame.midi
import numpy
import tkinter as tk

sampleRate = 44100

pygame.mixer.init(44100, -16, 2, 512)

# Define tuning ratios for other popular tunings
TUNINGS = {
    "12TET": lambda note: 440 * (2 ** ((note - 69) / 12)),
    "European": lambda note: 440 * (2 ** ((note - 69) / 12)) * (1.0125) ** (note - 69),
    # Add more tunings as desired
}

def list_devices():
    pygame.midi.init()
    num = pygame.midi.get_count()
    devices = []
    for i in range(num):
        names = pygame.midi.get_device_info(i)
        devices.append(names[1].decode() if names[1] else f'Unknown Device {i}')
    pygame.midi.quit()
    return devices

def key_pressed(device_id, tuning_function):
    pygame.init()
    pygame.midi.init()

    try:
        midi_input = pygame.midi.Input(device_id)
        active_sounds = {}  # Dictionary to store active sounds

        while True:
            if midi_input.poll():
                midi_events = midi_input.read(10)
                for midi_event in midi_events:
                    status, note, velocity, _ = midi_event[0]

                    if status & 0xF0 == 0x90:  # Note On event
                        frequency = tuning_function(note)
                        print(f"Note {note} pressed. Frequency: {frequency:.2f} Hz")
                        print(f"Velocity = {velocity}")
                        arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * frequency * x / sampleRate) for x in range(0, sampleRate)]).astype(numpy.int16)
                        arr2 = numpy.c_[arr, arr]
                        sound = pygame.sndarray.make_sound(arr2)
                        active_sounds[note] = sound.play(-1)  # Play continuously
                    elif status & 0xF0 == 0x80:  # Note Off event
                        print(f"Note {note} released.")
                        if note in active_sounds:
                            active_sounds[note].stop()  # Stop the sound
                            del active_sounds[note]  # Remove from active sounds

    except KeyboardInterrupt:
        print("bye")

    finally:
        pygame.midi.quit()
        pygame.quit()

def start_app(device_id, tuning_function):
    key_pressed(device_id, tuning_function)

def main():
    root = tk.Tk()
    root.title("MIDI Synthesizer")

    device_label = tk.Label(root, text="Select MIDI Device:")
    device_label.pack()

    devices = list_devices()
    device_var = tk.StringVar(root)
    device_var.set(devices[0])
    device_option = tk.OptionMenu(root, device_var, *devices)
    device_option.pack()

    tuning_label = tk.Label(root, text="Select Tuning:")
    tuning_label.pack()

    tuning_var = tk.StringVar(root)
    tuning_var.set("12TET")  # Default tuning
    tuning_option = tk.OptionMenu(root, tuning_var, *TUNINGS.keys())
    tuning_option.pack()

    start_button = tk.Button(root, text="Start", command=lambda: start_app(devices.index(device_var.get()), TUNINGS[tuning_var.get()]))
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
