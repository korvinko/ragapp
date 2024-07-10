from langchain_community.document_loaders import AsyncChromiumLoader
from bs4 import BeautifulSoup

from helpers import DatasetCleaner

content = """
Zendit API (1.0.0)Download OpenAPI specification:DownloadZendit Support: support@zendit.io URL: https://developers.zendit.io  OverviewOur cloud-based Prepaid as a Service platform is now even more accessible with our reliable and efficient REST API. Our API provides seamless access to catalogs, balance information, and transactions for our:

International Mobile Top Up Products
International Mobile Bundles
Digital Gift Cards
Utility Payments
eSIM

Our platform is built with industry-standard security protocols and is designed to integrate seamlessly with your existing systems. We are committed to providing top-notch support, so please don't hesitate to reach out to our experienced zendit support team with any questions or support needs.
Zendit UniversityAs a supplement to this API guide, head over to Zendit University to understand the features of the system, how transaction flows work and how to get details from the catalog for your integration.
EnvironmentsTesting and development before going live with your product or service is crucial. That’s why we provide easy access to both our test bed and production environments through our gateway.
When you register for zendit, you’ll be provided with a test mode API key to use for simulated transactions. These transactions will not transfer real value, but will deduct from your test bed wallet. No credit card is required for this environment, and you can manage your wallet balance through our administration console.
When you’re ready to switch to production mode and start processing real transactions, you’ll need to fund your prepay wallet with real value. This will allow you to process transactions using your production key.
For more information on using our testbed environment to simulate different responses, refer to our comprehensive test mode environment documentation.
Please don’t hesitate to contact our support team if you have any questions or need assistance.
API SecurityWhen you sign up for our platform, you’ll be given access to your test mode key for testing your integration with our API. To send requests to an API endpoint, please use the Authentication header and include your API key as follows:
Authorization: Bearer YOUR_API_KEY

This will authenticate your requests and allow our API to process them securely. If you’re ready to switch to production mode and start processing real transactions, you’ll need to use your production key instead.
For more information about our security, refer to our security guide.
TransactionsTransparency and visibility are most important when it comes to processing transactions. That’s why we process transactions asynchronously and provide detailed status updates throughout the process.
When you send a transaction through our platform, we first validate the parameters of the transaction and then return the transaction ID in the response, along with any error messages if the transaction cannot be processed. From there, the transaction enters the zendit ecosystem and begins to move through our system.
To check on the status of your transaction, you can periodically poll the transaction using the transaction ID. Our system provides detailed updates on the transaction’s status as it moves through the system, including updates on receipt, wallet authorization, offer fulfillment, and completion.
Once the transaction is complete, you’ll receive a final status update that reports whether it was successful or encountered any errors during processing. Additionally, each transaction contains a history log that shows all status updates throughout the transaction process, providing you with a comprehensive view of the transaction’s journey through our platform.
To understand more about how to work with transactions, refer to our transaction guide.
Transaction ID
Providing our users with maximum flexibility when it comes to tracking their transactions is important. That’s why we don’t automatically generate transaction IDs – instead, you can supply any alphanumeric string of your choosing (such as an autonumber or a GUID) to track your transaction in our system.
To ensure that your transaction is processed correctly, you must supply the ID you will use to track the transaction status with each transaction request. Please note that transaction IDs are unique per zendit account and environment, so you can use the same transaction ID in both your test environment and production environment (once per environment).
If you’re using an autonumber scheme and have test and production environments, there’s no need to worry about collisions of IDs between the two environments. We understand the importance of keeping your test and production environments separate, and our system is designed to handle this seamlessly.
Queue and RetryWe strive to ensure that your transactions are processed reliably and efficiently. While most transactions are processed in real time, occasional recoverable errors can occur when a product provider in the ecosystem encounters an issue.
To address this, our API automatically sets a 15-minute timeout on the transaction and then retries it. If there is an extended problem with a product provider, the system will continue to retry the transaction every 15 minutes until it either completes successfully or fails after 24 hours.
If you would prefer not to use the queue and retry feature, you may turn the feature off in the client console on the API settings page.
For more information refer to the Queue and Retry guide.
Digital Gift Card and Utility Payment Required FeldsDigital Gift Cards and Utility Payments based on the brand requirements may require more information than just the recipient’s phone number. For the specific requirements of a Digital Gift Card or Utility Payment offer the list of fields required will be provided in the catalog. You can find all the possible fields that a these offers may require on the required fields page.
Error MessagesFor a detailed list of possible error statuses, please see Error Message Guide.
Transaction Log Structure
zendit Transactions contain a log of activity as the transaction progresses through the system. You can find this on any transaction under the “log” structure. The log will give more detail about the transaction from when it was submitted, when it was authorized against the wallet, when it was submitted for fulfillment and any errors that were encountered while processing will be noted at the stage where the transaction failed.
Searching using createdAt date on transactionsWhen using the createdAt date on the transaction search endpoints (/topup/purchases, /transactions and /voucher/purchases) dates use the RFC 3339 format in UTC Timezone (e.g. 2023-02-15T03:15:22Z)
When searching with createdAt there are a few prefixes you can add to the time in order to search around the timestamp supplied. The search formats are as follows:



Format
Description
Example



No prefix
Search for an exact date/time
2023-02-15T03:15:22Z will search for transactions that match February 15, 2023 at 3:15 and 22 seconds in UTC timezone


lt
Search for a date/time that is earlier than the supplied value
lt2023-02-15T03:15:22Z will search for transactions that are before February 15, 2023 at 3:15 and 22 seconds in UTC timezone


lte
Search for a date/time that is equal to the supplied value and earlier
lte2023-02-15T03:15:22Z will search for transactions that are equal February 15, 2023 at 3:15 and 22 seconds in UTC timezone and transactions that are earlier


gt
Search for a date/time that is later than the supplied value
gt2023-02-15T03:15:22Z will search for transactions that are after February 15, 2023 at 3:15 and 22 seconds in UTC timezone


gte
Search for a date/time that is equal to the supplied value and later
gte2023-02-15T03:15:22Z will search for transactions that are equal to February 15, 2023 at 3:15 and 22 seconds in UTC timezone and transactions that are later


RegionsCatalog methods support filtering/searching products by region. Regions are string values and supported with the following values:

Global (includes global esim)
Africa
Asia
Caribbean
Central America
Eastern Europe
Western Europe
North America
Oceania
South America
South Asia
Southeast Asia
Middle East and North Africa

Try out the APISwagger pages for the api can be found at https://api.zendit.io/swagger/index.html
MSISDN (Phone Number) LookupPhone number lookup is currently in beta with select clients. The beta group is closed to new participants. For testing in the test mode environment, the following phone number patterns may be used to get simulated results:



Phone Number Pattern
Country Result
Carrier Result



+502 3XXX XXXX
GT
Claro


+502 5XXX XXXX
GT
Tigo


+1 5XX XXX XXXX
US
Verizon


+1 6XX XXX XXXX
US
T-Mobile


Using any number sequence to fill in the X in these numbers will yield these results in the test mode environment. All other phone numbers will yield a phone number not found error. For the production environment, all valid phone numbers will work.
Note that for US phone numbers and some destinations that use MVNOs (e.g. Boost, Mint) the carrier result will return the network the device is assigned to (e.g. T-Mobile in the case of Mint Mobile) and will not return the name of the MVNO. This is a limitation of the service. 
Clients who aren't included in the beta will receive an error on the endpoints of LOOKUP_NOT_ENABLED when calling the endpoint.
ReportsTransaction reports can be generated from the API. Transaction reports are generated asynchronously and are first called with the POST request to generate the report with a start datetime and end datetime. The report generates a CSV file of transactions that are either in DONE or FAILED status. Transactions that have not completed will not be included in the report since their final status is not known until they complete.
For the time period, the start datetime includes transactions that are at the start datetime or later. For the end datetime, transactions included in the report will be earlier than the set time. As an example, to produce a report for 1 day, set the start datetime to "2024-02-01T00:00:00Z" and the end datetime to "2024-02-02T00:00:00Z" and it will include all transactions starting from midnight on February 1, 2024 and completing before February 2, 2024. Transactions still in flight on February 1, 2024 but not completing until February 2, 2024 will appear on a report for 1 day for February 2, 2024.
When selecting a time period, consider the length of time between the start and end time and your transaction volume as a guide to how long a report may take to generate. The longer the period and number of transactions completed within this period will require more time to generate the report.
After sending a generate report, you will receive an acknoledgement of the request including a system generated report Id to track the status. You may poll the status endpoint (polling interval should be at least 1 second between poll requests) to check on the progress of the report. When the report status has responded with Ready, the file is ready to download.
Downloading the report you may use the reportId and filename included in the status response. You may also use the downloadUrl which has the fully formed API call to download the report. Downloading the report must include your API Key since report downloads are not on a public URL. 
In the case of failure, the failure reason will be returned in the error structure and the report will have a FAILED status. You can check the log structure in the report to find out more information as to why the report generation failed.
AccountCheck your account balance. 
For wallet inforatmion see the zendit wallet guide.
Get current balance of wallet Authorizations:ApiKeyResponses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/balancehttps://api.zendit.io/v1/balance Request samples CurlCopycurl -X GET -H "Authorization: [[apiKey]]" "https://https://api.zendit.io/v1//v1/balance"
 Response samples 200400401403500Content typeapplication/jsonCopy{"availableBalance": 0,"currency": "string"}eSIMeSIM Catalog and Transaction Operations. For more information about eSIM products see the eSIM Guide. 
For catalog operations refer to the zendit catalog guide.
For transactions refer to the zendit transaction guide.
For webhooks refer to the zendit webhook guide.
eSIM Purchase  Webhook Request Body schema: application/jsoneSIM purchase result
brandstring Brand of eSIM
confirmationobject (dto.ESimConfirmation)  Confirmation of a completed eSIM transaction
costinteger Cost of the eSIM to Partner
costCurrencystring Currency of cost to eSIM Partner
countrystring Destination country for eSIM offer (blank when eSIM offer is regional)
createdAtstring Date/time transaction was created
dataGBnumber GB of data included in eSIM (0 when data is unlimited)
dataSpeedsArray of strings (dataSpeed) Items Enum: "2G" "3G" "4G" "5G"  Data speeds available for eSIM
dataUnlimitedboolean Flag indicating whether data is unlimited on the eSIM
durationDaysinteger Duration of the eSIM offer in days
errorobject (dto.Error)  Error information encountered while processing transaction
logArray of objects (dto.TransactionLogItem)  Trace log for fulfillment of transaction
notesstring Notes included about the eSIM offer
offerIdstring Catalog ID of the offer (used for purchases)
priceinteger Price to customer for eSIM (when using the zendit pricing module)
priceCurrencystring Currency of price charged to customer for eSIM (when using the zendit pricing module)
priceTypestring (priceType)  Enum: "FIXED" "RANGE"  Price type for the eSIM (Fixed or Range)
productTypestring (productType)  Enum: "TOPUP" "VOUCHER" "ESIM" "RECHARGE_SANDBOX" "RECHARGE_WITH_CREDIT_CARD"  Product type for eSIM
regionsArray of strings (regions) Items Enum: "Global" "Africa" "Asia" "Caribbean" "Central America" "Eastern Europe" "Western Europe" "North America" "Oceania" "South America" "South Asia" "Southeast Asia" "Middle East and North Africa"  Regions for the eSIM
roamingArray of objects (dto.ESimRoaming)  Roaming information for regional eSIM products (empty array for NO ROAM eSIM offers)
shortNotesstring Short notes for eSIM offer
smsNumberinteger Included SMS messages with eSIM (0 when unlimited or not included, check smsUnlimited flag)
smsUnlimitedboolean Flag whether SMS messaging is unlimited for offer
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status of transaction
subTypesArray of strings Subtypes for the eSIM offer
transactionIdstring Transaction Id provided by partner
updatedAtstring Date/Time of last update to transaction
valueobject (dto.PurchaseValue)  Value and type of price used for purchase of ranged products
voiceMinutesinteger Voice minutes included in eSIM offer (0 when unlimited or not included, check voiceUnlimited Flag)
voiceUnlimitedboolean Flag whether voice minutes are unlimited for the offer
Responses200 Webhook processed successfully
500 Internal Server Error
 Request samples PayloadContent typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","confirmation": {"activationCode": "string","externalReferenceId": "string","iccid": "string","redemptionInstructions": "string","smdpAddress": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","dataGB": 0,"dataSpeeds": ["2G"],"dataUnlimited": true,"durationDays": 0,"error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","regions": ["Global"],"roaming": [{"country": "string","dataSpeeds": ["2G"]}],"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"status": "DONE","subTypes": ["string"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0},"voiceMinutes": 0,"voiceUnlimited": true}Get list of eSIM offers Authorizations:ApiKeyquery Parameters_limitrequirednumber Number of items to return (Minimum 1, Maximum 1,024)
_offsetrequirednumber Number of items to skip – use with limit for pagination
brandstring Brand (Carrier for MTU) to filter
countrystring 2 letter ISO code for the destination country to filter
regionsstring (regions)  Enum: "Global" "Africa" "Asia" "Caribbean" "Central America" "Eastern Europe" "Western Europe" "North America" "Oceania" "South America" "South Asia" "Southeast Asia" "Middle East and North Africa"  String for the name of the region to filter
subTypestring Offer subtype to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/esim/offershttps://api.zendit.io/v1/esim/offers Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/esim/offers?_limit=&_offset=&brand=&country=®ions=&subType="
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{"brand": "string","cost": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"country": "string","createdAt": "string","dataGB": 0,"dataSpeeds": ["2G"],"dataUnlimited": true,"durationDays": 0,"enabled": true,"notes": "string","offerId": "string","price": {"currency": "string","fixed": 0,"fx": 0,"margin": 0,"max": 0,"min": 0,"suggestedFixed": 0,"suggestedFx": 0},"priceType": "FIXED","productType": "TOPUP","regions": ["Global"],"roaming": [{"country": "string","dataSpeeds": ["2G"]}],"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"subTypes": ["string"],"updatedAt": "string","voiceMinutes": 0,"voiceUnlimited": true}],"offset": 0,"total": 0}Get an eSIM offer by the offer ID Authorizations:ApiKeypath ParametersofferIdrequiredstring Catalog Id to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Item not found
500 Internal Server Error
get/esim/offers/{offerId}https://api.zendit.io/v1/esim/offers/{offerId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/esim/offers/{offerId}"
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","cost": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"country": "string","createdAt": "string","dataGB": 0,"dataSpeeds": ["2G"],"dataUnlimited": true,"durationDays": 0,"enabled": true,"notes": "string","offerId": "string","price": {"currency": "string","fixed": 0,"fx": 0,"margin": 0,"max": 0,"min": 0,"suggestedFixed": 0,"suggestedFx": 0},"priceType": "FIXED","productType": "TOPUP","regions": ["Global"],"roaming": [{"country": "string","dataSpeeds": ["2G"]}],"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"subTypes": ["string"],"updatedAt": "string","voiceMinutes": 0,"voiceUnlimited": true}Get list of eSim transactions Authorizations:ApiKeyquery Parameters_limitrequirednumber Number of items to retrieve (Minimum 1, Masimum 1,024)
_offsetrequiredinteger Number of items to skip – use with limit for pagination
createdAtstring Data filter – see Overview section for filtering by date
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/esim/purchaseshttps://api.zendit.io/v1/esim/purchases Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/esim/purchases?_limit=&_offset=&createdAt=&status="
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{"brand": "string","confirmation": {"activationCode": "string","externalReferenceId": "string","iccid": "string","redemptionInstructions": "string","smdpAddress": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","dataGB": 0,"dataSpeeds": ["2G"],"dataUnlimited": true,"durationDays": 0,"error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","regions": ["Global"],"roaming": [{"country": "string","dataSpeeds": ["2G"]}],"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"status": "DONE","subTypes": ["string"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0},"voiceMinutes": 0,"voiceUnlimited": true}],"offset": 0,"total": 0}Purchase an eSIM offer for a new eSIM or add an offer to an existing eSIM Authorizations:ApiKeyRequest Body schema: application/jsoniccidstring ICCID to apply plan (omit to issue a new eSIM)
offerIdrequiredstring Catalog ID of the offer (used for purchases)
transactionIdrequiredstring Transaction Id provided by partner
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
post/esim/purchaseshttps://api.zendit.io/v1/esim/purchases Request samples PayloadCurlContent typeapplication/jsonCopy{"iccid": "string","offerId": "string","transactionId": "string"} Response samples 200400401403500Content typeapplication/jsonCopy{"status": "string","transactionId": "string"}Get eSim transaction by id Authorizations:ApiKeypath ParameterstransactionIdrequiredstring Transaction ID to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/esim/purchases/{transactionId}https://api.zendit.io/v1/esim/purchases/{transactionId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/esim/purchases/{transactionId}"
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","confirmation": {"activationCode": "string","externalReferenceId": "string","iccid": "string","redemptionInstructions": "string","smdpAddress": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","dataGB": 0,"dataSpeeds": ["2G"],"dataUnlimited": true,"durationDays": 0,"error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","regions": ["Global"],"roaming": [{"country": "string","dataSpeeds": ["2G"]}],"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"status": "DONE","subTypes": ["string"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0},"voiceMinutes": 0,"voiceUnlimited": true}Get eSim QR code by transaction id Authorizations:ApiKeypath ParameterstransactionIdrequiredstring Transaction ID to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/esim/purchases/{transactionId}/qrcodehttps://api.zendit.io/v1/esim/purchases/{transactionId}/qrcode Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/esim/purchases/{transactionId}/qrcode"
 Response samples 200400401403404500Content typeimage/pngapplication/jsonimage/pngNo sampleRetrieve usage of active and queued plans on an eSIM. Authorizations:ApiKeypath ParametersiccIdrequiredstring Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/esim/{iccId}/planshttps://api.zendit.io/v1/esim/{iccId}/plans Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/esim/{iccId}/plans" 
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"list": [{"description": "string","endAt": "string","iccid": "string","initialDataGB": 0,"offerId": "string","reamainingDataGB": 0,"startAt": "string","status": "ACTIVE"}],"total": 0}Mobile Top UpMobile Top Up, Mobile Bundle, and Mobile Data Catalog and Transaction Operations
For catalog operations refer to the zendit catalog guide.
For transactions refer to the zendit transaction guide.
For webhooks refer to the zendit webhook guide.
Mobile Top Up Purchase  Webhook Request Body schema: application/jsonMobile Top Up, Mobile Bundle, and Mobile Data purchase result
brandstring Brand of TopUp (Carrier)
confirmationobject (dto.Confirmation)  Confirmation information for the topup
costinteger Zendit price for partner
costCurrencystring 3 letter ISO code for currency of cost
countrystring Destination country for Topup
createdAtstring Date/time transaction was created
dataGBnumber Amount of data included in offer for Bundles and Data plans (0 when data is unlimited)
dataUnlimitedboolean Flag for bundles and data plans with unlimited data
durationDaysinteger Duration of the bundle or data plan offer in days
errorobject (dto.Error)  Error information encountered while processing transaction
logArray of objects (dto.TransactionLogItem)  Trace log for fulfillment of transaction
notesstring Notes included about the Topup offer
offerIdstring Catalog ID of the offer (used for purchases)
priceinteger Price to customer for Topup (when using the zendit pricing module)
priceCurrencystring Currency of price charged to customer for Topup (when using the zendit pricing module)
priceTypestring (priceType)  Enum: "FIXED" "RANGE"  Price type for the Topup (Fixed or Range)
productTypestring (productType)  Enum: "TOPUP" "VOUCHER" "ESIM" "RECHARGE_SANDBOX" "RECHARGE_WITH_CREDIT_CARD"  Product type for Topup
recipientPhoneNumberstring Recipient of the topup
regionsArray of strings (regions) Items Enum: "Global" "Africa" "Asia" "Caribbean" "Central America" "Eastern Europe" "Western Europe" "North America" "Oceania" "South America" "South Asia" "Southeast Asia" "Middle East and North Africa"  Regions for the Topup
sendinteger Value sent to the recipient
sendCurrencystring Currency of the value sent
senderobject (dto.TopupSender)  Sender information for the topup
shortNotesstring Short notes for Topup offer
smsNumberinteger Included SMS messages with Topup (0 when unlimited or not included, check smsUnlimited flag)
smsUnlimitedboolean Flag whether SMS messaging is unlimited for offer
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status of transaction
subTypesArray of strings (topupSubtypes) Items Enum: "Mobile Top Up" "Mobile Bundle" "Mobile Data"  Subtypes for the Topup offer
transactionIdstring Transaction Id provided by partner
updatedAtstring Date/Time of last update to transaction
valueobject (dto.PurchaseValue)  Value and type of price used for purchase of ranged products
voiceMinutesinteger Voice minutes included with Topup (0 when unlimited or not included, check voiceUnlimited Flag)
voiceUnlimitedboolean Flag whether voice minutes are unlimited for the offer
Responses200 Webhook processed successfully
500 Internal Server Error
 Request samples PayloadContent typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","confirmation": {"confirmationNumber": "string","externalReferenceId": "string","transactionTime": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","dataGB": 0,"dataUnlimited": true,"durationDays": 0,"error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","recipientPhoneNumber": "string","regions": ["Global"],"send": 0,"sendCurrency": "string","sender": {"country": "string","phoneNumber": "string"},"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"status": "DONE","subTypes": ["Mobile Top Up"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0},"voiceMinutes": 0,"voiceUnlimited": true}Get list of topup offers Authorizations:ApiKeyquery Parameters_limitrequirednumber Number of items to return (Minimum 1, Maximum 1,024)
_offsetrequirednumber Number of items to skip – use with limit for pagination
brandstring Brand (Carrier for MTU) to filter
countrystring 2 letter ISO code for the destination country to filter
regionsstring (regions)  Enum: "Global" "Africa" "Asia" "Caribbean" "Central America" "Eastern Europe" "Western Europe" "North America" "Oceania" "South America" "South Asia" "Southeast Asia" "Middle East and North Africa"  String for the name of the region to filter
subTypestring (topupSubtypes)  Enum: "Mobile Top Up" "Mobile Bundle" "Mobile Data"  Offer subtype to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/topups/offershttps://api.zendit.io/v1/topups/offers Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/topups/offers?_limit=&_offset=&brand=&country=®ions=&subType="        
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{"brand": "string","cost": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"country": "string","createdAt": "string","dataGB": 0,"dataUnlimited": true,"durationDays": 0,"enabled": true,"notes": "string","offerId": "string","price": {"currency": "string","fixed": 0,"fx": 0,"margin": 0,"max": 0,"min": 0,"suggestedFixed": 0,"suggestedFx": 0},"priceType": "string","productType": "TOPUP","regions": ["Global"],"send": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"subTypes": ["Mobile Top Up"],"updatedAt": "string","voiceMinutes": 0,"voiceUnlimited": true}],"offset": 0,"total": 0}Get a topup offer by the offer ID Authorizations:ApiKeypath ParametersofferIdrequiredstring Catalog Id to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Item not found
500 Internal Server Error
get/topups/offers/{offerId}https://api.zendit.io/v1/topups/offers/{offerId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/topups/offers/{offerId}"        
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","cost": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"country": "string","createdAt": "string","dataGB": 0,"dataUnlimited": true,"durationDays": 0,"enabled": true,"notes": "string","offerId": "string","price": {"currency": "string","fixed": 0,"fx": 0,"margin": 0,"max": 0,"min": 0,"suggestedFixed": 0,"suggestedFx": 0},"priceType": "string","productType": "TOPUP","regions": ["Global"],"send": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"subTypes": ["Mobile Top Up"],"updatedAt": "string","voiceMinutes": 0,"voiceUnlimited": true}Get list of topup transactions Authorizations:ApiKeyquery Parameters_limitrequiredinteger Number of items to return (Minimum 1, Maximum 1,024)
_offsetrequiredinteger Number of items to skip – use with limit for pagination
createdAtstring Data filter – see Overview section for filtering by date
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/topups/purchaseshttps://api.zendit.io/v1/topups/purchases Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/topups/purchases?_limit=&_offset=&createdAt=&status="
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{"brand": "string","confirmation": {"confirmationNumber": "string","externalReferenceId": "string","transactionTime": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","dataGB": 0,"dataUnlimited": true,"durationDays": 0,"error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","recipientPhoneNumber": "string","regions": ["Global"],"send": 0,"sendCurrency": "string","sender": {"country": "string","phoneNumber": "string"},"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"status": "DONE","subTypes": ["Mobile Top Up"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0},"voiceMinutes": 0,"voiceUnlimited": true}],"offset": 0,"total": 0}Create transaction for purchase Authorizations:ApiKeyRequest Body schema: application/jsonofferIdrequiredstring Catalog ID of the offer
recipientPhoneNumberrequiredstring Recipient of the topup in e.164 format
senderobject (dto.TopupSender)  Optional sender information
transactionIdrequiredstring Transaction Id provided by partner
valueobject (dto.PurchaseValue)  Purchase amount and type required for RANGE offers/omitted for FIXED offers
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
post/topups/purchaseshttps://api.zendit.io/v1/topups/purchases Request samples PayloadCurlContent typeapplication/jsonCopy Expand all  Collapse all {"offerId": "string","recipientPhoneNumber": "string","sender": {"country": "string","phoneNumber": "string"},"transactionId": "string","value": {"type": "COST","value": 0}} Response samples 200400401403500Content typeapplication/jsonCopy{"status": "string","transactionId": "string"}Get topup transaction by id Authorizations:ApiKeypath ParameterstransactionIdrequiredstring Transaction Id to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/topups/purchases/{transactionId}https://api.zendit.io/v1/topups/purchases/{transactionId} Request samples CurlCopycurl -X POST\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
-H "Content-Type: application/json"\
"https://api.zendit.io/v1/topups/purchases"      
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","confirmation": {"confirmationNumber": "string","externalReferenceId": "string","transactionTime": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","dataGB": 0,"dataUnlimited": true,"durationDays": 0,"error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","recipientPhoneNumber": "string","regions": ["Global"],"send": 0,"sendCurrency": "string","sender": {"country": "string","phoneNumber": "string"},"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"status": "DONE","subTypes": ["Mobile Top Up"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0},"voiceMinutes": 0,"voiceUnlimited": true}VoucherDigital Gift Card and Prepaid Utilities Catalog and Transaction Operations
For catalog operations refer to the zendit catalog guide.
For transactions refer to the zendit transaction guide.
For webhooks refer to the zendit webhook guide.
Voucher Purchase  Webhook Request Body schema: application/jsonDigital Gift Card and Utility purchase result
brandstring Brand of Gift Card or Utility
confirmationobject (dto.Confirmation)  Confirmation information for the gift or utility
costinteger Zendit price for partner
costCurrencystring 3 letter ISO code for currency of cost
countrystring Destination country for Gift Card or Utility
createdAtstring Date/time transaction was created
errorobject (dto.Error)  Error information encountered while processing transaction
fieldsArray of objects (dto.VoucherField)  Required fields for transaction
logArray of objects (dto.TransactionLogItem)  Trace log for fulfillment of transaction
notesstring Notes included about the gift card or utility offer
offerIdstring Catalog ID of the offer
priceinteger Price to customer for gift card or utility (when using the zendit pricing module)
priceCurrencystring Currency of price charged to customer for gift card or utility (when using the zendit pricing module)
priceTypestring (priceType)  Enum: "FIXED" "RANGE"  Price type for the gift card or utility (Fixed or Range)
productTypestring (productType)  Enum: "TOPUP" "VOUCHER" "ESIM" "RECHARGE_SANDBOX" "RECHARGE_WITH_CREDIT_CARD"  Product type for gift card or utility
receiptobject (dto.VoucherReceipt)  Receipt for the gift card or utility
regionsArray of strings (regions) Items Enum: "Global" "Africa" "Asia" "Caribbean" "Central America" "Eastern Europe" "Western Europe" "North America" "Oceania" "South America" "South Asia" "Southeast Asia" "Middle East and North Africa"  Regions for the gift card or utility
sendinteger Value sent to the recipient
sendCurrencystring Currency of the value sent
shortNotesstring Short notes for gift card or utility offer
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status of transaction
subTypesArray of strings Subtypes for the gift card or utility offer
transactionIdstring Transaction Id provided by partner
updatedAtstring Date/Time of last update to transaction
valueobject (dto.PurchaseValue)  Value and type of price used for purchase of ranged products
Responses200 Webhook processed successfully
500 Internal Server Error
 Request samples PayloadContent typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","confirmation": {"confirmationNumber": "string","externalReferenceId": "string","transactionTime": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","error": {"code": "string","description": "string","message": "string"},"fields": [{"key": "string","value": "string"}],"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","receipt": {"currency": "string","epin": "string","expiresAt": "string","instructions": "string","notes": "string","recipientCustomerServiceNumber": "string","send": 0,"senderCustomerServiceNumber": "string","terms": "string"},"regions": ["Global"],"send": 0,"sendCurrency": "string","shortNotes": "string","status": "DONE","subTypes": ["string"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0}}Get list of voucher offers Authorizations:ApiKeyquery Parameters_limitrequirednumber Number of items to return (Minimum 1, Maximum 1,024)
_offsetrequirednumber Number of items to skip – use with limit for pagination
brandstring Brand (Carrier for MTU) to filter
countrystring 2 letter ISO code for the destination country to filter
regionsstring (regions)  Enum: "Global" "Africa" "Asia" "Caribbean" "Central America" "Eastern Europe" "Western Europe" "North America" "Oceania" "South America" "South Asia" "Southeast Asia" "Middle East and North Africa"  String for the name of the region to filter
subTypestring Offer subtype to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/vouchers/offershttps://api.zendit.io/v1/vouchers/offers Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/vouchers/offers?_limit=&_offset=&brand=&country=&subType="     
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{"brand": "string","cost": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"country": "string","createdAt": "string","dataGB": 0,"dataUnlimited": true,"durationDays": 0,"enabled": true,"notes": "string","offerId": "string","price": {"currency": "string","fixed": 0,"fx": 0,"margin": 0,"max": 0,"min": 0,"suggestedFixed": 0,"suggestedFx": 0},"priceType": "string","productType": "TOPUP","regions": ["Global"],"send": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"shortNotes": "string","smsNumber": 0,"smsUnlimited": true,"subTypes": ["Mobile Top Up"],"updatedAt": "string","voiceMinutes": 0,"voiceUnlimited": true}],"offset": 0,"total": 0}Get a voucher offer by the offer ID Authorizations:ApiKeypath ParametersofferIdrequiredstring Catalog Id to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Item not found
500 Internal Server Error
get/vouchers/offers/{offerId}https://api.zendit.io/v1/vouchers/offers/{offerId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/vouchers/offers/{offerId}"
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","cost": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"country": "string","createdAt": "string","enabled": true,"notes": "string","offerId": "string","price": {"currency": "string","fixed": 0,"fx": 0,"margin": 0,"max": 0,"min": 0,"suggestedFixed": 0,"suggestedFx": 0},"priceType": "string","productType": "TOPUP","regions": ["Global"],"requiredFields": ["string"],"send": {"currency": "string","fixed": 0,"fx": 0,"max": 0,"min": 0},"shortNotes": "string","subTypes": ["string"],"updatedAt": "string"}Get list of transactions Authorizations:ApiKeyquery Parameters_limitrequirednumber Number of items to return (Minimum 1, Maximum 1,024)
_offsetrequirednumber Number of items to skip – use with limit for pagination
createdAtstring Data filter – see Overview section for filtering by date
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
get/vouchers/purchaseshttps://api.zendit.io/v1/vouchers/purchases Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/vouchers/purchases?_limit=&_offset=&createdAt=&status="      
 Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{ }],"offset": 0,"total": 0}Create transaction for purchase Authorizations:ApiKeyRequest Body schema: application/jsonfieldsrequiredArray of objects (dto.VoucherField)  Fields required for offer
offerIdrequiredstring Catalog ID of the offer
transactionIdrequiredstring Transaction Id provided by partner
valueobject (dto.PurchaseValue)  Purchase amount and type required for RANGE offers/omitted for FIXED offers
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
post/vouchers/purchaseshttps://api.zendit.io/v1/vouchers/purchases Request samples PayloadCurlContent typeapplication/jsonCopy Expand all  Collapse all {"fields": [{"key": "string","value": "string"}],"offerId": "string","transactionId": "string","value": {"type": "COST","value": 0}} Response samples 200400401403500Content typeapplication/jsonCopy{"status": "string","transactionId": "string"}Get purchase transaction by id Authorizations:ApiKeypath ParameterstransactionIdrequiredstring Transaction Id to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/vouchers/purchases/{transactionId}https://api.zendit.io/v1/vouchers/purchases/{transactionId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/vouchers/purchases/{transactionId}"
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"brand": "string","confirmation": {"confirmationNumber": "string","externalReferenceId": "string","transactionTime": "string"},"cost": 0,"costCurrency": "string","country": "string","createdAt": "string","error": {"code": "string","description": "string","message": "string"},"fields": [{"key": "string","value": "string"}],"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"notes": "string","offerId": "string","price": 0,"priceCurrency": "string","priceType": "FIXED","productType": "TOPUP","receipt": {"currency": "string","epin": "string","expiresAt": "string","instructions": "string","notes": "string","recipientCustomerServiceNumber": "string","send": 0,"senderCustomerServiceNumber": "string","terms": "string"},"regions": ["Global"],"send": 0,"sendCurrency": "string","shortNotes": "string","status": "DONE","subTypes": ["string"],"transactionId": "string","updatedAt": "string","value": {"type": "COST","value": 0}}Transaction StatusStatus of Zendit Transactions
For transactions refer to the zendit transaction guide.
Transaction ShieldWall  Webhook Request Body schema: application/jsonTransaction info for verification
amountinteger Value of the transaction in Cost
createdAtstring Date/Time the transaction was created
currencystring 3 letter ISO code for currency of the amount
errorobject (dto.Error)  Error information for transaction
logArray of objects (dto.TransactionLogItem)  Trace log for fulfillment of transaction
productTypestring (productType)  Enum: "TOPUP" "VOUCHER" "ESIM" "RECHARGE_SANDBOX" "RECHARGE_WITH_CREDIT_CARD"  Product type for transaction
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status of transaction
transactionIdstring Transaction Id provided by partner
typestring (transactionType)  Enum: "DEBIT" "CREDIT"  Type of transaction (Credit or Debit)
updatedAtstring Date/Time of last update to transaction
Responses200 Return a 200 for recognized transactions.
404 Return a 404 to block unrecognized transactions.
 Request samples PayloadContent typeapplication/jsonCopy Expand all  Collapse all {"amount": 0,"createdAt": "string","currency": "string","error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"productType": "TOPUP","status": "DONE","transactionId": "string","type": "DEBIT","updatedAt": "string"}Get list of transactions Authorizations:ApiKeyquery Parameters_limitrequirednumber Number of items to return (Minimum 1, Maximum 1,024)
_offsetrequirednumber Number of items to skip – use with limit for pagination
createdAtstring Data filter – see Overview section for filtering by date
productTypestring (productType)  Enum: "TOPUP" "VOUCHER" "ESIM" "RECHARGE_SANDBOX" "RECHARGE_WITH_CREDIT_CARD"  Product type to filter
statusstring (transactionStatus)  Enum: "DONE" "FAILED" "PENDING" "ACCEPTED" "AUTHORIZED" "IN_PROGRESS"  Status to filter
typestring (transactionType)  Enum: "DEBIT" "CREDIT"  Type of transaction to filter
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/transactionshttps://api.zendit.io/v1/transactions Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/transactions?_limit=&_offset=&createdAt=&productType=&status=&type="
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"limit": 0,"list": [{"amount": 0,"createdAt": "string","currency": "string","error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"productType": "TOPUP","status": "DONE","transactionId": "string","type": "DEBIT","updatedAt": "string"}],"offset": 0,"total": 0}Get transaction by id Authorizations:ApiKeypath ParameterstransactionIdrequiredstring Transaction Id to find
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/transactions/{transactionId}https://api.zendit.io/v1/transactions/{transactionId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/transactions/{transactionId}"
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"amount": 0,"createdAt": "string","currency": "string","error": {"code": "string","description": "string","message": "string"},"log": [{"dateTime": "string","status": "DONE","statusMessage": "string"}],"productType": "TOPUP","status": "DONE","transactionId": "string","type": "DEBIT","updatedAt": "string"}ToolsTools for Zendit API 
Tools currently includes the Phone Number Lookup tool that is currently in beta for select clients. 
BETA Lookup an MSISDN. Authorizations:ApiKeypath Parametersmsisdnrequiredstring MSISDN (phone number) to lookup in e.164 format
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/tools/phonenumberlookup/{msisdn}https://api.zendit.io/v1/tools/phonenumberlookup/{msisdn} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/tools/{msisdn}"
 Response samples 200400401403404500Content typeapplication/jsonCopy{"brand": "string","country": "string","mobileCountryCode": "string","mobileNetworkCode": "string","msisdn": "string"}ReportsTransacion detail reports that can be downloaded in CSV format for a specified start datetime and ending at a specified end datetime 
Generate a transaction report Authorizations:ApiKeyRequest Body schema: application/jsonendLtrequiredstring End date for the report. Transactions returned will have a finish date less than this value (e.g. 2024-02-01T00:00:00Z would return all transactions less than the date/time specified.)
startGterequiredstring Start date for the report. Transactions returned will start at the date/time specified including the date/time that is specified and will return transactions with a finished date that is greater than or equal to sthe start date time.
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
500 Internal Server Error
post/reports/transactionshttps://api.zendit.io/v1/reports/transactions Request samples PayloadCurlContent typeapplication/jsonCopy{"endLt": "string","startGte": "string"} Response samples 200400401403500Content typeapplication/jsonCopy Expand all  Collapse all {"createdAt": "string","error": {"code": "string","description": "string","message": "string"},"file": {"downloadUrl": "string","name": "string"},"log": [{"message": "string","recordedAt": "string","status": "REQUESTED"}],"period": {"endLt": "string","startGte": "string"},"reportId": "string","status": "REQUESTED","updatedAt": "string"}Get the status of a requested report Authorizations:ApiKeypath ParametersreportIdrequiredstring Report Id to check status
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/reports/transactions/{reportId}https://api.zendit.io/v1/reports/transactions/{reportId} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/json"\
"https://api.zendit.io/v1/reports/transactions/{reportId}"
 Response samples 200400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"createdAt": "string","error": {"code": "string","description": "string","message": "string"},"file": {"downloadUrl": "string","name": "string"},"log": [{"message": "string","recordedAt": "string","status": "REQUESTED"}],"period": {"endLt": "string","startGte": "string"},"reportId": "string","status": "REQUESTED","updatedAt": "string"}Download a Report Authorizations:ApiKeypath ParametersreportIdrequiredstring Report Id to check status
filerequiredstring File name to download
Responses200 OK
400 Bad Request
401 Unauthorized – API Token Missing or Unrecognized
403 Forbidden – IP Not Allowed
404 Not Found – Transaction not found
500 Internal Server Error
get/reports/transactions/{reportId}/{file}https://api.zendit.io/v1/reports/transactions/{reportId}/{file} Request samples CurlCopycurl -X GET\
-H "Authorization: Bearer [[accessToken]]"\
-H "Accept: application/octet-stream"\
"https://api.zendit.io/v1/reports/transactions/{reportId}/{file}"
 Response samples 400401403404500Content typeapplication/jsonCopy Expand all  Collapse all {"errorCode": "string","fields": {"property1": "string","property2": "string"},"message": "string"}
"""



dc = DatasetCleaner()

result = dc.clean(str(content))
print(result)
