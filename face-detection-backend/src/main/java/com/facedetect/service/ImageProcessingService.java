package com.facedetect.service;

import org.springframework.web.multipart.MultipartFile;

import com.facedetect.dto.FaceDetectionResponse;

/**
 * Face detection service interface
 * 
 * @author Nguyen Tuan Khanh
 */
public interface ImageProcessingService {
      /**
     * Detect faces in uploaded image
     * 
     * @param imageFile Uploaded image file
     * @param minSize Minimum face size in pixels
     * @param scaleFactor Scale factor for detection
     * @param minNeighbors Minimum neighbors for detection
     * @return Face detection response
     */
    FaceDetectionResponse detectFaces(MultipartFile imageFile, int minSize, double scaleFactor, int minNeighbors);
    
    /**
     * Validate if file is a valid image
     * 
     * @param file File to validate
     * @return true if valid image, false otherwise
     */
    boolean isValidImageFile(MultipartFile file);
}
