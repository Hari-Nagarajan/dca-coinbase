
# Cost Averaging on Coinbase Pro

This is currently configured to buy $50 worth of ETH every day. 

DCA is a long-term strategy, where an investor regularly buys smaller amounts of an asset over a period of time, no matter the price (for example, investing $100 in Bitcoin every month for a year, instead of $1,200 at once). Their DCA schedule may change over time and — depending on their goals — it can last just a few months or many years. 
See: https://www.coinbase.com/learn/tips-and-tutorials/dollar-cost-averaging


# How to Deploy
1. Make sure you have AWS Credentials
2. ```cdk deploy```
3. Navigate to the AWS Console (AWS Secrets Manager)
4. Locate ```coinbaseProCredentials```
5. Add a secret value: 
```
{
  "key": "key",
  "passphrase": "passphrase",
  "b64secret": "b64secret==",
  "sandbox": "False"
}
```

Set sandbox to "True" to use sandbox credentials. 

## TODO Add directions on how to get pro.coinbase API credentials
## TODO Add the ability to easily set the amount and crypto token to purchase

# Workflow
1. Check balances
2. If balance is insufficient for the next order. Deposit Funds. This step is not instantaneous so the balance needs to be sufficient before this workflow is ran. 
3. Place Order
4. Deposit funds for the next order.
######TODO Need to implement a wait between step 2 and 3, which would allow us to eliminate step 4. 
