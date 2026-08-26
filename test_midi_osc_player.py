import unittest

from midi_osc_player import midi_note_name, discover_note_addresses


class MidiOscPlayerTests(unittest.TestCase):
    def test_midi_note_name_uses_standard_piano_names(self):
        self.assertEqual(midi_note_name(60), "C4")
        self.assertEqual(midi_note_name(61), "C4+")

    def test_discovery_maps_note_names_to_addresses(self):
        addresses = ["/PianoKeys/C4", "/PianoKeys/C4+", "/other/ignored"]
        mapping = discover_note_addresses(addresses)
        self.assertEqual(mapping[60], "/PianoKeys/C4")
        self.assertEqual(mapping[61], "/PianoKeys/C4+")


if __name__ == "__main__":
    unittest.main()
