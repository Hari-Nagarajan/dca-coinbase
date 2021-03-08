import boto3
import cbpro
import os
import logging

from credentials import Credentials
from coinbase import get_balances, deposit_funds

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    logger.info('## EVENT')
    logger.info(event)

    creds_secret_id = os.getenv('creds_secret_id')
    secrets_manager = boto3.client('secretsmanager')
    logger.info("Initializing credentials from AWS SecretsManager")
    creds = Credentials(creds_secret_id, secrets_manager)

    AMOUNT_TO_BUY = float(os.getenv("amount", "50.00"))
    PRODUCT = os.getenv("token", "ETH")

    if creds.sandbox:
        logger.info("Running in sandbox mode.")
    auth_client = cbpro.AuthenticatedClient(creds.key, creds.b64secret, creds.passphrase, api_url=creds.api_url)

    logger.info(f"Getting balances.")
    try:
        balances = get_balances(auth_client)
    except Exception as e:
        logger.error("Invalid API Key")
        raise e

    logger.info(f"We currently have {balances[PRODUCT]['available']} {PRODUCT} and {balances['USD']['available']} USD")
    logger.info(f"We want to buy {AMOUNT_TO_BUY} worth of {PRODUCT}")

    if balances['USD']['available'] < AMOUNT_TO_BUY:
        logger.info(f"We don't have enough available USD balance. ({AMOUNT_TO_BUY})")
        logger.info("Reloading balance for the next purchase.")
        deposit_funds(auth_client, AMOUNT_TO_BUY)
    else:
        logger.info(f"We have enough available USD balance.({AMOUNT_TO_BUY})")
        logger.info(f"Placing order for {PRODUCT}-USD in the amount of {AMOUNT_TO_BUY}")
        resp = auth_client.place_market_order(product_id=f'{PRODUCT}-USD',
                                              side='buy',
                                              funds=AMOUNT_TO_BUY)
        logger.info(resp)

        if balances['USD']['available'] < (AMOUNT_TO_BUY * 2):
            logger.info("Reloading balance for the next purchase.")
            deposit_funds(auth_client, AMOUNT_TO_BUY)


if __name__ == "__main__":
    lambda_handler({}, {})
