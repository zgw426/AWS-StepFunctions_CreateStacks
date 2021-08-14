## 各Lambdaの動作確認

テストイベントの設定例

## Lambda "stp1_loadJSONfromS3" のテストイベント

＜規則＞

'''
{
  "bucketName": "{{JSONファイルのS3バケット名}}",
  "prefix": "{{JSONファイルのプレフィックス}}",
  "json": "{{JSONファイル名}}",
  "s3ForCfn": "{{CloudFormationテンプレートのS3バケット名}}",
  "prefixForCfn": "{{CloudFormationテンプレートのプレフィックス}}"
}
'''

＜設定例＞

'''
{
  "bucketName": "tmp-i6xldhl0mm",
  "prefix": "test",
  "json": "sample_vpc.json",
  "s3ForCfn": "tmp-i6xldhl0mm",
  "prefixForCfn": "cfn"
}
'''

- (S3バケット) tmp-i6xldhl0mm
    - (プレフィックス) test
        - (JSONファイル) sample_vpc.json
    - (プレフィックス) cfn
        - (CFnテンプレート) xxx.yml

## Lambda "stp2_createStack" のテストイベント

＜規則＞

'''
{
  "StackName": "{{スタック名}}",
  "Code": "{{CloudFormationテンプレートファイル名}}",
  "{{スタック実行時に指定するパラメータ１}}": "{{パラメータの値}}",
  "{{スタック実行時に指定するパラメータ２}}": "{{パラメータの値}}",
  "{{スタック実行時に指定するパラメータ３}}": "{{パラメータの値}}",
        ：
  "{{スタック実行時に指定するパラメータｎ}}": "{{パラメータの値}}"
}
'''

＜設定例＞

'''
{
  "StackName": "test001-vpc",
  "Code": "vpc.yml",
  "PJPrefix": "Project1",
  "VPCCIDR": "10.11.0.0/16",
  "s3bucketName": "tmp-2-i6xldhl0mm",
  "s3prefix": "cfn"
}
'''

## Lambda "stp3_checkStack" のテストイベント

＜規則＞

'''
{
  "StackName": "{{スタック名}}"
}
'''

＜設定例＞

'''
{
  "StackName": "test001-vpc"
}
'''


