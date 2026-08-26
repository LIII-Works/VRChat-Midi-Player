"""Simple MIDI-file player for piano-style VRChat OSC avatars."""

import json
import urllib.request
from pathlib import Path

import mido
from pythonosc.udp_client import SimpleUDPClient

OSC_HOST = "127.0.0.1"
OSC_PORT = 9000
OSCQUERY_URL = "http://127.0.0.1:9001/query?full"
NOTE_NAMES = ("C", "C+", "D", "D+", "E", "F", "F+", "G", "G+", "A", "A+", "B")


def midi_note_name(note):
    name = NOTE_NAMES[note % 12]
    octave = note // 12 - 1
    return f"{name[0]}{octave}{'+' if name.endswith('+') else ''}"


def discover_note_addresses(addresses):
    result = {}
    by_name = {midi_note_name(n): n for n in range(128)}
    for address in addresses:
        leaf = address.rsplit("/", 1)[-1]
        if leaf in by_name:
            result[by_name[leaf]] = address
    return result


def _flatten_addresses(value):
    found = []
    if isinstance(value, dict):
        if isinstance(value.get("FULL_PATH"), str):
            found.append(value["FULL_PATH"])
        if isinstance(value.get("CONTENTS"), dict):
            for child_name, child in value["CONTENTS"].items():
                found.extend(_flatten_addresses(child))
        for child in value.values():
            if isinstance(child, (dict, list)):
                found.extend(_flatten_addresses(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_flatten_addresses(child))
    return list(dict.fromkeys(found))


def discover_addresses():
    try:
        with urllib.request.urlopen(OSCQUERY_URL, timeout=1.5) as response:
            return discover_note_addresses(_flatten_addresses(json.load(response)))
    except Exception:
        return {}


def default_addresses():
    return {note: f"/PianoKeys/{midi_note_name(note)}" for note in range(21, 109)}


def play_file(path, midi_out):
    mid = mido.MidiFile(str(path))
    print(f"Playing: {path.name}  (Ctrl+C to stop)")
    for message in mid.play():
        if message.type in ("note_on", "note_off"):
            midi_out.send(message)


def midi_output_names():
    try:
        return mido.get_output_names()
    except ImportError as exc:
        raise RuntimeError(
            "MIDI backend is missing. Install dependencies with "
            "'python -m pip install -r requirements.txt'. "
            "If python-rtmidi has no wheel for your Python version, use Python 3.12."
        ) from exc


def main():
    print("VRChat MIDI to OSC player")
    print("Press Ctrl+C during playback to stop; Ctrl+C at the prompt to quit.")
    try:
        outputs = midi_output_names()
    except RuntimeError as exc:
        print(exc)
        return
    if not outputs:
        print("No MIDI output ports found. Install loopMIDI or LoopBe1, then run again.")
        return
    print("Available MIDI output ports:")
    for index, name in enumerate(outputs, 1):
        print(f"  {index}. {name}")
    while True:
        try:
            choice = input("Select MIDI output port (number): ").strip()
            midi_out = mido.open_output(outputs[int(choice) - 1])
            break
        except (ValueError, IndexError):
            print("Enter a valid port number.")
        except Exception as exc:
            print(f"Could not open MIDI port: {exc}")
    while True:
        try:
            raw = input("\nMIDI file path (blank to quit): ").strip().strip('"')
        except KeyboardInterrupt:
            print()
            return
        if not raw:
            return
        path = Path(raw)
        if path.suffix.lower() != ".mid" or not path.is_file():
            print("Please enter an existing .mid file.")
            continue
        try:
            play_file(path, midi_out)
        except KeyboardInterrupt:
            for note in range(128):
                midi_out.send(mido.Message("note_off", note=note, velocity=0))
            print("\nStopped.")
        except Exception as exc:
            print(f"Could not play file: {exc}")


if __name__ == "__main__":
    main()
