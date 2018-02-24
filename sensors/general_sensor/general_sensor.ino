/*
 * This code is the implementation of a generic SERIAL interface to
 * access and measure in a timely fashion sensors.
 *
 * Serial Connection: 115200 bauds, \r\n
 * Line oriented connection.
 * 	- commands (requests) are lines.
 *	- values (responses) are lines.
 *	- Values are string.
 *
 * The code implementation has:
 * 	- Read n values one just after the other "rn"
 *		ex: "r1\r\n" measures and sends value.
 * 	- Read nonstop fashion. "r"
 *		ex: "r\r\n" measures until other command.
 * 	- Read periodically each q microseconds. "mq"
 *		ex: "m1\r\n" read and send each microsecond. (uC will not able to achive that).
 *		    "m1000000\r\n" read and send each second.
 * - Juan Carlos Gómez P.
 *	Last review: 24/02/2018
 */

/**
 * TODOs are written through the code.
 * Include a help "h" command to show possible commands.
 * Include debug command.
 */


bool echo = 0; // Debugging option.
bool echo_2 =0; // Second debuggin option.
char cmd [11];
byte cmd_length;
byte cmd_counter=0;

/**
 * Init Serial.
 */
void setup() {
  Serial.setTimeout(1000);
  Serial.begin(115200);
  // Serial available
  while(!Serial){}
  Serial.println("Good morning Mr. Marshall");
}

void loop() {
  // put your main code here, to run repeatedly:
  readMsg();
}

/**
 * Demo example does nothing.
 */
int measure(){
  return 0;
}

void measureAndSend(int b){
  for(int i=0; i<b;i++){
    int value = measure();
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

