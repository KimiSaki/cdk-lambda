from aws_cdk import core
from aws_cdk import aws_lambda as _lambda


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
