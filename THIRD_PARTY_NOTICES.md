# Third-Party Notices

This file records project-level provenance notices. It is not a replacement for the license files shipped by HOMR or its dependencies. Review the applicable source, model-weight, and dependency licenses before redistributing a product.

## HOMR

- Project: [HOMR](https://github.com/liebharc/homr)
- Project author listed in `pyproject.toml`: Christian Liebhardt
- License in this checkout: GNU AGPL-3.0; see [`LICENSE`](LICENSE).
- OMR pipeline: SegNet staff segmentation followed by TrOMR transformer-based score transcription. The repository's [Training.md](Training.md) records model training and validation history.

## TrOMR

The transcription architecture is based on the TrOMR paper: [arXiv:2308.09370](https://arxiv.org/abs/2308.09370). HOMR's implementation and trained checkpoints are maintained in the HOMR repository; do not assume the paper, implementation, and checkpoints share identical licensing terms.

## SegNet

The segmentation implementation documents its basis in the [segmentation-models-pytorch CamVid example](https://github.com/qubvel-org/segmentation_models.pytorch/blob/main/examples/camvid_segmentation_multiclass.ipynb). Consult that upstream project for its license and notices.

## Relieur

`homr/relieur.py` states that the score-merging code is based on [relieur](https://github.com/papoteur-mga/relieur/tree/master), licensed under Apache-2.0, and thanks Papoteur and contributors. Preserve that source notice and include the applicable Apache-2.0 license text when distributing the covered component as required by its license.

## Dependencies and Model Weights

Python dependencies are declared in `pyproject.toml` and have their own licenses. HOMR downloads ONNX model checkpoints from the HOMR GitHub releases on first use. Verify the current checkpoint terms and any additional notices in the release before shipping those files with a product.