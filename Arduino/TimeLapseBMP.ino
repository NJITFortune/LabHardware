//http://forum.arduino.cc/index.php?topic=285778.0
// inspired by http://sauerwine.blogspot.fr/2013/07/an-arduino-time-lapse-camera-using.html
// and http://www.arducam.com/how-arducam-use-a-external-trigger-from-a-sensor/

//#include <UTFT_SPI.h>
#include <SD.h>
#include <Wire.h>
#include <ArduCAM.h>
#include <SPI.h>
#include "memorysaver.h"
//#include <avr/pgmspace.h>
//#include <ov2640_regs.h>

// pin 11 = MOSI, pin 12 = MISO, pin 13 = SCK

#define BMPIMAGEOFFSET 54
#define SD_CS 10 
const int CS1 = 7;

// Constants that define the format of the picture taken
const int bmp_mode = 0;
const int mode = bmp_mode;

const char bmp_header[54] PROGMEM =
{
      0x42, 0x4D, 0x36, 0x58, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x36, 0x00, 0x00, 0x00, 0x28, 0x00,
      0x00, 0x00, 0x40, 0x01, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x01, 0x00, 0x10, 0x00, 0x00, 0x00,
      0x00, 0x00, 0x00, 0x58, 0x02, 0x00, 0xC4, 0x0E, 0x00, 0x00, 0xC4, 0x0E, 0x00, 0x00, 0x00, 0x00,
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};
// Instanciation of the class ArduCAM
ArduCAM myCAM1(OV2640, CS1);

// Used in takePicture() to transfer the buffer of the ArduCAM into a BMP file
// inspired by http://sauerwine.blogspot.fr/2013/07/an-arduino-time-lapse-camera-using.html
void writeBMP(File outFile){
  
  char VH, VL;
  uint8_t temp,temp_last;
  int i, j, posn, nextNum;
  
    //Write the BMP header
  for( i = 0; i < 54; i++)
  {
    char ch = pgm_read_byte(&bmp_header[i]);
    outFile.write((uint8_t*)&ch,1);
  }

  //Read the first dummy byte from FIFO
  temp = myCAM1.read_fifo();
  //Read 320x240x2 byte from FIFO
  for(i = 0; i < 240; i++)
    for(j = 0; j < 320; j++)
    {
      VH = myCAM1.read_fifo();
      VL = myCAM1.read_fifo();
      //RGB565 to RGB555 Conversion
      if (false) {
        VL = (VH << 7) | ((VL & 0xC0) >> 1) | (VL & 0x1f);
        VH = VH >> 1;
      }
      //Write image data to file
      outFile.write(VL);
      outFile.write(VH);
  }
}

// IMAGE FILE GENERATION
// generates a name and returns the opened file
File imageFile(){
 // generates the filename
 char filename[13];
File outFile;

  strcpy(filename, "IMAGE00.BMP");
  for (int i = 0; i < 100; i++) {
    filename[5] = '0' + i/10;
    filename[6] = '0' + i%10;
    // create if does not exist, do not open existing, write, sync after write
    if (! SD.exists(filename)) {
      break;
    }}
   Serial.println(filename); 
   
 // opens the file
 outFile = SD.open(filename,O_WRITE | O_CREAT | O_TRUNC);
 if (! outFile){ 
 Serial.println("open file failed");
 } else {
 Serial.println("File opened sucessfully");
 }

 return outFile;
}

// ========= TAKE PICTURE ========
// simple to use function, which takes a picture
// either in JPEG (bugged) or BMP format in function 
// of the 'mode' constant

void takePicture(){
  Serial.println("Taking picture...");
  File outFile;

  uint8_t start_capture = 0;
  
  myCAM1.write_reg(ARDUCHIP_MODE, 0x00);
  
  // Initialisation
  // Warning : if you use set_format(JPEG) before Init, it will freeze
  myCAM1.set_format(BMP);
  Serial.print("Init ? ");
  myCAM1.InitCAM();
  Serial.println("OK");
  
  
  myCAM1.flush_fifo(); // clean ArduCAM buffer
  myCAM1.clear_fifo_flag(); // start capture
  myCAM1.start_capture();
  Serial.print("Waiting for capture..."); //waiting until capture is done
  while (!(myCAM1.read_reg(ARDUCHIP_TRIG) & CAP_DONE_MASK)) {
   delay(10); 
  }
  Serial.println("OK");
  
  // open a file onto the SD card
  outFile = imageFile();
    
    // writes the content of the ArduCAM buffer into the file, with the right
    // function, defined by the 'mode' value
    Serial.print("Buffering...");
    writeBMP(outFile);
    Serial.println("OK");
    
    // close the file and clean the flags and the buffers
    outFile.close(); 
    Serial.println("Capture finished");
    myCAM1.clear_fifo_flag();
    start_capture = 0;
    myCAM1.InitCAM();
}

// Function that waits for n seconds, writing a countdown on the Serial console
void countdown(int n = 10){
 while (n>0){
    Serial.print(n);
    Serial.println("... ");
    n=n-1;
    delay(1000);
  }
}

// ======== SETUP ========

void setup(){
  uint8_t vid,pid;
  uint8_t temp; 
  #if defined (__AVR__)
    Wire.begin(); 
  #endif
  #if defined(__arm__)
    Wire1.begin(); 
  #endif
  // begins the Serial communication
  Serial.begin(115200);
  Serial.println("ArduCAM Start!");
  pinMode(CS1, OUTPUT);
  SPI.begin();
 
  myCAM1.write_reg(ARDUCHIP_TEST1, 0x55);
  temp = myCAM1.read_reg(ARDUCHIP_TEST1);
  if(temp != 0x55)
  {
   Serial.println("SPI interface Error!");
   while(1);
  } 
  else {
  Serial.println("SPI All Good");
  }  
  
  // change MCU mode (?)
  myCAM1.write_reg(ARDUCHIP_MODE, 0x00);
  myCAM1.InitCAM();
  
  // SD card initialisation
  if (!SD.begin(SD_CS)) 
  {
    while (1); //If failed, stop here
    Serial.println("SD Card Error");
  }
  else
 {   Serial.println("SD Card detected!");
}}



void loop(){
 takePicture();
 delay(20000);
 
}
