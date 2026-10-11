#!/usr/bin/env python3
"""
Music Theory Master - Interactive Learning Application
=======================================================
A comprehensive PySide6 application for learning Western, Eastern, and World music theory.

Features:
- Interactive Piano Keyboard with note highlighting
- Scale Explorer (Western, Eastern, World scales)
- Chord Encyclopedia with voicings
- Circle of Fifths interactive diagram
- Interval Calculator and visualizer
- Ear Training mini-games
- Key Signature quiz
- Fretboard visualizer (guitar)
- Note naming and identification exercises

Requirements: PySide6
Install: pip install PySide6

Run: python music_theory_master.py
"""

import sys
import math
import random
from typing import List, Optional, Tuple

try:
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
except ImportError:
    try:
        from PyQt6.QtWidgets import *
        from PyQt6.QtCore import *
        from PyQt6.QtGui import *
    except ImportError:
        print("ERROR: Please install PySide6: pip install PySide6")
        sys.exit(1)

# =============================================================================
# MUSIC THEORY DATA
# =============================================================================

NOTE_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
NOTE_NAMES_ALL = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

OCTAVE_NOTES = 12

# Interval names (semitones -> name)
INTERVALS = {
    0: ('Perfect Unison', 'P1'),
    1: ('Minor Second', 'm2'),
    2: ('Major Second', 'M2'),
    3: ('Minor Third', 'm3'),
    4: ('Major Third', 'M3'),
    5: ('Perfect Fourth', 'P4'),
    6: ('Tritone / Augmented Fourth', 'TT/A4'),
    7: ('Perfect Fifth', 'P5'),
    8: ('Minor Sixth', 'm6'),
    9: ('Major Sixth', 'M6'),
    10: ('Minor Seventh', 'm7'),
    11: ('Major Seventh', 'M7'),
    12: ('Perfect Octave', 'P8'),
    13: ('Minor Ninth', 'm9'),
    14: ('Major Ninth', 'M9'),
    15: ('Minor Tenth', 'm10'),
    16: ('Major Tenth', 'M10'),
    17: ('Perfect Eleventh', 'P11'),
    18: ('Augmented Eleventh', 'A11'),
    19: ('Perfect Twelfth', 'P12'),
    20: ('Minor Thirteenth', 'm13'),
    21: ('Major Thirteenth', 'M13'),
}

# Scale definitions: (name, intervals, description, category)
WESTERN_SCALES = [
    ('Major (Ionian)', [0, 2, 4, 5, 7, 9, 11], 'The foundation of Western music. Bright, happy, stable.', 'Western'),
    ('Natural Minor (Aeolian)', [0, 2, 3, 5, 7, 8, 10], 'Sad, serious, introspective. Relative minor of Major.', 'Western'),
    ('Harmonic Minor', [0, 2, 3, 5, 7, 8, 11], 'Exotic, dramatic. Raised 7th creates leading tone.', 'Western'),
    ('Melodic Minor (asc)', [0, 2, 3, 5, 7, 9, 11], 'Jazz staple. Raised 6th and 7th ascending.', 'Western'),
    ('Dorian', [0, 2, 3, 5, 7, 9, 10], 'Minor with raised 6th. Jazzy, sophisticated, Celtic feel.', 'Western (Mode)'),
    ('Phrygian', [0, 1, 3, 5, 7, 8, 10], 'Spanish/flamenco flavor. Minor with lowered 2nd.', 'Western (Mode)'),
    ('Lydian', [0, 2, 4, 6, 7, 9, 11], 'Dreamy, floating. Major with raised 4th (sharp 11).', 'Western (Mode)'),
    ('Mixolydian', [0, 2, 4, 5, 7, 9, 10], 'Bluesy, rock. Major with lowered 7th.', 'Western (Mode)'),
    ('Locrian', [0, 1, 3, 5, 6, 8, 10], 'Dark, unstable. Diminished feel. Rarely used as tonic.', 'Western (Mode)'),
    ('Pentatonic Major', [0, 2, 4, 7, 9], 'Five notes. Universal, folk, pop, rock. No half steps.', 'Western/World'),
    ('Pentatonic Minor', [0, 3, 5, 7, 10], 'Blues, rock, Eastern influence. Most versatile scale.', 'Western/World'),
    ('Blues Scale', [0, 3, 5, 6, 7, 10], 'The "blue note" (b5) gives it soul. Essential for blues/jazz.', 'Western'),
    ('Chromatic', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'All 12 notes. Used for color and tension.', 'Western'),
    ('Whole Tone', [0, 2, 4, 6, 8, 10], 'Dreamy, ambiguous. All whole steps. Used in impressionism.', 'Western'),
    ('Diminished (H-W)', [0, 1, 3, 4, 6, 7, 9, 10], 'Tension, jazz. Alternating half and whole steps.', 'Western'),
    ('Augmented', [0, 3, 4, 7, 8, 11], 'Mysterious, symmetrical. Two augmented triads.', 'Western'),
    ('Bebop Dominant', [0, 2, 4, 5, 7, 9, 10, 11], 'Jazz scale. Adds major 7th to Mixolydian for chromatic passing.', 'Western (Jazz)'),
    ('Bebop Major', [0, 2, 4, 5, 7, 8, 9, 11], 'Jazz scale. Adds b6 to Major for chromatic passing.', 'Western (Jazz)'),
    ('Altered Scale', [0, 1, 3, 4, 6, 8, 10], 'Super Locrian. All altered tensions. Modern jazz.', 'Western (Jazz)'),
]

EASTERN_SCALES = [
    ('Raga Yaman (Kalyan)', [0, 2, 4, 6, 7, 9, 11], 'Evening raga. Similar to Lydian mode. Devotional, serene.', 'Indian Classical'),
    ('Raga Bhairav', [0, 1, 4, 5, 7, 8, 11], 'Morning raga. Komal re and teevra ma. Serious, profound.', 'Indian Classical'),
    ('Raga Darbari', [0, 2, 3, 5, 7, 9, 10], 'Deep night raga. Andolit (oscillating) ga and dha. Very serious.', 'Indian Classical'),
    ('Raga Todi', [0, 1, 3, 6, 7, 8, 11], 'Morning raga. Komal ga and dha, teevra ma. Pathos.', 'Indian Classical'),
    ('Raga Bhoopali (Bhup)', [0, 2, 4, 7, 9], 'Pentatonic. Evening raga. Peaceful, meditative.', 'Indian Classical'),
    ('Raga Desh', [0, 2, 4, 7, 9, 10], 'Monsoon raga. Uses both natural and komal ni. Romantic.', 'Indian Classical'),
    ('Maqam Bayati', [0, 1.5, 3, 5, 7, 8, 10], 'Quarter tone! Central to Arabic music. Emotional, longing.', 'Arabic/Middle Eastern'),
    ('Maqam Rast', [0, 2, 3.5, 5, 7, 9, 10.5], 'Quarter tones! "Rast" = straight/just. Neutral 3rd.', 'Arabic/Middle Eastern'),
    ('Maqam Hijaz', [0, 1, 4, 5, 7, 8, 11], 'Dramatic, exotic. Characteristic augmented 2nd interval.', 'Arabic/Middle Eastern'),
    ('Maqam Nahawand', [0, 2, 3, 5, 7, 8, 10], 'Similar to natural minor. Melancholic, classical.', 'Arabic/Middle Eastern'),
    ('Maqam Saba', [0, 1.5, 3, 4, 6, 8, 10], 'Quarter tones! Very emotional, weeping quality.', 'Arabic/Middle Eastern'),
    ('Persian Scale', [0, 1, 4, 5, 6, 8, 11], 'Exotic, mysterious. Augmented 2nd and diminished 4th.', 'Persian'),
    ('Hirajoshi (Japan)', [0, 2, 3, 7, 8], 'Pentatonic. Traditional Japanese. Contemplative.', 'Japanese'),
    ('Insen (Japan)', [0, 1, 5, 7, 10], 'Pentatonic. Traditional Japanese. Dark, meditative.', 'Japanese'),
    ('Iwato (Japan)', [0, 1, 5, 6, 10], 'Pentatonic. Traditional Japanese. Mysterious, floating.', 'Japanese'),
    ('Yo Scale (Japan)', [0, 2, 5, 7, 9], 'Pentatonic. Bright, used in folk and festival music.', 'Japanese'),
    ('Pelog (Indonesia)', [0, 1, 3, 7, 8], 'Gamelan scale. Approximate - actual tuning varies by region.', 'Indonesian (Gamelan)'),
    ('Slendro (Indonesia)', [0, 2, 5, 7, 9], 'Gamelan pentatonic. Equally spaced, no exact Western equivalent.', 'Indonesian (Gamelan)'),
    ('Gong Scale (China)', [0, 2, 4, 7, 9], 'Pentatonic. Do-Re-Mi-So-La. Foundation of Chinese music.', 'Chinese'),
    ('Shang Scale (China)', [0, 2, 3, 7, 8], 'Pentatonic mode. Re-Mi-So-La-Do. Sad, pastoral.', 'Chinese'),
    ('Zhi Scale (China)', [0, 2, 5, 7, 9], 'Pentatonic mode. Mi-So-La-Do-Re. Bright, active.', 'Chinese'),
]

WORLD_SCALES = [
    ('Byzantine (Double Harmonic)', [0, 1, 4, 5, 7, 8, 11], 'Also "Arabic scale". Two augmented 2nds. Exotic.', 'Byzantine/Middle East'),
    ('Hungarian Minor', [0, 2, 3, 6, 7, 8, 11], 'Also "Gypsy scale". Augmented 4th. Dramatic, folk.', 'Hungarian/Gypsy'),
    ('Hungarian Major', [0, 3, 4, 6, 7, 9, 10], 'Unusual major variant. Lydian with flat 2nd and flat 6th.', 'Hungarian'),
    ('Enigmatic', [0, 1, 4, 6, 8, 10, 11], 'Giuseppe Verdi. Very exotic, unresolved quality.', 'Italian'),
    ('Neapolitan Minor', [0, 1, 3, 5, 7, 8, 11], 'Minor with flat 2nd. Dramatic, operatic.', 'Italian'),
    ('Neapolitan Major', [0, 1, 4, 5, 7, 9, 11], 'Major with flat 2nd. Dreamy, floating.', 'Italian'),
    ('Spanish Gypsy', [0, 1, 4, 5, 7, 8, 10], 'Also "Phrygian Dominant". Flamenco, Middle Eastern.', 'Spanish/Middle East'),
    ('Prometheus', [0, 2, 4, 6, 9, 10], 'Alexander Scriabin. Mystic chord. Lydian with flat 7, no 5th.', 'Russian'),
    ('Mystic (Scriabin)', [0, 4, 6, 9, 10, 2], 'Prometheus chord. Quartal harmony. Atonal precursor.', 'Russian'),
    ('Balinese', [0, 1, 3, 7, 8], 'Pentatonic. Similar to Pelog. Gamelan influence.', 'Indonesian'),
    ('Egyptian', [0, 2, 5, 7, 10], 'Pentatonic. Similar to minor pentatonic without 3rd.', 'Egyptian'),
    ('Ethiopian (Tizita)', [0, 2, 3, 5, 7, 8, 10], 'Similar to natural minor. Used in Ethiopian music.', 'Ethiopian'),
    ('Scottish Pentatonic', [0, 2, 5, 7, 9], 'Major pentatonic without 3rd. Folk, bagpipes.', 'Scottish'),
    ('Kumoi (Japan)', [0, 2, 3, 7, 9], 'Pentatonic. Traditional Japanese. Melancholic.', 'Japanese'),
    ('Okinawa (Japan)', [0, 4, 5, 7, 11], 'Pentatonic. Ryukyu Islands. Bittersweet, unique.', 'Japanese (Okinawa)'),
    ('Yo (Korea)', [0, 2, 5, 7, 9], 'Pentatonic. Bright, masculine. Used in pansori.', 'Korean'),
    ('Pyongjo (Korea)', [0, 2, 4, 7, 9], 'Pentatonic. Similar to major pentatonic.', 'Korean'),
    ('Ujo (Korea)', [0, 3, 5, 7, 10], 'Pentatonic. Similar to minor pentatonic. Sad, feminine.', 'Korean'),
    ('Akebono (Japan)', [0, 2, 3, 7, 9], 'Pentatonic. Dawn scale. Gentle, awakening.', 'Japanese'),
    ('Phrygian Dominant', [0, 1, 4, 5, 7, 8, 10], 'Fifth mode of harmonic minor. Spanish, Jewish, Arabic.', 'Middle Eastern'),
    ('Lydian Dominant', [0, 2, 4, 6, 7, 9, 10], 'Fourth mode of melodic minor. Jazz, film scores.', 'Western/Jazz'),
    ('Mixolydian b6', [0, 2, 4, 5, 7, 8, 10], 'Fifth mode of melodic minor. Dark, mysterious.', 'Western/Jazz'),
    ('Locrian #2', [0, 2, 3, 5, 6, 8, 10], 'Sixth mode of melodic minor. Semi-stable diminished.', 'Western/Jazz'),
    ('Altered Dominant', [0, 1, 3, 4, 6, 8, 10], 'Super Locrian. All possible alterations. Modern jazz.', 'Western (Jazz)'),
    ('Whole-Half Diminished', [0, 2, 3, 5, 6, 8, 9, 11], 'Symmetric. Used over diminished chords.', 'Western (Jazz)'),
]

