import json
import boto3

cf = boto3.client("cloudformation")

def lambda_handler(event, context):
    stack_name   = event["StackName"]
    bucketName   = event["s3bucketName"]
    prefix       = event["s3prefix"]
    template_url = "https://"+ bucketName +".s3-ap-northeast-1.amazonaws.com/" + prefix + "/" + event["Code"]
    params = {}
    paramVal = []
    
    for param in event:
        #print("param = {0}".format(param) )
        if param == "Code":
            print("Code = {0}".format(event[param]))
        elif param == "StackName":
            print("StackName = {0}".format(event[param]))
        elif param == "s3bucketName":
            print("s3bucketName = {0}".format(event[param]))
        elif param == "s3prefix":
            print("s3prefix = {0}".format(event[param]))
        else:
            paramVal.append({"ParameterKey": param ,"ParameterValue": event[param]})

    params = {
        'StackName': stack_name,
        'TemplateURL': template_url,
        'Parameters': paramVal,
    }
    
    print("params = {0}".format(params) )
    res = cf.create_stack( **params )

    return {
        "statusCode": 200,
        "StackName": stack_name
    }
