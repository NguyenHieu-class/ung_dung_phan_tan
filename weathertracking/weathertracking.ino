// ESP8266 
// DHT22
// InfluxDB
// Raspberry Pi

#include <Wire.h>
#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
ESP8266WiFiMulti wifiMulti;
#define DEVICE "ESP8266"

#include <InfluxDbClient.h>
#include <InfluxDbCloud.h>

#define WIFI_SSID "P301"
#define WIFI_PASSWORD "baohieubinhan"
#define INFLUXDB_URL "https://us-east-1-1.aws.cloud2.influxdata.com"                                                                                                                                         
#define INFLUXDB_TOKEN "4-XRly87wW4L8C0EGkjZWDzCep6eKkgWUgwl1DonbLqwVBQ1gfKd0GN-oLjBft2XK1M7k_FaQjlYKlSUf_rI-A=="           
#define INFLUXDB_ORG "e0ef5192b44f689d"                                                                                     
#define INFLUXDB_BUCKET "weatherv1"                                                                                         
#define TZ_INFO "UTC7"                                                                                                      

DHT dht(4,DHT11);                                                   

int temp = 0;                                                       
int humid = 0;

InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);                

Point sensor("weather");                                            

void setup() 
{
    Serial.begin(9600);                                            
    
    dht.begin();                                                      

    WiFi.mode(WIFI_STA);                                              
    wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);

    Serial.print("Connecting to wifi");                               
    while (wifiMulti.run() != WL_CONNECTED) 
    {
        Serial.print(".");
        delay(100);
    }
    Serial.println();

    sensor.addTag("device", DEVICE);                                   
    sensor.addTag("SSID", WIFI_SSID);

    timeSync(TZ_INFO, "pool.ntp.org", "time.nis.gov");                 

    if (client.validateConnection())                                   
    {
        Serial.print("Connected to InfluxDB: ");
        Serial.println(client.getServerUrl());
    } 
    else 
    {
        Serial.print("InfluxDB connection failed: ");
        Serial.println(client.getLastErrorMessage());
    }
}

void loop()                                                          
{
    delay(2000);
    temp = dht.readTemperature();                                      
    humid = dht.readHumidity();

    sensor.clearFields();                                              

    sensor.addField("temperature", temp);                              
    sensor.addField("humidity", humid);                                
        
    if (wifiMulti.run() != WL_CONNECTED)                               
        Serial.println("Wifi connection lost");

    if (!client.writePoint(sensor))                                    
    {
        Serial.print("InfluxDB write failed: ");
        Serial.println(client.getLastErrorMessage());
    }
    
    Serial.print("Temp: ");                                            
    Serial.println(temp);
    Serial.print("°C\nHumidity: ");
    Serial.println(humid);
    Serial.println(" %");
    delay(10000);                                                      
}