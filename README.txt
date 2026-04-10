# PCB Local Inspection

A local Python-based PCB defect inspection prototype for comparing a perfect PCB image with defective PCB images.

## Features
- Detects visible PCB defects using classical image processing
- Supports:
  - scratch
  - missing component / major mismatch
  - dent / blob-like defect
- Saves:
  - annotated images
  - masks
  - heatmaps
  - crops
  - text reports

## Project Structure
```text
PCB_LOCAL_INSPECTION/
├── input/
├── output/
├── scripts/
├── models/
├── requirements.txt
├── README.md
└── .gitignore