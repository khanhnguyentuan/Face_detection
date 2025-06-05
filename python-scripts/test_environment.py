#!/usr/bin/env python3
"""
Test script to verify OpenCV installation and basic face detection setup
"""
import cv2
import numpy as np
import sys
import os

def test_opencv_installation():
    """Test if OpenCV is properly installed"""
    print("🔍 Testing OpenCV installation...")
    print(f"OpenCV version: {cv2.__version__}")
    print("✅ OpenCV installed successfully!")
    return True

def test_haar_cascade_loading():
    """Test if Haar Cascade file can be loaded"""
    print("\n🔍 Testing Haar Cascade loading...")
    
    # Get current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    
    if not os.path.exists(cascade_path):
        print(f"❌ Haar Cascade file not found at: {cascade_path}")
        return False
    
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            print("❌ Failed to load Haar Cascade classifier")
            return False
        
        print("✅ Haar Cascade loaded successfully!")
        print(f"📁 Cascade file location: {cascade_path}")
        return True
    
    except Exception as e:
        print(f"❌ Error loading Haar Cascade: {str(e)}")
        return False

def test_image_processing():
    """Test basic image processing capabilities"""
    print("\n🔍 Testing basic image processing...")
    
    try:
        # Create a simple test image
        test_image = np.zeros((300, 300, 3), dtype=np.uint8)
        test_image[:] = (255, 255, 255)  # White background
        
        # Convert to grayscale
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        
        print("✅ Basic image processing works!")
        print(f"📊 Test image shape: {test_image.shape}")
        print(f"📊 Grayscale image shape: {gray.shape}")
        return True
    
    except Exception as e:
        print(f"❌ Error in image processing: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting OpenCV and Face Detection Environment Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: OpenCV Installation
    if test_opencv_installation():
        tests_passed += 1
    
    # Test 2: Haar Cascade Loading
    if test_haar_cascade_loading():
        tests_passed += 1
    
    # Test 3: Basic Image Processing
    if test_image_processing():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Environment is ready for face detection.")
        print("✅ You can proceed to implement face_detector.py")
        return True
    else:
        print("❌ Some tests failed. Please check the setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
