#!/usr/bin/env python3
"""
Simple test to check if Haar Cascade file is working
"""
import cv2
import os

def test_cascade():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    
    print(f"Testing cascade at: {cascade_path}")
    print(f"File exists: {os.path.exists(cascade_path)}")
    
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
        print(f"Cascade empty: {face_cascade.empty()}")
        
        if not face_cascade.empty():
            print("✅ Haar Cascade loaded successfully!")
            return True
        else:
            print("❌ Haar Cascade is empty")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_cascade()
