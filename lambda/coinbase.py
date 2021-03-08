import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_balances(auth_client):
    accounts = auth_client.get_accounts()
    balances = {}
    for account in accounts:
        if account['currency'] in ['USD', "BTC", "ETH"]:
            balances[account['currency']] = {
                'available': float(account['available']),
                'balance': float(account['balance'])
            }
    return balances


def get_primary_payment_method(auth_client):
    logger.info("Getting payment methods.")
    methods = auth_client.get_payment_methods()
    for method in methods:
        if method['primary_buy']:
            payment_method_id = method['id']
            logger.info(f"The payment method we will be using is {method['name']}")
            return payment_method_id
    logger.info("No primary payment method found.")
    return None


def deposit_funds(auth_client, amount):
    logger.info(f"Depositing {amount}.")
    payment_method_id = get_primary_payment_method(auth_client)
    if payment_method_id:
        resp = auth_client.deposit(amount=amount, currency="USD", payment_method_id=payment_method_id)
        logger.info(resp)
