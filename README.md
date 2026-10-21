# HOMR: Optical Music Recognition

HOMR converts a raster image of printed sheet music into MusicXML. The core pipeline first detects and segments staff systems with SegNet, then transcribes the symbols on each staff with the TrOMR vision-transformer model, and finally writes MusicXML. The repository does **not** write JSON directly; JSON export is a separate conversion step described below.

## Quick Start

Requirements: Python `>=3.11,<3.16`, Poetry, and an internet connection on first run so HOMR can download its ONNX model weights and OCR data.

From PowerShell, clone the repository and install the runtime plus JSON-converter dependencies:

```powershell
git clone https://github.com/liebharc/homr.git
cd homr
python -m pip install poetry
poetry self add "poetry-dynamic-versioning[plugin]"
poetry install --only main --extras cpu --extras json
poetry run homr --init
```

Put an image such as `score.png` in `data/input/`, create an output folder, and run the two conversion steps:

```powershell
New-Item -ItemType Directory -Force -Path data/input,data/output | Out-Null
poetry run homr data/input/score.png
poetry run python coverted_to_json.py data/input/score.musicxml data/output/score.json
```

The first command creates `data/input/score.musicxml` beside the input image. The second creates `data/output/score.json` in the flat `metadata` + `notes[]` format. You can skip `--init`; HOMR downloads missing runtime weights automatically when first run. To use only HOMR's MusicXML output, install without the JSON converter extra: `poetry install --only main --extras cpu`.

The CLI also accepts PDF input, multiple images, and directories. See `poetry run homr --help` for options. When passing a directory, HOMR processes supported images recursively and writes MusicXML beside each input image.

## JSON Output

The converter is `coverted_to_json.py` (the filename is spelled this way in the repository). It reads MusicXML with `music21` and emits the source sample's shape:

```json
{
	"metadata": {
		"title": "Score title",
		"composer": "Composer",
		"tempo": 115,
		"keySignature": "C",
		"timeSignature": {"beats": 4, "beatType": 4}
	},
	"notes": [
		{"id": "n1", "pitch": "E4", "duration": "8"},
		{"id": "n2", "pitch": "G4", "duration": "q"}
	]
}
```

Duration codes are `w`, `h`, `q`, `8`, `16`, `32`, and `64`; dots are appended, for example `q.`. The current converter skips rests, flattens parts into a single notes list, and does not preserve measure numbers or note onset positions. Treat this JSON as a simple melody/export format, not a lossless MusicXML replacement. Use MusicXML when the application needs voices, rests, layout, or exact rhythmic structure.

## Algorithm and Source Attribution

This repository is the HOMR project: [github.com/liebharc/homr](https://github.com/liebharc/homr). The project metadata identifies Christian Liebhardt as author. The implementation combines staff segmentation (SegNet) and score transcription (TrOMR); see [Training.md](Training.md) for the repository's training history and validation notes. The TrOMR architecture is based on the [TrOMR paper](https://arxiv.org/abs/2308.09370). The SegNet implementation notes its basis in the [segmentation-models-pytorch CamVid example](https://github.com/qubvel-org/segmentation_models.pytorch/blob/main/examples/camvid_segmentation_multiclass.ipynb).

The score-merging code in `homr/relieur.py` is based on [relieur by Papoteur and contributors](https://github.com/papoteur-mga/relieur/tree/master), under Apache-2.0; its source file retains the original notice. Additional model weights and Python dependencies have their own terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and review each applicable license before product distribution.

## Using HOMR in a Product

The repository's [LICENSE](LICENSE) is GNU AGPL-3.0. It permits commercial use, copying, and modification under its conditions; it is not a permissive license for closed-source reuse. In particular, distributing a covered application requires providing corresponding source under the AGPL. Section 13 also requires users interacting remotely with a modified AGPL program to be offered its corresponding source. Whether a separately deployed service and a product form one covered work depends on the integration; review that question for your architecture.

Keep the license and copyright notices, include a copy of `LICENSE`, identify your modifications, and provide the required source and notices when conveying a covered work. If your product cannot comply with the AGPL, obtain a separate license from the relevant copyright holder before integrating the code. This README is project guidance, not legal advice. Do not edit or replace the AGPL text in `LICENSE`; add attribution or notices in separate files.

## Contributing and Testing

See [CONTRIBUTING.md](CONTRIBUTING.md) for code, test, provenance, and contribution-license guidance. For local development, initialize the project with `make init`; run the project checks with `make ci`.

For integrating image upload and JSON download into a website, see the [Application Integration Guide](APPLICATION_GUIDE.md).
