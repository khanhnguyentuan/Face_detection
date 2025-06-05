@echo off
REM Face Detection API JAR Runner
REM Alternative startup script using JAR file

echo ========================================
echo    Face Detection API (JAR Mode)
echo ========================================
echo.

REM Check if JAR file exists
if not exist "target\face-detection-api-1.0.0.jar" (
    echo Building JAR file...
    mvn clean package -DskipTests
)

echo Starting Face Detection API from JAR...
echo Port: 8080
echo Swagger UI: http://localhost:8080/swagger-ui.html
echo.

REM Start the JAR application
java -jar target\face-detection-api-1.0.0.jar

echo.
echo Application stopped.
pause
