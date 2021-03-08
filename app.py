#!/usr/bin/env python3

from monocdk import App

from dca_coinbase.dca_coinbase_stack import DcaCoinbaseStack


app = App()
DcaCoinbaseStack(app, "dca-coinbase")

app.synth()
