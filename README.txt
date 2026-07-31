<div align="center">

# 🔍 PCB Local Inspection

### Classical Computer Vision for Local PCB Defect Detection

**Compare a reference PCB with defective samples, locate suspicious regions, and generate inspection-ready visual outputs.**

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Processing-100%25%20Local-16A34A?style=for-the-badge" alt="Local Processing" />
  <img src="https://img.shields.io/badge/Model-No%20Training%20Required-F59E0B?style=for-the-badge" alt="No Training Required" />
</p>

<p>
  <img src="https://img.shields.io/badge/Inspection-Front%20%26%20Back-0891B2?style=flat-square" alt="Front and Back Inspection" />
  <img src="https://img.shields.io/badge/Output-Masks%20%7C%20Heatmaps%20%7C%20Reports-7C3AED?style=flat-square" alt="Inspection Outputs" />
</p>

[Overview](#-overview) •
[Features](#-features) •
[Workflow](#-inspection-workflow) •
[Setup](#-local-setup) •
[Usage](#-how-to-use) •
[Limitations](#-current-limitations)

</div>

---

## 📌 Overview

**PCB Local Inspection** is a Python-based prototype for visually comparing a known-good printed circuit board with one or more potentially defective PCB images.

The system runs entirely on the local machine and uses classical image-processing techniques rather than a trained deep-learning model. It aligns each defective image with its matching reference image, calculates visual differences, detects suspicious regions, and produces annotated inspection outputs.

The current implementation supports separate inspection workflows for the **front** and **back** sides of a PCB.

> **Reference PCB + Defective PCB → Alignment → Difference Analysis → Defect Detection → Inspection Outputs**

---

## 🎯 Project Objective

Manual PCB inspection can be slow, inconsistent, and difficult when small visual defects must be identified across multiple boards.

This project explores a lightweight local inspection workflow that can:

* Compare defective PCB images against a perfect reference
* Identify visible differences automatically
* Separate suspicious regions into basic defect categories
* Produce visual and text-based outputs for review
* Run without cloud services or model training

The project is intended as a **classical computer-vision prototype**, not as a production-certified Automated Optical Inspection system.

---

## ✨ Features

### 🖼️ Reference-Based Inspection

* Uses one known-good reference image for each PCB side
* Processes multiple defective images in one run
* Supports separate `front` and `back` inspection folders
* Automatically resizes large images while preserving aspect ratio

### 📐 Image Alignment

* Resizes the defective image to match the reference dimensions when required
* Uses OpenCV ECC registration with an affine motion model
* Falls back to resize-only processing when ECC alignment fails
* Records the alignment result inside the generated report

### 🔎 Classical Defect Detection

The current prototype contains three independent detectors:

| Detector                           | Main approach                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------ |
| Scratch                            | Absolute difference, Canny edges, Hough line detection, shape filtering        |
| Missing component / major mismatch | Absolute difference, thresholding, morphology, contour filtering               |
| Dent / blob-like defect            | Absolute difference, thresholding, morphology, area and aspect-ratio filtering |

### 📦 Batch Processing

* Processes all supported images inside the defective folders
* Supports JPG, JPEG, PNG, BMP, TIFF, and WebP images
* Runs both front-side and back-side inspection in one command
* Creates missing output directories automatically

### 📊 Inspection Outputs

For every processed image, the project can generate:

* Annotated PCB image
* Combined binary defect mask
* Color heatmap
* Cropped suspicious regions
* Text inspection report

---

## 🧠 Detection Methods

### 1. Missing Component or Major Mismatch

The detector:

1. Converts the reference and inspected images to grayscale
2. Calculates their absolute pixel difference
3. Applies Gaussian blur
4. Uses binary thresholding
5. Cleans the mask using morphological opening and closing
6. Extracts contours
7. Filters very small regions using contour area and bounding-box size

This detector is intended to locate large visual changes such as absent components, displaced regions, or major mismatches.

---

### 2. Scratch Detection

The scratch detector:

1. Calculates the grayscale difference between both images
2. Applies Gaussian smoothing
3. Extracts edges using Canny detection
4. Expands the edges using dilation
5. Finds line segments using the Probabilistic Hough Transform
6. Filters lines using length and angle
7. Groups the remaining regions into bounding boxes
8. Removes regions that are not sufficiently elongated

This method is designed to find narrow, line-like changes that may represent visible scratches.

---

### 3. Dent or Blob-Like Defect

The detector:

1. Calculates the grayscale difference
2. Applies Gaussian blur
3. Creates a binary difference mask
4. Performs morphological opening and closing
5. Extracts connected contours
6. Filters regions by area
7. Removes highly elongated shapes using aspect ratio

This method targets compact, irregular visual changes that differ from line-shaped scratches.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    A["Reference PCB Image"] --> N1["Image Normalization"]
    B["Defective PCB Image"] --> N2["Image Normalization"]

    N1 --> AL["ECC Affine Alignment"]
    N2 --> AL

    AL --> M["Missing / Mismatch Detector"]
    AL --> S["Scratch Detector"]
    AL --> D["Dent / Blob Detector"]

    M --> CM["Combined Defect Mask"]
    S --> CM
    D --> CM

    M --> R["Detection Results"]
    S --> R
    D --> R

    CM --> H["Heatmap"]
    CM --> BM["Binary Mask"]
    R --> AN["Annotated Image"]
    R --> CR["Defect Crops"]
    R --> TR["Text Report"]
```

---

## 🔄 Inspection Workflow

```mermaid
flowchart TD
    A(["Start Inspection"]) --> B["Load first reference image"]
    B --> C["Load defective PCB image"]
    C --> D["Resize and normalize images"]
    D --> E{"ECC alignment successful?"}

    E -- Yes --> F["Use affine-aligned image"]
    E -- No --> G["Use resized image"]
    F --> H["Run three defect detectors"]
    G --> H

    H --> I["Combine detector masks"]
    I --> J["Draw labeled bounding boxes"]
    J --> K["Save annotated image"]
    J --> L["Save defect crops"]
    I --> M["Save binary mask"]
    I --> N["Generate heatmap"]
    H --> O["Write text report"]

    K --> P{"More defective images?"}
    L --> P
    M --> P
    N --> P
    O --> P

    P -- Yes --> C
    P -- No --> Q(["Inspection Complete"])
```

---

## 🧩 Project Structure

```text
PCB_LOCAL_INSPECTION/
│
├── input/
│   ├── reference/
│   │   ├── front/             # Known-good front PCB image
│   │   └── back/              # Known-good back PCB image
│   │
│   └── defective/
│       ├── front/             # Front-side images to inspect
│       └── back/              # Back-side images to inspect
│
├── output/
│   ├── annotated/             # Images with labeled bounding boxes
│   ├── masks/                 # Combined binary defect masks
│   ├── heatmaps/              # Colorized defect masks
│   ├── crops/                 # Cropped suspicious regions
│   └── reports/               # Text inspection reports
│
├── scripts/
│   ├── config.py              # Project paths and processing settings
│   ├── utils.py               # Image, directory, and file utilities
│   ├── preprocess.py          # Image normalization and board masking
│   ├── align.py               # ECC image alignment
│   ├── detect_classical.py    # Classical defect detectors
│   └── run_inspection.py      # Main batch inspection runner
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠️ Technology Stack

| Category              | Technology                       |
| --------------------- | -------------------------------- |
| Programming language  | Python                           |
| Computer vision       | OpenCV                           |
| Numerical processing  | NumPy                            |
| Image support         | Pillow                           |
| Configuration support | PyYAML                           |
| Progress utilities    | tqdm                             |
| Processing type       | Local, classical computer vision |
| Model training        | Not required                     |

---

## 🚀 Local Setup

### Prerequisites

* Python 3.x
* `pip`
* Reference and defective PCB images captured from similar viewpoints

### 1. Clone the Repository

```bash
git clone https://github.com/Nithish-code17/PCB_LOCAL_INSPECTION.git
cd PCB_LOCAL_INSPECTION
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📁 Prepare the Input Images

Place the known-good reference images inside:

```text
input/reference/front/
input/reference/back/
```

Place the PCB images that must be inspected inside:

```text
input/defective/front/
input/defective/back/
```

Example:

```text
input/
├── reference/
│   ├── front/
│   │   └── perfect_front.png
│   └── back/
│       └── perfect_back.png
│
└── defective/
    ├── front/
    │   ├── pcb_front_01.png
    │   └── pcb_front_02.png
    └── back/
        └── pcb_back_01.png
```

> The program uses the first valid image found in each reference folder.

---

## ▶️ How to Use

Run the inspection script from the repository root:

```bash
python scripts/run_inspection.py
```

Example terminal output:

```text
[INFO] Processing front: pcb_front_01.png
[INFO] Processing front: pcb_front_02.png
[INFO] Processing back: pcb_back_01.png
[DONE] Inspection complete.
```

If a reference or defective folder is empty, the program prints a warning and continues with the remaining side.

---

## 📤 Generated Outputs

For an input such as:

```text
input/defective/front/pcb_front_01.png
```

the system generates files similar to:

```text
output/
├── annotated/
│   └── front_pcb_front_01_annotated.png
├── masks/
│   └── front_pcb_front_01_mask.png
├── heatmaps/
│   └── front_pcb_front_01_heatmap.png
├── crops/
│   ├── crop_1.png
│   ├── crop_2.png
│   └── ...
└── reports/
    └── front_pcb_front_01_report.txt
```

### Bounding-Box Colors

| Defect type                        | Color  |
| ---------------------------------- | ------ |
| Scratch                            | Red    |
| Missing component / major mismatch | Blue   |
| Dent / blob-like defect            | Orange |

---

## 📝 Report Format

A generated text report contains:

```text
Image: pcb_front_01.png
Side: front
Alignment: {'method': 'ecc', 'ok': True}
Total defects: 3

Defect #1
  Type : scratch
  Score: 170.0
  BBox : (250, 522, 46, 12)
```

### Understanding the Fields

* `Type` — detector category assigned to the region
* `BBox` — bounding box in `(x, y, width, height)` format
* `Alignment` — whether ECC alignment succeeded
* `Score` — contour area used by the detector

> The score is a geometric area value, not an AI confidence percentage.

---

## ⚙️ Important Configuration

The project currently uses:

```python
MAX_DIM = 1600
```

Images larger than this value are resized while preserving aspect ratio.

The detector thresholds, contour limits, angle filters, and morphology kernels are defined directly inside:

```text
scripts/detect_classical.py
```

These values may need calibration when the PCB design, lighting, camera distance, or image resolution changes.

---

## ✅ Best Results

For more consistent inspection:

* Use the same camera for reference and defective images
* Keep the camera angle fixed
* Maintain similar lighting
* Use a stable PCB position
* Avoid shadows and reflections
* Keep the background consistent
* Capture both images at similar resolution
* Use a clean, defect-free reference PCB

---

## ⚠️ Current Limitations

* The project uses fixed thresholds and handcrafted rules.
* It does not contain a trained classification or object-detection model.
* Lighting, rotation, reflections, and camera-position changes can create false positives.
* Different detectors can identify overlapping regions and count the same defect more than once.
* There is no confidence calibration or accuracy benchmark.
* The reported score is contour area rather than prediction confidence.
* Only the first image in each reference folder is used.
* Crop filenames do not currently include the source image name and can be overwritten during batch processing.
* The board-mask helper exists, but the main inspection runner does not currently apply it.
* The project has no graphical user interface.
* Thresholds are not automatically adapted for different PCB designs.

---

## 🔮 Future Enhancements

* [ ] Add duplicate detection and overlapping-box merging
* [ ] Include source image names in crop filenames
* [ ] Apply the PCB board mask before defect analysis
* [ ] Add automatic threshold calibration
* [ ] Add SSIM-based structural comparison
* [ ] Add ORB or feature-based alignment fallback
* [ ] Add perspective correction
* [ ] Add a Streamlit inspection dashboard
* [ ] Add per-defect severity levels
* [ ] Generate CSV or PDF reports
* [ ] Add batch summary statistics
* [ ] Train a YOLO or segmentation model for defect classification
* [ ] Create a labeled evaluation dataset
* [ ] Measure precision, recall, and false-positive rate

---

## 🔐 Privacy

All PCB images are processed locally. The current project does not upload inspection data to an external API or cloud service.

This makes it suitable for early experimentation with private PCB images, provided the local machine and repository files are secured correctly.

---

## 👨‍💻 Author

<div align="center">

### Nithish Sarwin

**Artificial Intelligence & Machine Learning Student | Java and Backend Developer**

[![GitHub](https://img.shields.io/badge/GitHub-Nithish--code17-181717?style=for-the-badge\&logo=github)](https://github.com/Nithish-code17)

</div>

---

<div align="center">

**A lightweight first step toward automated PCB visual quality inspection.**

⭐ Star the repository if you find the project useful.

</div>
