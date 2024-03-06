import structlog
import sys

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from script.utils import generateLog, LogLevel, setSuccess, setError, setFailed

from app.transaksi import TransaksiApp
from model.transaksi import Tabung, Tarik, Transfer, GetSaldo, GetMutasi

router = APIRouter()
log = structlog.get_logger('uvicorn')
transaksiApp = TransaksiApp()

@router.post("/tabung", description="Tabung saldo nasabah")
async def Tabung(request: Tabung):
    response = setSuccess("", "Berhasil menambah saldo tabungan!")
    try:
        response = transaksiApp.tabung(request)

        if response.get('status', 500) == 200:
            generateLog(LogLevel.INFO, "Success Response", "", response)
        else:
            generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    except Exception as e:
        response = setError("(99) Gagal menambah saldo tabungan!")
    # --

    return response
# --


@router.post("/tarik", description="Tarik saldo nasabah")
async def Tarik(request: Tarik):
    response = setSuccess("", "Berhasil menarik saldo!")
    try:
        response = transaksiApp.tarik(request)

        if response['status'] == 200:
            generateLog(LogLevel.INFO, "Success Response", "", response)
        else:
            generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    except Exception as e:
        response = setError("(99) Gagal menarik saldo!")
    # --

    return response
# --


@router.post("/transfer", description="Transfer dana nasabah")
async def Transfer(request: Transfer):
    response = setSuccess("", "Berhasil transfer dana!")
    try:
        response = transaksiApp.transfer(request)

        if response['status'] == 200:
            generateLog(LogLevel.INFO, "Success Response", "", response)
        else:
            generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    except Exception as e:
        response = setError("(99) Gagal transfer dana!")
    # --

    return response
# --


@router.post("/saldo", description="Cek Saldo nasabah")
async def GetSaldo(request: GetSaldo):
    response = setSuccess("", "Berhasil mengambil data saldo tabungan")
    try:
        response = transaksiApp.saldo(request)

        if response['status'] == 200:
            generateLog(LogLevel.INFO, "Success Response", "", response)
        else:
            generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    except Exception as e:
        response = setError("(99) Gagal mengambil data saldo tabungan!")
    # --

    return response
# --


@router.post("/mutasi", description="Mutasi nasabah")
async def GetMutasi(request: GetMutasi):
    response = transaksiApp.mutasi(request)

    if response.get('status', 500) == 200:
        generateLog(LogLevel.INFO, "Success Response", "", response)
    else:
        generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)

    return response
# --
