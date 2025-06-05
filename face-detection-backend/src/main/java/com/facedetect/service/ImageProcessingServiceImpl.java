package com.facedetect.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.facedetect.dto.FaceCoordinate;
import com.facedetect.dto.FaceDetectionResponse;
import com.facedetect.dto.FaceDetectionResponse.FaceDetectionData;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Image processing service implementation
 * 
 * @author Nguyen Tuan Khanh
 */
@Service
public class ImageProcessingServiceImpl implements ImageProcessingService {
    
    private static final Logger logger = LoggerFactory.getLogger(ImageProcessingServiceImpl.class);
    
    private final ObjectMapper objectMapper;
      // Configuration
    @Value("${app.python.script-path:../python-scripts/enhanced_face_detector.py}")
    private String pythonScriptPath;
    
    @Value("${app.python.executable:python}")
    private String pythonExecutable;
    
    @Value("${app.temp.directory:#{systemProperties['java.io.tmpdir']}}")
    private String tempDirectory;
    
    @Value("${app.max.file.size:10485760}") // 10MB default
    private long maxFileSize;
    
    private static final List<String> ALLOWED_EXTENSIONS = Arrays.asList("jpg", "jpeg", "png", "bmp", "gif");
    private static final List<String> ALLOWED_MIME_TYPES = Arrays.asList(
        "image/jpeg", "image/jpg", "image/png", "image/bmp", "image/gif"
    );
    
    public ImageProcessingServiceImpl() {
        this.objectMapper = new ObjectMapper();
    }
      @Override
    public FaceDetectionResponse detectFaces(MultipartFile imageFile, int minSize, double scaleFactor, int minNeighbors) {
        logger.info("Starting face detection for file: {} with params - minSize: {}, scaleFactor: {}, minNeighbors: {}", 
                   imageFile.getOriginalFilename(), minSize, scaleFactor, minNeighbors);
        
        // Validate file
        if (!isValidImageFile(imageFile)) {
            return FaceDetectionResponse.error("Invalid image file");
        }
        
        Path tempImagePath = null;
        
        try {
            // Save uploaded file to temporary location
            tempImagePath = saveTemporaryFile(imageFile);
            logger.debug("Temporary file saved: {}", tempImagePath);            // Execute Python script with parameters
            String pythonOutput = executePythonScript(tempImagePath.toString(), minSize, scaleFactor, minNeighbors);
            logger.debug("Python script output: {}", pythonOutput);
            
            // Parse Python output
            FaceDetectionResponse response = parsePythonOutput(pythonOutput);
            logger.info("Face detection completed. Found {} faces", 
                       response.getData() != null ? response.getData().getFaceCount() : 0);
            
            return response;
            
        } catch (Exception e) {
            logger.error("Error during face detection", e);
            return FaceDetectionResponse.error("Face detection failed: " + e.getMessage());
            
        } finally {
            // Clean up temporary file
            if (tempImagePath != null) {
                cleanupTemporaryFile(tempImagePath);
            }
        }
    }
    
    @Override
    public boolean isValidImageFile(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            logger.warn("File is null or empty");
            return false;
        }
        
        // Check file size
        if (file.getSize() > maxFileSize) {
            logger.warn("File size {} exceeds maximum allowed size {}", file.getSize(), maxFileSize);
            return false;
        }
        
        // Check file extension
        String filename = file.getOriginalFilename();
        if (filename == null) {
            logger.warn("Filename is null");
            return false;
        }
        
        String extension = getFileExtension(filename).toLowerCase();
        if (!ALLOWED_EXTENSIONS.contains(extension)) {
            logger.warn("File extension '{}' is not allowed", extension);
            return false;
        }
        
        // Check MIME type
        String contentType = file.getContentType();
        if (contentType == null || !ALLOWED_MIME_TYPES.contains(contentType.toLowerCase())) {
            logger.warn("Content type '{}' is not allowed", contentType);
            return false;
        }
        
