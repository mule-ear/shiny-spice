
int digit1Cathode = 11;
int digit2Cathode = 12;
int chr[16]= { 0b01110111,20,179,182,212,230,231,52,247,246,245,199,131,151,227,225 };
// I probably should have written that(119) as 0b01110111 to indicate the segment to turn on
int segments[8] = {2,3,4,5,6,7,8,9};
    
     
void setup()
{
     
  Serial.begin(9600);
  Serial.println("\n7 Segment6 Driver");
      
  //Set the DISPLAY low
  for (int i = 0; i<= 8; i++)
  {
    pinMode(segments[i], OUTPUT);
    digitalWrite( segments[i], LOW );
  }
    pinMode(digit1Cathode, OUTPUT);
    pinMode(digit2Cathode, OUTPUT);
    digitalWrite (digit1Cathode, LOW);
    digitalWrite (digit2Cathode, LOW);
}         
    
void loop()
{
  for (int i = 0; i<=255 ; i++) 
  {
    dsplyDigits (int(i/16), 16);
    delay(10000);

  }

      
}
    
void dsplyDigits( int  digits2Write, int base ){
  // For now, I'm going to use base 16 only
  int digit2Write;
  int digit2Write1 = digits2Write % 16;
  int digit2Write2 = int (digits2Write/16);
  int x = digitalRead(digit1Cathode);
  //I know there's a slick way of doing this - but brute force today
  Serial.print("At the start from function,  -->");
  Serial.print(digits2Write);
  Serial.print(digit2Write1);
  Serial.println(digit2Write2);
  
  
  if (x == LOW ) { // Then we are writing digit 1
    digit2Write = digit2Write1 ;
    Serial.print("Inside first if -->");
    Serial.println(digit2Write1);
  
    digitalWrite(digit1Cathode, HIGH); 
    digitalWrite(digit2Cathode, LOW); 
  }
  else {
    digit2Write = digit2Write2 ;
    Serial.print("Inside 2nd if -->");
    Serial.println(digit2Write2);
    digitalWrite(digit1Cathode, LOW); 
    digitalWrite(digit2Cathode, HIGH);
  }
  Serial.println(digit2Write);
  for (int i = 0; i<=7; i++) 
  {
    Serial.print("Inside for -->");
    Serial.println(digit2Write);
    if ( chr[digit2Write] & int(round(pow(2,i))))
    {
      digitalWrite (segments[i], HIGH);
    }
    else{       digitalWrite (segments[i], LOW);
    }  
  }
 
}
