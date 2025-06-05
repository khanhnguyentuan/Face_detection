#!/usr/bin/env python3
"""
Simplified Face Detection Script - Working Version
"""
import cv2
import json
import sys
import os

def detect_faces_simple(image_path):
    """Simple face detection function"""
    
    # Try to find cascade file
    cascade_files = [
        'haarcascade_frontalface_default.xml',
        'haarcascade_frontalface_alt.xml'
    ]
    
    face_cascade = None
    for cascade_file in cascade_files:
        if os.path.exists(cascade_file):
            try:
                face_cascade = cv2.CascadeClassifier(cascade_file)
                if not face_cascade.empty():
                    break
            except:
                continue
    
    # If no local file works, try using cv2 data
    if face_cascade is None or face_cascade.empty():
        try:
            # This should work with OpenCV installation
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            return {
                "success": False,
                "message": "Could not load face cascade",
                "data": {"face_count": 0, "faces": []}
            }
    
    # Check if image exists
    if not os.path.exists(image_path):
        return {
            "success": False,
            "message": f"Image not found: {image_path}",
            "data": {"face_count": 0, "faces": []}
        }
    
    # Read and process image
    try:
        image = cv2.imread(image_path)
        if image is None:
            return {
                "success": False,
                "message": f"Could not read image: {image_path}",
                "data": {"face_count": 0, "faces": []}
            }
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Format results
        face_list = []
        for (x, y, w, h) in faces:
            face_list.append({
                "x": int(x),
                "y": int(y), 
                "width": int(w),
                "height": int(h)
            })
        
        return {
            "success": True,
            "message": "Face detection completed",
            "data": {
                "face_count": len(face_list),
                "faces": face_list
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing image: {str(e)}",
            "data": {"face_count": 0, "faces": []}
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_face_detector.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = detect_faces_simple(image_path)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
