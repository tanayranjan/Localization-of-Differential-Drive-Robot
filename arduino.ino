#include <Servo.h>

// Instantiating a servo object
Servo myServo;

// Defining the pins attached
int trigPin = 2;
int echoPin = 8;
int servoPin = 5;
int tlcwPin = 6;
int tlccwPin = 7;
int trcwPin = 3;
int trccwPin = 4;
int blcwPin = 11;
int blccwPin = 12;
int brcwPin = 10;
int brccwPin = 9;

// Defining variables
int pingTravelTime;
float pingTravelDistance;

// Servo Sweep + sensor data collection function
void sweep(int start, int finish, int angles[], float distances[]) {
  int angle = start;
  if(start < finish) {
    while(angle <= finish) {
      myServo.write(angle);
      delay(200);
    
      digitalWrite(trigPin,LOW);
      delayMicroseconds(10);

      digitalWrite(trigPin,HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin,LOW);

      pingTravelTime = pulseIn(echoPin,HIGH);
      delay(25);

      pingTravelDistance = (340*(pingTravelTime/2.0))/1000000;

      angles[angle] += angle;
      distances[angle] += pingTravelDistance;

      angle++;
    }
  }
  else {
    while(angle >= finish) {
      myServo.write(angle);
      delay(200);
    
      digitalWrite(trigPin,LOW);
      delayMicroseconds(10);

      digitalWrite(trigPin,HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin,LOW);

      pingTravelTime = pulseIn(echoPin,HIGH);
      delay(25);

      pingTravelDistance = (340*(pingTravelTime/2.0))/1000000;

      angles[angle] += angle;
      distances[angle] += pingTravelDistance;

      angle--;
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, OUTPUT);
  pinMode(tlcwPin, OUTPUT);
  pinMode(tlccwPin, OUTPUT);
  pinMode(trcwPin, OUTPUT);
  pinMode(trccwPin, OUTPUT);
  pinMode(blcwPin, OUTPUT);
  pinMode(blccwPin, OUTPUT);
  pinMode(brcwPin, OUTPUT);
  pinMode(brccwPin, OUTPUT);
  
  myServo.attach(servoPin);
}

void loop() {
  // put your main code here, to run repeatedly:
  myServo.write(0);

  // Sweep the ultrasonic sensor three times and collect sensor data
  int angles[180] = {0};
  float distances[180] = {0};
  sweep(0, 180, angles, distances);
  sweep(180, 0, angles, distances);
  sweep(0, 180, angles, distances);

  // To find out the distance an angle at which the landmarks are located
  float min1 = 1000;
  float min2 = 1000;
  int ind1 = -1;
  int ind2 = -1;

  int angle = 0;
  while(angle < 90) {
    if(min1 > distances[angle]) {
      min1 = distances[angle];
      ind1 = angle;
    }
    
    angle++;
  }
  
  angle = 91;
  while(angle <= 180) {
    if(min2 > distances[angle]) {
      min2 = distances[angle];
      ind2 = angle;
    }

    angle++;
  }

  Serial.print(min1/3);
  Serial.print(" ");
  Serial.print(ind1/3);
  Serial.print(",");
  Serial.print(min2/3);
  Serial.print(" ");
  Serial.println(ind2/3);

  // To run the motors for 1 sec
  digitalWrite(tlcwPin,HIGH);
  digitalWrite(tlccwPin,LOW);
  digitalWrite(trcwPin,HIGH);
  digitalWrite(trccwPin,LOW);
  digitalWrite(blcwPin,HIGH);
  digitalWrite(blccwPin,LOW);
  digitalWrite(brcwPin,HIGH);
  digitalWrite(brccwPin,LOW);
  
  delay(1000);
}