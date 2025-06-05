package com.facedetect.dto;

import java.time.LocalDateTime;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Face detection response data transfer object
 * 
 * @author Nguyen Tuan Khanh
 */
@Schema(description = "Face detection API response")
public class FaceDetectionResponse {
    
    @Schema(description = "Success status", example = "true")
    @JsonProperty("success")
    private boolean success;
    
    @Schema(description = "Response message", example = "Face detection completed successfully")
    @JsonProperty("message")
    private String message;
    
    @Schema(description = "Face detection data")
    @JsonProperty("data")
    private FaceDetectionData data;
    
    @Schema(description = "Processing timestamp", example = "2025-06-04T10:30:00")
    @JsonProperty("timestamp")
    private LocalDateTime timestamp;
    
    // Default constructor
    public FaceDetectionResponse() {
        this.timestamp = LocalDateTime.now();
    }
    
    // Constructor for success response
    public FaceDetectionResponse(boolean success, String message, FaceDetectionData data) {
        this.success = success;
        this.message = message;
        this.data = data;
        this.timestamp = LocalDateTime.now();
    }
      // Static factory methods
    public static FaceDetectionResponse success(String message, FaceDetectionData data) {
        return new FaceDetectionResponse(true, message, data);
    }
      public static FaceDetectionResponse error(String message) {
        FaceDetectionData emptyData = new FaceDetectionData();
        emptyData.setFaceCount(0);
        emptyData.setFaces(List.of());
        return new FaceDetectionResponse(false, message, emptyData);
    }
    
    // Getters and Setters
    public boolean isSuccess() {
        return success;
    }
    
    public void setSuccess(boolean success) {
        this.success = success;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public FaceDetectionData getData() {
        return data;
    }
    
    public void setData(FaceDetectionData data) {
        this.data = data;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    /**
     * Nested class for face detection data
     */
    @Schema(description = "Face detection result data")
    public static class FaceDetectionData {
        
        @Schema(description = "Number of faces detected", example = "2")
        @JsonProperty("face_count")
        private int faceCount;
        
        @Schema(description = "List of detected face coordinates")
        @JsonProperty("faces")
        private List<FaceCoordinate> faces;
        
        // Default constructor
        public FaceDetectionData() {
            this.faceCount = 0;
            this.faces = List.of();
        }
        
        // Constructor with parameters
        public FaceDetectionData(int faceCount, List<FaceCoordinate> faces) {
            this.faceCount = faceCount;
            this.faces = faces != null ? faces : List.of();
        }
        
        // Getters and Setters
        public int getFaceCount() {
            return faceCount;
        }
        
        public void setFaceCount(int faceCount) {
            this.faceCount = faceCount;
        }
        
        public List<FaceCoordinate> getFaces() {
            return faces;
        }
        
        public void setFaces(List<FaceCoordinate> faces) {
            this.faces = faces != null ? faces : List.of();
            this.faceCount = this.faces.size();
        }
    }
}