ALL_SCALES = WESTERN_SCALES + EASTERN_SCALES + WORLD_SCALES

CHORDS = [
    ('Major Triad', [0, 4, 7], 'Happy, stable, resolved. The most basic chord.', 'Triads'),
    ('Minor Triad', [0, 3, 7], 'Sad, serious, introspective. Major with lowered 3rd.', 'Triads'),
    ('Diminished Triad', [0, 3, 6], 'Tense, unstable, wants to resolve. Two minor 3rds.', 'Triads'),
    ('Augmented Triad', [0, 4, 8], 'Mysterious, floating, unresolved. Two major 3rds.', 'Triads'),
    ('Sus2', [0, 2, 7], 'Open, airy. No 3rd, replaced by 2nd.', 'Triads'),
    ('Sus4', [0, 5, 7], 'Suspended, waiting. No 3rd, replaced by 4th.', 'Triads'),
    ('Major 7th', [0, 4, 7, 11], 'Jazzy, sophisticated, dreamy. Major triad + major 7th.', 'Seventh Chords'),
    ('Dominant 7th', [0, 4, 7, 10], 'Bluesy, wants to resolve. Major triad + minor 7th.', 'Seventh Chords'),
    ('Minor 7th', [0, 3, 7, 10], 'Smooth, mellow. Minor triad + minor 7th.', 'Seventh Chords'),
    ('Minor Major 7th', [0, 3, 7, 11], 'Dark, cinematic. Minor triad + major 7th.', 'Seventh Chords'),
    ('Half-Diminished 7th', [0, 3, 6, 10], 'Tense, sophisticated. Diminished triad + minor 7th.', 'Seventh Chords'),
    ('Fully Diminished 7th', [0, 3, 6, 9], 'Very tense, symmetric. All minor 3rds.', 'Seventh Chords'),
    ('Augmented 7th', [0, 4, 8, 10], 'Exotic, unstable. Augmented triad + minor 7th.', 'Seventh Chords'),
    ('Major 9th', [0, 4, 7, 11, 14], 'Lush, colorful. Major 7th + 9th.', 'Extended Chords'),
    ('Dominant 9th', [0, 4, 7, 10, 14], 'Funky, jazz. Dominant 7th + 9th.', 'Extended Chords'),
    ('Minor 9th', [0, 3, 7, 10, 14], 'Smooth, sophisticated. Minor 7th + 9th.', 'Extended Chords'),
    ('Major 6/9', [0, 4, 7, 9, 14], 'Hip, sophisticated. Major + 6th and 9th.', 'Eastern/Color'),
    ('Minor 6/9', [0, 3, 7, 9, 14], 'Cool jazz. Minor + 6th and 9th.', 'Eastern/Color'),
    ('Dominant 7b9', [0, 4, 7, 10, 13], 'Hendrix chord. Bluesy, tense.', 'Altered Chords'),
    ('Dominant 7#9', [0, 4, 7, 10, 15], 'Hendrix chord! Blues/funk staple.', 'Altered Chords'),
    ('Dominant 7b5', [0, 4, 6, 10], 'Altered, wants to resolve. Tritone sub.', 'Altered Chords'),
    ('Dominant 7#5', [0, 4, 8, 10], 'Augmented dominant. Dramatic.', 'Altered Chords'),
    ('Quartal (C-F-Bb)', [0, 5, 10], 'Stacked 4ths. Modern, open, modal jazz.', 'Modern/Quartal'),
    ('Quartal (C-F-Bb-Eb)', [0, 5, 10, 15], 'Four-note quartal. McCoy Tyner style.', 'Modern/Quartal'),
    ('Major Add 9', [0, 4, 7, 14], 'Open, Eastern feel. Major triad + 9th.', 'Eastern/Color'),
    ('Minor Add 9', [0, 3, 7, 14], 'Melancholic, Eastern. Minor triad + 9th.', 'Eastern/Color'),
    ('Major 7#11', [0, 4, 7, 11, 18], 'Lydian chord. Dreamy, modern.', 'Eastern/Color'),
]

KEY_SIGNATURES = {
    'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7,
    'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7,
    'a': 0, 'e': 1, 'b': 2, 'f#': 3, 'c#': 4, 'g#': 5, 'd#': 6, 'a#': 7,
    'd': -1, 'g': -2, 'c': -3, 'f': -4, 'bb': -5, 'eb': -6, 'ab': -7,
}

CIRCLE_OF_FIFTHS_MAJOR = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'Ab', 'Eb', 'Bb', 'F']
CIRCLE_OF_FIFTHS_MINOR = ['a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#', 'f', 'c', 'g', 'd']

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def note_to_midi(note_name: str, octave: int = 4) -> int:
    """Convert note name to MIDI note number."""
    note_name = note_name.strip().capitalize()
    if note_name in NOTE_NAMES_SHARP:
        idx = NOTE_NAMES_SHARP.index(note_name)
    elif note_name in NOTE_NAMES_FLAT:
        idx = NOTE_NAMES_FLAT.index(note_name)
    else:
        idx = 0
    return (octave + 1) * 12 + idx


def midi_to_note(midi_num: int, use_sharp: bool = True) -> str:
    """Convert MIDI note number to note name."""
    names = NOTE_NAMES_SHARP if use_sharp else NOTE_NAMES_FLAT
    return names[midi_num % 12]


def get_scale_notes(root: str, intervals: List[float]) -> List[str]:
    """Get note names for a scale given root and intervals."""
    if root in NOTE_NAMES_SHARP:
        root_idx = NOTE_NAMES_SHARP.index(root)
    elif root in NOTE_NAMES_FLAT:
        root_idx = NOTE_NAMES_FLAT.index(root)
    else:
        root_idx = 0

    notes = []
    for iv in intervals:
        idx = (root_idx + int(round(iv))) % 12
        notes.append(NOTE_NAMES_SHARP[idx])
    return notes


def get_chord_notes(root: str, intervals: List[int]) -> List[str]:
    """Get note names for a chord."""
    return get_scale_notes(root, intervals)


def get_interval_name(semitones: int) -> str:
    """Get the name of an interval."""
    st = abs(semitones) % 12
    if st in INTERVALS:
        return INTERVALS[st][0]
    return f"{st} semitones"


def get_key_signature(key: str) -> int:
    """Get number of sharps (positive) or flats (negative) for a key."""
    return KEY_SIGNATURES.get(key, 0)


def get_relative_major(minor_key: str) -> str:
    """Get the relative major of a minor key."""
    minor_root = minor_key[0].upper()
    if minor_key.startswith('bb') or minor_key.startswith('eb') or minor_key.startswith('ab'):
        minor_root = minor_key[:2].capitalize()

    idx = NOTE_NAMES_FLAT.index(minor_root) if minor_root in NOTE_NAMES_FLAT else NOTE_NAMES_SHARP.index(minor_root)
    rel_idx = (idx + 3) % 12
    return NOTE_NAMES_SHARP[rel_idx]


def get_relative_minor(major_key: str) -> str:
    """Get the relative minor of a major key."""
    major_root = major_key[0].upper()
    if len(major_key) > 1 and major_key[1] in '#b':
        major_root = major_key[:2].capitalize()

    idx = NOTE_NAMES_SHARP.index(major_root) if major_root in NOTE_NAMES_SHARP else NOTE_NAMES_FLAT.index(major_root)
    rel_idx = (idx - 3) % 12
    return NOTE_NAMES_SHARP[rel_idx].lower()

# =============================================================================
# PIANO KEYBOARD WIDGET
# =============================================================================

