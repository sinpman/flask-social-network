from paypal import PayPalConfig
from paypal import PayPalInterface

config = PayPalConfig(API_USERNAME = "kapurkaran91_api1.gmail.com",
                      API_PASSWORD = "WUNHUNSYJ7R24G6C",
                      API_SIGNATURE = "ARJ3i6R11uqkA7Oilyp9Gg-y3foBAXzMhlvgGUVkmd2KXZQsVtuWvNAy",
                      DEBUG_LEVEL=0)

interface = PayPalInterface(config=config)
