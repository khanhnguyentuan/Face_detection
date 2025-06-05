package com.facedetect.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import com.facedetect.dto.FaceDetectionResponse;

/**
 * Global exception handler for the Face Detection API
 * Handles various exceptions and returns appropriate error responses
 */
@ControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * Handle file size exceeded exception
     */    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public ResponseEntity<FaceDetectionResponse> handleMaxUploadSizeExceeded(
            MaxUploadSizeExceededException ex) {
        
        logger.error("File size exceeds maximum allowed size", ex);
        
        FaceDetectionResponse response = FaceDetectionResponse.error(
            "File size exceeds maximum allowed size (10MB)"
        );
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    /**
     * Handle illegal argument exceptions (validation errors)
     */    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<FaceDetectionResponse> handleIllegalArgument(
            IllegalArgumentException ex) {
        
        logger.error("Validation error: {}", ex.getMessage(), ex);
        
        FaceDetectionResponse response = FaceDetectionResponse.error(
            "Invalid input: " + ex.getMessage()
        );
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    /**
     * Handle runtime exceptions (processing errors)
     */    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<FaceDetectionResponse> handleRuntimeException(
            RuntimeException ex) {
        
        logger.error("Processing error: {}", ex.getMessage(), ex);
        
        FaceDetectionResponse response = FaceDetectionResponse.error(
            "Processing failed: " + ex.getMessage()
        );
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }    /**
     * Handle generic exceptions
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<FaceDetectionResponse> handleGenericException(
            Exception ex) {
        
        logger.error("Unexpected error occurred", ex);
        
        FaceDetectionResponse response = FaceDetectionResponse.error(
            "An unexpected error occurred. Please try again later."
        );
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
