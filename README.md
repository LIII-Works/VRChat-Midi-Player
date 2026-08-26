# VRChat MIDI → OSC player

Requires Python 3.10+:

```powershell
py -m pip install -r requirements.txt
py midi_osc_player.py
```

Install and run a virtual MIDI port such as [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) or LoopBe1. In VRChat, enter a world using `VRC Midi Listener`, then select the same virtual port if the world supports device selection. The player sends the MIDI file's note-on and note-off events directly to that port.

Enter a `.mid` path when prompted. Press Ctrl+C to stop the current song and return to the prompt; leave the prompt blank (or press Ctrl+C there) to quit.
