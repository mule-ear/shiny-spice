
int clockPulse[2] = {10 , 11};
//int digit2Enable = 11;
int masterReset = 12;
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
    pinMode(clockPulse[0], OUTPUT);
    pinMode(clockPulse[1], OUTPUT);
    pinMode(masterReset, OUTPUT);
    digitalWrite (clockPulse[0], LOW);
    digitalWrite (clockPulse[1], LOW);
    digitalWrite (masterReset, HIGH);
}         
    
void loop()
{
  for (int i = 0; i<=255 ; i++) 
  {
    dsplyDigits (int(i), 16);
    delay(1000);
  }
  for (int i = 0; i<=99 ; i++) 
  {
    dsplyDigits (int(i), 10);
    delay(500);
  }
      
}
    
void dsplyDigits( int  digits2Write, int base ){
  // For now, I'm going to use base 16 only
  //base=16;
  int dig2Write[2]; // ={ int (digits2Write/16), (digits2Write % 16)};
  dig2Write[0] = digits2Write % base;
  dig2Write[1] = int (digits2Write/base);
  //int x = digitalRead(digit1Enable);
  //I know there's a slick way of doing this - but brute force today
  Serial.print("At the start from function,  -->");

  for (int j = 0; j<2 ; j++){
    // Turn them on bit by bit
    for (int i = 0; i<=7; i++) 
    {
      // Check if it needs to be HIGH else set it LOW
      if ( chr[dig2Write[j]] & int(round(pow(2,i))))
      {
        digitalWrite (segments[i], HIGH);
      }
      else{       digitalWrite (segments[i], LOW);
      }
    
    }
    //Provide a leading edge to latch the output
    digitalWrite (clockPulse[j], HIGH);
    delay (30);
    digitalWrite (clockPulse[j], LOW);
  }
 
}
