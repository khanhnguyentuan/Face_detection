#!/usr/bin/env python3
"""
Enhanced Face Detection Script with Parameters
"""
import cv2
import json
import sys
import os
import argparse

def remove_overlapping_faces(faces, overlap_threshold=0.3):
    """Remove overlapping face detections"""
    if len(faces) == 0:
        return faces
    
    # Convert to list for easier processing
    faces_list = [(x, y, w, h) for (x, y, w, h) in faces]
    keep = []
    
    for i, face1 in enumerate(faces_list):
        x1, y1, w1, h1 = face1
        overlap_found = False
        
        for j, face2 in enumerate(keep):
            x2, y2, w2, h2 = face2
            
            # Calculate overlap
            overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
            overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
            overlap_area = overlap_x * overlap_y
            
            area1 = w1 * h1
            area2 = w2 * h2
            
            # Check if overlap ratio is too high
            if overlap_area / min(area1, area2) > overlap_threshold:
                overlap_found = True
                break
        
        if not overlap_found:
            keep.append(face1)
    
    return keep

def detect_faces_with_params(image_path, min_size=30, scale_factor=1.1, min_neighbors=5):
    """
    Face detection function with customizable parameters
    
    Args:
        image_path: Path to the image file
        min_size: Minimum possible object size, smaller objects are ignored
        scale_factor: How much the image size is reduced at each scale
        min_neighbors: How many neighbors each candidate rectangle should retain
    """
    
    # Get absolute path to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Debug current working directory
    print(f"DEBUG: Current working directory: {os.getcwd()}", file=sys.stderr)
    print(f"DEBUG: Script directory: {script_dir}", file=sys.stderr)
    
    # Try to find cascade file với absolute paths
    cascade_files = [
        os.path.join(script_dir, 'haarcascade_frontalface_default.xml'),
        os.path.join(script_dir, 'haarcascade_frontalface_alt.xml'),
        'haarcascade_frontalface_default.xml',  # Fallback for current directory
        os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'),
        os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_alt.xml')
    ]
    face_cascade = None
    cascade_used = None
    for cascade_file in cascade_files:
        print(f"DEBUG: Trying cascade file: {cascade_file}", file=sys.stderr)
        if os.path.exists(cascade_file):
            try:
                face_cascade = cv2.CascadeClassifier(cascade_file)
                if not face_cascade.empty():
                    cascade_used = cascade_file
                    print(f"DEBUG: Successfully loaded cascade: {cascade_file}", file=sys.stderr)
                    break
                else:
                    print(f"DEBUG: Cascade file empty: {cascade_file}", file=sys.stderr)
            except Exception as e:
                print(f"DEBUG: Failed to load cascade {cascade_file}: {e}", file=sys.stderr)
                continue
        else:
            print(f"DEBUG: Cascade file not found: {cascade_file}", file=sys.stderr)
    
    if face_cascade is None or face_cascade.empty():
        return {
            "success": False,
            "message": "Could not load Haar Cascade classifier",
            "data": {
                "face_count": 0,
                "faces": []
            }
        }
    
    # Check if image exists
    if not os.path.exists(image_path):
        return {
            "success": False,
            "message": f"Image not found: {image_path}",
            "data": {
                "face_count": 0,
                "faces": []
            }
        }
    
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return {
                "success": False,
                "message": f"Could not read image: {image_path}",
                "data": {
                    "face_count": 0,
                    "faces": []
                }
            }
          # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization for better contrast
        gray = cv2.equalizeHist(gray)
        
        # Detect faces with multiple scale factors for better coverage
        all_faces = []
        
        # Use multiple detection strategies
        detection_params = [
            (scale_factor, min_neighbors),
            (max(1.05, scale_factor - 0.05), max(3, min_neighbors - 1)),
            (min(2.0, scale_factor + 0.1), min(8, min_neighbors + 2))
        ]
        
        for sf, mn in detection_params:
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=sf,
                minNeighbors=mn,
                minSize=(min_size, min_size),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            if len(faces) > 0:
                all_faces.extend(faces)
        
        # Remove duplicate/overlapping faces
        if len(all_faces) > 0:
            unique_faces = remove_overlapping_faces(all_faces)
        else:
            unique_faces = []
        
        print(f"DEBUG: Total detections before filtering: {len(all_faces)}", file=sys.stderr)
        print(f"DEBUG: Unique faces after filtering: {len(unique_faces)}", file=sys.stderr)
          # Convert faces to list format
        faces_list = []
        for (x, y, w, h) in unique_faces:
            faces_list.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            })
        
        return {
            "success": True,
            "message": "Face detection completed",
            "data": {
                "face_count": len(faces_list),
                "faces": faces_list,
                "parameters": {
                    "min_size": min_size,
                    "scale_factor": scale_factor,
                    "min_neighbors": min_neighbors
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during face detection: {str(e)}",
            "data": {
                "face_count": 0,
                "faces": []
            }
        }

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Face Detection with OpenCV')
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('--min-size', type=int, default=30, 
                        help='Minimum face size in pixels (default: 30)')
    parser.add_argument('--scale-factor', type=float, default=1.1,
                        help='Scale factor for detection (default: 1.1)')
    parser.add_argument('--min-neighbors', type=int, default=5,
                        help='Minimum neighbors for detection (default: 5)')
    
    args = parser.parse_args()
    
    # Validate parameters
    if args.min_size < 5 or args.min_size > 300:
        result = {
            "success": False,
            "message": "min_size must be between 10 and 300",
            "data": {"face_count": 0, "faces": []}
        }
        print(json.dumps(result, indent=2))
        return
    
    if args.scale_factor < 1.05 or args.scale_factor > 2.0:
        result = {
            "success": False,
            "message": "scale_factor must be between 1.05 and 2.0",
            "data": {"face_count": 0, "faces": []}
        }
        print(json.dumps(result, indent=2))
        return
    if args.min_neighbors < 1 or args.min_neighbors > 20:
        result = {
            "success": False,
            "message": "min_neighbors must be between 1 and 20",
            "data": {"face_count": 0, "faces": []}
        }
        print(json.dumps(result, indent=2))
        return
    
    # Perform face detection
    result = detect_faces_with_params(
        args.image_path, 
        args.min_size, 
        args.scale_factor, 
        args.min_neighbors
    )
    
    # Output JSON result
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
