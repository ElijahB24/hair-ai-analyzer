# Hair AI Analyzer

An AI-powered hair texture and hairstyle classification web app built with React, FastAPI, PyTorch, and OpenCV concepts. Users can upload images or use a live webcam scanner to detect hair types in real time.

## Features

- Real-time webcam hair analysis
- Image upload support
- AI-powered hair texture prediction
- Confidence score visualization
- Drag-and-drop image uploading
- Multiple hairstyle classifications
- Responsive modern UI

## Hair Types Supported

- Braids
- Coily
- Curly
- Locs
- Straight
- Wavy

## Tech Stack

### Frontend
- React
- Vite
- react-webcam
- react-dropzone

### Backend
- FastAPI
- PyTorch
- Torchvision
- PIL

### Machine Learning
- MobileNetV2 Transfer Learning
- Custom image dataset
- Real-time computer vision predictions

---

# Installation

## Clone Repository

```bash
git clone YOUR_GITHUB_LINK
cd Hair-AI-Analyzer
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Frontend Setup

```bash
cd frontend
npm install
```

---

# Running the App

## Start Backend

From the `src` folder:

```bash
uvicorn api:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## Start Frontend

From the `frontend` folder:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# Model Training

To retrain the AI model:

```bash
python src/train.py
```

The model uses transfer learning with MobileNetV2 and a custom dataset of hairstyle images.

---

# Future Improvements

- Higher accuracy training
- More hairstyle classes
- Better lighting normalization
- Mobile optimization
- Live bounding-box hair detection
- Deployment to cloud hosting

---

# Screenshots

(Add screenshots here later)

---

# Author

Built by Elijah Brathwaite