#include <Wire.h>
#include <MPU6050.h>  // Install from Arduino Library Manager

MPU6050 imu;  // Create an IMU object

void setup() {
    Serial.begin(115200);  // Start serial communication
    Wire.begin();          // Initialize I2C

    if (!imu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
        Serial.println("Could not find a valid MPU6050 sensor!");
        while (1);
    }

    Serial.println("MPU6050 initialized!");
    delay(1000);
}

void loop() {
    Vector acc = imu.readNormalizeAccel();  // Read accelerometer
    Vector gyro = imu.readNormalizeGyro();  // Read gyroscope

    Serial.print("Accel (g): X=");
    Serial.print(acc.XAxis);
    Serial.print(" Y=");
    Serial.print(acc.YAxis);
    Serial.print(" Z=");
    Serial.println(acc.ZAxis);

    Serial.print("Gyro (°/s): X=");
    Serial.print(gyro.XAxis);
    Serial.print(" Y=");
    Serial.print(gyro.YAxis);
    Serial.print(" Z=");
    Serial.println(gyro.ZAxis);

    Serial.println("----------------------------------");
    delay(500);
}
