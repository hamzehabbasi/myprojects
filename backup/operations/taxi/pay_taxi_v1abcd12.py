from AppBase.usage import usage
from Business.models import Taxi, iTTaxi
from Platform.models import Cache, iTransaction
from toolkit import load_request_payment_flags


@usage
def pay_taxi_v1abcd12(req, d, device):
    by_virdaar, by_card = load_request_payment_flags(d)
    customer = device.user
    try:
        key = d["key"]
        amount = float(d["amount"])
        taxi = Taxi.k(key)

    except:
        return 400

    if by_card == 1 and amount:
        payment_token, payment_url = Cache.pay_by_card(amount, d, device)
        return 402, {"link": payment_url, "payment_token": payment_token}

    transaction = iTransaction(
        amount=amount,
        src=customer,
        dst_id=1,
        trans_type="taxi"
    )
    transaction.save()

    ittaxi = iTTaxi(
        taxi=taxi,
        transaction=transaction,
    )
    ittaxi.save()
    customer.update_balance()

    return 200