class PianoKeyboard(QWidget):
    """Interactive piano keyboard widget with note highlighting."""

    noteClicked = Signal(str, int)  # note_name, midi_number

    def __init__(self, start_octave=3, num_octaves=3, parent=None):
        super().__init__(parent)
        self.start_octave = start_octave
        self.num_octaves = num_octaves
        self.highlighted_notes = {}  # midi_num -> color
        self.active_notes = set()  # Currently pressed notes
        self.show_labels = True
        self.label_type = 'name'  # 'name', 'degree', 'interval', 'none'
        self.current_root = 'C'
        self.current_scale_intervals = []
        self._hovered_key = None

        self.white_key_width = 40
        self.white_key_height = 180
        self.black_key_width = 24
        self.black_key_height = 110

        self.setMinimumSize(
            self.num_octaves * 7 * self.white_key_width + 20,
            self.white_key_height + 40
        )
        self.setMaximumHeight(self.white_key_height + 60)

        self.setMouseTracking(True)

    def get_key_rect(self, midi_num: int) -> QRect:
        """Get the rectangle for a given MIDI note."""
        octave = (midi_num // 12) - 1
        note_in_octave = midi_num % 12

        rel_octave = octave - self.start_octave
        if rel_octave < 0 or rel_octave >= self.num_octaves:
            return QRect()

        white_key_indices = [0, 2, 4, 5, 7, 9, 11]
        black_key_offsets = {1: 0, 3: 1, 6: 3, 8: 4, 10: 5}

        x_offset = 10
        octave_width = 7 * self.white_key_width

        if note_in_octave in white_key_indices:
            white_idx = white_key_indices.index(note_in_octave)
            x = x_offset + rel_octave * octave_width + white_idx * self.white_key_width
            return QRect(x, 10, self.white_key_width - 1, self.white_key_height)
        elif note_in_octave in black_key_offsets:
            black_idx = black_key_offsets[note_in_octave]
            x = x_offset + rel_octave * octave_width + black_idx * self.white_key_width + self.white_key_width - self.black_key_width // 2
            return QRect(x, 10, self.black_key_width, self.black_key_height)

        return QRect()

    def midi_at_pos(self, pos: QPoint) -> Optional[int]:
        """Get MIDI note at mouse position."""
        # Check black keys first (they're on top)
        for midi_num in range(self.start_octave * 12, (self.start_octave + self.num_octaves) * 12):
            rect = self.get_key_rect(midi_num)
            if rect.contains(pos) and midi_num % 12 in [1, 3, 6, 8, 10]:
                return midi_num

        # Then white keys
        for midi_num in range(self.start_octave * 12, (self.start_octave + self.num_octaves) * 12):
            rect = self.get_key_rect(midi_num)
            if rect.contains(pos) and midi_num % 12 in [0, 2, 4, 5, 7, 9, 11]:
                return midi_num

        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw white keys first
        for midi_num in range(self.start_octave * 12, (self.start_octave + self.num_octaves) * 12):
            if midi_num % 12 in [0, 2, 4, 5, 7, 9, 11]:
                self._draw_key(painter, midi_num)

        # Draw black keys on top
        for midi_num in range(self.start_octave * 12, (self.start_octave + self.num_octaves) * 12):
            if midi_num % 12 in [1, 3, 6, 8, 10]:
                self._draw_key(painter, midi_num)

    def _draw_key(self, painter: QPainter, midi_num: int):
        rect = self.get_key_rect(midi_num)
        if not rect.isValid():
            return

        is_black = midi_num % 12 in [1, 3, 6, 8, 10]
        is_highlighted = midi_num in self.highlighted_notes
        is_active = midi_num in self.active_notes
        is_hovered = midi_num == self._hovered_key

        # Determine color
        if is_active:
            color = QColor(100, 200, 255)
        elif is_highlighted:
            color = self.highlighted_notes[midi_num]
        elif is_hovered:
            color = QColor(200, 220, 255) if not is_black else QColor(80, 80, 100)
        else:
            color = QColor(255, 255, 255) if not is_black else QColor(30, 30, 30)

        # Draw key
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.setBrush(QBrush(color))

        if is_black:
            painter.drawRect(rect)
        else:
            # Round bottom corners for white keys
            path = QPainterPath()
            path.addRoundedRect(rect, 4, 4)
            painter.drawPath(path)

        # Draw label
        if self.show_labels and self.label_type != 'none':
            note_name = midi_to_note(midi_num)
            label = note_name

            if self.label_type == 'degree' and self.current_scale_intervals:
                root_idx = NOTE_NAMES_SHARP.index(self.current_root) if self.current_root in NOTE_NAMES_SHARP else 0
                note_idx = midi_num % 12
                for i, iv in enumerate(self.current_scale_intervals):
                    if (root_idx + int(round(iv))) % 12 == note_idx:
                        label = str(i + 1)
                        break

            painter.setPen(QPen(QColor(0, 0, 0) if not is_black else QColor(255, 255, 255)))
            font = painter.font()
            font.setPointSize(8)
            painter.setFont(font)

            text_rect = QRect(rect.x(), rect.bottom() - 25, rect.width(), 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label)

    def mousePressEvent(self, event):
        midi_num = self.midi_at_pos(event.pos())
        if midi_num is not None:
            self.active_notes.add(midi_num)
            note_name = midi_to_note(midi_num)
            self.noteClicked.emit(note_name, midi_num)
            self.update()

    def mouseReleaseEvent(self, event):
        self.active_notes.clear()
        self.update()

    def mouseMoveEvent(self, event):
        old_hover = self._hovered_key
        self._hovered_key = self.midi_at_pos(event.pos())
        if old_hover != self._hovered_key:
            self.update()

    def leaveEvent(self, event):
        self._hovered_key = None
        self.update()

    def highlight_notes(self, notes: List[str], color: QColor = QColor(255, 200, 100), root: str = None):
        """Highlight specific notes on the keyboard."""
        self.highlighted_notes.clear()
        self.current_root = root or self.current_root

        for note in notes:
            note = note.strip().capitalize()
            if note in NOTE_NAMES_SHARP:
                idx = NOTE_NAMES_SHARP.index(note)
            elif note in NOTE_NAMES_FLAT:
                idx = NOTE_NAMES_FLAT.index(note)
            else:
                continue

            # Highlight all octaves
            for oct_num in range(self.start_octave, self.start_octave + self.num_octaves):
                midi_num = (oct_num + 1) * 12 + idx
                if root and note == root:
                    self.highlighted_notes[midi_num] = QColor(255, 100, 100)  # Root in red
                else:
                    self.highlighted_notes[midi_num] = color

        self.update()

    def clear_highlight(self):
        """Clear all highlights."""
        self.highlighted_notes.clear()
        self.update()

    def set_scale_context(self, root: str, intervals: List[float]):
        """Set scale context for degree labeling."""
        self.current_root = root
        self.current_scale_intervals = intervals
        self.update()

# =============================================================================
# CIRCLE OF FIFTHS WIDGET
# =============================================================================

class CircleOfFifthsWidget(QWidget):
    """Interactive Circle of Fifths diagram."""

    keySelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_key = 'C'
        self.show_minor = True
        self._hovered_key = None
        self.setMinimumSize(500, 500)
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 40

        # Draw outer circle (major keys)
        for i, key in enumerate(CIRCLE_OF_FIFTHS_MAJOR):
            angle = i * 30 - 90  # Start at top
            rad = math.radians(angle)

            x = center.x() + radius * math.cos(rad)
            y = center.y() + radius * math.sin(rad)

            is_selected = key == self.selected_key
            is_hovered = key == self._hovered_key

            # Draw key circle
            if is_selected:
                color = QColor(255, 100, 100)
                size = 35
            elif is_hovered:
                color = QColor(255, 200, 150)
                size = 32
            else:
                color = QColor(240, 240, 240)
                size = 30

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(100, 100, 100), 2))
            painter.drawEllipse(QPointF(x, y), size, size)

            # Draw key name
            painter.setPen(QPen(QColor(0, 0, 0)))
            font = painter.font()
            font.setPointSize(10)
            font.setBold(is_selected)
            painter.setFont(font)
            painter.drawText(QRectF(x - 20, y - 10, 40, 20), Qt.AlignmentFlag.AlignCenter, key)

            # Draw sharps/flats count
            sig = get_key_signature(key)
            sig_text = f"+{sig}" if sig > 0 else str(sig) if sig < 0 else "0"
            font.setPointSize(7)
            painter.setFont(font)
            painter.drawText(QRectF(x - 20, y + 5, 40, 15), Qt.AlignmentFlag.AlignCenter, sig_text)

        # Draw inner circle (minor keys)
        if self.show_minor:
            inner_radius = radius * 0.6
            for i, key in enumerate(CIRCLE_OF_FIFTHS_MINOR):
                angle = i * 30 - 90
                rad = math.radians(angle)

                x = center.x() + inner_radius * math.cos(rad)
                y = center.y() + inner_radius * math.sin(rad)

                is_selected = key == self.selected_key
                is_hovered = key == self._hovered_key

                if is_selected:
                    color = QColor(100, 150, 255)
                    size = 28
                elif is_hovered:
                    color = QColor(180, 200, 255)
                    size = 25
                else:
                    color = QColor(220, 220, 220)
                    size = 23

                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor(100, 100, 100), 1))
                painter.drawEllipse(QPointF(x, y), size, size)

                painter.setPen(QPen(QColor(0, 0, 0)))
                font = painter.font()
                font.setPointSize(9)
                font.setBold(is_selected)
                painter.setFont(font)
                painter.drawText(QRectF(x - 18, y - 8, 36, 16), Qt.AlignmentFlag.AlignCenter, key)

        # Draw connecting lines
        painter.setPen(QPen(QColor(200, 200, 200), 1, Qt.PenStyle.DashLine))
        for i in range(12):
            angle = i * 30 - 90
            rad = math.radians(angle)
            x1 = center.x() + radius * 0.35 * math.cos(rad)
            y1 = center.y() + radius * 0.35 * math.sin(rad)
            x2 = center.x() + radius * 0.75 * math.cos(rad)
            y2 = center.y() + radius * 0.75 * math.sin(rad)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Draw center info
        painter.setPen(QPen(QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)

        sig = get_key_signature(self.selected_key)
        sig_text = f"{self.selected_key}\n"
        if sig > 0:
            sig_text += f"{sig} sharps"
        elif sig < 0:
            sig_text += f"{abs(sig)} flats"
        else:
            sig_text += "No accidentals"

        # Determine if major or minor
        is_minor = self.selected_key[0].islower() if self.selected_key else False
        if is_minor:
            rel = get_relative_major(self.selected_key)
            sig_text += f"\nRel: {rel}"
        else:
            rel = get_relative_minor(self.selected_key)
            sig_text += f"\nRel: {rel}"

        painter.drawText(QRectF(center.x() - 60, center.y() - 40, 120, 80), 
                        Qt.AlignmentFlag.AlignCenter, sig_text)

    def mousePressEvent(self, event):
        key = self._key_at_pos(event.pos())
        if key:
            self.selected_key = key
            self.keySelected.emit(key)
            self.update()

    def mouseMoveEvent(self, event):
        old_hover = self._hovered_key
        self._hovered_key = self._key_at_pos(event.pos())
        if old_hover != self._hovered_key:
            self.update()

    def leaveEvent(self, event):
        self._hovered_key = None
        self.update()

    def _key_at_pos(self, pos: QPoint) -> Optional[str]:
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 40

        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        dist = math.sqrt(dx * dx + dy * dy)
        angle = math.degrees(math.atan2(dy, dx)) + 90
        if angle < 0:
            angle += 360

        # Check major keys (outer)
        if radius * 0.75 < dist < radius + 35:
            idx = round(angle / 30) % 12
            return CIRCLE_OF_FIFTHS_MAJOR[idx]

        # Check minor keys (inner)
        if self.show_minor and radius * 0.4 < dist < radius * 0.75:
            idx = round(angle / 30) % 12
            return CIRCLE_OF_FIFTHS_MINOR[idx]

        return None

# =============================================================================
# SCALE VISUALIZER WIDGET
# =============================================================================

class ScaleVisualizer(QWidget):
    """Visual representation of a scale on a fretboard-like grid."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.notes = []
        self.root = 'C'
        self.scale_name = ''
        self.setMinimumSize(600, 120)

    def set_scale(self, root: str, notes: List[str], scale_name: str = ''):
        self.root = root
        self.notes = [n.capitalize() for n in notes]
        self.scale_name = scale_name
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cell_width = self.width() / 12
        cell_height = 60
        y_offset = (self.height() - cell_height) / 2

        # Draw all 12 chromatic notes
        for i, note in enumerate(NOTE_NAMES_SHARP):
            x = i * cell_width
            rect = QRectF(x + 2, y_offset, cell_width - 4, cell_height)

            if note == self.root:
                color = QColor(255, 100, 100)  # Root
            elif note in self.notes:
                color = QColor(255, 200, 100)  # Scale note
            else:
                color = QColor(240, 240, 240)  # Not in scale

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(150, 150, 150), 1))
            painter.drawRoundedRect(rect, 8, 8)

            # Draw note name
            painter.setPen(QPen(QColor(0, 0, 0)))
            font = painter.font()
            font.setPointSize(11)
            font.setBold(note == self.root)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, note)

            # Draw interval if in scale
            if note in self.notes and note != self.root:
                root_idx = NOTE_NAMES_SHARP.index(self.root) if self.root in NOTE_NAMES_SHARP else 0
                note_idx = i
                interval = (note_idx - root_idx) % 12
                if interval in INTERVALS:
                    int_name = INTERVALS[interval][1]
                    font.setPointSize(8)
                    painter.setFont(font)
                    painter.drawText(QRectF(x + 2, y_offset + 35, cell_width - 4, 20), 
                                   Qt.AlignmentFlag.AlignCenter, int_name)

        # Draw scale info
        if self.scale_name:
            painter.setPen(QPen(QColor(80, 80, 80)))
            font = painter.font()
            font.setPointSize(12)
            painter.setFont(font)
            info_text = f"{self.root} {self.scale_name}"
            painter.drawText(QRectF(10, 10, self.width() - 20, 25), 
                           Qt.AlignmentFlag.AlignLeft, info_text)


# =============================================================================
# GUITAR FRETBOARD WIDGET
# =============================================================================

class GuitarFretboard(QWidget):
    """Visual guitar fretboard with note highlighting."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tuning = ['E', 'A', 'D', 'G', 'B', 'E']  # Standard tuning
        self.num_frets = 15
        self.highlighted_notes = set()
        self.root_note = 'C'
        self.show_intervals = False
        self.setMinimumSize(700, 200)

    def set_highlighted_notes(self, notes: List[str], root: str = 'C'):
        self.highlighted_notes = set(n.capitalize() for n in notes)
        self.root_note = root.capitalize()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = 30
        fret_width = (self.width() - 2 * margin) / (self.num_frets + 1)
        string_spacing = (self.height() - 2 * margin) / (len(self.tuning) - 1)

        # Draw fretboard background
        board_rect = QRectF(margin, margin, self.width() - 2 * margin, self.height() - 2 * margin)
        painter.setBrush(QBrush(QColor(139, 90, 43)))  # Wood color
        painter.setPen(QPen(QColor(100, 60, 20), 2))
        painter.drawRect(board_rect)

        # Draw frets
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        for i in range(self.num_frets + 1):
            x = margin + i * fret_width
            painter.drawLine(QPointF(x, margin), QPointF(x, self.height() - margin))

        # Draw fret markers
        marker_frets = [3, 5, 7, 9, 12, 15]
        painter.setBrush(QBrush(QColor(240, 240, 240)))
        painter.setPen(Qt.PenStyle.NoPen)
        for fret in marker_frets:
            if fret <= self.num_frets:
                x = margin + (fret - 0.5) * fret_width
                if fret == 12:
                    # Double dot at 12th fret
                    painter.drawEllipse(QPointF(x - 8, self.height() / 2 - 15), 6, 6)
                    painter.drawEllipse(QPointF(x - 8, self.height() / 2 + 15), 6, 6)
                else:
                    painter.drawEllipse(QPointF(x - 6, self.height() / 2), 8, 8)

        # Draw strings
        for i, string_note in enumerate(self.tuning):
            y = margin + i * string_spacing
            thickness = 1 + (5 - i) * 0.3
            painter.setPen(QPen(QColor(220, 220, 220), thickness))
            painter.drawLine(QPointF(margin, y), QPointF(self.width() - margin, y))

            # Draw open string note
            painter.setPen(QPen(QColor(0, 0, 0)))
            font = painter.font()
            font.setPointSize(9)
            painter.setFont(font)
            painter.drawText(QRectF(2, y - 10, margin - 5, 20), 
                           Qt.AlignmentFlag.AlignCenter, string_note)

        # Draw notes on fretboard
        for string_idx, open_note in enumerate(self.tuning):
            open_idx = NOTE_NAMES_SHARP.index(open_note) if open_note in NOTE_NAMES_SHARP else 0

            for fret in range(self.num_frets + 1):
                note_idx = (open_idx + fret) % 12
                note_name = NOTE_NAMES_SHARP[note_idx]

                if note_name in self.highlighted_notes:
                    x = margin + (fret + 0.5) * fret_width
                    y = margin + string_idx * string_spacing

                    if note_name == self.root_note:
                        color = QColor(255, 80, 80)
                        size = 14
                    else:
                        color = QColor(255, 200, 80)
                        size = 12

                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(QColor(100, 100, 100), 1))
                    painter.drawEllipse(QPointF(x, y), size, size)

                    painter.setPen(QPen(QColor(0, 0, 0)))
                    font = painter.font()
                    font.setPointSize(7)
                    painter.setFont(font)

                    if self.show_intervals and note_name != self.root_note:
                        root_idx = NOTE_NAMES_SHARP.index(self.root_note) if self.root_note in NOTE_NAMES_SHARP else 0
                        interval = (note_idx - root_idx) % 12
                        if interval in INTERVALS:
                            label = INTERVALS[interval][1]
                        else:
                            label = note_name
                    else:
                        label = note_name

                    painter.drawText(QRectF(x - 12, y - 8, 24, 16), 
                                   Qt.AlignmentFlag.AlignCenter, label)

