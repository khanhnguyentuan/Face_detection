@echo off
REM Face Detection API Startup Script
REM Author: Nguyen Tuan Khanh
REM Description: Start the Spring Boot Face Detection API

echo ========================================
echo    Face Detection API Startup
echo ========================================
echo.

REM Check if Java is installed
java -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Java is not installed or not in PATH
    echo Please install Java 11 or higher
    pause
    exit /b 1
)

REM Check if Maven is installed
mvn -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Maven is not installed or not in PATH
    echo Please install Apache Maven
    pause
    exit /b 1
)

echo Starting Face Detection API...
echo Port: 8080
echo Swagger UI: http://localhost:8080/swagger-ui.html
echo.

REM Start the application
mvn spring-boot:run

echo.
echo Application stopped.
pause

