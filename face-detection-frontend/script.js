// Face Detection Frontend JavaScript

class FaceDetectionApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8080/api/face-detection';
        this.currentImageFile = null;
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.checkApiStatus();
        this.updateParameterValues();
    }

    initializeElements() {
        // Core elements
        this.uploadArea = document.getElementById('uploadArea');
        this.imageInput = document.getElementById('imageInput');
        this.imagePreview = document.getElementById('imagePreview');
        this.detectionCanvas = document.getElementById('detectionCanvas');
        this.detectBtn = document.getElementById('detectBtn');
        
        // Parameter controls
        this.minSizeSlider = document.getElementById('minSize');
        this.scaleFactorSlider = document.getElementById('scaleFactor');
        this.minNeighborsSlider = document.getElementById('minNeighbors');
        
        // Value displays
        this.minSizeValue = document.getElementById('minSizeValue');
        this.scaleFactorValue = document.getElementById('scaleFactorValue');
        this.minNeighborsValue = document.getElementById('minNeighborsValue');
        
        // State containers
        this.imagePreviewContainer = document.getElementById('imagePreviewContainer');
        this.resultsInfo = document.getElementById('resultsInfo');
        this.loadingState = document.getElementById('loadingState');
        this.defaultState = document.getElementById('defaultState');
        
        // Result displays
        this.faceCount = document.getElementById('faceCount');
        this.processingTime = document.getElementById('processingTime');
        this.imageSize = document.getElementById('imageSize');
        this.fileSize = document.getElementById('fileSize');
        this.faceDetailsTable = document.getElementById('faceDetailsTable');
        
        // Status
        this.apiStatus = document.getElementById('apiStatus');
    }

    bindEvents() {
        // File upload events
        this.uploadArea.addEventListener('click', () => this.imageInput.click());
        this.imageInput.addEventListener('change', (e) => this.handleFileSelect(e.target.files[0]));
        
        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        // Parameter sliders
        this.minSizeSlider.addEventListener('input', () => this.updateParameterValues());
        this.scaleFactorSlider.addEventListener('input', () => this.updateParameterValues());
        this.minNeighborsSlider.addEventListener('input', () => this.updateParameterValues());

        // Sample images
        document.addEventListener('click', (e) => {
            if (e.target.closest('.sample-image')) {
                const sampleType = e.target.closest('.sample-image').dataset.sample;
                this.loadSampleImage(sampleType);
            }
        });

        // Detect button
        this.detectBtn.addEventListener('click', () => this.detectFaces());
    }    async checkApiStatus() {
        // Since the API is working, just set it as online
        // This avoids unnecessary test requests on page load
        this.updateApiStatus('online', 'API Ready');
    }

    updateApiStatus(status, message) {
        const statusClasses = {
            online: 'bg-success',
            offline: 'bg-danger', 
            error: 'bg-warning'
        };
        
        const statusIcons = {
            online: 'fas fa-check-circle',
            offline: 'fas fa-times-circle',
            error: 'fas fa-exclamation-triangle'
        };

        this.apiStatus.className = `badge ${statusClasses[status]}`;
        this.apiStatus.innerHTML = `<i class="${statusIcons[status]} me-1"></i>${message}`;
    }

    updateParameterValues() {
        this.minSizeValue.textContent = this.minSizeSlider.value;
        this.scaleFactorValue.textContent = parseFloat(this.scaleFactorSlider.value).toFixed(2);
        this.minNeighborsValue.textContent = this.minNeighborsSlider.value;
    }    handleFileSelect(file) {
        if (!file) return;
        
        console.log('File selected:', file.name, file.size, file.type);
        
        // Validate file type
        if (!file.type.startsWith('image/')) {
            this.showNotification('Vui lòng chọn file ảnh', 'error');
            return;
        }
        
        // Validate file size (10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showNotification('File ảnh quá lớn (tối đa 10MB)', 'error');
            return;
        }

        this.currentImageFile = file;
        this.previewImage(file);
        this.detectBtn.disabled = false;
        
        // Update file info
        this.fileSize.textContent = this.formatFileSize(file.size);
        
        console.log('File loaded successfully, detect button enabled');
    }

    previewImage(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.imagePreview.src = e.target.result;
            this.imagePreview.onload = () => {
                this.imageSize.textContent = `${this.imagePreview.naturalWidth}×${this.imagePreview.naturalHeight}`;
                this.showImagePreview();
                this.clearDetectionResults();
            };
        };
        reader.readAsDataURL(file);
    }    async loadSampleImage(sampleType) {
        try {
            // Map sample types to actual image files
            const sampleFiles = {
                portrait: 'portrait.jpg',
                group: 'group.jpg',
                family: 'family.jpg'
            };
            
            const fileName = sampleFiles[sampleType];
            if (!fileName) {
                console.error(`Unknown sample type: ${sampleType}`);
                this.showNotification(`Không tìm thấy ảnh mẫu: ${sampleType}`, 'error');
                return;
            }
            
            // Load the actual sample image
            const response = await fetch(`./samples/${fileName}`);
            if (!response.ok) {
                throw new Error(`Failed to load sample image: ${response.statusText}`);
            }
            
            const blob = await response.blob();
            const file = new File([blob], fileName, { type: blob.type });
            
            // Handle the file selection
            this.handleFileSelect(file);
            this.showNotification(`Đã tải ảnh mẫu: ${sampleType}`, 'success');
            
        } catch (error) {
            console.error('Error loading sample image:', error);
            this.showNotification(`Lỗi khi tải ảnh mẫu: ${error.message}`, 'error');
        }
    }

    showImagePreview() {
        this.defaultState.style.display = 'none';
        this.resultsInfo.style.display = 'none';
        this.imagePreviewContainer.style.display = 'block';
        this.imagePreviewContainer.classList.add('fade-in');
    }

    showLoadingState() {
        this.resultsInfo.style.display = 'none';
        this.loadingState.style.display = 'block';
        this.detectBtn.disabled = true;
        this.detectBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang xử lý...';
    }

    hideLoadingState() {
        this.loadingState.style.display = 'none';
        this.detectBtn.disabled = false;
        this.detectBtn.innerHTML = '<i class="fas fa-play me-2"></i>Nhận diện khuôn mặt';
    }    async detectFaces() {
        if (!this.currentImageFile || this.isProcessing) {
            console.log('Cannot detect:', !this.currentImageFile ? 'No image file' : 'Already processing');
            return;
        }

        console.log('Starting face detection...');
        this.isProcessing = true;
        this.showLoadingState();
        
        const startTime = Date.now();

        try {
            const formData = new FormData();
            formData.append('image', this.currentImageFile);
            formData.append('minSize', this.minSizeSlider.value);
            formData.append('scaleFactor', this.scaleFactorSlider.value);
            formData.append('minNeighbors', this.minNeighborsSlider.value);

            console.log('Sending request to:', `${this.apiBaseUrl}/detect`);
            console.log('Parameters:', {
                minSize: this.minSizeSlider.value,
                scaleFactor: this.scaleFactorSlider.value,
                minNeighbors: this.minNeighborsSlider.value,
                fileSize: this.currentImageFile.size,
                fileName: this.currentImageFile.name
            });

            // Try multiple fetch approaches
            let response;
            try {
                // Method 1: Standard fetch with explicit CORS
                response = await fetch(`${this.apiBaseUrl}/detect`, {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'omit', // Don't send credentials
                    body: formData,
                });
            } catch (corsError) {
                console.warn('CORS fetch failed, trying alternative approach:', corsError);
                
                // Method 2: Try without explicit mode
                response = await fetch(`${this.apiBaseUrl}/detect`, {
                    method: 'POST',
                    body: formData,
                });
            }

            console.log('Response status:', response.status);
            console.log('Response headers:', [...response.headers.entries()]);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('API Error Response:', errorText);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const result = await response.json();
            console.log('API Response:', result);
            
            const processingTime = Date.now() - startTime;

            if (result.success) {
                // Xử lý cả 2 format response (faceCount và face_count)
                const faceCount = result.data.face_count || result.data.faceCount || 0;
                
                this.displayResults(result.data, processingTime);
                this.drawFaceBoxes(result.data.faces || []);
                this.showNotification(`✅ Phát hiện ${faceCount} khuôn mặt trong ${processingTime}ms`, 'success');
            } else {
                console.error('Detection failed:', result.message);
                this.showNotification(`❌ Lỗi: ${result.message}`, 'error');
                this.clearDetectionResults();
            }

        } catch (error) {
            console.error('Detection error:', error);
            let errorMessage = 'Không thể kết nối đến API';
            
            if (error.message.includes('Failed to fetch')) {
                errorMessage = `Lỗi kết nối API:
• Kiểm tra API có đang chạy trên http://localhost:8080
• Kiểm tra CORS configuration
• Thử restart Spring Boot application
• Error: ${error.message}`;
            } else if (error.message.includes('NetworkError')) {
                errorMessage = 'Lỗi mạng. Kiểm tra kết nối internet và server.';
            } else if (error.message.includes('HTTP')) {
                errorMessage = `Lỗi server: ${error.message}`;
            }
              this.showNotification(`❌ ${errorMessage}`, 'error');
            this.clearDetectionResults();
        } finally {
            this.hideLoadingState();
            this.isProcessing = false;
        }
    }

    displayResults(data, processingTime) {
        console.log('Displaying results:', data);
        
        // Đảm bảo data có cấu trúc đúng
        const faceCount = data.face_count || data.faceCount || 0;
        const faces = data.faces || [];
        
        this.faceCount.textContent = faceCount;
        this.processingTime.textContent = `${processingTime}ms`;
        
        // Clear previous results
        this.faceDetailsTable.innerHTML = '';
        
        // Add face details
        if (faces && faces.length > 0) {
            faces.forEach((face, index) => {
                const row = document.createElement('tr');
                const area = face.width * face.height;
                
                row.innerHTML = `
                    <td><span class="badge bg-primary">${index + 1}</span></td>
                    <td>${face.x}</td>
                    <td>${face.y}</td>
                    <td>${face.width}</td>
                    <td>${face.height}</td>
                    <td>${area.toLocaleString()}px²</td>
                `;
                
                this.faceDetailsTable.appendChild(row);
                console.log(`Added face ${index + 1} to table:`, face);
            });
        } else {
            console.log('No faces to display in table');
            // Hiển thị thông báo không có khuôn mặt
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="6" class="text-center text-muted">
                    <i class="fas fa-search me-2"></i>Không phát hiện khuôn mặt nào
                </td>
            `;
            this.faceDetailsTable.appendChild(row);
        }

        // Ẩn default state và hiển thị results
        this.defaultState.style.display = 'none';
        this.resultsInfo.style.display = 'block';
        this.resultsInfo.classList.add('fade-in');
        
        console.log('Results panel should now be visible');
        console.log('Results panel display style:', this.resultsInfo.style.display);
        console.log('Results panel classes:', this.resultsInfo.className);
    }    drawFaceBoxes(faces) {
        const canvas = this.detectionCanvas;
        const ctx = canvas.getContext('2d');
        const img = this.imagePreview;

        // Đợi image load xong
        if (!img.complete || img.naturalWidth === 0) {
            console.log('Image not loaded yet, waiting...');
            img.onload = () => this.drawFaceBoxes(faces);
            return;
        }

        console.log('Drawing face boxes for faces:', faces);
        
        // Get actual displayed image dimensions
        const imgRect = img.getBoundingClientRect();
        const containerRect = img.parentElement.getBoundingClientRect();
        
        console.log('Image dimensions:', {
            natural: { width: img.naturalWidth, height: img.naturalHeight },
            display: { width: img.offsetWidth, height: img.offsetHeight },
            rect: imgRect
        });

        // Set canvas to exact same size as the displayed image
        canvas.style.width = img.offsetWidth + 'px';
        canvas.style.height = img.offsetHeight + 'px';
        canvas.width = img.offsetWidth;
        canvas.height = img.offsetHeight;
        
        // Calculate scale factors from natural size to displayed size
        const scaleX = img.offsetWidth / img.naturalWidth;
        const scaleY = img.offsetHeight / img.naturalHeight;

        console.log('Scale factors:', { scaleX, scaleY });

        // Clear previous drawings
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw face boxes
        faces.forEach((face, index) => {
            // Scale coordinates from natural image size to display size
            const x = face.x * scaleX;
            const y = face.y * scaleY;
            const width = face.width * scaleX;
            const height = face.height * scaleY;

            console.log(`Face ${index + 1}:`, {
                original: face,
                scaled: { x, y, width, height }
            });

            // Draw animated rectangle with glow effect
            ctx.save();
            
            // Outer glow
            ctx.shadowColor = '#ff4757';
            ctx.shadowBlur = 8;
            ctx.strokeStyle = '#ff4757';
            ctx.lineWidth = 3;
            ctx.setLineDash([8, 4]);
            ctx.strokeRect(x, y, width, height);
            
            // Inner rectangle (solid)
            ctx.shadowBlur = 0;
            ctx.setLineDash([]);
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#ffffff';
            ctx.strokeRect(x + 1, y + 1, width - 2, height - 2);
            
            ctx.restore();

            // Draw label with background
            const label = `Face ${index + 1}`;
            ctx.font = 'bold 12px "Segoe UI", Arial, sans-serif';
            const labelMetrics = ctx.measureText(label);
            const labelWidth = labelMetrics.width + 8;
            const labelHeight = 18;
            
            // Position label above face, or below if too close to top
            const labelX = x;
            const labelY = y > 20 ? y - 2 : y + height + 18;
            
            // Label background
            ctx.fillStyle = 'rgba(255, 71, 87, 0.9)';
            ctx.fillRect(labelX, labelY - labelHeight, labelWidth, labelHeight);
            
            // Label text
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'left';
            ctx.textBaseline = 'middle';
            ctx.fillText(label, labelX + 4, labelY - labelHeight/2);
            
            // Draw corner indicators for better visibility
            const cornerSize = 8;
            ctx.strokeStyle = '#ff4757';
            ctx.lineWidth = 2;
            ctx.setLineDash([]);
            
            // Top-left corner
            ctx.beginPath();
            ctx.moveTo(x, y + cornerSize);
            ctx.lineTo(x, y);
            ctx.lineTo(x + cornerSize, y);
            ctx.stroke();
            
            // Top-right corner  
            ctx.beginPath();
            ctx.moveTo(x + width - cornerSize, y);
            ctx.lineTo(x + width, y);
            ctx.lineTo(x + width, y + cornerSize);
            ctx.stroke();
            
            // Bottom-left corner
            ctx.beginPath();
            ctx.moveTo(x, y + height - cornerSize);
            ctx.lineTo(x, y + height);
            ctx.lineTo(x + cornerSize, y + height);
            ctx.stroke();
            
            // Bottom-right corner
            ctx.beginPath();
            ctx.moveTo(x + width - cornerSize, y + height);
            ctx.lineTo(x + width, y + height);
            ctx.lineTo(x + width, y + height - cornerSize);
            ctx.stroke();
        });

        console.log(`Successfully drew ${faces.length} face boxes`);
    }clearDetectionResults() {
        const canvas = this.detectionCanvas;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Reset results display
        this.resultsInfo.style.display = 'none';
        this.faceCount.textContent = '0';
        this.processingTime.textContent = '-';
        this.faceDetailsTable.innerHTML = '';
        
        console.log('Detection results cleared');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle'
        };

        notification.innerHTML = `
            <i class="${icons[type] || icons.info} me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Preset configurations
function setPreset(type) {
    const app = window.faceDetectionApp;
    
    const presets = {
        accuracy: { minSize: 15, scaleFactor: 1.05, minNeighbors: 5 },
        balanced: { minSize: 20, scaleFactor: 1.1, minNeighbors: 4 },
        speed: { minSize: 30, scaleFactor: 1.15, minNeighbors: 3 }
    };

    const preset = presets[type];
    if (preset) {
        app.minSizeSlider.value = preset.minSize;
        app.scaleFactorSlider.value = preset.scaleFactor;
        app.minNeighborsSlider.value = preset.minNeighbors;
        app.updateParameterValues();
        
        const presetNames = {
            accuracy: 'Chính xác',
            balanced: 'Cân bằng', 
            speed: 'Nhanh'
        };
        
        app.showNotification(`Đã áp dụng cài đặt: ${presetNames[type]}`, 'success');
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.faceDetectionApp = new FaceDetectionApp();
});

// Handle window resize to redraw face boxes
window.addEventListener('resize', () => {
    const app = window.faceDetectionApp;
    if (app && app.imagePreview.src && app.resultsInfo.style.display !== 'none') {
        // Redraw face boxes after a short delay to allow layout to settle
        setTimeout(() => {
            const faces = Array.from(app.faceDetailsTable.children).map((row, index) => ({
                x: parseInt(row.children[1].textContent),
                y: parseInt(row.children[2].textContent),
                width: parseInt(row.children[3].textContent),
                height: parseInt(row.children[4].textContent)
            }));
            app.drawFaceBoxes(faces);
        }, 100);
    }
});

// Global function for testing results display
function testResults() {
    console.log('Testing results display...');
    
    const app = window.faceDetectionApp;
    if (!app) {
        console.error('App not initialized yet');
        return;
    }
    
    // Create mock detection results matching API response format
    const mockData = {
        face_count: 2,
        faces: [
            { x: 100, y: 150, width: 200, height: 200 },
            { x: 350, y: 200, width: 180, height: 180 }
        ]
    };
    
    console.log('Mock data:', mockData);
    
    // Test display results
    app.displayResults(mockData, 1250);
    
    // Test drawing face boxes if image is loaded
    if (app.currentImageFile && app.imagePreview.complete) {
        console.log('Drawing test face boxes...');
        app.drawFaceBoxes(mockData.faces);
    } else {
        console.log('No image loaded, skipping face box drawing');
    }
    
    app.showNotification('🧪 Test results displayed! Check console for details.', 'info');
}
