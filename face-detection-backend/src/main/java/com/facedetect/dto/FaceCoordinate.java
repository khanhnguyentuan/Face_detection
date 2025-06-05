package com.facedetect.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Face coordinate data transfer object
 * 
 * @author Nguyen Tuan Khanh
 */
@Schema(description = "Face coordinate information")
public class FaceCoordinate {
    
    @Schema(description = "X coordinate of face", example = "100")
    @JsonProperty("x")
    private int x;
    
    @Schema(description = "Y coordinate of face", example = "150")
    @JsonProperty("y")
    private int y;
    
    @Schema(description = "Width of face", example = "80")
    @JsonProperty("width")
    private int width;
    
    @Schema(description = "Height of face", example = "90")
    @JsonProperty("height")
    private int height;
    
    // Default constructor
    public FaceCoordinate() {}
    
    // Constructor with parameters
    public FaceCoordinate(int x, int y, int width, int height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
    
    // Getters and Setters
    public int getX() {
        return x;
    }
    
    public void setX(int x) {
        this.x = x;
    }
    
    public int getY() {
        return y;
    }
    
    public void setY(int y) {
        this.y = y;
    }
    
    public int getWidth() {
        return width;
    }
    
    public void setWidth(int width) {
        this.width = width;
    }
    
    public int getHeight() {
        return height;
    }
    
    public void setHeight(int height) {
        this.height = height;
    }
    
    @Override
    public String toString() {
        return String.format("FaceCoordinate{x=%d, y=%d, width=%d, height=%d}", 
                            x, y, width, height);
    }
}
