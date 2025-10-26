# AI Analysis API 

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
[![HuggingFace Model](https://img.shields.io/badge/HuggingFace-Prithvi--EO-orange)](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-1.0-100M-sen1floods11)

**AI Analysis API** is a FastAPI-based application for **geospatial and computer vision analysis**, including **object detection**, **pothole detection**, and **land cover classification**.

---

## 🔹 Features

- **Object Detection**: Detects objects in images and highlights them in **yellow**.  
- **Pothole Detection**: Uses **MobileNet**-based model for identifying road potholes.  
- **Land Cover Classification**: Uses `Prithvi-EO` model for satellite image analysis.  

---

## 🔹 Models Used

1. **Object Detection**  
   - Highlights detected objects in **yellow bounding boxes**.

2. **Pothole Detection**  
   - Model: **MobileNet** variant trained on pothole dataset.  

3. **Land Cover Classification**  
   - Model Name: `prithivMLmods/GiD-Land-Cover-Classification`  
   - HuggingFace Model:
     ```python
     from huggingface_hub import snapshot_download

     model_path = snapshot_download("ibm-nasa-geospatial/Prithvi-EO-1.0-100M-sen1floods11")
     print("Model downloaded to:", model_path)
     ```
   - Performs **remote sensing land cover analysis**.
     
<img width="1540" height="1079" alt="APISS" src="https://github.com/user-attachments/assets/125a2232-f89c-4ba7-93a3-8f454aa4bf97" />

<img width="1618" height="585" alt="FloodSS" src="https://github.com/user-attachments/assets/5d13038c-7999-493a-ae92-dc37df6ff936" />
<img width="1024" height="1024" alt="Gemini_Generated_Image_4xynp34xynp34xyn" src="https://github.com/user-attachments/assets/5c5d8497-f6f3-4b36-8c55-b453a56ac466" />

---

## 🔹 Installation

```bash
# Clone repository
git clone https://github.com/Abhishek-Comps-Engineer/AI_Analysis_API.git
cd AI_Analysis_API

# Install dependencies
pip install -r requirements.txt