# =============================================================================
# MAIN APPLICATION TABS
# =============================================================================

class ScaleExplorerTab(QWidget):
    """Tab for exploring scales from Western, Eastern, and World traditions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Category selector
        left_layout.addWidget(QLabel("<b>Category</b>"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(['All', 'Western', 'Western (Mode)', 'Western (Jazz)', 
                                      'Western/World', 'Indian Classical', 'Arabic/Middle Eastern',
                                      'Persian', 'Japanese', 'Chinese', 'Korean', 'Indonesian (Gamelan)',
                                      'Byzantine/Middle East', 'Hungarian/Gypsy', 'Hungarian',
                                      'Italian', 'Spanish/Middle East', 'Russian', 'Egyptian',
                                      'Ethiopian', 'Scottish', 'Japanese (Okinawa)', 'Middle Eastern'])
        self.category_combo.currentTextChanged.connect(self._filter_scales)
        left_layout.addWidget(self.category_combo)

        # Tradition selector
        left_layout.addWidget(QLabel("<b>Tradition</b>"))
        self.tradition_combo = QComboBox()
        self.tradition_combo.addItems(['All Traditions', 'Western Only', 'Eastern Only', 'World Only'])
        self.tradition_combo.currentTextChanged.connect(self._filter_scales)
        left_layout.addWidget(self.tradition_combo)

        # Root note selector
        left_layout.addWidget(QLabel("<b>Root Note</b>"))
        self.root_combo = QComboBox()
        self.root_combo.addItems(NOTE_NAMES_SHARP)
        self.root_combo.currentTextChanged.connect(self._update_display)
        left_layout.addWidget(self.root_combo)

        # Scale list
        left_layout.addWidget(QLabel("<b>Scale</b>"))
        self.scale_list = QListWidget()
        self.scale_list.setMinimumWidth(250)
        self.scale_list.currentRowChanged.connect(self._update_display)
        left_layout.addWidget(self.scale_list)

        # Scale info
        self.info_label = QLabel("Select a scale to see details")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("background: #f5f5f5; padding: 10px; border-radius: 5px;")
        left_layout.addWidget(self.info_label)

        # Play button
        self.play_btn = QPushButton("Play Scale (Visual)")
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50; color: white; padding: 10px; 
                border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background: #45a049; }
        """)
        self.play_btn.clicked.connect(self._play_scale)
        left_layout.addWidget(self.play_btn)

        left_layout.addStretch()
        layout.addWidget(left_panel, 1)

        # Right panel - Visualizations
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Piano keyboard
        self.piano = PianoKeyboard(start_octave=3, num_octaves=2)
        self.piano.setMinimumHeight(220)
        right_layout.addWidget(self.piano)

        # Scale visualizer
        self.scale_viz = ScaleVisualizer()
        right_layout.addWidget(self.scale_viz)

        # Guitar fretboard
        self.fretboard = GuitarFretboard()
        right_layout.addWidget(self.fretboard)

        # Interval breakdown
        self.interval_table = QTableWidget()
        self.interval_table.setColumnCount(3)
        self.interval_table.setHorizontalHeaderLabels(['Note', 'Interval', 'Semitones'])
        self.interval_table.setMaximumHeight(150)
        right_layout.addWidget(self.interval_table)

        layout.addWidget(right_panel, 3)

        # Initialize
        self._filter_scales()

    def _filter_scales(self):
        self.scale_list.clear()
        category = self.category_combo.currentText()
        tradition = self.tradition_combo.currentText()

        source = ALL_SCALES
        if tradition == 'Western Only':
            source = WESTERN_SCALES
        elif tradition == 'Eastern Only':
            source = EASTERN_SCALES
        elif tradition == 'World Only':
            source = WORLD_SCALES

        for name, intervals, desc, cat in source:
            if category == 'All' or category == cat:
                item = QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, (name, intervals, desc, cat))
                self.scale_list.addItem(item)

    def _update_display(self):
        item = self.scale_list.currentItem()
        if not item:
            return

        name, intervals, desc, cat = item.data(Qt.ItemDataRole.UserRole)
        root = self.root_combo.currentText()

        notes = get_scale_notes(root, intervals)

        # Update info
        notes_str = ' - '.join(notes)
        info = f"<b>{root} {name}</b><br>"
        info += f"<b>Category:</b> {cat}<br>"
        info += f"<b>Notes:</b> {notes_str}<br><br>"
        info += f"<i>{desc}</i>"
        self.info_label.setText(info)

        # Update piano
        self.piano.highlight_notes(notes, QColor(255, 200, 100), root)
        self.piano.set_scale_context(root, intervals)

        # Update scale visualizer
        self.scale_viz.set_scale(root, notes, name)

        # Update fretboard
        self.fretboard.set_highlighted_notes(notes, root)

        # Update interval table
        self.interval_table.setRowCount(len(notes))
        root_idx = NOTE_NAMES_SHARP.index(root) if root in NOTE_NAMES_SHARP else 0

        for i, note in enumerate(notes):
            note_idx = NOTE_NAMES_SHARP.index(note) if note in NOTE_NAMES_SHARP else 0
            semitones = (note_idx - root_idx) % 12
            interval_name = get_interval_name(semitones)

            self.interval_table.setItem(i, 0, QTableWidgetItem(note))
            self.interval_table.setItem(i, 1, QTableWidgetItem(interval_name))
            self.interval_table.setItem(i, 2, QTableWidgetItem(str(semitones)))

        self.interval_table.resizeColumnsToContents()

    def _play_scale(self):
        """Visual animation of scale notes."""
        item = self.scale_list.currentItem()
        if not item:
            return

        name, intervals, desc, cat = item.data(Qt.ItemDataRole.UserRole)
        root = self.root_combo.currentText()
        notes = get_scale_notes(root, intervals)

        # Animate through notes
        self.piano.clear_highlight()
        self._animate_note_index = 0
        self._animate_notes = notes
        self._animate_timer = QTimer(self)
        self._animate_timer.timeout.connect(self._animate_next_note)
        self._animate_timer.start(300)

    def _animate_next_note(self):
        if self._animate_note_index >= len(self._animate_notes):
            self._animate_timer.stop()
            self._update_display()
            return

        note = self._animate_notes[self._animate_note_index]
        self.piano.highlight_notes([note], QColor(100, 200, 255))
        self._animate_note_index += 1


