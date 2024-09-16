# buy
from Business.operations.buy.apply_buying_experience_v1abcd12 import apply_buying_experience_v1abcd12
from Business.operations.buy.apply_buying_experience_v2abcd12 import apply_buying_experience_v2abcd12
from Business.operations.buy.buy_new_customer_v1abcd12 import buy_new_customer_v1abcd12
from Business.operations.buy.buy_v1abcd12 import buy_v1abcd12
from Business.operations.buy.buy_v2abcd12 import buy_v2abcd12
from Business.operations.buy.buy_virdar_customer_v1abcd12 import buy_virdar_customer_v1abcd12

# categories
from Business.operations.categories import edit_category_v1abcd12
from Business.operations.categories.add_category_v1abcd12 import add_category_v1abcd12
from Business.operations.categories.add_to_category_v1abcd12 import add_to_category_v1abcd12
from Business.operations.categories.change_order_v1abcd12 import change_order_v1abcd12
from Business.operations.categories.delete_category_v1abcd12 import delete_category_v1abcd12
from Business.operations.categories.delete_from_category_v1abcd12 import delete_from_category_v1abcd12

# customer
from Business.operations.customer_group.add_customer_to_group_v1abcd12 import add_customer_to_group_v1abcd12
from Business.operations.customer_group.add_group_v1abcd12 import add_group_v1abcd12
from Business.operations.customer_group.delete_customer_from_group_v1abcd12 import delete_customer_from_group_v1abcd12
from Business.operations.customer_group.delete_group_v1 import delete_group_v1abcd12
from Business.operations.customer_group.edit_group_v1abcd12 import edit_group_v1abcd12

# labels
from Business.operations.labels.add_label_abcd1234 import add_label_abcd1234
from Business.operations.labels.delete_label_abcd1234 import delete_label_abcd1234
from Business.operations.labels.edit_label_abcd1234 import edit_label_abcd1234

# management
from Business.operations.management import active_business_abci1234
from Business.operations.management.add_business_abcd1234 import add_business_abcd1234
from Business.operations.management.delete_business_abcd1234 import delete_business_abcd1234
from Business.operations.management.edit_business_abcd1234 import edit_business_abcd1234
from Business.operations.management.start_business_abcd1234 import start_business_abcd1234
from Business.operations.management.start_public_business_abcd1234 import start_public_business_abcd1234
from Business.operations.management.update_cover_abcd1234 import update_cover_abcd1234
from Business.operations.management.update_turn_abcd1234 import update_turn_abcd1234

# offs
from Business.operations.offs.add_off_v1abcd12 import add_off_v1abcd12
from Business.operations.offs.add_off_v2abcd12 import add_off_v2abcd12
from Business.operations.offs.buy_affect_offs_abcd1234 import buy_affect_offs_abcd1234
from Business.operations.offs.calculate_order_off_data_abcd123 import calculate_order_off_data_abcd1234
from Business.operations.offs.delete_off_v1abcd12 import delete_off_v1abcd12
from Business.operations.offs.edit_off_v1abcd12 import edit_off_v1abcd12
from Business.operations.offs.edit_off_v2abcd12 import edit_off_v2abcd12

# products
from Business.operations.products.add_product_abcd1234 import add_product_abcd1234
from Business.operations.products.add_product_dcba4321 import add_product_dcba4321
from Business.operations.products.available_product_abcd1234 import available_product_abcd1234
from Business.operations.products.delete_product_abcd1234 import delete_product_abcd1234
from Business.operations.products.edit_product_abcd1234 import edit_product_abcd1234
from Business.operations.products.edit_product_dcba4321 import edit_product_dcba4321

# services
from Business.operations.services import edit_service_v2abcd12
from Business.operations.services.add_service_v1acdb12 import add_service_v1acdb12
from Business.operations.services.add_service_v2abcd12 import add_service_v2abcd12
from Business.operations.services.available_service_v1abcd12 import available_service_v1abcd12
from Business.operations.services.delete_service_v1abcd12 import delete_service_v1abcd12
from Business.operations.services.edit_service_v1abcd12 import edit_service_v1abcd12

# subscibes
from Business.operations.subscribes.activate_subscription_v1abcd12 import activate_subscription_v1abcd12
from Business.operations.subscribes.add_subscription_v1abcd12 import add_subscription_v1abcd12
from Business.operations.subscribes.cancel_subscription_v1abcd12 import cancel_subscription_v1abcd12
from Business.operations.subscribes.checkout_subscription_form_v1abcd12 import checkout_subscription_form_v1abcd12
from Business.operations.subscribes.delete_subscription_v1abcd12 import delete_subscription_v1abcd12
from Business.operations.subscribes.renew_subscription_v1abcd12 import renew_subscription_v1abcd12

# taxi
from Business.operations.taxi.add_taxi_v1abcd12 import add_taxi_v1abcd12
from Business.operations.taxi.pay_taxi_v1abcd12 import pay_taxi_v1abcd12

