// Written by mule-ear on or about 2015/04/14

int clockPulse[2] = {10 , 11};
//int digit2Enable = 11;
int masterReset = 12;
int chr[16]= { 0b01110111,20,179,182,212,230,231,52,247,246,245,199,131,151,227,225 };
// I probably should have written that(119) as 0b01110111 to indicate the segment to turn on
int segments[8] = {2,3,4,5,6,7,8,9};
/* 
Not sure ow to describe how I got these values
I numbered the segments in the order of the pins on my display
pin 1(Arduiono 2) is the left bottom, 2(3) is the bottom, 3 is ground (skipped), 4(4) is right bottom and 5(5) is the decimal (not used, but wired up anyway)
pin 6(6) is the right top, 7(7) is the top, 8(skipped) is ground, 9(8) is the left top and 10(9) is the center element.
That's how I got the values for chr[] - If I want the left bottom segment I use the 1st element of the array - e.g. 0b00000001 
Pin 2 is the LSB of my chr[] value. Or, another way too say it is:
Arduino pin 2 goea to pin 1 on the display
3 -> 2
4 -> 4
5 -> 5
6 -> 6
7 -> 7
8 -> 9
9 -> 10 
All through the D Type Flip-Flop, of course.
If I can figure out how to design a new part in Frizing, I'll include a Fritzing project.
*/

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
    
    test();
}         
    
void loop()
{
 
      
}
void test()
{
  // Very optional test sequence
  for (int i = 0; i<=255 ; i++) // Hex first
  {
    dsplyDigits (int(i), 16);
    delay(20);
  }
  for (int i = 0; i<=99 ; i++) // Decimal next
  {
    dsplyDigits (int(i), 10);
    delay(20);
  }
  // Clear the display after the test completes
  digitalWrite (masterReset, LOW);
  delay(50);
  digitalWrite (masterReset, HIGH);
      
}
    
void dsplyDigits( int  digits2Write, int base ){
  
  int dig2Write[2]; 
  dig2Write[0] = digits2Write % base; // The first digit
  dig2Write[1] = int (digits2Write/base); // The second digit 
  
  //I know there's a slick way of doing this - but brute force today
  
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
