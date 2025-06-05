#!/usr/bin/env python3
"""
Create simple test images for face detection testing
"""
import cv2
import numpy as np
import os

def create_simple_test_image():
    """Create a simple test image without faces"""
    # Create white background
    image = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw some geometric shapes
    cv2.rectangle(image, (50, 50), (150, 150), (0, 255, 0), -1)  # Green rectangle
    cv2.circle(image, (300, 200), 80, (255, 0, 0), -1)  # Blue circle
    cv2.rectangle(image, (450, 250), (550, 350), (0, 0, 255), -1)  # Red rectangle
    
    # Add text
    cv2.putText(image, "No Faces Here", (200, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    return image

def create_face_like_image():
    """Create an image with face-like patterns"""
    # Create white background
    image = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw face-like oval
    cv2.ellipse(image, (200, 200), (80, 100), 0, 0, 360, (220, 220, 220), -1)
    
    # Draw "eyes"
    cv2.circle(image, (175, 180), 15, (0, 0, 0), -1)  # Left eye
    cv2.circle(image, (225, 180), 15, (0, 0, 0), -1)  # Right eye
    
    # Draw "nose"
    cv2.line(image, (200, 200), (200, 220), (0, 0, 0), 3)
    
    # Draw "mouth"
    cv2.ellipse(image, (200, 240), (20, 10), 0, 0, 180, (0, 0, 0), 2)
    
    # Add text
    cv2.putText(image, "Face-like Pattern", (100, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return image

def main():
    print("🖼️ Creating test images...")
    
    # Create test images
    no_face_image = create_simple_test_image()
    face_like_image = create_face_like_image()
    
    # Save in current directory
    cv2.imwrite("test_no_face.jpg", no_face_image)
    cv2.imwrite("test_face_like.jpg", face_like_image)
    
    print("✅ Created test_no_face.jpg")
    print("✅ Created test_face_like.jpg")
    print("📝 Now you can test face detection with these images")

if __name__ == "__main__":
    main()
