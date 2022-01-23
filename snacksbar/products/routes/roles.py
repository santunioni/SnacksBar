from fastapi import Security

from snacksbar.security import check_credentials

modify_products = Security(
    check_credentials, scopes=["products:modify"], use_cache=False
)
read_products = Security(check_credentials, scopes=["products:read"], use_cache=False)
