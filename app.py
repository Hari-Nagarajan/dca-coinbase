#!/usr/bin/env python3

from aws_cdk import core

from dca_coinbase.dca_coinbase_stack import DcaCoinbaseStack


app = core.App()
DcaCoinbaseStack(app, "dca-coinbase")

app.synth()
