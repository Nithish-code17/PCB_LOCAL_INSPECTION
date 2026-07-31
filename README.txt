PCB Local Inspection:

A Python-based local PCB defect inspection prototype that compares a perfect reference PCB image with defective PCB images and identifies visible defects such as scratches, missing components, and dent/blob-like damage
Project Objective:

This project is built as a local prototype for automated PCB visual inspection. The goal is to detect visible defects from static PCB images using classical computer vision techniques.

The current system focuses on:

- scratch detection
- missing component / major mismatch detection
- dent / blob-like defect dete
- annotated visual output generation
- heatmap generation
- cropped defect views
- text-based inspection reports

Key Idea

The system takes:
- one perfect PCB image as reference
- one or more defective PCB images

It then:
1. aligns the defective image with the reference image
2. compares both images
3. identifies suspicious regions
4. classifies them into defect categories
5. saves the inspection output

Features

- Local/manual workflow
- No UI required
- Works on front and back PCB images
- Saves annotated images
- Saves heatmaps and masks
- Saves defect crops
- Saves text inspection reports

Supported Defect Types

The current prototype detects:

- Scratch
- Missing component / major mismatch
- Dent / blob-like defect

Project Structure

```text
PCB_LOCAL_INSPECTION/
├── input/
│   ├── reference/
│   │   ├── front/
│   │   └── back/
│   └── defective/
│       ├── front/
│       └── back/
│
├── output/
│   ├── annotated/
│   ├── masks/
│   ├── heatmaps/
│   ├── crops/
│   └── reports/
│
├── scripts/
│   ├── config.py
│   ├── utils.py
│   ├── preprocess.py
│   ├── align.py
│   ├── detect_classical.py
│   └── run_inspection.py
│
├── docs/
│   └── images/
│
├── requirements.txt
├── README.md
└── .gitignore
## Updated on July 2026