class ChordExplorerTab(QWidget):
    """Tab for exploring chords and their voicings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        left_layout.addWidget(QLabel("<b>Chord Category</b>"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(['All', 'Triads', 'Seventh Chords', 'Extended Chords', 
                                      'Altered Chords', 'Modern/Quartal', 'Eastern/Color'])
        self.category_combo.currentTextChanged.connect(self._filter_chords)
        left_layout.addWidget(self.category_combo)

        left_layout.addWidget(QLabel("<b>Root Note</b>"))
        self.root_combo = QComboBox()
        self.root_combo.addItems(NOTE_NAMES_SHARP)
        self.root_combo.currentTextChanged.connect(self._update_display)
        left_layout.addWidget(self.root_combo)

        left_layout.addWidget(QLabel("<b>Chord</b>"))
        self.chord_list = QListWidget()
        self.chord_list.setMinimumWidth(250)
        self.chord_list.currentRowChanged.connect(self._update_display)
        left_layout.addWidget(self.chord_list)

        self.info_label = QLabel("Select a chord to see details")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("background: #f5f5f5; padding: 10px; border-radius: 5px;")
        left_layout.addWidget(self.info_label)

        # Inversion selector
        left_layout.addWidget(QLabel("<b>Inversion</b>"))
        self.inversion_combo = QComboBox()
        self.inversion_combo.addItems(['Root Position', '1st Inversion', '2nd Inversion', '3rd Inversion'])
        self.inversion_combo.currentIndexChanged.connect(self._update_display)
        left_layout.addWidget(self.inversion_combo)

        left_layout.addStretch()
        layout.addWidget(left_panel, 1)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.piano = PianoKeyboard(start_octave=3, num_octaves=2)
        self.piano.setMinimumHeight(220)
        right_layout.addWidget(self.piano)

        # Chord formula display
        self.formula_label = QLabel()
        self.formula_label.setStyleSheet("font-size: 14px; padding: 10px; background: #e8f4f8; border-radius: 5px;")
        self.formula_label.setWordWrap(True)
        right_layout.addWidget(self.formula_label)

        # Voicing display
        self.voicing_table = QTableWidget()
        self.voicing_table.setColumnCount(4)
        self.voicing_table.setHorizontalHeaderLabels(['Note', 'Role', 'Interval', 'MIDI'])
        self.voicing_table.setMaximumHeight(150)
        right_layout.addWidget(self.voicing_table)

        layout.addWidget(right_panel, 3)

        self._filter_chords()

    def _filter_chords(self):
        self.chord_list.clear()
        category = self.category_combo.currentText()

        for name, intervals, desc, cat in CHORDS:
            if category == 'All' or category == cat:
                item = QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, (name, intervals, desc, cat))
                self.chord_list.addItem(item)

    def _update_display(self):
        item = self.chord_list.currentItem()
        if not item:
            return

        name, intervals, desc, cat = item.data(Qt.ItemDataRole.UserRole)
        root = self.root_combo.currentText()
        inversion = self.inversion_combo.currentIndex()

        # Calculate notes with inversion
        base_notes = get_chord_notes(root, intervals)

        if inversion > 0 and len(base_notes) > inversion:
            notes = base_notes[inversion:] + base_notes[:inversion]
            # Adjust octaves for inverted notes
            for i in range(inversion):
                notes[len(notes) - inversion + i] = notes[len(notes) - inversion + i]
        else:
            notes = base_notes

        # Update info
        notes_str = ' - '.join(notes)
        info = f"<b>{root} {name}</b><br>"
        info += f"<b>Category:</b> {cat}<br>"
        info += f"<b>Notes:</b> {notes_str}<br>"
        if inversion > 0:
            inv_names = ['', '1st', '2nd', '3rd']
            info += f"<b>Inversion:</b> {inv_names[inversion]}<br>"
        info += f"<br><i>{desc}</i>"
        self.info_label.setText(info)

        # Update piano
        self.piano.highlight_notes(notes, QColor(100, 200, 255), root)

        # Formula
        root_idx = NOTE_NAMES_SHARP.index(root) if root in NOTE_NAMES_SHARP else 0
        formula_parts = []
        for iv in intervals:
            if iv in INTERVALS:
                formula_parts.append(INTERVALS[iv][1])
            else:
                formula_parts.append(f"+{iv}")
        self.formula_label.setText(f"<b>Formula:</b> {' + '.join(formula_parts)}")

        # Voicing table
        self.voicing_table.setRowCount(len(notes))
        roles = ['Root', '3rd', '5th', '7th', '9th', '11th', '13th']

        for i, note in enumerate(notes):
            note_idx = NOTE_NAMES_SHARP.index(note) if note in NOTE_NAMES_SHARP else 0
            semitones = (note_idx - root_idx) % 12
            interval_name = get_interval_name(semitones)

            self.voicing_table.setItem(i, 0, QTableWidgetItem(note))
            self.voicing_table.setItem(i, 1, QTableWidgetItem(roles[i] if i < len(roles) else 'Extension'))
            self.voicing_table.setItem(i, 2, QTableWidgetItem(interval_name))
            self.voicing_table.setItem(i, 3, QTableWidgetItem(str(note_to_midi(note))))

        self.voicing_table.resizeColumnsToContents()

class IntervalCalculatorTab(QWidget):
    """Tab for calculating and visualizing intervals."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Top controls
        controls = QHBoxLayout()

        controls.addWidget(QLabel("<b>Note 1:</b>"))
        self.note1_combo = QComboBox()
        self.note1_combo.addItems(NOTE_NAMES_SHARP)
        self.note1_combo.currentTextChanged.connect(self._calculate)
        controls.addWidget(self.note1_combo)

        controls.addWidget(QLabel("<b>Note 2:</b>"))
        self.note2_combo = QComboBox()
        self.note2_combo.addItems(NOTE_NAMES_SHARP)
        self.note2_combo.setCurrentIndex(7)  # G
        self.note2_combo.currentTextChanged.connect(self._calculate)
        controls.addWidget(self.note2_combo)

        controls.addStretch()
        layout.addLayout(controls)

        # Result display
        self.result_frame = QFrame()
        self.result_frame.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        result_layout = QVBoxLayout(self.result_frame)

        self.interval_name_label = QLabel("Perfect Fifth")
        self.interval_name_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        self.interval_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.interval_name_label)

        self.interval_detail_label = QLabel("P5 | 7 semitones")
        self.interval_detail_label.setStyleSheet("font-size: 18px; color: #e0e0e0;")
        self.interval_detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.interval_detail_label)

        self.interval_desc_label = QLabel("The most stable interval after the octave. Foundation of all chords.")
        self.interval_desc_label.setStyleSheet("font-size: 14px; color: #d0d0d0; padding: 10px;")
        self.interval_desc_label.setWordWrap(True)
        self.interval_desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.interval_desc_label)

        layout.addWidget(self.result_frame)

        # Piano visualization
        self.piano = PianoKeyboard(start_octave=3, num_octaves=2)
        self.piano.setMinimumHeight(220)
        layout.addWidget(self.piano)

        # Interval reference table
        layout.addWidget(QLabel("<b>Interval Reference Table</b>"))
        self.ref_table = QTableWidget()
        self.ref_table.setColumnCount(4)
        self.ref_table.setHorizontalHeaderLabels(['Semitones', 'Name', 'Abbreviation', 'Description'])
        self.ref_table.setMaximumHeight(250)

        descriptions = {
            0: 'Same pitch. The starting point.',
            1: 'Smallest interval. Dissonant, tense.',
            2: 'Whole step. Major scale step.',
            3: 'Sad, minor quality.',
            4: 'Happy, major quality.',
            5: 'Stable, consonant. Subdominant.',
            6: 'Devil in music. Tense, wants resolution.',
            7: 'Most stable. Dominant. Power chord.',
            8: 'Minor 6th. Dark, mysterious.',
            9: 'Major 6th. Pleasant, consonant.',
            10: 'Dominant 7th. Bluesy, wants to resolve.',
            11: 'Leading tone. Strong pull to tonic.',
            12: 'Same note, higher register. Perfect consonance.',
        }

        self.ref_table.setRowCount(13)
        for i in range(13):
            if i in INTERVALS:
                name, abbr = INTERVALS[i]
                self.ref_table.setItem(i, 0, QTableWidgetItem(str(i)))
                self.ref_table.setItem(i, 1, QTableWidgetItem(name))
                self.ref_table.setItem(i, 2, QTableWidgetItem(abbr))
                self.ref_table.setItem(i, 3, QTableWidgetItem(descriptions.get(i, '')))

        self.ref_table.resizeColumnsToContents()
        layout.addWidget(self.ref_table)

        self._calculate()

    def _calculate(self):
        note1 = self.note1_combo.currentText()
        note2 = self.note2_combo.currentText()

        idx1 = NOTE_NAMES_SHARP.index(note1) if note1 in NOTE_NAMES_SHARP else 0
        idx2 = NOTE_NAMES_SHARP.index(note2) if note2 in NOTE_NAMES_SHARP else 0

        diff = (idx2 - idx1) % 12

        if diff in INTERVALS:
            name, abbr = INTERVALS[diff]
            self.interval_name_label.setText(name)
            self.interval_detail_label.setText(f"{abbr} | {diff} semitones | {note1} → {note2}")

            descriptions = {
                0: 'Same pitch. The starting point of all music.',
                1: 'The smallest interval. Creates tension and dissonance.',
                2: 'A whole step. The building block of major scales.',
                3: 'The minor third. Creates a sad, melancholic quality.',
                4: 'The major third. Creates a happy, bright quality.',
                5: 'Perfect fourth. Stable, consonant. The subdominant.',
                6: 'The tritone. Called "diabolus in musica" - the devil in music.',
                7: 'Perfect fifth. The most stable interval. Foundation of power chords.',
                8: 'Minor sixth. Dark, mysterious, used in minor keys.',
                9: 'Major sixth. Pleasant, consonant. Used in major 6th chords.',
                10: 'Minor seventh. Bluesy, dominant. Wants to resolve down.',
                11: 'Major seventh. The leading tone. Strong pull to the tonic.',
                12: 'Perfect octave. Same note class, perfect consonance.',
            }
            self.interval_desc_label.setText(descriptions.get(diff, ''))
        else:
            self.interval_name_label.setText(f"{diff} Semitones")
            self.interval_detail_label.setText(f"Compound interval | {note1} → {note2}")
            self.interval_desc_label.setText('')

        # Update piano
        self.piano.clear_highlight()
        self.piano.highlight_notes([note1], QColor(255, 100, 100))

        # Add second note highlight
        for oct_num in range(3, 5):
            midi_num = (oct_num + 1) * 12 + idx2
            self.piano.highlighted_notes[midi_num] = QColor(100, 200, 255)
        self.piano.update()


