#Introduction
This project is a smart alarm with emphasis on user customisation and ease of use. It allows the user to create and cancel briefings or alarms which trigger at a certain time and using text to speach will tell the user the alarm name, time and if selected, will say the top 3 headlines and/ or the current weather. It also provides some silent notifications which contain an update on the current weather, information on the spread of COVID-19 in a specified area and the top 5 headlines. These notifications are updated by default every 10 minnutes but can be changed in config.

#Requirements
This package was developed using python 3.9.0 so it is reccomended you run it also with python 3.9.0

The folloing modules are required to be dowloaded for this package:
* Flask
* pyttsx3

The following API key's are required:
* openweathermap api (https://openweathermap.org/)
* newsapi (https://newsapi.org/)

#Configuration
Contained in this package is a config.json file which is used to configure the opertion of the smart alarm. 
* In the API-Keys dictionary the API keys have been redacted and you will have to put your own keys in place for the program to work. 
* The values in the display dictionary do not affect the main running of the program, but how it is displayed to the user so the on screen title and image can be changed at will. 
* In the Settings dictionary, the update rate is how often the notifications will be updated in seconds. The City and Units values change where weather and covid data from the API's is taken from so it can be specified to your local region in the temperature units of choice. The news_filters is a list of strings, empty by default, which allows you to filter the headlines in notifications and announcements by keywords found in the title of each healine.

#Known Isuues
* Due to the nature of the sched module and it being a requirement to use it, alarms are accurate within a minute of when they are set.
* Alarms after triggering may freeze the page, and require manually refreshing to allow other events to happen again
* All issues to be fixed in a future update

#Author
* Nmae - Matthew Auger
* email - mga209@exeter.ac.uk
* github - ""

#License
Copyright 2020 Matthew Auger

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

