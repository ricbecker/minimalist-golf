#include "RTClib.h"
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>

#define MAX_SLEEP_ITERATIONS   1
#define MIN_POWER 800
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

// Function declarations
void printTime(DateTime now);
void printPower(int power);
void sleep();
bool piIsActive();
void powerOnPi();
void powerOffPi();

// Variables
RTC_DS3231 rtc;
int sleepIterations = 0;
volatile bool watchdogActivated = false;
int test_LED = 13;
int pi_GPIO = 12;
int relay_GPIO = 10;
bool systemOn = false;

// Setup Functions
void setupRTC(){
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    delay(1000);
  }

  if(rtc.lostPower()){
    Serial.println("RTC lost power, lets set the time!");
    // Set the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    DateTime now = rtc.now();
    printTime(now);
    delay(1000);
  }
}

void setupWatchdog(){  
  noInterrupts();

  /* Clear the reset flag. */
  MCUSR &= ~(1<<WDRF);
  
  /* In order to change WDE or the prescaler, we need to
   * set WDCE (This will allow updates for 4 clock cycles).
   */
  WDTCSR |= (1<<WDCE) | (1<<WDE);

  /* set new watchdog timeout prescaler value */
  WDTCSR = 1<<WDP0 | 1<<WDP3; /* 8.0 seconds */
  
  /* Enable the WD interrupt (note no reset). */
  WDTCSR |= _BV(WDIE);

  interrupts();
}

void setup() {
  Serial.begin(9600);
  pinMode(test_LED, OUTPUT);
  pinMode(pi_GPIO, OUTPUT);
  pinMode(relay_GPIO, OUTPUT);
  delay(1000);

  setupRTC();
  setupWatchdog();
}

void loop() {
  if(watchdogActivated || systemOn){
    
    watchdogActivated = false;
    sleepIterations += 1;

    if(sleepIterations >= MAX_SLEEP_ITERATIONS){
       // Read potentiometer
      int power = analogRead(A0);
      printPower(power);
    
      // Read RTC
      DateTime now = rtc.now();
      printTime(now);
      bool activeTime = checkTime(now);

      // Verify Power and Time
      if(power > MIN_POWER && !systemOn && activeTime) {
        powerOnPi();
      } else if ((power < MIN_POWER || !activeTime) && systemOn){
        powerOffPi();
      }
      delay(3000);
    }
  }
  
  if(systemOn) {
    delay(3000);
  } else {
    sleep();
  }
}

void printPower(int power){
  Serial.print("Current Power: ");
  Serial.println(power);
}

// Returns true if system should be on
bool checkTime(DateTime now){
  // 10am - 5pm Monday - Friday
  // 10am - 6pm Satuday - Sunday
  byte day = now.dayOfTheWeek();
  byte hour = now.hour();
  byte minute = now.minute();
  
  if(day > 0 && day < 6){ // Weekday
    if(hour >= 10 && hour < 18){
      return true;
    } 
    else {
      return false;
    }
  } 
  else { // Weekend
    if(hour >= 10 && hour < 19){
      return true;
    } 
    else {
      return false;
    }
  }
}

void printTime(DateTime now){
  Serial.print("Current Time: ");
  Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
  Serial.print(" ");
  Serial.print(now.year(), DEC);
  Serial.print('/');
  Serial.print(now.month(), DEC);
  Serial.print('/');
  Serial.print(now.day(), DEC);
  Serial.print(" ");
  Serial.print(now.hour(), DEC);
  Serial.print(':');
  Serial.print(now.minute(), DEC);
  Serial.print(':');
  Serial.print(now.second(), DEC);
  Serial.println();
}

ISR(WDT_vect)
{
  watchdogActivated = true;
}

void sleep()
{
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  
  /* Now enter sleep mode. */
  sleep_mode();
  
  /* The program will continue from here after the WDT timeout*/
  sleep_disable(); /* First thing to do is disable sleep. */
  
  /* Re-enable the peripherals. */
  power_all_enable();
}

// Raspberry Pi Commands
void powerOnPi(){
  systemOn = true;
  digitalWrite(pi_GPIO, LOW);
  digitalWrite(relay_GPIO, HIGH);
  Serial.println("Powering On Raspberry Pi");
}

void powerOffPi(){
  digitalWrite(pi_GPIO, HIGH);
  Serial.println("Powering Off Raspberry Pi");
  delay(20000);
  digitalWrite(pi_GPIO, LOW);
  digitalWrite(relay_GPIO, LOW); // TODO: Is there a better way to test if Pi is active?
  systemOn = false;
}

// TODO: Communicate with pi to check if is on
bool piIsActive(){
  return systemOn;
}


