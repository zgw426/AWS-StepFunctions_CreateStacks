import boto3
import json

def lambda_handler(event, context):
    print(event)
    s3 = boto3.resource("s3")
    bucket = s3.Bucket( event["bucketName"] )
    jsonFile = bucket.Object(event["prefix"] + "/" + event["json"])
    print(jsonFile)
    jsonData = jsonFile.get()
    jsonByte = jsonData['Body'].read()
    jsonInfo = json.loads(jsonByte)

    for stack in jsonInfo["Stacks"]:
        stack["s3bucketName"] = event["s3ForCfn"]
        stack["s3prefix"]     = event["prefixForCfn"]

    print("jsonInfo = {0}".format(jsonInfo) )

    return jsonInfo
