# AWS-StepFunctions_CreateStacks

## 概要

- AWS StepFunctionsとLambdaでCloudFormationスタックを複数実行する
- 実行したスタックが完了するまで次のスタックは実行しない

## 準備

### StepFunctions実行前の準備

- S3バケットを作成し以下の構成でデータを格納する
    - s3://{S3バケット名}/pipe/sample.json
    - s3://{S3バケット名}/pipe/sample_vpc.json
    - s3://{S3バケット名}/cfn/vpc.yml
    - s3://{S3バケット名}/cfn/subnet-public.yml
    - s3://{S3バケット名}/cfn/sg.yml
- Lambdaを作成する
    - stp1_loadJSONfromS3
    - stp2_createStack
    - stp3_checkStack
- Stepfunctionsを作成する
    - ※参照※ stepfunctions.json


### IAMロールの準備

- Lambda用のIAMロール
    - AmazonS3FullAccess
    - AWSCloudFormationFullAccess
    - AmazonVPCFullAccess
    - CloudWatchLogs-policy

```json:CloudWatchLogs-policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

- StepFuncitions用のIAMロール
    - LambdaInvokeScopedAccessPolicy
    - CloudWatchLogsDeliveryFullAccessPolicy

```json:LambdaInvokeScopedAccessPolicy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:ap-northeast-1:000000000000:function:*:*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:ap-northeast-1:000000000000:function:*"
            ]
        }
    ]
}
```

```json:CloudWatchLogsDeliveryFullAccessPolicy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogDelivery",
                "logs:GetLogDelivery",
                "logs:UpdateLogDelivery",
                "logs:DeleteLogDelivery",
                "logs:ListLogDeliveries",
                "logs:PutResourcePolicy",
                "logs:DescribeResourcePolicies",
                "logs:DescribeLogGroups"
            ],
            "Resource": "*"
        }
    ]
}
```


## AWSリソースの作成

### S3の作成

- `準備`で作成済

### IAMロールの作成

- `準備`で作成済

### Lambdaの作成

以下3つのLambdaを作成する

- stp1_loadJSONfromS3.py
- stp2_createStack.py
- stp3_checkStack.py

### StepFunctionsの作成

- stepfunctions/stepfunctions.json と同じフローを作成する

---

## 実行する

### StepFunctions実行時のペイロード

- ペイロード

```
{
    "bucketName": "{{JSONファイルを格納したS3バケット名}}",
    "prefix": "{{JSONファイルを格納したプレフィックス（ディレクトリ）}}",
    "json": "{{JSONファイル名}}",
    "s3ForCfn": "{{CloudFormationテンプレートのS3バケット名}}",
    "prefixForCfn": "{{CloudFormationテンプレートのプレフィックス（ディレクトリ）}}"
}
```

- ペイロード(例)
    - S3バケット`tmp-i6xldhl0mm`にjson,CFnテンプレートを格納した場合

```
{
    "bucketName": "tmp-i6xldhl0mm",
    "prefix": "pipe",
    "json": "sample.json",
    "s3ForCfn": "tmp-i6xldhl0mm",
    "prefixForCfn": "cfn"
}
```

## Stepfunctionsの処理概要

- Stepfunctionsの各フローの処理概要
- フロー図はQiita参照 ( https://qiita.com/suo-takefumi/items/1b3ba01ba22b47471fc7 )

- stp1_loadJSONfromS3
    - S3バケットにあるJSONファイルをロードする
    - ロードしたJSONデータのStack配下の要素に、CloudFormationテンプレートファイルが格納されたS3バケット、プレフィックス情報を設定する
    - 加工したJSONデータを次の処理に渡す
- Pass(Debug)
    - デバッグ
    - 処理は何もしない
- Pass(Filter)
    - 入力として受け取ったJSONデータの`$.Payload`配下の情報を次の処理に渡す
- Map
    - 入力として受け取ったJSONデータの`$.Stacks`配下の配列でループする
    - `$.Stacks`の n 番目のデータを次の処理に渡す
- Pass(debug)
    - デバッグ
    - 処理は何もしない
- Choice(SelectExecType)
    - 入力値の $.ExcecType により次の処理を決める
    - $.ExcecType == "cfn" の場合は、CloudFormationスタックを実行する
- stp2_createStack
    - 入力として受け取ったJSONデータでCloudFormationスタックを実行する
- wait
    - 5秒間まち
- stp3_checkStack
    - 実行したスタックの状態を確認
    - 確認結果を次の処理に渡す
    - 確認結果は、`InProgress`,`Complete`,`Failed` の3通り
- Choice
    - 入力として受け取ったJSONデータ(`InProgress`,`Complete`,`Failed`)を元に次に進む処理を決定する
        - `InProgress`： `wait`フローに進む
        - `Complete`： `stp2_createStack`フローに進む
        - `Failed`： `Fail`フローに進む
