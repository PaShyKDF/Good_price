from good_price.analitic.parser_dns_shop import (
    get_dns_products_name_price_link, get_dns_processory_info
)
from good_price.analitic.parser_regard import (
    get_regard_products_name_price_link, get_regard_processory_info
)


CHARACTERISTICS_FROM_REGARD = [
    'lineup', 'tech_process', 'clock_frequency', 'turboboost_frequency',
    'cores_amount', 'productive_cores_amount', 'energy_efficient_cores_amount',
    'threads_amount', 'tdp', 'second_level_cache', 'third_level_cache',
    'free_multiplier', 'graphics_core'
]

CHARACTERISTICS_FROM_DNS = [
    'tech_process', 'clock_frequency', 'turboboost_frequency',
    'cores_amount', 'productive_cores_amount', 'energy_efficient_cores_amount',
    'threads_amount', 'tdp', 'second_level_cache', 'third_level_cache',
    'free_multiplier', 'RAM_support', 'graphics_core'
]

STORES_PRICE_NOT_DEPEND_ON_REGION = ['www.regard.ru']

# PROCESSORY_FUNCTIONS = [
#     (get_dns_products_name_price_link, get_dns_processory_info),
#     (get_regard_products_name_price_link, get_regard_processory_info)
# ]

FUNCTIONS_DEPEND_ON_REGION = [
    (CHARACTERISTICS_FROM_DNS, get_dns_products_name_price_link,
     get_dns_processory_info)
]

FUNCTIONS_NOT_DEPEND_ON_REGION = [
    (CHARACTERISTICS_FROM_REGARD, get_regard_products_name_price_link,
     get_regard_processory_info)
]