class KeySignaturesTab(QWidget):
    """Tab for learning key signatures."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Circle of fifths
        layout.addWidget(QLabel("<b>Interactive Circle of Fifths</b> - Click any key to explore"))
        self.circle = CircleOfFifthsWidget()
        self.circle.setMinimumHeight(450)
        self.circle.keySelected.connect(self._on_key_selected)
        layout.addWidget(self.circle)

        # Key info panel
        self.info_panel = QFrame()
        self.info_panel.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #dee2e6;
            }
        """)
        info_layout = QHBoxLayout(self.info_panel)

        self.key_info = QLabel("Click a key in the Circle of Fifths to see details")
        self.key_info.setWordWrap(True)
        self.key_info.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.key_info, 2)

        # Scale notes display
        self.scale_notes_label = QLabel()
        self.scale_notes_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #495057;")
        info_layout.addWidget(self.scale_notes_label, 1)

        layout.addWidget(self.info_panel)

        # Quick reference
        layout.addWidget(QLabel("<b>Key Signature Quick Reference</b>"))

        ref_widget = QWidget()
        ref_layout = QHBoxLayout(ref_widget)

        # Sharp keys
        sharp_group = QGroupBox("Sharp Keys")
        sharp_layout = QVBoxLayout(sharp_group)
        sharp_keys = ['C (0)', 'G (1♯)', 'D (2♯)', 'A (3♯)', 'E (4♯)', 'B (5♯)', 'F# (6♯)', 'C# (7♯)']
        for sk in sharp_keys:
            lbl = QLabel(sk)
            lbl.setStyleSheet("padding: 3px;")
            sharp_layout.addWidget(lbl)
        ref_layout.addWidget(sharp_group)

        # Flat keys
        flat_group = QGroupBox("Flat Keys")
        flat_layout = QVBoxLayout(flat_group)
        flat_keys = ['C (0)', 'F (1♭)', 'Bb (2♭)', 'Eb (3♭)', 'Ab (4♭)', 'Db (5♭)', 'Gb (6♭)', 'Cb (7♭)']
        for fk in flat_keys:
            lbl = QLabel(fk)
            lbl.setStyleSheet("padding: 3px;")
            flat_layout.addWidget(lbl)
        ref_layout.addWidget(flat_group)

        # Relative minors
        rel_group = QGroupBox("Relative Minors")
        rel_layout = QVBoxLayout(rel_group)
        rel_pairs = [
            'C Major ↔ a minor',
            'G Major ↔ e minor',
            'D Major ↔ b minor',
            'A Major ↔ f# minor',
            'E Major ↔ c# minor',
            'B Major ↔ g# minor',
            'F# Major ↔ d# minor',
            'F Major ↔ d minor',
            'Bb Major ↔ g minor',
            'Eb Major ↔ c minor',
        ]
        for rp in rel_pairs:
            lbl = QLabel(rp)
            lbl.setStyleSheet("padding: 3px;")
            rel_layout.addWidget(lbl)
        ref_layout.addWidget(rel_group)

        layout.addWidget(ref_widget)

    def _on_key_selected(self, key: str):
        sig = get_key_signature(key)

        is_minor = key[0].islower()
        if is_minor:
            rel_major = get_relative_major(key)
            info = f"<b>{key} minor</b><br>"
            info += f"Relative Major: <b>{rel_major}</b><br>"
            scale_notes = get_scale_notes(key[0].upper() + key[1:] if len(key) > 1 else key[0].upper(), [0, 2, 3, 5, 7, 8, 10])
        else:
            rel_minor = get_relative_minor(key)
            info = f"<b>{key} Major</b><br>"
            info += f"Relative Minor: <b>{rel_minor}</b><br>"
            scale_notes = get_scale_notes(key, [0, 2, 4, 5, 7, 9, 11])

        if sig > 0:
            info += f"Key Signature: <b>{sig} sharp{'s' if sig > 1 else ''}</b><br>"
            sharps = ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#']
            info += f"Order: {', '.join(sharps[:sig])}"
        elif sig < 0:
            info += f"Key Signature: <b>{abs(sig)} flat{'s' if abs(sig) > 1 else ''}</b><br>"
            flats = ['Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb']
            info += f"Order: {', '.join(flats[:abs(sig)])}"
        else:
            info += "No sharps or flats"

        self.key_info.setText(info)
        self.scale_notes_label.setText(' - '.join(scale_notes))