apply_cmd_private_methods = {

    # management
    "start_business_abcd1234": start_business_abcd1234,  # management
    "active_business_abci1234": active_business_abci1234,  # management
    "edit_business_abcd1234": edit_business_abcd1234,  # management
    "delete_business_abcd1234": delete_business_abcd1234,  # management
    "update_cover_abcd1234": update_cover_abcd1234,  # management
    "update_turn_abcd1234": update_turn_abcd1234,  # management
    "add_business_abcd1234": add_business_abcd1234,  # management
    "start_public_business_abcd1234": start_public_business_abcd1234,  # management

    # products
    "edit_product_dcba4321": edit_product_dcba4321,  # products
    "edit_product_abcd1234": edit_product_abcd1234,  # products
    "add_product_dcba4321": add_product_dcba4321,  # products
    "add_product_abcd1234": add_product_abcd1234,  # products
    "delete_product_abcd1234": delete_product_abcd1234,  # products
    "available_product_abcd1234": available_product_abcd1234,  # products

    # services
    "add_service_v2abcd12": add_service_v2abcd12,  # services
    "add_service_v1acdb12": add_service_v1acdb12,  # services
    "edit_service_v2abcd12": edit_service_v2abcd12,  # services
    "edit_service_v1abcd12": edit_service_v1abcd12,  # services
    "delete_service_v1abcd12": delete_service_v1abcd12,  # services
    "available_service_v1abcd12": available_service_v1abcd12,  # services

    # labels
    "add_label_abcd1234": add_label_abcd1234,  # labels
    "edit_label_abcd1234": edit_label_abcd1234,  # labels
    "delete_label_abcd1234": delete_label_abcd1234,  # labels

    # offs
    "add_off_v2abcd12": add_off_v2abcd12,  # offs
    "add_off_v1abcd12": add_off_v1abcd12,  # offs
    "edit_off_v2abcd12": edit_off_v2abcd12,  # offs
    "edit_off_v1abcd12": edit_off_v1abcd12,  # offs
    "delete_off_v1abcd12": delete_off_v1abcd12,  # offs
    "buy_affect_offs_abcd1234": buy_affect_offs_abcd1234,  # offs
    "calculate_order_off_data_abcd1234": calculate_order_off_data_abcd1234,  # offs

    # subscribes
    "delete_subscription_v1abcd12": delete_subscription_v1abcd12,  # subscribes
    "renew_subscription_v1abcd12": renew_subscription_v1abcd12,  # subscribes
    "cancel_subscription_v1abcd12": cancel_subscription_v1abcd12,  # subscribes
    "activate_subscription_v1abcd12": activate_subscription_v1abcd12,  # subscribes

    # categories
    "add_category_v1abcd12": add_category_v1abcd12,  # categories
    "edit_category_v1abcd12": edit_category_v1abcd12,  # categories
    "delete_category_v1abcd12": delete_category_v1abcd12,  # categories
    "add_to_category_v1abcd12": add_to_category_v1abcd12,  # categories
    "delete_from_category_v1abcd12": delete_from_category_v1abcd12,  # categories
    "change_order_v1abcd12": change_order_v1abcd12,  # categories

    # customer_group
    "add_customer_to_group_v1abcd12": add_customer_to_group_v1abcd12,
    "add_group_v1abcd12": add_group_v1abcd12,
    "delete_customer_from_group_v1abcd12": delete_customer_from_group_v1abcd12,
    "delete_group_v1abcd12": delete_group_v1abcd12,
    "edit_group_v1abcd12": edit_group_v1abcd12,
    # orders

    # vitrine
}

apply_cmd_public_methods = {

    # buy
    "apply_buying_experience_v1abcd12": apply_buying_experience_v1abcd12,  # buy
    "buy_v2abcd12": buy_v2abcd12,  # buy
    "buy_v1abcd12": buy_v1abcd12,  # buy
    "apply_buying_experience_v2abcd12": apply_buying_experience_v2abcd12,  # buy
    "buy_new_customer_v1abcd12": buy_new_customer_v1abcd12,  # buy
    "buy_virdar_customer_v1abcd12": buy_virdar_customer_v1abcd12,  # buy

    # management
    "add_business_abcd1234": add_business_abcd1234,  # management
    "start_public_business_abcd1234": start_public_business_abcd1234,  # management

    # subscribes
    "add_subscription_v1abcd12": add_subscription_v1abcd12,  # subscribes
    "checkout_subscription_form_v1abcd12": checkout_subscription_form_v1abcd12,  # subscribes

    # subscribes
    "pay_taxi_v1abcd12": pay_taxi_v1abcd12,  # taxi
    "add_taxi_v1abcd12": add_taxi_v1abcd12,  # taxi
}

apply_cmd_version_control = {
    "active_business": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "start_business": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": ""
        },
    ],
    "start_public_business": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "edit_business": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "delete_business": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "update_cover": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "update_turn": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "edit_product": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        },
    ],
    "add_product": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        },
    ],
    "delete_product": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "available_product": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "add_category": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "edit_category": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "delete_category": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "add_service": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        },
    ],
    "edit_service": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        },
    ],
    "available_service": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "delete_service": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "add_label": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "edit_label": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "delete_label": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "add_off": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        },
    ],
    "edit_off": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        },
    ],
    "delete_off": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "renew_subscription": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "cancel_subscription": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "activate_subscription": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "buying_experience": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        }
    ],
    "buy": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 103,
            "method_version": 1
        },
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 104,
            "max_version": 300,
            "method_version": 2
        }
    ],

    "add_business": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "delete_subscription": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "add_subscription": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "checkout_subscription_form": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

    "pay_taxi": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "add_taxi": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ]
}
