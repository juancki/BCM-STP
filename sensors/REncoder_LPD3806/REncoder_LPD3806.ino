/*
 * Photoresistor based encoder, four pins:
 *  + RED   -> +5V
 *  + BLACK -> GND
 *  + WHITE -> Pin2
 *  + GREEN -> Pin3
 *  DATA: 2Bytes Unsigned Integer [0,...,2^16-1]
 *
 * Serial Connection: 115200 bauds, \r\n
 * Line oriented connection.
 *   - commands (requests) are lines.
 *  - values (responses) are lines.
 *  - Values are string.
 *
 * The code implementation has:
 *  - Read n values one just after the other "rn"
 *    ex: "r1\r\n" measures and sends value.
 *  - Read nonstop fashion. "r"
 *    ex: "r\r\n" measures until other command.
 *  - Read periodically each q microseconds. "mq"
 *    ex: "m1\r\n" read and send each microsecond. (uC will not able to achive that).
 *        "m1000000\r\n" read and send each second.
 * - Juan Carlos Gómez P.
 *  Last review: 24/02/2018
 */


#define encoder0PinA  2
#define encoder0PinB  3
volatile unsigned int encoder0Pos = 0;


bool echo = 0; // Debugging option.
bool echo_2 =0; // Second debuggin option.
char cmd [11];
byte cmd_length;
byte cmd_counter=0;



/**
 * Init Serial and encoder setup pin
 */
void setup() {
  Serial.setTimeout(1000);
  Serial.begin(115200);
  encoder_setup();
  while(!Serial){}
  if(echo)
    Serial.println("Good morning Mr. Marshall");
}


/////////////////////////////////////////////////////////////////////////////////
void encoder_setup(){
  pinMode(encoder0PinA, INPUT);
  pinMode(encoder0PinB, INPUT);
  // encoder pin on interrupt 0 (pin 2)
  attachInterrupt(0, doEncoderA, CHANGE);
  // encoder pin on interrupt 1 (pin 3)
  attachInterrupt(1, doEncoderB, CHANGE);
}


void doEncoderA() {
  // look for a low-to-high on channel A
  if (digitalRead(encoder0PinA) == HIGH) {
    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinB) == LOW) {
      encoder0Pos = encoder0Pos + 1;         // CW
    }else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }else{   // must be a high-to-low edge on channel A
    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinB) == HIGH) {
      encoder0Pos = encoder0Pos + 1;          // CW
    }else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
}

void doEncoderB() {
  // look for a low-to-high on channel B
  if (digitalRead(encoder0PinB) == HIGH) {
    // check channel A to see which way encoder is turning
    if (digitalRead(encoder0PinA) == HIGH) {
      encoder0Pos = encoder0Pos + 1;         // CW
    }else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }else {  // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinA) == LOW) {
      encoder0Pos = encoder0Pos + 1;          // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
}

unsigned int measure(){
  return encoder0Pos;
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////


void loop() {
  // put your main code here, to run repeatedly:
  readMsg();
}

void measureAndSend(int b){
  for(int i=0; i<b;i++){
    unsigned int value = measure();
    Serial.println(value);
  }
}

/*
 * Autoexplanatory.
 */

void measureUntilStop(){
  int r;
  while(Serial.available()==0){
    measureAndSend(1);
  }
}

void eachMicros(){
  long micros_ = 0;
  byte l = cmd_length-1;
  char aux[] = "000";
  if(l<3){
    memcpy(aux+3-l,cmd+1,l);
    micros_=atoi(aux);
  }else if(l>=3){
    memcpy(aux,cmd+l-2,3);
    micros_ = atoi(aux);
    if(l>=6){
      memcpy(aux,cmd+l-5,3);
      micros_ += ((long)1000)*((long)atoi(aux));
      memcpy(aux,"000",3);
      memcpy(aux+3-(l-6),cmd+1,l-6);
      micros_ += ((long)1000000)*((long)atoi(aux));
    }else{
      memcpy(aux,"000",3);
      memcpy(aux+3-(l-3),cmd+1,l-3);
      micros_+=((long)1000)*((long)atoi(aux));
    }
  }
  Serial.print(">< ");
  Serial.println(micros_);
  measureEachMicros(micros_);
}
/**
 * TODO: This function needs better precision.
 */
void measureEachMicros(long micros_){
  unsigned long t = micros();
  unsigned long last = micros();
  while(Serial.available()==0){
    measureAndSend(1);
    t = micros();
    while(Serial.available()==0 and micros()-t<micros_){}
  }
}

/**
 * Non-blocking serial command reading function.
 */
void readMsg(){
  if(readCmd()){
    if(cmd[0]=='m'){
      if(cmd_length==1){
        Serial.println("Error,m requires parameters");
      }else{
        eachMicros();
      }
    }
    if(cmd[0]=='r' and cmd_length==1){
      if(echo)
        Serial.println("Measure until stop");
      measureUntilStop();
    }
    if(cmd[0]=='r' and cmd_length>1){
      char number_c[cmd_length];
      memcpy(number_c,cmd+1,cmd_length);
      int repetitions=atoi(number_c);
      if(echo_2)
        Serial.println(number_c);
      if(echo)
        Serial.println("Measure and send");
      measureAndSend(repetitions);
    }
  }
}

/**
 * This function takes decions on received command. 
 */
bool readCmd(){
  byte available_bytes = Serial.available();
  if(available_bytes==0){return false;}
  if(cmd_counter+available_bytes>10){
    available_bytes=10-cmd_counter;
    cmd_counter+=1;
    cmd[10]='\n';
  }
  byte copied = Serial.readBytes(cmd+cmd_counter,available_bytes);
  cmd_counter+=copied;
  /* "\r\n" is not a command nor part of it */
  if(cmd_counter>2 and cmd[cmd_counter-1]=='\n'){  
    cmd_length=cmd_counter-2;
    cmd_counter=0;
    if(echo)
      cmdEcho(); // echo response.
    return true;
  }
  /* if "\r\n" reset cmd variable*/
  if(cmd_counter==2 and cmd[cmd_counter-1]=='\n'){
    cmd_counter = 0;
  }
  return false;
}
/**
 * Returns everything serially read to the serial
 * output preceeded by ">>> ".
 */
void cmdEcho(){
    char cmd_to_print[cmd_length+1];
    cmd_to_print[cmd_length]=0;
    memcpy(cmd_to_print,cmd,cmd_length);
    Serial.print(">>> ");
    Serial.print(cmd_to_print);
    Serial.println(); 
}

