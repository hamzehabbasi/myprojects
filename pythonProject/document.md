The list of valid market symbols are:
list_symbol=[
    "BTCIRT", "ETHIRT", "LTCIRT", "USDTIRT", "XRPIRT", "BCHIRT", "BNBIRT", "EOSIRT", "XLMIRT",
    "ETCIRT", "TRXIRT", "DOGEIRT", "UNIIRT", "DAIIRT", "LINKIRT", "DOTIRT", "AAVEIRT", "ADAIRT",
    "SHIBIRT", "FTMIRT", "MATICIRT", "AXSIRT", "MANAIRT", "SANDIRT", "AVAXIRT", "MKRIRT", "GMTIRT",
    "USDCIRT", "BTCUSDT", "ETHUSDT", "LTCUSDT", "XRPUSDT", "BCHUSDT", "BNBUSDT", "EOSUSDT", "XLMUSDT",
    "ETCUSDT", "TRXUSDT", "PMNUSDT", "DOGEUSDT", "UNIUSDT", "DAIUSDT", "LINKUSDT", "DOTUSDT", "AAVEUSDT",
    "ADAUSDT", "SHIBUSDT", "FTMUSDT", "MATICUSDT","AXSUSDT", "MANAUSDT", "SANDUSDT", "AVAXUSDT", "MKRUSDT",
    "GMTUSDT", "USDCUSDT"]

Types of currency:
currency=[
    "rls","btc", "eth", "ltc", "usdt", "xrp", "bch", "bnb", "eos", "xlm", "etc",
    "trx", "pmn", "doge", "uni", "dai", "link", "dot", "aave", "ada", "shib",
    "ftm", "matic", "axs", "mana", "sand", "avax", "mkr", "gmt", "usdc"]

notice:you should use a symbol from list_symbol in the body and front of the "symbol" 
or use a currency from list currency , in the body and front of the "symbol_dif" 
# nobitex_orderbook.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
    {"status": "ok", "lastUpdate": 1709005747995, "lastTradePrice": "56300", 
    "bids":
        [["56299.96", "0.007276"], 
        ["56299.97", "0.004382"], 
        ["56300", "0.017219"], 
        ["56327", "0.001206"], 
        ["56330", "0.03"], 
        ["56349.96", "0.0004"], 
        ["56350", "0.025998"], 
        ["56351", "0.019335"],  
        ["56549.99", "0.047382"], 
        ["56590", "0.030184"],
        ["56826", "0.002606"]], 
    "asks": 
         [["56250", "0.000711"], 
         ["56205.03", "0.059475"], 
         ["56205", "0.003736"], 
         ["56200.32", "0.000327"], 
         ["56200.26", "0.000242"], 
         ["56200.02", "0.000269"], 
         ["56066", "0.013035"], 
         ["56061.18", "0.000476"], 
         ["56061.13", "0.007279"], 
         ["56000", "0.040414"]]}
```
bids= order buy
asks=order sell

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_deep_chart.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{'status': 'ok',
 'lastUpdate': 1709018358022, 
 'lastTradePrice': '56150', 
 'bids':
      [['56140', '0.005762'],['56150', '0.005674'], 
      ['56200', '0.003518'],['56229', '0.000965'], 
       ['56299.97', '0.009873'], ['56299.98', '0.00044'], 
       ['56300', '0.002773'], ['56309.92', '0.00206'],
       ['56310', '0.000355'], ['56319.77', '0.000277'],
       ['56368', '0.000177'], ['56369.93', '0.007158'],
       ['56452.96', '0.004116']], 
 'asks':
        [['56100.02', '0.018464'], 
        ['56070.03', '0.019849'], ['56070', '0.000183'],
        ['56050', '0.002676'], ['56026', '0.001'],
        ['56015', '0.046934'], ['56013', '0.0015'], 
        ['56010.8', '0.023735'], ['56010', '0.000224'],
        ['56006.06', '0.004318'], ['56001', '0.017603'],
        ['55850', '0.001836']]}

```
bids= order buy
asks=order sell

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_deep_chart.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json


