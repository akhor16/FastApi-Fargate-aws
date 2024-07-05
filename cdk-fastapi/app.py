#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_fastapi.cdk_fastapi_stack import CdkFastapiStack


app = cdk.App()


# Ensure you set your AWS Account and Region
env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT', '305572817819'), region=os.getenv('CDK_DEFAULT_REGION', 'eu-central-1'))

CdkFastapiStack(app, "CdkFastapiStack", env=env)

app.synth()
