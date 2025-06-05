#!/usr/bin/env python3
"""
Face Detection Script for FaceDetectAPI
Author: Nguyen Tuan Khanh
Description: Detects faces in images using OpenCV Haar Cascades
Output: JSON format with face coordinates
"""

import cv2
import numpy as np
import json
import sys
import os
import argparse
from typing import List, Dict, Any

class FaceDetector:
    """Face detection class using OpenCV Haar Cascades"""
    
    def __init__(self, cascade_path: str = None):
        """
        Initialize face detector
        
        Args:
            cascade_path: Path to Haar Cascade XML file
        """
        if cascade_path is None:
            # Default path in same directory as script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
        
        self.cascade_path = cascade_path
        self.face_cascade = self._load_cascade()
    
    def _load_cascade(self) -> cv2.CascadeClassifier:
        """Load Haar Cascade classifier"""
        if not os.path.exists(self.cascade_path):
            raise FileNotFoundError(f"Haar Cascade file not found: {self.cascade_path}")
        
        cascade = cv2.CascadeClassifier(self.cascade_path)
        if cascade.empty():
            raise ValueError(f"Failed to load Haar Cascade from: {self.cascade_path}")
        
        return cascade
    
    def detect_faces(self, image_path: str) -> Dict[str, Any]:
        """
        Detect faces in an image
        
        Args:
            image_path: Path to input image
            
        Returns:
            Dictionary with detection results in JSON format
        """
        try:
            # Validate input file
            if not os.path.exists(image_path):
                return self._create_error_response(f"Image file not found: {image_path}")
            
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return self._create_error_response(f"Failed to read image: {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Process results
            face_list = []
            for (x, y, w, h) in faces:
                face_data = {
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h)
                }
                face_list.append(face_data)
            
            # Create response
            response = {
                "success": True,
                "message": "Face detection completed successfully",
                "data": {
                    "face_count": len(face_list),
                    "faces": face_list,
                    "image_info": {
                        "width": image.shape[1],
                        "height": image.shape[0],
                        "channels": image.shape[2] if len(image.shape) > 2 else 1
                    }
                },
                "processing_info": {
                    "cascade_file": os.path.basename(self.cascade_path),
                    "detection_params": {
                        "scaleFactor": 1.1,
                        "minNeighbors": 5,
                        "minSize": [30, 30]
                    }
                }
            }
            
            return response
            
        except Exception as e:
            return self._create_error_response(f"Error during face detection: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "success": False,
            "message": error_message,
            "data": {
                "face_count": 0,
                "faces": []
            }
        }

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Face Detection using OpenCV Haar Cascades",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python face_detector.py path/to/image.jpg
  python face_detector.py --image path/to/image.jpg --cascade custom_cascade.xml
  python face_detector.py --image image.jpg --pretty
        """
    )
    
    parser.add_argument(
        'image_path',
        nargs='?',
        help='Path to input image file'
    )
    
    parser.add_argument(
        '--image', '-i',
        help='Path to input image file (alternative to positional argument)'
    )
    
    parser.add_argument(
        '--cascade', '-c',
        help='Path to Haar Cascade XML file (optional)'
    )
    
    parser.add_argument(
        '--pretty', '-p',
        action='store_true',
        help='Pretty print JSON output'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-JSON output'
    )
    
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()
    
    # Determine image path
    image_path = args.image_path or args.image
    
    if not image_path:
        if not args.quiet:
            print("❌ Error: No image path provided", file=sys.stderr)
            print("Usage: python face_detector.py <image_path>", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Initialize face detector
        detector = FaceDetector(cascade_path=args.cascade)
        
        if not args.quiet:
            print(f"🔍 Processing image: {image_path}", file=sys.stderr)
        
        # Detect faces
        result = detector.detect_faces(image_path)
        
        # Output JSON
        if args.pretty:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))
        
        # Exit with appropriate code
        sys.exit(0 if result["success"] else 1)
        
    except Exception as e:
        error_response = {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": {
                "face_count": 0,
                "faces": []
            }
        }
        
        if args.pretty:
            print(json.dumps(error_response, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(error_response, ensure_ascii=False))
        
        sys.exit(1)

if __name__ == "__main__":
    main()
