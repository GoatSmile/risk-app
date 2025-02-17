NT:
nt@NT-Mac risk-app % source risk-env/bin/activate
(risk-env) nt@NT-Mac risk-app % which streamlit             
/Users/nt/Projects/risk-app/risk-env/bin/streamlit

RUN:
(risk-env) nt@NT-Mac risk-app %  cd /Users/nt/Projects/risk-app ; /usr/bin
/env /Users/nt/Projects/risk-app/risk-env/bin/python /Users/nt/.vscode/ext
ensions/ms-python.debugpy-2025.0.0-darwin-arm64/bundled/libs/debugpy/adapt
er/../../debugpy/launcher 50285 -- /Users/nt/Projects/risk-app/risk-env/bi
n/streamlit run risk-app-p.py --server.port 8501 --logger.level=debug 
2025-02-10 20:56:37.802 Starting server...
2025-02-10 20:56:37.802 Serving static content from /Users/nt/Projects/risk-app/risk-env/lib/python3.11/site-packages/streamlit/static
2025-02-10 20:56:37.805 Server started on port 8501
2025-02-10 20:56:37.806 Runtime state: RuntimeState.INITIAL -> RuntimeState.NO_SESSIONS_CONNECTED



/Users/nt/.vscode/extensions/ms-python.python-2025.0.0-darwin-arm64/python_files/deactivate/zsh /Users/nt/Projects/risk-app/risk-env/bin /Users/nt/.pyenv/shims /opt/homebrew/bin /Users/nt/.vscode/extensions/ms-python.python-2025.0.0-darwin-arm64/python_files/deactivate/zsh /Users/nt/Projects/risk-app/risk-env/bin /usr/local/bin /System/Cryptexes/App/usr/bin /usr/bin /bin /usr/sbin /sbin /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin /Users/nt/.vscode/extensions/ms-python.python-2025.0.0-darwin-arm64/python_files/deactivate/zsh /Users/nt/Projects/risk-app/risk-env/bin /opt/homebrew/bin


 cd /Users/nt/Projects/risk-app ; /usr/bin/env /Users/nt/Projects/risk-app/risk-env/bin/python /Users/nt/.vscode/extensions/ms-python.debugpy-2025.0.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 49341 -- -m streamlit run risk-app-p.py --server.port 8501 --logger.level=debug 
(risk-env) nt@NT-Mac risk-app %  cd /Users/nt/Projects/risk-app ; /usr/bin/env 
/Users/nt/Projects/risk-app/risk-env/bin/python /Users/nt/.vscode/extensions/ms
-python.debugpy-2025.0.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugp
y/launcher 49341 -- -m streamlit run risk-app-p.py --server.port 8501 --logger.
level=debug 

(risk-env) nt@NT-Mac risk-app %  /usr/bin/env /Users/nt/Projects/risk-app/risk-
env/bin/python /Users/nt/.vscode/extensions/ms-python.debugpy-2025.0.0-darwin-a
rm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 53563 -- -m streamlit 
run risk-app-p.py --server.port 8501 --logger.level=debug 


streamlit run /Users/nt/Projects/risk-app/risk-app-p.py --server.port=8501

streamlit run /Users/nt/Projects/risk-app/risk-app-p.py --server.port=8501

streamlit run risk-app-p.py

#  Right DEBUG
cd ~/Projects/risk-app
python -m venv risk-env
source risk-env/bin/activate
streamlit run risk-app-p.py -- --debug




-----------------------------------

{
    "python.envFile": "~/Projects/astrology-app/.vscode/.env"
}


#----
# Invokes the Python interpreter. creates virtual environments.
python -m venv astrology-env
# Open Terminal & Navigate to Project
cd ~/astrology-app 
# Reactivate Virtual Environment
source astrology-env/bin/activate 


# New start
cd ~/astrology-app
source astrology-env/bin/activate
streamlit run app.py


streamlit cache clear
streamlit run app.py

chmod +x ~/astrology-app/launch_app.sh
chmod +x ~/astrology-app/Launch_Astrology_App.sh


