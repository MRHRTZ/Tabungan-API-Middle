from fastapi import APIRouter
from . import nasabah, transaksi

api_router = APIRouter()

prefix = '/api/v1'

api_router.include_router(nasabah.router, prefix=prefix, tags=["Nasabah"])
api_router.include_router(transaksi.router, prefix=prefix, tags=["Transaksi"])