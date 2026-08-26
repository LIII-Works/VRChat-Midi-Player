# VRChat MIDI Player

Command-line MIDI-file player for VRChat worlds using native `VRC Midi Listener` input.

## Setup

1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) or LoopBe1.
3. Open loopMIDI, create a port named `VRChat MIDI`, and leave it running.
4. In Steam, open **VRChat → Properties → Launch Options** and add:

```text
--midi="VRChat MIDI"
```

5. Start VRChat and enter a world that contains a `VRC Midi Listener`.
6. Install this program's Python dependencies:

```powershell
py -m pip install -r requirements.txt
py midi_osc_player.py
```

For an easier start, double-click **Start VRChat MIDI Player.cmd**. It installs the requirements automatically and starts the player.

When prompted, choose the `VRChat MIDI` output port and enter a `.mid` file path.

Press Ctrl+C to stop the current song and return to the prompt. Leave the prompt blank (or press Ctrl+C there) to quit.

## Notes

This sends MIDI events, not audio or OSC packets. The VRChat world must be built to receive MIDI and connect its `MidiNoteOn`/`MidiNoteOff` events to visible behavior.
