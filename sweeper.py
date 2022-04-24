# This project generates random BTC private keys, then converts them into wallet addresses
# These wallet addresses are then checked with a server to verify that they exist
# after we verify the address, it checks the balance, and appends any address with more than 0 BTC to address.txt

import blocksmith
import requests

## generate addresses https://github.com/Destiner/blocksmith

number_of_address = int(input("Enter number of addresses: "))

for i in range(number_of_address):
    kg = blocksmith.KeyGenerator()
    kg.seed_input('Truly random string. I rolled a dice and got 4.')
    # variable key is the private key
    key = kg.generate_key()
    # variable address is the wallet address
    address = blocksmith.BitcoinWallet.generate_address(key)


    ## checks whether address is valid
    address = {"network": "BTC", "address": address}
    r = requests.get("https://chain.so/api/v2/is_address_valid/BTC/",params=address)

    r_dict = r.json()
    r_dict_2 = r_dict['data']

    wallet_address = r_dict_2['address']
    btc_verify = bool(r_dict_2['is_valid'])

    # checks balance of address

    url = 'https://blockchain.info/balance?active='+wallet_address
    r2 = requests.get(url)
    r2_dict = r2.json()
    r2_dict_2 = r2_dict[wallet_address]

    btc_balance = int(r2_dict_2['final_balance'])
    

    ## prints if the address is valid
    
    if btc_verify == True:
        print(wallet_address,'is valid with',btc_balance,'BTC')
    else:
        print(wallet_address,'is not valid')

    ## saves only addresses with balance to file

    if btc_balance > 0:
        with open('address.txt','a') as f:
            f.writelines('Address:',wallet_address,'Private key:',key,'Balance:',btc_balance)
        
