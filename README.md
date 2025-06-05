# 👥 Face Detection System

A complete face detection system with REST API backend and modern web frontend, built with Spring Boot and vanilla JavaScript.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Java](https://img.shields.io/badge/Java-17+-orange.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.0+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Sample Images](#sample-images)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Face Detection**: Fast and accurate face detection using OpenCV Haar Cascades
- **REST API**: Clean RESTful API built with Spring Boot
- **Modern Web Interface**: Responsive frontend with drag-and-drop image upload
- **Parameter Tuning**: Adjustable detection parameters (minSize, scaleFactor, minNeighbors)
- **Visual Results**: Interactive face detection with bounding boxes overlay
- **Sample Images**: Pre-loaded test images for quick testing
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling and user feedback
- **Performance Metrics**: Processing time and detection statistics

## 🎬 Demo

### Video Demo
*📹 [Demo Video](https://youtu.be/bLiLCBRuZGk)*

> **Note**: Video demo coming soon! Will showcase real-time face detection with parameter tuning.

### Screenshots

#### Main Interface
![Main Interface]
![image](https://github.com/user-attachments/assets/c372b17c-9946-49d0-9dad-f431a8245df6)

*Modern, responsive web interface with drag-and-drop upload*

#### Face Detection Results
![Detection Results]
![image](https://github.com/user-attachments/assets/545e01a4-4386-4afc-bc45-70b128e6736f)

*Real-time face detection with bounding boxes and detailed statistics*

#### Parameter Tuning
![Parameter Settings]
![image](https://github.com/user-attachments/assets/e8f6ed5f-8240-41a6-af58-60774c1ee84b)

*Adjustable detection parameters for optimal results*


## 🏗️ Architecture

```
Face Detection System
├── Backend (Spring Boot)
│   ├── REST API Controller
│   ├── Image Processing Service  
│   ├── OpenCV Integration
│   └── CORS Configuration
├── Frontend (Vanilla JS)
│   ├── Responsive Web Interface
│   ├── Canvas-based Visualization
│   ├── Real-time Parameter Control
│   └── Sample Image Gallery
└── Python Scripts
    ├── Environment Testing
    ├── Sample Image Generation
    └── Standalone Detectors
```

## 🛠️ Technologies

### Backend
- **Java 17+**
- **Spring Boot 3.0+**
- **OpenCV Java 4.8.0**
- **Maven** for dependency management
- **Swagger/OpenAPI** for API documentation

### Frontend
- **HTML5 & CSS3**
- **Vanilla JavaScript (ES6+)**
- **Bootstrap 5** for responsive design
- **Font Awesome** for icons
- **Canvas API** for visualization

### Development Tools
- **Python 3.8+** for utilities
- **Git** for version control
- **IntelliJ IDEA / VS Code**

## 🚀 Installation

### Prerequisites

1. **Java 17+** - [Download](https://adoptium.net/)
2. **Maven 3.6+** - [Download](https://maven.apache.org/download.cgi)
3. **Python 3.8+** (optional, for utilities) - [Download](https://python.org/downloads/)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/face-detection-system.git
   cd face-detection-system
   ```

2. **Start the Backend API**
   ```bash
   cd face-detection-backend
   mvn clean install
   mvn spring-boot:run
   ```
   
   Or use the batch file:
   ```bash
   start-api.bat
   ```

3. **Start the Frontend**
   ```bash
   cd face-detection-frontend
   # Using Python
   python -m http.server 3000
   
   # Or using Node.js
   npx serve -l 3000
   ```

4. **Open your browser**
   ```
   http://localhost:3000
   ```

## 📖 Usage

### Basic Usage

1. **Upload an Image**: Drag and drop or click to select an image file
2. **Adjust Parameters** (optional):
   - **Min Size**: Minimum face size in pixels (default: 20)
   - **Scale Factor**: Image pyramid scaling factor (default: 1.1)
   - **Min Neighbors**: Minimum neighbor rectangles (default: 4)
3. **Click "Nhận diện khuôn mặt"** to start detection
4. **View Results**: See detected faces with bounding boxes and statistics

### Using Sample Images

Click on any sample image to quickly test the detection:
- **Portrait**: Single person photo
- **Group**: Multiple people in one image  
- **Family**: Mixed adults and children

### Preset Configurations

- **🎯 Accuracy**: High precision, slower processing
- **⚖️ Balanced**: Good balance of speed and accuracy
- **⚡ Speed**: Fast processing, may miss some faces

## 📚 API Documentation

### Base URL
```
http://localhost:8080/api/face-detection
```

### Endpoints

#### POST `/detect`
Detect faces in an uploaded image.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `image` (file): Image file (JPG, PNG, BMP)
  - `minSize` (optional): Minimum face size (default: 20)
  - `scaleFactor` (optional): Scale factor (default: 1.1)
  - `minNeighbors` (optional): Min neighbors (default: 4)

**Response:**
```json
{
  "success": true,
  "message": "Face detection completed successfully",
  "data": {
    "face_count": 2,
    "faces": [
      {
        "x": 100,
        "y": 150,
        "width": 200,
        "height": 200
      }
    ]
  }
}
```

#### GET `/health`
Check API health status.

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Swagger UI
Visit `http://localhost:8080/swagger-ui.html` for interactive API documentation.

## 🖼️ Sample Images

The project includes sample images in `face-detection-frontend/samples/`:

- **portrait.jpg**: Single person portrait for basic testing
- **group.jpg**: Group photo with multiple faces
- **family.jpg**: Family photo with adults and children

Each sample includes optimal parameter recommendations in the README.

## ⚙️ Configuration

### Backend Configuration

Edit `face-detection-backend/src/main/resources/application.yml`:

```yaml
server:
  port: 8080

spring:
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 10MB

app:
  cors:
    allowed-origins: "http://localhost:3000"
```

### Frontend Configuration

Edit `face-detection-frontend/script.js`:

```javascript
this.apiBaseUrl = 'http://localhost:8080/api/face-detection';
```

## 🔧 Development

### Building from Source

```bash
# Backend
cd face-detection-backend
mvn clean compile

# Run tests
mvn test

# Create JAR
mvn package
```

### Adding New Features

1. **Backend**: Add new endpoints in `ImageProcessingController`
2. **Frontend**: Extend `FaceDetectionApp` class
3. **Testing**: Add test images to `samples/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow Java coding standards
- Add appropriate error handling
- Include unit tests for new features
- Update documentation
- Test across different browsers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) for computer vision capabilities
- [Spring Boot](https://spring.io/projects/spring-boot) for the robust backend framework
- [Bootstrap](https://getbootstrap.com/) for responsive UI components
- [Font Awesome](https://fontawesome.com/) for beautiful icons

## 📞 Contact

**Nguyen Tuan Khanh**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com

---

⭐ **If you found this project helpful, please give it a star!** ⭐
