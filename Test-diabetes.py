import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
data = {
    "Inputs": {
        "WebServiceInput0":
        [
            {
                'PatientID': "1882185",
                'Pregnancies': "9",
                'PlasmaGlucose': "104",
                'DiastolicBloodPressure': "51",
                'TricepsThickness': "7",
                'SerumInsulin': "24",
                'BMI': "27.36983156",
                'DiabetesPedigree': "1.3504720469999998",
                'Age': "43",
            },
        ],
    },
    "GlobalParameters": {
    }
}

body = str.encode(json.dumps(data))

url = 'http://54c4ea9c-4dd5-40e0-8017-ab449b1fb0c1.eastus2.azurecontainer.io/score'
api_key = 'yeOad03BVwStJhQl8VXtxQRbN2JlUMNj' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))
