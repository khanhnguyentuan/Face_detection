# Sample Images for Face Detection Testing

This directory contains sample images for testing the Face Detection API.

## Available Sample Images:

### 1. portrait.jpg
- **Description**: Single person portrait photo
- **Best settings**: minSize: 30-50, scaleFactor: 1.1, minNeighbors: 5
- **Expected faces**: 1

### 2. group.jpg  
- **Description**: Group photo with multiple people
- **Best settings**: minSize: 15-25, scaleFactor: 1.05, minNeighbors: 3-4
- **Expected faces**: 3-5

### 3. family.jpg
- **Description**: Family photo with adults and children
- **Best settings**: minSize: 20-30, scaleFactor: 1.1, minNeighbors: 4
- **Expected faces**: 2-4

## Testing Tips:

1. **Start with default settings** (minSize: 20, scaleFactor: 1.1, minNeighbors: 4)
2. **Adjust minSize** based on the smallest faces you want to detect
3. **Lower scaleFactor** for more accuracy (slower processing)
4. **Higher minNeighbors** to reduce false positives

## Creating Your Own Test Images:

For best results with the face detection algorithm:
- Use clear, well-lit images
- Faces should be at least 30x30 pixels
- Avoid heavily shadowed or blurred faces
- JPG, PNG, BMP formats are supported
- Maximum file size: 10MB
