
int digitEnable[2] = {10 , 11};
//int digit2Enable = 11;
int outputEnable = 12;
int chr[16]= { 0b01110111,20,179,182,212,230,231,52,247,246,245,199,131,151,227,225 };
// I probably should have written that(119) as 0b01110111 to indicate the segment to turn on
int segments[8] = {2,3,4,5,6,7,8,9};
//adding line for git test 2    
// adding another line in master to see how to merge into a branch
<<<<<<< HEAD
//and one more from latches
// simulate work in latches branch while newBranch was merged and pushed to master
=======
// and one more

>>>>>>> 49f5354431b94b2261e1ddc2fdd85f217fffebff
     
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
    pinMode(digitEnable[0], OUTPUT);
    pinMode(digitEnable[1], OUTPUT);
    pinMode(outputEnable, OUTPUT);
    digitalWrite (digitEnable[0], LOW);
    digitalWrite (digitEnable[1], LOW);
    digitalWrite (outputEnable, LOW);
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
  int dig2Write[2]; // ={ int (digits2Write/16), (digits2Write % 16)};
  dig2Write[0] = digits2Write % 16;
  dig2Write[1] = int (digits2Write/16);
  //int x = digitalRead(digit1Enable);
  //I know there's a slick way of doing this - but brute force today
  Serial.print("At the start from function,  -->");
  //Serial.print(digits2Write);
  //Serial.print(digit2Write1);
  //Serial.println(digit2Write2);
  
//  
//  if (x == LOW ) { // Then we are writing digit 1
//    //digit2Write = digit2Write[0] ;
//    Serial.print("Inside first if -->");
//    //Serial.println(digit2Write1);
//  
//    digitalWrite(digit1Enable, HIGH); 
//    digitalWrite(digit2Enable, LOW); 
//  }
//  else {
//    //digit2Write = digit2Write[1] ;
//    //Serial.print("Inside 2nd if -->");
//    //Serial.println(digit2Write2);
//    digitalWrite(digit1Enable, LOW); 
//    digitalWrite(digit2Enable, HIGH);
//  }
//  //Serial.println(digit2Write);
  for (int j = 0; j<2 ; j++){
    digitalWrite ( digitEnable[j], HIGH);
    for (int i = 0; i<=7; i++) 
    {
      //Serial.print("Inside for -->");
      //Serial.println(digit2Write);
      //di
      if ( chr[dig2Write[j]] & int(round(pow(2,i))))
      {
        digitalWrite (segments[i], HIGH);
      }
      else{       digitalWrite (segments[i], LOW);
      }
    digitalWrite ( digitEnable[j], LOW);
    }
  }
 
}
