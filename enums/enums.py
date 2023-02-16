from enum import Enum


class ProductScentEnum(Enum):
    """
    产品香型枚举
    """
    老白干香型 = 0
    浓香型 = 1
    清香型 = 2
    其他香型 = 99


class OrderNameEnum(Enum):
    """
    排序的产品列名枚举
    """
    product_name = 'product_name'
    specifications = 'specifications'
    specification_of_piece = 'specification_of_piece'
    unit_price = "unit_price"
    price_of_piece = "price_of_piece"
    suggested_retail_price = "suggested_retail_price"
    scanning_price = "scanning_price"
    create_time = "create_time"
