void setup(){
  Serial.begin(115100);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  
  pinMode(8,OUTPUT);
  pinMode(9,INPUT_PULLUP);
  pinMode(10,INPUT_PULLUP);
  pinMode(11,INPUT_PULLUP);
  pinMode(12,OUTPUT);

  digitalWrite(12,HIGH);
  digitalWrite(8,LOW);
  digitalWrite(7,LOW);
  digitalWrite(5,LOW);
  
}
int f = 90;
int q = 100;
long i = 0;
int n = q;
long x_s = 8000;
float m = (float)(f-q)/x_s;
void loop(){
  if (i<(long)x_s+100){
    delayMicroseconds(m*i+n);
    digitalWrite(2,HIGH);
    digitalWrite(2,LOW);
    i++;
  }else{
    delayMicroseconds(m*i+n);
    digitalWrite(2,HIGH);
    digitalWrite(2,LOW);
  }
}

