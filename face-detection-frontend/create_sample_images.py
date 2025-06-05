"""
Script to create sample test images for Face Detection API
Creates simple test images with geometric shapes representing faces
"""

import cv2
import numpy as np
import os

def create_sample_images():
    """Create sample images for testing face detection"""
    
    # Create samples directory if it doesn't exist
    samples_dir = "samples"
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    
    # Sample 1: Single portrait-like image
    print("Creating portrait.jpg...")
    img1 = np.ones((400, 300, 3), dtype=np.uint8) * 240  # Light gray background
    
    # Draw a simple face-like shape
    center = (150, 200)
    # Face outline (circle)
    cv2.circle(img1, center, 80, (200, 180, 160), -1)  # Face color
    cv2.circle(img1, center, 80, (150, 130, 110), 2)   # Face outline
    
    # Eyes
    cv2.circle(img1, (120, 180), 8, (50, 50, 50), -1)   # Left eye
    cv2.circle(img1, (180, 180), 8, (50, 50, 50), -1)   # Right eye
    
    # Nose
    cv2.circle(img1, (150, 200), 3, (150, 130, 110), -1)
    
    # Mouth
    cv2.ellipse(img1, (150, 220), (15, 8), 0, 0, 180, (100, 80, 60), 2)
    
    cv2.imwrite(os.path.join(samples_dir, "portrait.jpg"), img1)
    
    # Sample 2: Group image with multiple faces
    print("Creating group.jpg...")
    img2 = np.ones((400, 600, 3), dtype=np.uint8) * 220  # Light background
    
    # Draw multiple face-like shapes
    faces = [(150, 150), (300, 150), (450, 150), (225, 280)]
    
    for i, center in enumerate(faces):
        # Vary face sizes slightly
        radius = 60 + (i * 5)
        
        # Face
        cv2.circle(img2, center, radius, (200, 180, 160), -1)
        cv2.circle(img2, center, radius, (150, 130, 110), 2)
        
        # Eyes
        eye_offset = radius // 3
        cv2.circle(img2, (center[0] - eye_offset//2, center[1] - eye_offset//2), 6, (50, 50, 50), -1)
        cv2.circle(img2, (center[0] + eye_offset//2, center[1] - eye_offset//2), 6, (50, 50, 50), -1)
        
        # Nose
        cv2.circle(img2, (center[0], center[1]), 2, (150, 130, 110), -1)
        
        # Mouth
        cv2.ellipse(img2, (center[0], center[1] + eye_offset//2), (12, 6), 0, 0, 180, (100, 80, 60), 2)
    
    cv2.imwrite(os.path.join(samples_dir, "group.jpg"), img2)
    
    # Sample 3: Family-style image with different sized faces
    print("Creating family.jpg...")
    img3 = np.ones((450, 500, 3), dtype=np.uint8) * 230  # Light background
    
    # Draw faces of different sizes (adults and children)
    family_faces = [
        (150, 150, 70),  # Adult 1
        (350, 150, 70),  # Adult 2
        (150, 320, 50),  # Child 1
        (350, 320, 45)   # Child 2
    ]
    
    for center_x, center_y, radius in family_faces:
        center = (center_x, center_y)
        
        # Face
        cv2.circle(img3, center, radius, (200, 180, 160), -1)
        cv2.circle(img3, center, radius, (150, 130, 110), 2)
        
        # Eyes
        eye_offset = radius // 3
        cv2.circle(img3, (center[0] - eye_offset//2, center[1] - eye_offset//2), max(4, radius//12), (50, 50, 50), -1)
        cv2.circle(img3, (center[0] + eye_offset//2, center[1] - eye_offset//2), max(4, radius//12), (50, 50, 50), -1)
        
        # Nose
        cv2.circle(img3, center, max(2, radius//25), (150, 130, 110), -1)
        
        # Mouth
        mouth_size = max(8, radius//6)
        cv2.ellipse(img3, (center[0], center[1] + eye_offset//2), (mouth_size, mouth_size//2), 0, 0, 180, (100, 80, 60), 2)
    
    cv2.imwrite(os.path.join(samples_dir, "family.jpg"), img3)
    
    # Sample 4: Test image with challenging conditions
    print("Creating challenge.jpg...")
    img4 = np.ones((400, 500, 3), dtype=np.uint8) * 180  # Darker background
    
    # Add some noise/texture
    noise = np.random.randint(0, 50, img4.shape, dtype=np.uint8)
    img4 = cv2.add(img4, noise)
    
    # Draw faces with varying lighting conditions
    challenge_faces = [(150, 150, 60), (350, 150, 65), (250, 300, 55)]
    
    for i, (center_x, center_y, radius) in enumerate(challenge_faces):
        center = (center_x, center_y)
        
        # Vary brightness for each face
        brightness = 200 - (i * 30)
        
        # Face
        cv2.circle(img4, center, radius, (brightness, brightness-20, brightness-40), -1)
        cv2.circle(img4, center, radius, (brightness-50, brightness-70, brightness-90), 2)
        
        # Eyes
        eye_offset = radius // 3
        cv2.circle(img4, (center[0] - eye_offset//2, center[1] - eye_offset//2), 5, (50, 50, 50), -1)
        cv2.circle(img4, (center[0] + eye_offset//2, center[1] - eye_offset//2), 5, (50, 50, 50), -1)
        
        # Nose and mouth
        cv2.circle(img4, center, 2, (brightness-70, brightness-90, brightness-110), -1)
        cv2.ellipse(img4, (center[0], center[1] + eye_offset//2), (10, 5), 0, 0, 180, (100, 80, 60), 2)
    
    cv2.imwrite(os.path.join(samples_dir, "challenge.jpg"), img4)
    
    print(f"\n✅ Sample images created successfully in '{samples_dir}' directory!")
    print("\nCreated files:")
    print("- portrait.jpg (1 face)")
    print("- group.jpg (4 faces)")  
    print("- family.jpg (4 faces, different sizes)")
    print("- challenge.jpg (3 faces, varying conditions)")
    print("\nYou can now use these images to test your Face Detection API!")

if __name__ == "__main__":
    create_sample_images()