python -m venv .venv  # Creates a `.venv` folder in your project

Use Virtual Environments:

# Create a project-specific environment
python -m venv ~/Projects/my_ai_project/.venv
source ~/Projects/my_ai_project/.venv/bin/activate

python -m venv my_project_env
source my_project_env/bin/activate


~/Projects/my_ai_project/  
├── src/                 # Python source code
├── data/                # Datasets
├── models/              # Trained models
├── notebooks/           # Jupyter notebooks
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation


find . -name "*.pyc" -delete

# NEW
cd ~/Projects/astrology-app 
python -m venv astrology-env
source astrology-env/bin/activate
streamlit run import-csv.py

# New env
pip install streamlit


# RISK PROJECTION


#  Right 
cd ~/Projects/risk-app
python -m venv risk-env
source risk-env/bin/activate
streamlit run risk-app-p.py

#  Right DEBUG
cd ~/Projects/risk-app
python -m venv risk-env
source risk-env/bin/activate
streamlit run risk-app-p.py -- --debug


# LOGGING 
python risk-app-p.py --debug light
python risk-app-p.py --debug heavy

logger.debug("Detailed information, typically of interest only when diagnosing problems.")
logger.info("Confirmation that things are working as expected.")
logger.warning("An indication that something unexpected happened, or indicative of some problem in the near future.")
logger.error("Due to a more serious problem, the software has not been able to perform some function.")
logger.critical("A serious error, indicating that the program itself may be unable to continue running.")


# Light debug
debug1("This is a light debug message")
# Heavy debug
debug2("This is a heavy debug message with details: %s", some_variable)

# Regular logging still works
logger.info("This is an info message")
logger.error("This is an error message")


pip install pydantic tenacity

cd ~/Projects/risk-app
python -m venv risk-env
source risk-env/bin/activate
streamlit run import-csv.py



snscrape.modules.twitter

Installation
$ pip install newsapi-python
Usage
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='API_KEY')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
sources = newsapi.get_sources()


Your API key is: 74a2bd236e034856a8ec0609ef8675e0


pip list | grep streamlit

pip list | grep certifi

pip install newsapi-python
pip install python-dotenv


pip install snscrape

export SSL_CERT_FILE=$(python -m certifi)


OK. I want to change the logic, in cases when Departure time is after current time, I want to use coordinats from the Departure time and to set some flag that this vessel is in the future and mark on the map in a different color.

