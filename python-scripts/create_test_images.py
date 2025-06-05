#!/usr/bin/env python3
"""
Create simple test images for face detection testing
"""
import cv2
import numpy as np
import os

def create_test_image():
    """Create a simple test image with geometric shapes"""
    # Create white background
    image = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw some geometric shapes to simulate a non-face image
    cv2.rectangle(image, (50, 50), (150, 150), (0, 255, 0), -1)  # Green rectangle
    cv2.circle(image, (300, 200), 80, (255, 0, 0), -1)  # Blue circle
    cv2.rectangle(image, (450, 250), (550, 350), (0, 0, 255), -1)  # Red rectangle
    
    # Add some text
    cv2.putText(image, "Test Image - No Faces", (150, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    return image

def main():
    """Create test images"""
    print("🎨 Creating test images...")
      # Create demo directory if not exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    demo_dir = os.path.join(project_dir, "demo", "sample-images")
    os.makedirs(demo_dir, exist_ok=True)
    
    # Create test image
    test_image = create_test_image()
    
    # Save test image
    test_path = os.path.join(demo_dir, "test_no_face.jpg")
    cv2.imwrite(test_path, test_image)
    
    print(f"✅ Created test image: {test_path}")
    print("📝 This image contains no faces and should return face_count: 0")

if __name__ == "__main__":
    main()
