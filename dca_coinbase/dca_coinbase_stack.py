from monocdk import Stack, Construct, Duration
from monocdk.aws_lambda import Function, LayerVersion, Runtime, Code
from monocdk.aws_secretsmanager import Secret
from monocdk.aws_events import Rule, Schedule
from monocdk.aws_events_targets import LambdaFunction

import os
import subprocess


class DcaCoinbaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        creds = Secret(self, 'Secret', description="CoinBase Pro Credentials", secret_name="coinbaseProCredentials")

        entrypoint_name = 'lambda'

        function = Function(
            self,
            entrypoint_name,
            runtime=Runtime.PYTHON_3_8,
            code=Code.asset(f'{entrypoint_name}'),
            handler='handler.lambda_handler',
            function_name="dca_coinbase",
            layers=[self.create_dependencies_layer(self.stack_name, entrypoint_name)],
            environment={
                'creds_secret_id': creds.secret_name,
                'token': 'ETH',
                'amount': '50.00'
            }
        )

        lambda_schedule = Schedule.rate(Duration.days(1))

        Rule(
            self,
            "dailyBuyRule",
            description="The once per day CloudWatch event trigger for the Lambda",
            enabled=True,
            schedule=lambda_schedule,
            targets=[LambdaFunction(handler=function)]
        )

        creds.grant_read(function.role)

    def create_dependencies_layer(self, project_name, function_name: str) -> LayerVersion:
        requirements_file = f'lambda/requirements.txt'
        output_dir = f'.build/{function_name}'

        if not os.environ.get('SKIP_PIP'):
            subprocess.check_call(
                f'pip install -r {requirements_file} -t {output_dir}/python'.split()
            )

        layer_id = f'{project_name}-{function_name}-dependencies'
        layer_code = Code.from_asset(output_dir)

        return LayerVersion(self, layer_id, code=layer_code)
