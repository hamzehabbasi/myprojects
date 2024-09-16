from AppBase.usage import usage
from Business.operations.buy.buy_new_customer_v1abcd12 import buy_new_customer_v1abcd12
from Business.operations.buy.buy_virdar_customer_v1abcd12 import buy_virdar_customer_v1abcd12


@usage
def buy_v2abcd12(_, d, device):
    try:
        if device.user:
            return buy_virdar_customer_v1abcd12(_, d, device)
    except AttributeError:
        return buy_new_customer_v1abcd12(_, d, device)