        return true;
    }
      private Path saveTemporaryFile(MultipartFile file) throws IOException {
        // Create temp directory if not exists
        Path tempDir = Paths.get(tempDirectory);
        if (!Files.exists(tempDir)) {
            Files.createDirectories(tempDir);
            logger.debug("Created temp directory: {}", tempDir.toAbsolutePath());
        }
        
        // Generate unique filename with proper extension
        String originalFilename = file.getOriginalFilename();
        String extension = originalFilename != null && originalFilename.contains(".") 
            ? originalFilename.substring(originalFilename.lastIndexOf(".")) 
            : ".jpg";
        
        String uniqueFilename = "face_detection_" + UUID.randomUUID().toString() + extension;
        Path tempPath = tempDir.resolve(uniqueFilename);
        
        // Save file
        try (InputStream inputStream = file.getInputStream()) {
            Files.copy(inputStream, tempPath);
        }
        
        logger.debug("Temporary file saved: {}", tempPath.toAbsolutePath());
        
        return tempPath;
    }    private String executePythonScript(String imagePath, int minSize, double scaleFactor, int minNeighbors) throws IOException, InterruptedException {
        // Convert to absolute path để đảm bảo Python script có thể tìm thấy file
        Path imagePathObj = Paths.get(imagePath);
        String absoluteImagePath = imagePathObj.toAbsolutePath().toString();
        
        // Build command with parameters using absolute path
        ProcessBuilder processBuilder = new ProcessBuilder();
        processBuilder.command(pythonExecutable, pythonScriptPath, absoluteImagePath, 
                              "--min-size", String.valueOf(minSize),
                              "--scale-factor", String.valueOf(scaleFactor), 
                              "--min-neighbors", String.valueOf(minNeighbors));
        
        // Log paths for debugging
        logger.info("Image path (relative): {}", imagePath);
        logger.info("Image path (absolute): {}", absoluteImagePath);
        logger.info("Working directory: {}", System.getProperty("user.dir"));
        logger.debug("Executing command: {} {} {} --min-size {} --scale-factor {} --min-neighbors {}", 
                    pythonExecutable, pythonScriptPath, absoluteImagePath, minSize, scaleFactor, minNeighbors);
        
        // Start process
        Process process = processBuilder.start();
        
        // Read output
        StringBuilder output = new StringBuilder();
        StringBuilder errorOutput = new StringBuilder();
        
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
             BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()))) {
            
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            while ((line = errorReader.readLine()) != null) {
                errorOutput.append(line).append("\n");
            }
        }
        
        // Wait for process to complete
        int exitCode = process.waitFor();
        
        if (exitCode != 0) {
            logger.error("Python script failed with exit code: {}. Error: {}", exitCode, errorOutput.toString());
            throw new RuntimeException("Python script execution failed: " + errorOutput.toString());
        }
        
        if (errorOutput.length() > 0) {
            logger.warn("Python script stderr: {}", errorOutput.toString());
        }
        
        return output.toString().trim();
    }
    
    private FaceDetectionResponse parsePythonOutput(String pythonOutput) {
        try {
            JsonNode rootNode = objectMapper.readTree(pythonOutput);
            
            boolean success = rootNode.get("success").asBoolean();
            String message = rootNode.get("message").asText();
            
            if (!success) {
                return FaceDetectionResponse.error(message);
            }
            
            JsonNode dataNode = rootNode.get("data");
            int faceCount = dataNode.get("face_count").asInt();
            
            List<FaceCoordinate> faces = new ArrayList<>();
            JsonNode facesArray = dataNode.get("faces");
            
            if (facesArray != null && facesArray.isArray()) {
                for (JsonNode faceNode : facesArray) {
                    FaceCoordinate face = new FaceCoordinate(
                        faceNode.get("x").asInt(),
                        faceNode.get("y").asInt(),
                        faceNode.get("width").asInt(),
                        faceNode.get("height").asInt()
                    );
                    faces.add(face);
                }
            }
            
            FaceDetectionData data = new FaceDetectionData(faceCount, faces);
            return FaceDetectionResponse.success(message, data);
            
        } catch (Exception e) {
            logger.error("Error parsing Python output: {}", pythonOutput, e);
            return FaceDetectionResponse.error("Failed to parse detection results");
        }
    }
    
    private void cleanupTemporaryFile(Path tempPath) {
        try {
            if (Files.exists(tempPath)) {
                Files.delete(tempPath);
                logger.debug("Temporary file deleted: {}", tempPath);
            }
        } catch (IOException e) {
            logger.warn("Failed to delete temporary file: {}", tempPath, e);
        }
    }
    
    private String getFileExtension(String filename) {
        if (filename == null) {
            return "";
        }
        
        int lastDotIndex = filename.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return "";
        }
        
        return filename.substring(lastDotIndex + 1);
    }
}
