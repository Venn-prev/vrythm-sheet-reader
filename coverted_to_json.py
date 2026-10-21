import json
import sys
from pathlib import Path

from music21 import converter
from music21 import note
from music21 import chord
from music21 import tempo
from music21 import meter
from music21 import key


# ============================================================
# MusicXML duration -> JSON duration
# ============================================================

def duration_to_json(duration):
    """
    Chuyển duration của music21 sang format:

        whole    -> "w"
        half     -> "h"
        quarter  -> "q"
        eighth   -> "8"
        16th     -> "16"
        32nd     -> "32"
        64th     -> "64"

    Với duration phức tạp / dotted:
        ưu tiên type + dot nếu có.
    """

    duration_type = duration.type

    mapping = {
        "whole": "w",
        "half": "h",
        "quarter": "q",
        "eighth": "8",
        "16th": "16",
        "32nd": "32",
        "64th": "64",
        "breve": "breve",
        "longa": "longa"
    }

    result = mapping.get(duration_type)

    if result is None:
        # fallback
        return str(duration.quarterLength)

    # dotted note
    if duration.dots > 0:
        result += "."

        if duration.dots > 1:
            result += str(duration.dots)

    return result


# ============================================================
# Pitch
# ============================================================

def get_pitch(n):
    """
    Trả về pitch dạng:

        C4
        D#4
        Bb3
        F5
    """

    if not hasattr(n, "pitch"):
        return None

    return n.pitch.nameWithOctave


# ============================================================
# Metadata
# ============================================================

def extract_metadata(score):

    result = {
        "title": None,
        "composer": None,
        "tempo": None,
        "keySignature": None,
        "timeSignature": None
    }

    # --------------------------------------------------------
    # Title / composer
    # --------------------------------------------------------

    if score.metadata:

        result["title"] = score.metadata.title
        result["composer"] = score.metadata.composer

    # --------------------------------------------------------
    # Tempo
    # --------------------------------------------------------

    tempos = score.flatten().getElementsByClass(
        tempo.MetronomeMark
    )

    if tempos:

        tempo_value = tempos[0].number

        if tempo_value is not None:
            result["tempo"] = float(tempo_value)

            # 115.0 -> 115
            if result["tempo"].is_integer():
                result["tempo"] = int(result["tempo"])

    # --------------------------------------------------------
    # Time Signature
    # --------------------------------------------------------

    time_signatures = score.flatten().getElementsByClass(
        meter.TimeSignature
    )

    if time_signatures:

        ts = time_signatures[0]

        result["timeSignature"] = {
            "beats": ts.numerator,
            "beatType": ts.denominator
        }

    # --------------------------------------------------------
    # Key Signature
    # --------------------------------------------------------

    key_signatures = score.flatten().getElementsByClass(
        key.Key
    )

    if key_signatures:

        k = key_signatures[0]

        # Ví dụ:
        # C major -> C
        # G major -> G
        # A minor -> Am

        tonic = k.tonic.name

        if k.mode:
            if k.mode.lower() == "minor":
                result["keySignature"] = tonic + "m"
            else:
                result["keySignature"] = tonic
        else:
            result["keySignature"] = tonic

    else:

        # fallback: thử KeySignature
        ks = score.flatten().getElementsByClass(
            key.KeySignature
        )

        if ks:

            result["keySignature"] = ks[0].asKey("major").tonic.name

    return result


# ============================================================
# Extract notes
# ============================================================

def extract_notes(score):

    notes = []

    note_counter = 1

    # --------------------------------------------------------
    # Lấy các part
    # --------------------------------------------------------

    parts = score.parts

    if not parts:
        parts = [score]

    # --------------------------------------------------------
    # Duyệt từng part
    # --------------------------------------------------------

    for part in parts:

        # flatten giúp lấy note từ toàn bộ score
        elements = part.flatten().notesAndRests

        for element in elements:

            # ------------------------------------------------
            # REST
            # ------------------------------------------------

            if isinstance(element, note.Rest):

                # Nếu muốn bỏ rest:
                continue

            # ------------------------------------------------
            # NOTE
            # ------------------------------------------------

            elif isinstance(element, note.Note):

                pitch = get_pitch(element)

                duration = duration_to_json(
                    element.duration
                )

                notes.append({
                    "id": f"n{note_counter}",
                    "pitch": pitch,
                    "duration": duration
                })

                note_counter += 1

            # ------------------------------------------------
            # CHORD
            # ------------------------------------------------

            elif isinstance(element, chord.Chord):

                duration = duration_to_json(
                    element.duration
                )

                # Chord có nhiều pitch.
                # Tách thành từng note.
                for p in element.pitches:

                    notes.append({
                        "id": f"n{note_counter}",
                        "pitch": p.nameWithOctave,
                        "duration": duration
                    })

                    note_counter += 1

    return notes


# ============================================================
# Main converter
# ============================================================

def convert_musicxml_to_json(
    input_file,
    output_file
):

    print(f"Reading: {input_file}")

    # --------------------------------------------------------
    # Parse MusicXML
    # --------------------------------------------------------

    score = converter.parse(input_file)

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    metadata_data = extract_metadata(score)

    # --------------------------------------------------------
    # Notes
    # --------------------------------------------------------

    notes_data = extract_notes(score)

    # --------------------------------------------------------
    # Final JSON
    # --------------------------------------------------------

    result = {
        "metadata": metadata_data,
        "notes": notes_data
    }

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("Conversion completed!")
    print(f"Notes: {len(notes_data)}")
    print(f"Output: {output_file}")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) > 3:

        print(
            "Usage: python coverted_to_json.py [input.musicxml] [output.json]"
        )

        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    input_file = (
        Path(sys.argv[1]) if len(sys.argv) >= 2 else script_dir / "download.musicxml"
    )
    output_file = (
        Path(sys.argv[2]) if len(sys.argv) == 3 else input_file.with_suffix(".json")
    )

    convert_musicxml_to_json(
        input_file,
        output_file
    )