# personalfinances
Read transactions report from home banking and insert it into personal finances app. This first version read from report from Crédito Agricola Home Banking (Portugal) and write it into a google spreadsheet.

## Usage
```
usage: personalfinances [-h] [-v] [-c CONFIG] file_path

This allow us to load transactions from home banking report into Personal Finances app. This app could be a Google Spreadsheet, or other (not developed yet in this version).

positional arguments:
  file_path             path to the excel file with extraction

options:
  -h, --help            show this help message and exit
  -v, --version         show version
  -c CONFIG, --config CONFIG
                        path to configuration file
```
## Google Spreadsheet
### Get Google API Credentials
#### Enable the API
Before using Google API, you need to turn them on in a Google Cloud project.
You can turn on one or more APIs in a single Google Cloud project.
You can enable the Google Sheets API in the Google Cloud console (https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com).

#### Authorize credentials for a desktop application
To authenticate as an end user and access user data in the app, you need to create one or more OAuth 2.0 Client IDs.
A client ID is used to identify a single app to Google's OAuth servers.
If your app runs on multiple platforms, you must create a separate client ID for each platform.
1. In the Google Cloud console (https://console.cloud.google.com/apis/credentials), go to **Menu => APIs & Services => Credentials**
2. Click **Create Credentials => OAuth client ID**
3. Click **Application type => Desktop app**
4. In the **Name** field, type a name for the credential. This name is only shown in Google Cloud console
5. Click **Create**. The OAuth client created screen appears, showing your new Client ID and Client secret
6. Click **OK**. The newly created credential appears under **OAuth 2.0 Client IDs**
7. Save the downloaded JSON file as `credentials.json`, and move the file to your working directory.

Above information from Google Sheets documentation (https://developers.google.com/sheets/api/quickstart/python)

### Get Spreadsheet ID
A Google Spreadsheet has a unique spreadsheetId value, containing letters, numbers, hyphens, or underscores.
You can find the spreadsheet ID in a Google Sheets URL:

https://<span></span>docs.google.com/spreadsheets/d/<span style='color:green'>spreadsheetId</span>/edit#gid=0

## Future Work
For this project, I have a few ideas for future implementations:
* Add formula for the balance (last column on Google Spreadsheet);
* Create a decision tree/neuronal network/AI for fill the Category column;
* Add new home banking reports;
* Add other personal finances apps;