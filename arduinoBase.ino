#include <Servo.h>

Servo xServo;
Servo yServo;

void setup() {
  Serial.begin(9600);
  xServo.attach(9); // Connect the X servo to pin 9
  yServo.attach(10); // Connect the Y servo to pin 10
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');

    if (commaIndex != -1) {
      String xStr = data.substring(0, commaIndex);
      String yStr = data.substring(commaIndex + 1);

      int x = xStr.toInt();
      int y = yStr.toInt();

      // Map the values to servo angles (adjust the range based on your servo specifications)
      int xAngle = map(x, 0, 1000, 0, 180);
      int yAngle = map(y, 0, 1000, 0, 180);

      xServo.write(xAngle);
      yServo.write(yAngle);
    }
  }
}
