package com.facedetect.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;

/**
 * OpenAPI/Swagger configuration for the Face Detection API
 */
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI faceDetectionOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Face Detection API")
                        .description("Professional face detection service using Spring Boot and OpenCV Python integration. " +
                                   "Upload images and get precise face coordinates for computer vision applications.")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Nguyen Tuan Khanh")
                                .email("your.email@example.com")
                                .url("https://github.com/yourusername"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")));
    }
}
