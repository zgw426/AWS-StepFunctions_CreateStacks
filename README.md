# AWS-StepFunctions_CreateStacks

## 概要

- AWS StepFunctionsとLambdaでCloudFormationスタックを複数実行する
- 実行したスタックが完了するまで次のスタックは実行しない

## 準備
StepFunctions実行前の準備

- S3バケットを作成し以下の構成でデータを格納する
    - test/sample.json
    - cfn/vpc.yml
    - cfn/subnet-public.yml
    - cfn/sg.yml
- Lambdaを作成する
    - stp1_loadJSONfromS3
    - stp2_createStack
    - stp3_checkStack
- Stepfunctionsを作成する
    - ※参照※ stepfunctions.json

## StepFunctions実行時のペイロード

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
    "prefix": "test",
    "json": "sample.json",
    "s3ForCfn": "tmp-i6xldhl0mm",
    "prefixForCfn": "cfn"
}
```

## Stepfunctionsの処理概要

Stepfumctionsの各フローの処理概要

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

