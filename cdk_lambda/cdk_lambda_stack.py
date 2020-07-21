from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications,
    aws_events as _events,
    aws_events_targets as _targets
)


class CdkLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        lambdaFn = _lambda.Function(self, "SampleLambdaFunction", 
            code=_lambda.Code.from_asset('function/'),
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            function_name="sample_lambda_function"
        )

        # 環境変数を追加
        lambdaFn.add_environment(key="STAGE", value="DEV")

        # s3バケットを作成し、通知イベントを設定
        bucket = _s3.Bucket(self, "SampleBucket", bucket_name="kimi-first-cdk-bucket")
        notification = aws_s3_notifications.LambdaDestination(lambdaFn)
        bucket.add_event_notification(_s3.EventType.OBJECT_CREATED, notification, _s3.NotificationKeyFilter(prefix="hoge", suffix=".csv"))

        # 定期的に実行するイベントを設定
        rule = _events.Rule(self, "SampleEventRule", 
            rule_name="schedule_trigger_event",
            schedule=_events.Schedule.expression("cron(10 * * * ? *)")
        )
        rule.add_target(_targets.LambdaFunction(lambdaFn))