2025-02-05 21:44:55,977 - DEBUG - VIS: efore calc position. Vessel: 9318761
2025-02-05 21:44:55,977 - DEBUG - Calculating position at time 2025-02-05T21:44:55.977546+01:00
2025-02-05 21:44:55,977 - DEBUG - Sorted vessel calls: [{'facility': {'locationType': 'TERMINAL', 'locationName': 'Ceuta Terminal', 'carrierTerminalCode': 'ESCUTTM', 'carrierTerminalGeoID': '0ZLAUQ3LM10O7', 'countryCode': 'ES', 'countryName': 'Spain', 'cityName': 'Ceuta', 'portName': 'Ceuta', 'carrierCityGeoID': '0AF077MB2CZUM', 'UNLocationCode': 'ESCEU'}, 'transport': {'inboundService': {'carrierVoyageNumber': '505N', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}, 'outboundService': {'carrierVoyageNumber': '506W', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'ACT', 'classifierDateTime': '2025-02-05T08:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'ACT', 'classifierDateTime': '2025-02-05T15:00:00'}]}, {'facility': {'locationType': 'TERMINAL', 'locationName': 'Gijon Terminal', 'carrierTerminalCode': 'ESGIJTM', 'carrierTerminalGeoID': '32QFEFWY64RI9', 'countryCode': 'ES', 'countryName': 'Spain', 'cityName': 'Gijon', 'portName': 'Gijon', 'carrierCityGeoID': '2QTZQCWBI7GQM', 'UNLocationCode': 'ESGIJ'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506W', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}, 'outboundService': {'carrierVoyageNumber': '506E', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-08T08:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-08T20:00:00'}]}, {'facility': {'locationType': 'TERMINAL', 'locationName': 'CSP Iberian Bilbao Terminal SL', 'carrierTerminalCode': 'ESBIOTM', 'carrierTerminalGeoID': '2VHNIB9V2TUVG', 'countryCode': 'ES', 'countryName': 'Spain', 'cityName': 'Bilbao', 'portName': 'Bilbao', 'carrierCityGeoID': '2QU0FZR1WG4FY', 'UNLocationCode': 'ESBIO'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506W', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}, 'outboundService': {'carrierVoyageNumber': '506E', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-09T08:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-10T14:00:00'}]}]
2025-02-05 21:44:55,977 - DEBUG - Raw input for dep_port: {'facility': {'locationType': 'TERMINAL', 'locationName': 'Ceuta Terminal', 'carrierTerminalCode': 'ESCUTTM', 'carrierTerminalGeoID': '0ZLAUQ3LM10O7', 'countryCode': 'ES', 'countryName': 'Spain', 'cityName': 'Ceuta', 'portName': 'Ceuta', 'carrierCityGeoID': '0AF077MB2CZUM', 'UNLocationCode': 'ESCEU'}, 'transport': {'inboundService': {'carrierVoyageNumber': '505N', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}, 'outboundService': {'carrierVoyageNumber': '506W', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'ACT', 'classifierDateTime': '2025-02-05T08:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'ACT', 'classifierDateTime': '2025-02-05T15:00:00'}]}
2025-02-05 21:44:55,978 - DEBUG - Raw input for arr_port: {'facility': {'locationType': 'TERMINAL', 'locationName': 'Gijon Terminal', 'carrierTerminalCode': 'ESGIJTM', 'carrierTerminalGeoID': '32QFEFWY64RI9', 'countryCode': 'ES', 'countryName': 'Spain', 'cityName': 'Gijon', 'portName': 'Gijon', 'carrierCityGeoID': '2QTZQCWBI7GQM', 'UNLocationCode': 'ESGIJ'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506W', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}, 'outboundService': {'carrierVoyageNumber': '506E', 'carrierServiceCode': 'Z03', 'carrierServiceName': 'Z03'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-08T08:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-08T20:00:00'}]}
2025-02-05 21:44:55,978 - DEBUG - dep_port['callSchedules'][1]['classifierDateTime']: 2025-02-05T15:00:00
2025-02-05 21:44:55,978 - DEBUG - arr_port['callSchedules'][0]['classifierDateTime']: 2025-02-08T08:00:00
2025-02-05 21:44:55,978 - DEBUG - Current time (now): 2025-02-05T21:44:55.978784+01:00
2025-02-05 21:44:55,978 - DEBUG - Parsed dep_time: 2025-02-05T15:00:00
2025-02-05 21:44:55,978 - DEBUG - Parsed arr_time: 2025-02-08T08:00:00
2025-02-05 21:44:55,979 - DEBUG - dep_time tzinfo: None
2025-02-05 21:44:55,979 - DEBUG - arr_time tzinfo: None
2025-02-05 21:44:55,979 - DEBUG - Departure time: 2025-02-05 15:00:00, Arrival time: 2025-02-08 08:00:00
2025-02-05 21:44:55,979 - ERROR - VIS: Error processing vessel 9318761: can't compare offset-naive and offset-aware datetimes


vesselIMONumber=9365843
dateRange=P7D


{
  "vessel": {
    "vesselIMONumber": "9365843",
    "carrierVesselCode": "Q8J",
    "vesselName": "ADMIRAL GALAXY",
    "vesselFlagCode": "LR",
    "vesselCallSign": "D5VL9"
  },
  "vesselCalls": [
    {
      "facility": {
        "locationType": "TERMINAL",
        "locationName": "East Port Said Terminal",
        "carrierTerminalCode": "EGPSDTM",
        "carrierTerminalGeoID": "0FYKXUTLQUD49",
        "countryCode": "EG",
        "countryName": "Egypt",
        "cityName": "Port Said East",
        "portName": "Port Said East",
        "carrierCityGeoID": "3I6W2NB2MQV7I",
        "UNLocationCode": "EGPSE"
      },
      "transport": {
        "inboundService": {
          "carrierVoyageNumber": "506S",
          "carrierServiceCode": "Z51",
          "carrierServiceName": "Z51 UFS PSD - LMS - ASD"
        },
        "outboundService": {
          "carrierVoyageNumber": "506N",
          "carrierServiceCode": "Z51",
          "carrierServiceName": "Z51 UFS PSD - LMS - ASD"
        }
      },
      "callSchedules": [
        {
          "transportEventTypeCode": "ARRI",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-07T09:00:00"
        },
        {
          "transportEventTypeCode": "DEPA",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-08T14:00:00"
        }
      ]
    },
    {
      "facility": {
        "locationType": "TERMINAL",
        "locationName": "Ashdod Terminal",
        "carrierTerminalCode": "ILASDPT",
        "carrierTerminalGeoID": "3NY2QH14JCGDD",
        "countryCode": "IL",
        "countryName": "Israel",
        "cityName": "Ashdod",
        "portName": "Ashdod",
        "carrierCityGeoID": "2JZIXTBC98ZGF",
        "UNLocationCode": "ILASH"
      },
      "transport": {
        "inboundService": {
          "carrierVoyageNumber": "506N",
          "carrierServiceCode": "Z51",
          "carrierServiceName": "Z51 UFS PSD - LMS - ASD"
        },
        "outboundService": {
          "carrierVoyageNumber": "507S",
          "carrierServiceCode": "Z51",
          "carrierServiceName": "Z51 UFS PSD - LMS - ASD"
        }
      },
      "callSchedules": [
        {
          "transportEventTypeCode": "ARRI",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-09T23:00:00"
        },
        {
          "transportEventTypeCode": "DEPA",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-11T23:00:00"
        }
      ]
    }
  ]
}

vesselIMONumber=9318761
dateRange=P7D

{
  "vessel": {
    "vesselIMONumber": "9318761",
    "carrierVesselCode": "R3U",
    "vesselName": "ADILIA I",
    "vesselFlagCode": "PT",
    "vesselCallSign": "CQEA7"
  },
  "vesselCalls": [
    {
      "facility": {
        "locationType": "TERMINAL",
        "locationName": "Ceuta Terminal",
        "carrierTerminalCode": "ESCUTTM",
        "carrierTerminalGeoID": "0ZLAUQ3LM10O7",
        "countryCode": "ES",
        "countryName": "Spain",
        "cityName": "Ceuta",
        "portName": "Ceuta",
        "carrierCityGeoID": "0AF077MB2CZUM",
        "UNLocationCode": "ESCEU"
      },
      "transport": {
        "inboundService": {
          "carrierVoyageNumber": "505N",
          "carrierServiceCode": "Z03",
          "carrierServiceName": "Z03"
        },
        "outboundService": {
          "carrierVoyageNumber": "506W",
          "carrierServiceCode": "Z03",
          "carrierServiceName": "Z03"
        }
      },
      "callSchedules": [
        {
          "transportEventTypeCode": "ARRI",
          "eventClassifierCode": "ACT",
          "classifierDateTime": "2025-02-05T08:00:00"
        },
        {
          "transportEventTypeCode": "DEPA",
          "eventClassifierCode": "ACT",
          "classifierDateTime": "2025-02-05T15:00:00"
        }
      ]
    },
    {
      "facility": {
        "locationType": "TERMINAL",
        "locationName": "Gijon Terminal",
        "carrierTerminalCode": "ESGIJTM",
        "carrierTerminalGeoID": "32QFEFWY64RI9",
        "countryCode": "ES",
        "countryName": "Spain",
        "cityName": "Gijon",
        "portName": "Gijon",
        "carrierCityGeoID": "2QTZQCWBI7GQM",
        "UNLocationCode": "ESGIJ"
      },
      "transport": {
        "inboundService": {
          "carrierVoyageNumber": "506W",
          "carrierServiceCode": "Z03",
          "carrierServiceName": "Z03"
        },
        "outboundService": {
          "carrierVoyageNumber": "506E",
          "carrierServiceCode": "Z03",
          "carrierServiceName": "Z03"
        }
      },
      "callSchedules": [
        {
          "transportEventTypeCode": "ARRI",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-08T08:00:00"
        },
        {
          "transportEventTypeCode": "DEPA",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-08T20:00:00"
        }
      ]
    },
    {
      "facility": {
        "locationType": "TERMINAL",
        "locationName": "CSP Iberian Bilbao Terminal SL",
        "carrierTerminalCode": "ESBIOTM",
        "carrierTerminalGeoID": "2VHNIB9V2TUVG",
        "countryCode": "ES",
        "countryName": "Spain",
        "cityName": "Bilbao",
        "portName": "Bilbao",
        "carrierCityGeoID": "2QU0FZR1WG4FY",
        "UNLocationCode": "ESBIO"
      },
      "transport": {
        "inboundService": {
          "carrierVoyageNumber": "506W",
          "carrierServiceCode": "Z03",
          "carrierServiceName": "Z03"
        },
        "outboundService": {
          "carrierVoyageNumber": "506E",
          "carrierServiceCode": "Z03",
          "carrierServiceName": "Z03"
        }
      },
      "callSchedules": [
        {
          "transportEventTypeCode": "ARRI",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-09T08:00:00"
        },
        {
          "transportEventTypeCode": "DEPA",
          "eventClassifierCode": "EST",
          "classifierDateTime": "2025-02-10T14:00:00"
        }
      ]
    }
  ]
}


2025-02-05 22:26:54,110 - DEBUG - VIS: BEFORE calc position. Vessel: 9365843
2025-02-05 22:26:54,111 - DEBUG - Calculating position at time 2025-02-05T22:26:54.110982+01:00
2025-02-05 22:26:54,111 - DEBUG - Sorted vessel calls: [{'facility': {'locationType': 'TERMINAL', 'locationName': 'East Port Said Terminal', 'carrierTerminalCode': 'EGPSDTM', 'carrierTerminalGeoID': '0FYKXUTLQUD49', 'countryCode': 'EG', 'countryName': 'Egypt', 'cityName': 'Port Said East', 'portName': 'Port Said East', 'carrierCityGeoID': '3I6W2NB2MQV7I', 'UNLocationCode': 'EGPSE'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506S', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}, 'outboundService': {'carrierVoyageNumber': '506N', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-07T09:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-08T14:00:00'}]}, {'facility': {'locationType': 'TERMINAL', 'locationName': 'Ashdod Terminal', 'carrierTerminalCode': 'ILASDPT', 'carrierTerminalGeoID': '3NY2QH14JCGDD', 'countryCode': 'IL', 'countryName': 'Israel', 'cityName': 'Ashdod', 'portName': 'Ashdod', 'carrierCityGeoID': '2JZIXTBC98ZGF', 'UNLocationCode': 'ILASH'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506N', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}, 'outboundService': {'carrierVoyageNumber': '507S', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-09T23:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-11T23:00:00'}]}]
2025-02-05 22:26:54,111 - DEBUG - Raw input for dep_port: {'facility': {'locationType': 'TERMINAL', 'locationName': 'East Port Said Terminal', 'carrierTerminalCode': 'EGPSDTM', 'carrierTerminalGeoID': '0FYKXUTLQUD49', 'countryCode': 'EG', 'countryName': 'Egypt', 'cityName': 'Port Said East', 'portName': 'Port Said East', 'carrierCityGeoID': '3I6W2NB2MQV7I', 'UNLocationCode': 'EGPSE'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506S', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}, 'outboundService': {'carrierVoyageNumber': '506N', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-07T09:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-08T14:00:00'}]}
2025-02-05 22:26:54,111 - DEBUG - Raw input for arr_port: {'facility': {'locationType': 'TERMINAL', 'locationName': 'Ashdod Terminal', 'carrierTerminalCode': 'ILASDPT', 'carrierTerminalGeoID': '3NY2QH14JCGDD', 'countryCode': 'IL', 'countryName': 'Israel', 'cityName': 'Ashdod', 'portName': 'Ashdod', 'carrierCityGeoID': '2JZIXTBC98ZGF', 'UNLocationCode': 'ILASH'}, 'transport': {'inboundService': {'carrierVoyageNumber': '506N', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}, 'outboundService': {'carrierVoyageNumber': '507S', 'carrierServiceCode': 'Z51', 'carrierServiceName': 'Z51 UFS PSD - LMS - ASD'}}, 'callSchedules': [{'transportEventTypeCode': 'ARRI', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-09T23:00:00'}, {'transportEventTypeCode': 'DEPA', 'eventClassifierCode': 'EST', 'classifierDateTime': '2025-02-11T23:00:00'}]}
2025-02-05 22:26:54,111 - DEBUG - dep_port['callSchedules'][1]['classifierDateTime']: 2025-02-08T14:00:00
2025-02-05 22:26:54,111 - DEBUG - arr_port['callSchedules'][0]['classifierDateTime']: 2025-02-09T23:00:00
2025-02-05 22:26:54,111 - DEBUG - Current time (now): 2025-02-05T22:26:54.111438+01:00
2025-02-05 22:26:54,111 - DEBUG - Parsed dep_time: 2025-02-08T14:00:00
2025-02-05 22:26:54,111 - DEBUG - Parsed arr_time: 2025-02-09T23:00:00
2025-02-05 22:26:54,111 - DEBUG - Departure time: 2025-02-08T14:00:00+01:00, Arrival time: 2025-02-09T23:00:00+01:00
2025-02-05 22:26:54,111 - DEBUG - dep_time tzinfo: CET
2025-02-05 22:26:54,111 - DEBUG - arr_time tzinfo: CET
2025-02-05 22:26:54,111 - DEBUG - No valid port interval found for current time



,ES,GIJ,Gijón,Gijon,O,AI,1234----,1207,,4332N 00540W,

EGDAM,Damietta,31.4667,31.75
EGEDK,Alexandria,31.1333,29.8167
EGPSD,Port Said,31.2667,32.3167

,EG,DAM,Dumyat (Damietta),Dumyat (Damietta),,RL,1234----,1401,QDX,3125N 03149E,
,EG,EDK,El Dekheila,El Dekheila,,RQ,1-------,9506,,,
,EG,PSD,Port Said,Port Said,,AI,1--4----,9601,,,

ESGIJ
EGPSE

,"AE","AMU","Abu Musa","Abu Musa",,"1-------","RL","0201",,"2552N 05501E",
,"AE","AJM","Ajman","Ajman",,"1-3-----","RL","0103","QAJ",,


2025-02-06 04:08:32,931 - INFO - Positions ---------- [{'name': 'ADAMS', 'lat': 29.8667, 'lon': 121.5167, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ADILIA I', 'lat': 43.5333, 'lon': -5.6667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ADMIRAL GALAXY', 'lat': 55.9667, 'lon': -2.8667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'AKACIA', 'lat': 55.55, 'lon': 9.75, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'AL QIBLA EXPRESS', 'lat': 36.05, 'lon': 120.3333, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ALESSIA', 'lat': 29.95, 'lon': 90.0667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ALEXANDRA MAERSK', 'lat': 51.2333, 'lon': 4.3833, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ALIANCA LEBLON', 'lat': 0.0, 'lon': 0.0, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ALIANCA MANAUS', 'lat': 0.0, 'lon': 0.0, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ALPHA KIRAWIRA', 'lat': -4.0667, 'lon': 39.6667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ALS KRONOS', 'lat': -27.45, 'lon': 153.0667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'AMERICO VESPUCIO', 'lat': 0.0, 'lon': 0.0, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'AMSTERDAM EXPRESS', 'lat': 12.05, 'lon': 77.1667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ANDREA', 'lat': 55.9667, 'lon': -2.8667, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}, {'name': 'ANGELICA MAERSK', 'lat': 25.0, 'lon': 55.05, 'last_update': '2025-02-06 04:08', 'status': 'future departure only', 'color': [255, 255, 0, 160]}]