class NoteIdentificationTab(QWidget):
    """Tab for note identification exercises."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.total = 0
        self.current_note = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Score display
        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.score_label)

        # Instructions
        instr = QLabel("<b>Note Identification Exercise</b><br>Click the correct note name for the highlighted key on the piano.")
        instr.setWordWrap(True)
        instr.setStyleSheet("background: #e8f4f8; padding: 10px; border-radius: 5px;")
        layout.addWidget(instr)

        # Piano
        self.piano = PianoKeyboard(start_octave=3, num_octaves=2)
        self.piano.setMinimumHeight(220)
        layout.addWidget(self.piano)

        # Note buttons
        buttons_layout = QHBoxLayout()
        self.note_buttons = []
        for note in NOTE_NAMES_SHARP:
            btn = QPushButton(note)
            btn.setMinimumSize(50, 50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px; font-weight: bold;
                    background: #3498db; color: white;
                    border-radius: 8px;
                }
                QPushButton:hover { background: #2980b9; }
                QPushButton:pressed { background: #1a5276; }
            """)
            btn.clicked.connect(lambda checked, n=note: self._check_answer(n))
            buttons_layout.addWidget(btn)
            self.note_buttons.append(btn)

        layout.addLayout(buttons_layout)

        # Feedback
        self.feedback_label = QLabel("Press 'New Note' to start!")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 5px;")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)

        # Control buttons
        controls = QHBoxLayout()

        self.new_note_btn = QPushButton("New Note")
        self.new_note_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60; color: white; padding: 12px 24px;
                font-size: 16px; font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover { background: #229954; }
        """)
        self.new_note_btn.clicked.connect(self._new_question)
        controls.addWidget(self.new_note_btn)

        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.setStyleSheet("""
            QPushButton {
                background: #e67e22; color: white; padding: 12px 24px;
                font-size: 16px; border-radius: 8px;
            }
            QPushButton:hover { background: #d35400; }
        """)
        self.show_answer_btn.clicked.connect(self._show_answer)
        controls.addWidget(self.show_answer_btn)

        self.reset_btn = QPushButton("Reset Score")
        self.reset_btn.clicked.connect(self._reset_score)
        controls.addWidget(self.reset_btn)

        controls.addStretch()
        layout.addLayout(controls)

        layout.addStretch()

    def _new_question(self):
        self.piano.clear_highlight()

        # Pick a random note
        octave = random.randint(3, 4)
        note_idx = random.randint(0, 11)
        self.current_note = NOTE_NAMES_SHARP[note_idx]
        midi_num = (octave + 1) * 12 + note_idx

        # Highlight on piano
        self.piano.highlighted_notes[midi_num] = QColor(255, 200, 100)
        self.piano.update()

        self.feedback_label.setText("What note is highlighted?")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #fff3cd; border-radius: 5px;")

    def _check_answer(self, answer: str):
        if not self.current_note:
            self.feedback_label.setText("Press 'New Note' first!")
            return

        self.total += 1

        if answer == self.current_note:
            self.score += 1
            self.feedback_label.setText(f"✓ Correct! That's {self.current_note}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #d4edda; color: #155724; border-radius: 5px;")
        else:
            self.feedback_label.setText(f"✗ Wrong! That's {self.current_note}, not {answer}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #f8d7da; color: #721c24; border-radius: 5px;")

        self.score_label.setText(f"Score: {self.score} / {self.total} ({int(self.score/self.total*100)}%)")
        self.current_note = None

    def _show_answer(self):
        if self.current_note:
            self.feedback_label.setText(f"The answer is: {self.current_note}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #d1ecf1; color: #0c5460; border-radius: 5px;")

    def _reset_score(self):
        self.score = 0
        self.total = 0
        self.score_label.setText("Score: 0 / 0")
        self.current_note = None
        self.piano.clear_highlight()
        self.feedback_label.setText("Press 'New Note' to start!")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 5px;")


class ScaleIdentificationTab(QWidget):
    """Tab for scale identification exercises."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.total = 0
        self.current_scale = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.score_label)

        instr = QLabel("<b>Scale Identification Exercise</b><br>Identify the scale shown on the piano keyboard.")
        instr.setWordWrap(True)
        instr.setStyleSheet("background: #e8f4f8; padding: 10px; border-radius: 5px;")
        layout.addWidget(instr)

        self.piano = PianoKeyboard(start_octave=3, num_octaves=2)
        self.piano.setMinimumHeight(220)
        layout.addWidget(self.piano)

        # Scale buttons - group by category
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(200)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Western scales
        western_group = QWidget()
        western_layout = QHBoxLayout(western_group)
        western_layout.addWidget(QLabel("<b>Western:</b>"))
        for name, intervals, desc, cat in WESTERN_SCALES[:8]:
            btn = QPushButton(name)
            btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
            btn.clicked.connect(lambda checked, n=name: self._check_answer(n))
            western_layout.addWidget(btn)
        western_layout.addStretch()
        scroll_layout.addWidget(western_group)

        # Eastern scales
        eastern_group = QWidget()
        eastern_layout = QHBoxLayout(eastern_group)
        eastern_layout.addWidget(QLabel("<b>Eastern:</b>"))
        for name, intervals, desc, cat in EASTERN_SCALES[:6]:
            btn = QPushButton(name)
            btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
            btn.clicked.connect(lambda checked, n=name: self._check_answer(n))
            eastern_layout.addWidget(btn)
        eastern_layout.addStretch()
        scroll_layout.addWidget(eastern_group)

        # World scales
        world_group = QWidget()
        world_layout = QHBoxLayout(world_group)
        world_layout.addWidget(QLabel("<b>World:</b>"))
        for name, intervals, desc, cat in WORLD_SCALES[:6]:
            btn = QPushButton(name)
            btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
            btn.clicked.connect(lambda checked, n=name: self._check_answer(n))
            world_layout.addWidget(btn)
        world_layout.addStretch()
        scroll_layout.addWidget(world_group)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Feedback
        self.feedback_label = QLabel("Press 'New Scale' to start!")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 5px;")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)

        # Controls
        controls = QHBoxLayout()

        self.new_scale_btn = QPushButton("New Scale")
        self.new_scale_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60; color: white; padding: 12px 24px;
                font-size: 16px; font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover { background: #229954; }
        """)
        self.new_scale_btn.clicked.connect(self._new_question)
        controls.addWidget(self.new_scale_btn)

        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.clicked.connect(self._show_answer)
        controls.addWidget(self.show_answer_btn)

        self.reset_btn = QPushButton("Reset Score")
        self.reset_btn.clicked.connect(self._reset_score)
        controls.addWidget(self.reset_btn)

        controls.addStretch()
        layout.addLayout(controls)

        layout.addStretch()

    def _new_question(self):
        self.piano.clear_highlight()

        # Pick random scale
        scale_data = random.choice(ALL_SCALES)
        self.current_scale = scale_data
        name, intervals, desc, cat = scale_data

        # Pick random root
        root = random.choice(NOTE_NAMES_SHARP)
        notes = get_scale_notes(root, intervals)

        # Highlight on piano
        self.piano.highlight_notes(notes, QColor(255, 200, 100), root)

        self.feedback_label.setText(f"What scale is this in {root}?")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #fff3cd; border-radius: 5px;")

    def _check_answer(self, answer: str):
        if not self.current_scale:
            self.feedback_label.setText("Press 'New Scale' first!")
            return

        self.total += 1
        correct_name = self.current_scale[0]

        if answer == correct_name:
            self.score += 1
            self.feedback_label.setText(f"✓ Correct! That's {correct_name}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #d4edda; color: #155724; border-radius: 5px;")
        else:
            self.feedback_label.setText(f"✗ Wrong! That's {correct_name}, not {answer}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #f8d7da; color: #721c24; border-radius: 5px;")

        self.score_label.setText(f"Score: {self.score} / {self.total} ({int(self.score/self.total*100)}%)")
        self.current_scale = None

    def _show_answer(self):
        if self.current_scale:
            self.feedback_label.setText(f"The answer is: {self.current_scale[0]}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #d1ecf1; color: #0c5460; border-radius: 5px;")

    def _reset_score(self):
        self.score = 0
        self.total = 0
        self.score_label.setText("Score: 0 / 0")
        self.current_scale = None
        self.piano.clear_highlight()
        self.feedback_label.setText("Press 'New Scale' to start!")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 5px;")

class EarTrainingTab(QWidget):
    """Tab for ear training with visual feedback."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.total = 0
        self.current_notes = []
        self.current_answer = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.score_label)

        # Mode selector
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("<b>Exercise Mode:</b>"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Note Identification', 'Interval Identification', 'Chord Identification', 'Scale Identification'])
        self.mode_combo.currentTextChanged.connect(self._change_mode)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        # Instructions
        self.instr_label = QLabel("Press 'Play' to hear (see) the notes, then identify them.")
        self.instr_label.setWordWrap(True)
        self.instr_label.setStyleSheet("background: #e8f4f8; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.instr_label)

        # Piano
        self.piano = PianoKeyboard(start_octave=3, num_octaves=2)
        self.piano.setMinimumHeight(220)
        layout.addWidget(self.piano)

        # Answer area
        self.answer_widget = QWidget()
        self.answer_layout = QVBoxLayout(self.answer_widget)
        layout.addWidget(self.answer_widget)

        self._setup_note_mode()

        # Feedback
        self.feedback_label = QLabel("Press 'Play' to start!")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 5px;")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)

        # Controls
        controls = QHBoxLayout()

        self.play_btn = QPushButton("▶ Play")
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: #3498db; color: white; padding: 12px 24px;
                font-size: 16px; font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover { background: #2980b9; }
        """)
        self.play_btn.clicked.connect(self._play_sequence)
        controls.addWidget(self.play_btn)

        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.clicked.connect(self._show_answer)
        controls.addWidget(self.show_answer_btn)

        self.reset_btn = QPushButton("Reset Score")
        self.reset_btn.clicked.connect(self._reset_score)
        controls.addWidget(self.reset_btn)

        controls.addStretch()
        layout.addLayout(controls)

        layout.addStretch()

    def _change_mode(self, mode):
        # Clear answer widgets
        while self.answer_layout.count():
            child = self.answer_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if mode == 'Note Identification':
            self._setup_note_mode()
        elif mode == 'Interval Identification':
            self._setup_interval_mode()
        elif mode == 'Chord Identification':
            self._setup_chord_mode()
        elif mode == 'Scale Identification':
            self._setup_scale_mode()

    def _setup_note_mode(self):
        buttons_layout = QHBoxLayout()
        for note in NOTE_NAMES_SHARP:
            btn = QPushButton(note)
            btn.setMinimumSize(50, 50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px; font-weight: bold;
                    background: #3498db; color: white;
                    border-radius: 8px;
                }
                QPushButton:hover { background: #2980b9; }
            """)
            btn.clicked.connect(lambda checked, n=note: self._check_note_answer(n))
            buttons_layout.addWidget(btn)
        self.answer_layout.addLayout(buttons_layout)

    def _setup_interval_mode(self):
        grid = QGridLayout()
        row = 0
        col = 0
        for semitones in range(13):
            if semitones in INTERVALS:
                name, abbr = INTERVALS[semitones]
                btn = QPushButton(f"{name}\n({abbr})")
                btn.setMinimumSize(80, 50)
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 11px; font-weight: bold;
                        background: #9b59b6; color: white;
                        border-radius: 6px;
                    }
                    QPushButton:hover { background: #8e44ad; }
                """)
                btn.clicked.connect(lambda checked, s=semitones: self._check_interval_answer(s))
                grid.addWidget(btn, row, col)
                col += 1
                if col > 3:
                    col = 0
                    row += 1
        self.answer_layout.addLayout(grid)

    def _setup_chord_mode(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(150)

        content = QWidget()
        layout = QVBoxLayout(content)

        categories = {}
        for name, intervals, desc, cat in CHORDS:
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)

        for cat, names in categories.items():
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.addWidget(QLabel(f"<b>{cat}:</b>"))
            for name in names:
                btn = QPushButton(name)
                btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
                btn.clicked.connect(lambda checked, n=name: self._check_chord_answer(n))
                row_layout.addWidget(btn)
            row_layout.addStretch()
            layout.addWidget(row)

        scroll.setWidget(content)
        self.answer_layout.addWidget(scroll)

    def _setup_scale_mode(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(150)

        content = QWidget()
        layout = QVBoxLayout(content)

        for tradition, scales in [("Western", WESTERN_SCALES), ("Eastern", EASTERN_SCALES), ("World", WORLD_SCALES)]:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.addWidget(QLabel(f"<b>{tradition}:</b>"))
            for name, intervals, desc, cat in scales[:8]:
                btn = QPushButton(name)
                btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
                btn.clicked.connect(lambda checked, n=name: self._check_scale_answer(n))
                row_layout.addWidget(btn)
            row_layout.addStretch()
            layout.addWidget(row)

        scroll.setWidget(content)
        self.answer_layout.addWidget(scroll)

    def _play_sequence(self):
        self.piano.clear_highlight()
        self.current_notes = []
        mode = self.mode_combo.currentText()

        if mode == 'Note Identification':
            note_idx = random.randint(0, 11)
            octave = random.randint(3, 4)
            self.current_answer = NOTE_NAMES_SHARP[note_idx]
            midi_num = (octave + 1) * 12 + note_idx
            self.current_notes = [midi_num]
            self._animate_notes([midi_num])

        elif mode == 'Interval Identification':
            self.current_answer = random.randint(1, 12)
            root_idx = random.randint(0, 11)
            root_octave = random.randint(3, 4)
            second_idx = (root_idx + self.current_answer) % 12
            second_octave = root_octave + (1 if second_idx < root_idx else 0)

            root_midi = (root_octave + 1) * 12 + root_idx
            second_midi = (second_octave + 1) * 12 + second_idx
            self.current_notes = [root_midi, second_midi]
            self._animate_notes([root_midi, second_midi])

        elif mode == 'Chord Identification':
            chord_data = random.choice(CHORDS)
            self.current_chord = chord_data
            self.current_answer = chord_data[0]
            root = random.choice(NOTE_NAMES_SHARP)
            notes = get_chord_notes(root, chord_data[1])

            root_idx = NOTE_NAMES_SHARP.index(root) if root in NOTE_NAMES_SHARP else 0
            midi_nums = []
            for note in notes:
                note_idx = NOTE_NAMES_SHARP.index(note) if note in NOTE_NAMES_SHARP else 0
                octave = 4 if note_idx >= root_idx else 5
                midi_nums.append((octave + 1) * 12 + note_idx)

            self.current_notes = midi_nums
            self._animate_notes(midi_nums)

        elif mode == 'Scale Identification':
            scale_data = random.choice(ALL_SCALES)
            self.current_scale = scale_data
            self.current_answer = scale_data[0]
            root = random.choice(NOTE_NAMES_SHARP)
            notes = get_scale_notes(root, scale_data[1])

            root_idx = NOTE_NAMES_SHARP.index(root) if root in NOTE_NAMES_SHARP else 0
            midi_nums = []
            for note in notes:
                note_idx = NOTE_NAMES_SHARP.index(note) if note in NOTE_NAMES_SHARP else 0
                octave = 4 if note_idx >= root_idx else 5
                midi_nums.append((octave + 1) * 12 + note_idx)

            self.current_notes = midi_nums
            self._animate_notes(midi_nums)

        self.feedback_label.setText("What do you hear?")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #fff3cd; border-radius: 5px;")

    def _animate_notes(self, midi_nums):
        """Animate notes on piano one by one."""
        self._anim_index = 0
        self._anim_notes = midi_nums

        def next_note():
            if self._anim_index < len(self._anim_notes):
                self.piano.clear_highlight()
                midi = self._anim_notes[self._anim_index]
                self.piano.highlighted_notes[midi] = QColor(255, 200, 100)
                self.piano.update()
                self._anim_index += 1
            else:
                self._anim_timer.stop()
                self.piano.clear_highlight()

        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(next_note)
        self._anim_timer.start(400)
        next_note()

    def _check_note_answer(self, answer):
        self._check_answer(answer)

    def _check_interval_answer(self, semitones):
        self._check_answer(semitones)

    def _check_chord_answer(self, answer):
        self._check_answer(answer)

    def _check_scale_answer(self, answer):
        self._check_answer(answer)

    def _check_answer(self, answer):
        if self.current_answer is None:
            self.feedback_label.setText("Press 'Play' first!")
            return

        self.total += 1

        mode = self.mode_combo.currentText()
        if mode == 'Interval Identification':
            correct = (answer == self.current_answer)
            correct_text = f"{INTERVALS[answer][0]} ({answer} semitones)" if answer in INTERVALS else str(answer)
            actual_text = f"{INTERVALS[self.current_answer][0]} ({self.current_answer} semitones)" if self.current_answer in INTERVALS else str(self.current_answer)
        else:
            correct = (answer == self.current_answer)
            correct_text = str(answer)
            actual_text = str(self.current_answer)

        if correct:
            self.score += 1
            self.feedback_label.setText(f"✓ Correct!")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #d4edda; color: #155724; border-radius: 5px;")
        else:
            self.feedback_label.setText(f"✗ Wrong! It was {actual_text}")
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #f8d7da; color: #721c24; border-radius: 5px;")

        self.score_label.setText(f"Score: {self.score} / {self.total} ({int(self.score/self.total*100)}%)")
        self.current_answer = None

    def _show_answer(self):
        if self.current_answer is not None:
            mode = self.mode_combo.currentText()
            if mode == 'Interval Identification' and self.current_answer in INTERVALS:
                text = f"The answer is: {INTERVALS[self.current_answer][0]}"
            else:
                text = f"The answer is: {self.current_answer}"
            self.feedback_label.setText(text)
            self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; background: #d1ecf1; color: #0c5460; border-radius: 5px;")

    def _reset_score(self):
        self.score = 0
        self.total = 0
        self.score_label.setText("Score: 0 / 0")
        self.current_answer = None
        self.piano.clear_highlight()
        self.feedback_label.setText("Press 'Play' to start!")
        self.feedback_label.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 5px;")

class ReferenceTab(QWidget):
    """Tab with comprehensive music theory reference."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Music Theory Reference")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        tabs = QTabWidget()

        # Notes reference
        notes_tab = QWidget()
        notes_layout = QVBoxLayout(notes_tab)
        notes_text = QTextEdit()
        notes_text.setReadOnly(True)
        notes_text.setHtml("""
        <h2>Note Names & Accidentals</h2>
        <p>The musical alphabet uses 7 letter names: <b>A, B, C, D, E, F, G</b></p>
        <p>Each note can be modified with accidentals:</p>
        <ul>
            <li><b>♯ (Sharp)</b> - Raises a note by one semitone</li>
            <li><b>♭ (Flat)</b> - Lowers a note by one semitone</li>
            <li><b>♮ (Natural)</b> - Cancels a sharp or flat</li>
            <li><b>𝄪 (Double Sharp)</b> - Raises by two semitones</li>
            <li><b>𝄫 (Double Flat)</b> - Lowers by two semitones</li>
        </ul>
        <h3>Enharmonic Equivalents</h3>
        <p>Notes that sound the same but are written differently:</p>
        <ul>
            <li>C♯ = D♭</li>
            <li>D♯ = E♭</li>
            <li>F♯ = G♭</li>
            <li>G♯ = A♭</li>
            <li>A♯ = B♭</li>
        </ul>
        <h3>MIDI Note Numbers</h3>
        <p>MIDI uses numbers 0-127 to represent notes. Middle C (C4) is MIDI 60.</p>
        """)
        notes_layout.addWidget(notes_text)
        tabs.addTab(notes_tab, "Notes")

        # Intervals reference
        intervals_tab = QWidget()
        intervals_layout = QVBoxLayout(intervals_tab)
        intervals_text = QTextEdit()
        intervals_text.setReadOnly(True)
        intervals_text.setHtml("""
        <h2>Intervals</h2>
        <p>An interval is the distance between two pitches, measured in semitones (half steps).</p>
        <h3>Simple Intervals (within an octave)</h3>
        <table border='1' cellpadding='5'>
            <tr><th>Semitones</th><th>Name</th><th>Abbreviation</th><th>Quality</th></tr>
            <tr><td>0</td><td>Perfect Unison</td><td>P1</td><td>Perfect</td></tr>
            <tr><td>1</td><td>Minor Second</td><td>m2</td><td>Minor</td></tr>
            <tr><td>2</td><td>Major Second</td><td>M2</td><td>Major</td></tr>
            <tr><td>3</td><td>Minor Third</td><td>m3</td><td>Minor</td></tr>
            <tr><td>4</td><td>Major Third</td><td>M3</td><td>Major</td></tr>
            <tr><td>5</td><td>Perfect Fourth</td><td>P4</td><td>Perfect</td></tr>
            <tr><td>6</td><td>Tritone / Augmented Fourth</td><td>TT/A4</td><td>Augmented</td></tr>
            <tr><td>7</td><td>Perfect Fifth</td><td>P5</td><td>Perfect</td></tr>
            <tr><td>8</td><td>Minor Sixth</td><td>m6</td><td>Minor</td></tr>
            <tr><td>9</td><td>Major Sixth</td><td>M6</td><td>Major</td></tr>
            <tr><td>10</td><td>Minor Seventh</td><td>m7</td><td>Minor</td></tr>
            <tr><td>11</td><td>Major Seventh</td><td>M7</td><td>Major</td></tr>
            <tr><td>12</td><td>Perfect Octave</td><td>P8</td><td>Perfect</td></tr>
        </table>
        <h3>Interval Qualities</h3>
        <ul>
            <li><b>Perfect</b> (P): Unison, 4th, 5th, Octave - cannot be major or minor</li>
            <li><b>Major</b> (M): 2nd, 3rd, 6th, 7th - the "normal" larger version</li>
            <li><b>Minor</b> (m): 2nd, 3rd, 6th, 7th - one semitone smaller than major</li>
            <li><b>Augmented</b> (A): One semitone larger than perfect or major</li>
            <li><b>Diminished</b> (d): One semitone smaller than perfect or minor</li>
        </ul>
        """)
        intervals_layout.addWidget(intervals_text)
        tabs.addTab(intervals_tab, "Intervals")

        # Scales reference
        scales_tab = QWidget()
        scales_layout = QVBoxLayout(scales_tab)
        scales_text = QTextEdit()
        scales_text.setReadOnly(True)
        scales_text.setHtml("""
        <h2>Scale Theory</h2>
        <p>A scale is an ordered collection of pitches used as the basis for a composition.</p>
        <h3>Scale Degrees</h3>
        <p>Each note in a scale has a function:</p>
        <ul>
            <li><b>1 - Tonic</b>: The home note. Most stable.</li>
            <li><b>2 - Supertonic</b>: One step above tonic. Tendency to resolve to tonic.</li>
            <li><b>3 - Mediant</b>: Determines major/minor quality.</li>
            <li><b>4 - Subdominant</b>: Builds tension, opposite of dominant.</li>
            <li><b>5 - Dominant</b>: Strong pull back to tonic. Second most stable.</li>
            <li><b>6 - Submediant</b>: Relative minor/major relationship.</li>
            <li><b>7 - Leading Tone</b>: Strongest pull to tonic (half step below).</li>
        </ul>
        <h3>Modes of the Major Scale</h3>
        <table border='1' cellpadding='5'>
            <tr><th>Mode</th><th>Start Degree</th><th>Characteristic</th><th>Mood</th></tr>
            <tr><td>Ionian (Major)</td><td>1</td><td>Natural 3rd, 7th</td><td>Bright, stable</td></tr>
            <tr><td>Dorian</td><td>2</td><td>Raised 6th</td><td>Jazzy, Celtic</td></tr>
            <tr><td>Phrygian</td><td>3</td><td>Lowered 2nd</td><td>Spanish, dark</td></tr>
            <tr><td>Lydian</td><td>4</td><td>Raised 4th</td><td>Dreamy, floating</td></tr>
            <tr><td>Mixolydian</td><td>5</td><td>Lowered 7th</td><td>Bluesy, rock</td></tr>
            <tr><td>Aeolian (Minor)</td><td>6</td><td>Natural minor</td><td>Sad, serious</td></tr>
            <tr><td>Locrian</td><td>7</td><td>Lowered 2nd, 5th</td><td>Dark, unstable</td></tr>
        </table>
        <h3>Pentatonic Scales</h3>
        <p>Five-note scales found in virtually all musical traditions:</p>
        <ul>
            <li><b>Major Pentatonic</b>: 1-2-3-5-6 (no 4th or 7th)</li>
            <li><b>Minor Pentatonic</b>: 1-b3-4-5-b7 (no 2nd or 6th)</li>
        </ul>
        """)
        scales_layout.addWidget(scales_text)
        tabs.addTab(scales_tab, "Scales")

        # Chords reference
        chords_tab = QWidget()
        chords_layout = QVBoxLayout(chords_tab)
        chords_text = QTextEdit()
        chords_text.setReadOnly(True)
        chords_text.setHtml("""
        <h2>Chord Theory</h2>
        <p>A chord is three or more notes played simultaneously.</p>
        <h3>Triads</h3>
        <table border='1' cellpadding='5'>
            <tr><th>Type</th><th>Formula</th><th>Quality</th><th>Example (C)</th></tr>
            <tr><td>Major</td><td>1-3-5</td><td>Happy, stable</td><td>C-E-G</td></tr>
            <tr><td>Minor</td><td>1-b3-5</td><td>Sad, serious</td><td>C-Eb-G</td></tr>
            <tr><td>Diminished</td><td>1-b3-b5</td><td>Tense, unstable</td><td>C-Eb-Gb</td></tr>
            <tr><td>Augmented</td><td>1-3-#5</td><td>Mysterious</td><td>C-E-G#</td></tr>
            <tr><td>Sus2</td><td>1-2-5</td><td>Open, airy</td><td>C-D-G</td></tr>
            <tr><td>Sus4</td><td>1-4-5</td><td>Suspended</td><td>C-F-G</td></tr>
        </table>
        <h3>Seventh Chords</h3>
        <table border='1' cellpadding='5'>
            <tr><th>Type</th><th>Formula</th><th>Quality</th><th>Example (C)</th></tr>
            <tr><td>Major 7</td><td>1-3-5-7</td><td>Jazzy, sophisticated</td><td>C-E-G-B</td></tr>
            <tr><td>Dominant 7</td><td>1-3-5-b7</td><td>Bluesy, wants resolution</td><td>C-E-G-Bb</td></tr>
            <tr><td>Minor 7</td><td>1-b3-5-b7</td><td>Smooth, mellow</td><td>C-Eb-G-Bb</td></tr>
            <tr><td>Half-Diminished</td><td>1-b3-b5-b7</td><td>Tense, sophisticated</td><td>C-Eb-Gb-Bb</td></tr>
            <tr><td>Fully Diminished</td><td>1-b3-b5-bb7</td><td>Very tense</td><td>C-Eb-Gb-A</td></tr>
        </table>
        <h3>Chord Inversions</h3>
        <ul>
            <li><b>Root Position</b>: Root is the lowest note</li>
            <li><b>1st Inversion</b>: 3rd is the lowest note</li>
            <li><b>2nd Inversion</b>: 5th is the lowest note</li>
            <li><b>3rd Inversion</b>: 7th is the lowest note (7th chords only)</li>
        </ul>
        """)
        chords_layout.addWidget(chords_text)
        tabs.addTab(chords_tab, "Chords")

        # World music reference
        world_tab = QWidget()
        world_layout = QVBoxLayout(world_tab)
        world_text = QTextEdit()
        world_text.setReadOnly(True)
        world_text.setHtml("""
        <h2>World Music Theory</h2>
        <h3>Indian Classical Music (Raga System)</h3>
        <p>Ragas are melodic frameworks with specific rules:</p>
        <ul>
            <li><b>Sa (S)</b> - Tonic (fixed)</li>
            <li><b>Re (R)</b> - 2nd (komal or shuddha)</li>
            <li><b>Ga (G)</b> - 3rd (komal or shuddha)</li>
            <li><b>Ma (M)</b> - 4th (shuddha or teevra)</li>
            <li><b>Pa (P)</b> - 5th (fixed)</li>
            <li><b>Dha (D)</b> - 6th (komal or shuddha)</li>
            <li><b>Ni (N)</b> - 7th (komal or shuddha)</li>
        </ul>
        <p><b>Komal</b> = flat (lowered) | <b>Shuddha</b> = natural | <b>Teevra</b> = sharp (raised)</p>

        <h3>Arabic Maqam System</h3>
        <p>Maquamat are melodic modes with quarter-tone inflections:</p>
        <ul>
            <li><b>Ajam</b> - Similar to major scale</li>
            <li><b>Nahawand</b> - Similar to natural minor</li>
            <li><b>Hijaz</b> - Characteristic augmented 2nd</li>
            <li><b>Sikah</b> - Built on E half-flat (quarter tone)</li>
            <li><b>Rast</b> - Neutral 3rd (quarter tone)</li>
            <li><b>Bayati</b> - Built on D half-flat</li>
        </ul>

        <h3>East Asian Pentatonic Systems</h3>
        <p><b>Chinese:</b> Gong (1), Shang (2), Jiao (3), Zhi (5), Yu (6) - five modes</p>
        <p><b>Japanese:</b> Hirajoshi, Insen, Iwato, Yo, Kumoi - various pentatonic scales</p>
        <p><b>Korean:</b> Ujo (minor), Pyongjo (major), Gyemyonjo (mixed)</p>

        <h3>Gamelan (Indonesia)</h3>
        <p>Two main tuning systems:</p>
        <ul>
            <li><b>Slendro</b> - 5 notes, roughly equidistant</li>
            <li><b>Pelog</b> - 7 notes, unequal spacing (5 used at a time)</li>
        </ul>
        """)
        world_layout.addWidget(world_text)
        tabs.addTab(world_tab, "World Music")

        layout.addWidget(tabs)


# =============================================================================
# MAIN WINDOW
# =============================================================================

class MusicTheoryMaster(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Theory Master - Interactive Learning")
        self.setMinimumSize(1200, 800)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Header
        header = QLabel("🎵 Music Theory Master 🎵")
        header.setStyleSheet("""
            font-size: 28px; font-weight: bold; color: #2c3e50;
            padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Subtitle
        subtitle = QLabel("Learn Western, Eastern & World Music Theory")
        subtitle.setStyleSheet("font-size: 14px; color: #666; padding: 5px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid #dee2e6; border-radius: 5px; }
            QTabBar::tab {
                background: #e9ecef; padding: 10px 20px; margin-right: 2px;
                border-top-left-radius: 5px; border-top-right-radius: 5px;
            }
            QTabBar::tab:selected { background: #495057; color: white; }
            QTabBar::tab:hover { background: #ced4da; }
        """)

        # Add tabs
        self.tabs.addTab(ScaleExplorerTab(), "🎹 Scale Explorer")
        self.tabs.addTab(ChordExplorerTab(), "🎸 Chord Explorer")
        self.tabs.addTab(KeySignaturesTab(), "🔄 Circle of Fifths")
        self.tabs.addTab(IntervalCalculatorTab(), "📏 Interval Calculator")
        self.tabs.addTab(NoteIdentificationTab(), "🎵 Note ID Game")
        self.tabs.addTab(IntervalIdentificationTab(), "📊 Interval ID Game")
        self.tabs.addTab(ChordIdentificationTab(), "🎶 Chord ID Game")
        self.tabs.addTab(ScaleIdentificationTab(), "🌍 Scale ID Game")
        self.tabs.addTab(EarTrainingTab(), "👂 Ear Training")
        self.tabs.addTab(ReferenceTab(), "📚 Reference")

        layout.addWidget(self.tabs)

        # Status bar
        self.statusBar().showMessage("Ready - Explore scales, chords, intervals and more!")

        # Apply global stylesheet
        self.setStyleSheet("""
            QMainWindow { background: #f8f9fa; }
            QGroupBox {
                font-weight: bold; border: 2px solid #dee2e6;
                border-radius: 8px; margin-top: 10px; padding-top: 10px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QPushButton {
                padding: 8px 16px; border-radius: 5px;
                background: #6c757d; color: white;
            }
            QPushButton:hover { background: #5a6268; }
            QComboBox { padding: 5px; border-radius: 4px; }
            QListWidget { border-radius: 5px; border: 1px solid #ced4da; }
            QTableWidget { border-radius: 5px; gridline-color: #dee2e6; }
            QTableWidget::item { padding: 5px; }
            QLabel { color: #495057; }
        """)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MusicTheoryMaster()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