```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_trade_list.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{'status': 'ok', 'trades': 
    [{'time': 1709019489413, 'price': '55847.01', 'volume': '0.000875', 'type': 'sell'}, 
    {'time': 1709019470136, 'price': '55850', 'volume': '0.00059', 'type': 'sell'}, 
    {'time': 1709019470136, 'price': '55849.63', 'volume': '0.007045', 'type': 'buy'}, 
    {'time': 1709019463054, 'price': '55849.63', 'volume': '0.000625', 'type': 'buy'}, 
    {'time': 1709019463054, 'price': '55849.63', 'volume': '0.00017', 'type': 'sell'},
    {'time': 1709019460924, 'price': '55849.97', 'volume': '0.004033', 'type': 'buy'},
    {'time': 1709019449157, 'price': '55849.97', 'volume': '0.000431', 'type': 'buy'},
    {'time': 1709019440441, 'price': '55849.97', 'volume': '0.000971', 'type': 'sell'},
    {'time': 1709019418492, 'price': '55850', 'volume': '0.000029', 'type': 'sell'}, 
    {'time': 1709019411481, 'price': '55896.97', 'volume': '0.000161', 'type': 'buy'},
    {'time': 1709019308525, 'price': '55848', 'volume': '0.002561', 'type': 'sell'}]}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_nobitex_market_state.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
  "status": "ok",
  "stats": {
    "btc-rls": {
      "isClosed": false,
      "bestSell": "749976360",
      "bestBuy": "733059600",
      "volumeSrc": "0.2929480000",
      "volumeDst": "212724856.0678640000",
      "latest": "750350000",
      "mark": "747461987",
      "dayLow": "686021860",
      "dayHigh": "750350000",
      "dayOpen": "686021860",
      "dayClose": "750350000",
      "dayChange": "9.38"
    }
  }
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !

# ----------------------------------


# nobitex_ohlc_market_chart.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
  "s": "ok",
  "t": [1562095800, 1562182200],
  "o": [10850.0, 11247.23],
  "h": [11474.06, 11910.0],
  "l": [10655.11, 11247.23], 
  "c": [151440200, 157000000],
  "v": [11185.14, 11677.49]
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------

# nobitex_global_states.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
    "ltc": {
        "kraken": {
            "price": "41.69"
        }
    },
    "btc": {
        "kraken": {
            "price": "5517.2"
        }
    },
    ...

    "status": "ok"
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_customer_profile.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
  "status": "ok",
  "profile": {
    "firstName": "مهدی",
    "lastName": "رضایی",
    "nationalCode": "011122333",
    "email": "name@example.com",
    "username": "name@example.com",
    "phone": "02142719000-9012",
    "mobile": "09151111111",
    "city": "مشهد",
    "bankCards": [
      {
        "number": "6037-9900-0000-0000",
        "bank": "ملی",
        "owner": "مهدی رضایی",
        "confirmed": true,
        "status": "confirmed"
      }
    ],
    "bankAccounts": [
      {
        "id": 1999,
        "number": "0346666666666",
        "shaba": "IR460170000000346666666666",
        "bank": "ملی",
        "owner": "مهدی رضایی",
        "confirmed": true,
        "status": "confirmed"
      }
    ],
    "verifications": {
      "email": true,
      "phone": true,
      "mobile": true,
      "identity": true,
      "selfie": false,
      "bankAccount": true,
      "bankCard": true,
      "address": true,
      "city": true,
      "nationalSerialNumber": true
    },
    "pendingVerifications": {
      "email": false,
      "phone": false,
      "mobile": false,
      "identity": false,
      "selfie": false,
      "bankAccount": false,
      "bankCard": false
    },
    "options": {
      "fee": "0.35",
      "feeUsdt": "0.2",
      "isManualFee": false,
      "tfa": false,
      "socialLoginEnabled": false
    },
    "withdrawEligible": true
  },
  "tradeStats": {
    "monthTradesTotal": "10867181.5365000000",
    "monthTradesCount": 3
  }
}

```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_blockchain_address_create.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
    "status": "ok",
    "address": "LRf3vuTMy4UwD5b72G84hmkfGBQYJeTwUs"
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_bank_cards_add.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
    "status": "ok"
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_wallet_lists_selective.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
    "status": "ok",
    "wallets": {
        "RLS": {
            "id": 133777,
            "balance": "0E-10",
            "blocked": "0"
        },
        "BTC": {
            "id": 133778,
            "balance": "0E-10",
            "blocked": "0"
        }
    }
}
```
Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !

# ----------------------------------


# nobitex_wallet_list.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
  "status": "ok",
  "wallets": [
    {
      "depositAddress": null,
      "depositTag": null,
      "depositInfo": {
        "FIAT_MONEY": {
          "address": null,
          "tag": null
        }
      },
      "id": 2693280,
      "currency": "rls",
      "balance": "746212980",
      "blockedBalance": "0",
      "activeBalance": "746212980",
      "rialBalance": 746212980,
      "rialBalanceSell": 746212980
    },
    {
      "depositAddress": "bc1qp8dvtrhgjae6qhjfmvs2dj80ck0hgdjs6ts720",
      "depositTag": null,
      "depositInfo": {
        "BTC-LEGACY": {
          "address": null,
          "tag": null
        },
        "BTC": {
          "address": "bc1qp8dvtrhgjae6qhjfmvs2dj80ck0hgdjs6ts720",
          "tag": null
        },
        "BTCLN": {
          "address": null,
          "tag": null
        },
        "BSC": {
          "address": null,
          "tag": null
        }
      },
      "id": 133778,
      "currency": "btc",
      "balance": "0",
      "blockedBalance": "0",
      "activeBalance": "0",
      "rialBalance": 0,
      "rialBalanceSell": 0
    }
  ]
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !

# ----------------------------------


# nobitex_favorite_market.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
    "status": "ok",
    "favoriteMarkets": [
        "XLMIRT",
        "BTCUSDT",
        "BTCIRT"
    ]
}
```
Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !

