import json
import boto3

cf = boto3.client("cloudformation")

def lambda_handler(event, context):
    stack_name = event["StackName"]
    res = cf.describe_stack_events(
        StackName = stack_name
    )

    lpFlg = 1
    progressCnt = 0 # Count 'CREATE_IN_PROGRESS'
    failedCnt   = 0 # Count 'CREATE_FAILED'
    completeCnt = 0 # Count 'CREATE_COMPLETE'
    
    while lpFlg == 1:
        for stack in res["StackEvents"]:
            #print("StackName={0}, LogicalResourceId={1}, Status={2}".format(stack['StackName'], stack['LogicalResourceId'], stack['ResourceStatus']) )
            if stack['LogicalResourceId'] == stack_name:
                if stack['ResourceStatus'] == 'CREATE_IN_PROGRESS':
                    progressCnt += 1
                elif stack['ResourceStatus'] == 'CREATE_FAILED':
                    failedCnt += 1
                elif stack['ResourceStatus'] == 'CREATE_COMPLETE':
                    completeCnt += 1
        if 'NextToken' in res:
                res = cf.describe_stack_events(
                    StackName = stack_name,
                    NextToken = res['NextToken']
                )
        else:
            lpFlg = 0
    
    rtnStatus = ""
    if failedCnt != 0:
        rtnStatus = "Failed"
    elif progressCnt == completeCnt:
        rtnStatus = "Complete"
    else:
        rtnStatus = "InProgress"

    return {
        "statusCode": 200,
        "StackName" : stack_name,
        "Status"    : rtnStatus,
    }
