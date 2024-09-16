# from Business.operations.buy import load_buying_experiences_v1
# from Business.operations.categories import load_categories_v1
from Business.operations.buy.load_buying_experiences_v1abcd12 import load_buying_experiences_v1abcd12
from Business.operations.categories.load_categories_v1abcd12 import load_categories_v1abcd12
from Business.operations.labels.load_labels_abcd1234 import load_labels_abcd1234
from Business.operations.management.load_businesses_abcd1234 import load_businesses_abcd1234
from Business.operations.management.load_businesses_cdba4321 import load_businesses_cdba4321
from Business.operations.offs.load_offs_v1abcd12 import load_offs_v2abcd12
from Business.operations.offs.load_offs_v2abcd12 import load_offs_v1abcd12
# from Business.operations.orders import load_orders_v1
from Business.operations.orders.load_orders_v1abcd12 import load_orders_v1abcd12
from Business.operations.products.load_products_v1abc432 import load_products_v1abc432
from Business.operations.products.load_products_v2abcd12 import load_products_v2abcd12
from Business.operations.services.load_subscription_services_v1abcd12 import load_subscription_services_v1abcd12
from Business.operations.services.load_subscription_services_v2abcd12 import load_subscription_services_v2abcd12
from Business.operations.subscribes.load_subscriptions_v1abcd12 import load_subscriptions_v1abcd12
from Business.operations.taxi.load_taxis_v1abcd12 import load_taxis_v1abcd12

app_data_private_methods = {
    "buying_experiences_v1": load_buying_experiences_v1abcd12,  # buy

    "load_products_v2abcd12": load_products_v2abcd12,  # products

    "load_products_v1abc432": load_products_v1abc432,  # products

    "load_orders_v1abcd12": load_orders_v1abcd12,  # orders

    "load_labels_abcd1234": load_labels_abcd1234,  # labels

    "load_categories_v1abcd12": load_categories_v1abcd12,  # categories

    "load_subscriptions_v1abcd12": load_subscriptions_v1abcd12,  # subscribes

    "load_offs_v1abcd12": load_offs_v1abcd12,  # offs
    "load_offs_v2abcd12": load_offs_v2abcd12,  # offs

    "load_taxis_v1abcd12": load_taxis_v1abcd12,  # taxi
}

app_data_public_methods = {
    "businesses_v2": load_businesses_cdba4321,  # management and vitrine

    "businesses_v1": load_businesses_abcd1234,  # management and vitrine

    "load_categories_v1abcd12": load_categories_v1abcd12,  # management and vitrine

    "load_subscription_services_v2abcd12": load_subscription_services_v2abcd12,  # services

    "load_subscription_services_v1abcd12": load_subscription_services_v1abcd12,  # services

}

app_data_version_control = {
    "buying_experiences": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "products": [
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
    "orders": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "labels": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "subscriptions": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        }
    ],
    "offs": [
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
    "taxis": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],
    "businesses": [
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
    "subscription_services": [
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
    "categories": [
        {
            "devices": ["android", "ios", "windows", "macos", "web", "PWA"],
            "min_version": 98,
            "max_version": 300,
            "method_version": 1
        },
    ],

}
