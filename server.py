import boto3
from flask import Flask, request
import logging

#Resources details for different services
REGION = "us-east-1"
S3_BUCKET_NAME = "1229604729-in-bucket"
SDB_DOMAIN_NAME = "1229604729-simpleDB"
PORT = 8000

#Logging phrases for request tracing
LOG_REQUEST = "Request received for input"
ERROR_SBD = "Error fetching from SimpleDB"
ERROR_S3 = "Error Uploading to S3"
SUCCESS_SDB = "Fetched Successfully from SimpleDB for"
SUCCESS_S3 = "Uploaded Successfully to S3 for"

#Using s3 client from boto3
s3 = boto3.client("s3",region_name=REGION)

#Using SimpleDB client from boto3
sdb = boto3.client("sdb",region_name=REGION)

#Method for uploading to S3 bucket 
def upload_to_s3(file,filename_with_extension):
    try:
        #Uploading actual data as file with filename_with_extension as key
        s3.upload_fileobj(file,S3_BUCKET_NAME,filename_with_extension)
        logging.info(f"{SUCCESS_S3} {filename_with_extension}")
    except Exception as e:
        logging.error(f"{ERROR_S3} {str(e)}")

#method to fetch given from SimpleDB
def check_from_sdb(key):
    try:
        #Fetching actual key from database
        response = sdb.select(SelectExpression=f"SELECT Results FROM `{SDB_DOMAIN_NAME}` WHERE itemName() = '{key}'")
        logging.info(f"{SUCCESS_SDB} {key} {response}")
        #Parsing the response to check required attribute
        if "Items" in response and len(response["Items"]) > 0:
            item = response["Items"][0]
            logging.info(item)
            if "Attributes" in item:
                for attr in item["Attributes"]:
                    if attr["Name"] == "Results":
                        return attr["Value"]
        #Default response incase the value for given key is not present in database
        return "Unknown"
    except Exception as e:
        logging.error(f"{ERROR_SBD} {str(e)}")

#initiating flask
app = Flask(__name__)

#POST method take inputFile in body
@app.route("/",methods=["POST"])
def handle_resquest():
    #Checking if inputFile is present in request
    if "inputFile" not in request.files:
        return "Bad Request",200
    file = request.files["inputFile"]
    filename_with_extension = file.filename
    if not filename_with_extension:
        return "Bad Request",200
    file_name_only = filename_with_extension.split(".")[0]
    logging.info(f"{LOG_REQUEST} {file_name_only}")
    #calling upload_to_s3 with key as filename_with_extension and file as object
    upload_to_s3(file,filename_with_extension)
    #checking if file_name_only i.e. person name exists on check_from_sdb
    result = check_from_sdb(file_name_only)
    response = f"{file_name_only}:{result}"
    return response,200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=PORT,threaded=True)



