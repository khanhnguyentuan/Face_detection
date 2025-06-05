package com.facedetect.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.facedetect.dto.FaceDetectionResponse;
import com.facedetect.service.ImageProcessingService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;

/**
 * REST Controller for Face Detection API
 * Provides endpoints for uploading images and detecting faces
 */
@RestController
@RequestMapping("/api/face-detection")
@Tag(name = "Face Detection", description = "Face detection API using OpenCV")
@CrossOrigin(origins = "*", allowedHeaders = "*", methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.OPTIONS})
public class ImageProcessingController {

    @Autowired
    private ImageProcessingService imageProcessingService;

    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    @Operation(summary = "Health Check", description = "Check if the API is running")
    @ApiResponse(responseCode = "200", description = "API is healthy")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Face Detection API is running!");
    }

    /**
     * Detect faces in uploaded image
     */
    @PostMapping(value = "/detect", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(
        summary = "Detect Faces", 
        description = "Upload an image and detect faces using OpenCV. Returns coordinates of detected faces."
    )
    @ApiResponses(value = {
        @ApiResponse(
            responseCode = "200", 
            description = "Face detection completed successfully",
            content = @Content(schema = @Schema(implementation = FaceDetectionResponse.class))
        ),
        @ApiResponse(responseCode = "400", description = "Invalid file format or size"),
        @ApiResponse(responseCode = "500", description = "Internal server error during processing")
    })
    public ResponseEntity<FaceDetectionResponse> detectFaces(
        @Parameter(description = "Image file to process (JPG, PNG, JPEG)", required = true)
        @RequestParam("image") MultipartFile imageFile,
        
        @Parameter(description = "Minimum face size (default: 10)", required = false)
        @RequestParam(value = "minSize", defaultValue = "10") int minSize,
        
        @Parameter(description = "Scale factor for detection (default: 1.1)", required = false)
        @RequestParam(value = "scaleFactor", defaultValue = "1.1") double scaleFactor,
        
        @Parameter(description = "Minimum neighbors (default: 1)", required = false)
        @RequestParam(value = "minNeighbors", defaultValue = "1") int minNeighbors
    ) {
        
        // Process the image and detect faces
        FaceDetectionResponse response = imageProcessingService.detectFaces(
            imageFile, minSize, scaleFactor, minNeighbors
        );
        
        return ResponseEntity.ok(response);
    }

    /**
     * Get API information
     */
    @GetMapping("/info")
    @Operation(summary = "API Information", description = "Get information about the Face Detection API")
    public ResponseEntity<Object> getApiInfo() {
        return ResponseEntity.ok(new Object() {
            public final String name = "Face Detection API";
            public final String version = "1.0.0";
            public final String description = "OpenCV-based face detection service";
            public final String author = "Nguyen Tuan Khanh";
            public final String[] supportedFormats = {"JPG", "JPEG", "PNG"};
            public final int maxFileSize = 10; // MB
        });
    }

    /**
     * Get detection parameters information
     */
    @GetMapping("/parameters")
    @Operation(summary = "Detection Parameters", description = "Get information about available detection parameters")
    public ResponseEntity<Object> getParameters() {
        return ResponseEntity.ok(new Object() {
            public final Object minSize = new Object() {
                public final String description = "Minimum face size in pixels";
                public final int defaultValue = 30;
                public final int minValue = 10;
                public final int maxValue = 300;
            };
            public final Object scaleFactor = new Object() {
                public final String description = "How much the image size is reduced at each scale";
                public final double defaultValue = 1.1;
                public final double minValue = 1.05;
                public final double maxValue = 2.0;
            };
            public final Object minNeighbors = new Object() {
                public final String description = "How many neighbors each candidate rectangle should retain";
                public final int defaultValue = 5;
                public final int minValue = 1;
                public final int maxValue = 10;
            };
        });
    }
}