# ----------------------------------


# nobitex_wallet_deposit_list.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
    "status": "ok",
    "deposits": [
        {
            "txHash": "c5d84268a0bf02307b5a0460a68b61987a9b3009d3a82a817e41558e619ec1d2",
            "address": "32KfyTNh162UoKithfDrWHZPYq5uePGmf7",
            "confirmed": true,
            "transaction": {
                "id": 10,
                "amount": "3.0000000000",
                "currency": "btc",
                "description": "Deposit - address:36n452uGq1x4mK7bfyZR8wgE47AnBb2pzi, tx:c5d84268a0bf02307b5a0460a68b61987a9b3009d3a82a817e41558e619ec1d2",
                "created_at": "2018-11-06T03:56:18+00:00",
                "calculatedFee": "0"
            },
            "currency": "Bitcoin",
            "blockchainUrl": "https://btc.com/c5d84268a0bf02307b5a0460a68b61987a9b3009d3a82a817e41558e619ec1d2",
            "confirmations": 2,
            "requiredConfirmations": 3,
            "amount": "3.0000000000"
        }
    ],
    "hasNext": true
}
```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !


# ----------------------------------


# nobitex_user_restrictions.

# Request  

``` json
body =
    {"token": "token 743fa839a9cc55cf2d65463b5ce535545559b9bf",
    "symbol":"BTCUSDT",
    "symbol_dif":"btc",
    "bank":"تجارت",
    "card_bank":"58483949292"}
```

# result
Our output is a content and a status. If the status of the code = 200 .!

``` json
{
  "status": "ok",
  "limitations": {
    "userLevel": "level2",
    "features": {
      "crypto_trade": false,
      "rial_trade": false,
      "coin_deposit": false,
      "rial_deposit": false,
      "coin_withdrawal": false,
      "rial_withdrawal": false
    },
    "limits": {
      "withdrawRialDaily": {
        "used": "0",
        "limit": "900000000"
      },
      "withdrawCoinDaily": {
        "used": "0",
        "limit": "2000000000"
      },
      "withdrawTotalDaily": {
        "used": "0",
        "limit": "2000000000"
      },
      "withdrawTotalMonthly": {
        "used": "0",
        "limit": "30000000000"
      }
    }
  }
}

```

Other status codes :400, 401, 403, 404 , 500  For more information, go to the Error section !

# ----------------------------------


Error section(common errors):

400:{tittle:Bad Request	,description:The parameters of the request are incorrect or insufficient, so that it is not possible to investigate further and give a better answer.}

401:{tittle:Unauthorized, description:The user is not authenticated}

403:{tittle:Forbidden, description:This operation is not allowed}

404:{tittle:Not Found , description:The address or object does not exist}

500:{tittle:Internal Server Error, description:A temporary problem has occurred on the Nobitex server }

