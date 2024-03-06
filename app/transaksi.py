from model.nasabah import Nasabah 
from model.transaksi import CreateTransaction, Transaction 
from datastore.nasabah import NasabahData
from datastore.transaksi import TransaksiData
from script.utils import generateLog, LogLevel, setSuccess, setError, setFailed, encrypt_string, get_random, RandomType, getCurrentTime

class TransaksiApp:
    def __init__(self):
        self.nasabah_data = NasabahData()
        self.transaksi_data = TransaksiData()

    def tabung(self, data):
        try:
            response = setSuccess("", "Berhasil menambahkan tabungan")
            
            if data.no_rekening in [None, "", 0]:
                response = setFailed('field no_rekening masih kosong!')
                return response
            
            if data.nominal in [None, "", 0]:
                response = setFailed('field nominal masih kosong!')
                return response

            count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening)
            if count_acc_no == 0:
                response = setFailed('(999) No Rekening tidak dikenali.')
                return response

            self.nasabah_data.save_money(data.no_rekening, data.nominal)

            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening)
            if saldo_nasabah == False and (saldo_nasabah != 0):
                response = setFailed('(999) Gagal mengambil data saldo.')
                return response

            response['result'] = {'saldo': saldo_nasabah}

            transactionObj = {}
            transactionObj['no_rekening'] = data.no_rekening
            transactionObj['kode_transaksi'] = 'C'
            transactionObj['nominal'] = data.nominal
            transactionObj['waktu'] = getCurrentTime()
            transaction = CreateTransaction(**transactionObj)
            self.transaksi_data.create_transaction(transaction)

            return response
        except Exception as e:
            return setError("(99) Gagal menambah tabungan!")
        # --

    def tarik(self, data):
        try:
            response = setSuccess("", "Berhasil tarik tabungan")
            
            if data.no_rekening in [None, "", 0]:
                response = setFailed('field no_rekening masih kosong!')
                return response
            
            if data.nominal in [None, "", 0]:
                response = setFailed('field nominal masih kosong!')
                return response

            count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening)
            if count_acc_no == 0:
                response = setFailed('(999) No Rekening tidak dikenali.')
                return response

            self.nasabah_data.withdraw(data.no_rekening, data.nominal)

            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening)
            if saldo_nasabah == False and (saldo_nasabah != 0):
                response = setFailed('(999) Gagal mengambil data saldo.')
                return response

            response['result'] = {'saldo': saldo_nasabah}

            transactionObj = {}
            transactionObj['no_rekening'] = data.no_rekening
            transactionObj['kode_transaksi'] = 'D'
            transactionObj['nominal'] = data.nominal
            transactionObj['waktu'] = getCurrentTime()
            transaction = CreateTransaction(**transactionObj)

            self.transaksi_data.create_transaction(transaction)

            return response
        except Exception as e:
            return setError("(99) Gagal tarik tabungan!")
        # --

    def transfer(self, data):
        try:
            response = setSuccess("", "Berhasil transfer dana")
            
            if data.no_rekening_asal in [None, "", 0]:
                response = setFailed('field no_rekening_asal masih kosong!')
                return response

            if data.no_rekening_tujuan in [None, "", 0]:
                response = setFailed('field no_rekening_tujuan masih kosong!')
                return response
            
            if data.nominal in [None, "", 0]:
                response = setFailed('field nominal masih kosong!')
                return response

            source_count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening_asal)
            if source_count_acc_no == 0:
                response = setFailed('(999) No Rekening Asal tidak dikenali.')
                return response

            target_count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening_tujuan)
            if target_count_acc_no == 0:
                response = setFailed('(999) No Rekening Tujuan tidak dikenali.')
                return response

            self.nasabah_data.withdraw(data.no_rekening_asal, data.nominal)
            self.nasabah_data.save_money(data.no_rekening_tujuan, data.nominal)

            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening_asal)
            if saldo_nasabah == False and (saldo_nasabah != 0):
                response = setFailed('(999) Gagal mengambil data saldo.')
                return response

            response['result'] = {'saldo': saldo_nasabah}

            transactionObj = {}
            transactionObj['no_rekening'] = data.no_rekening_asal
            transactionObj['kode_transaksi'] = 'D'
            transactionObj['nominal'] = data.nominal
            transactionObj['waktu'] = getCurrentTime()
            transaction_source = CreateTransaction(**transactionObj)
            self.transaksi_data.create_transaction(transaction_source)

            transactionObj = {}
            transactionObj['no_rekening'] = data.no_rekening_tujuan
            transactionObj['kode_transaksi'] = 'C'
            transactionObj['nominal'] = data.nominal
            transactionObj['waktu'] = getCurrentTime()
            transaction_target = CreateTransaction(**transactionObj)
            self.transaksi_data.create_transaction(transaction_target)

            return response
        except Exception as e:
            return setError("(99) Gagal tarik tabungan!")
        # --
    
    def saldo(self, data):
        try:
            response = setSuccess("", "Berhasil mendapatkan saldo tabungan")
            
            if data.no_rekening in [None, "", 0]:
                response = setFailed('field no_rekening masih kosong!')
                return response
     
            count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening)
            if count_acc_no == 0:
                response = setFailed('(999) No Rekening tidak dikenali.')
                return response

            saldo_nasabah = self.nasabah_data.get_saldo(data.no_rekening)

            if saldo_nasabah == False and (saldo_nasabah != 0):
                response = setFailed('(999) Gagal mengambil data saldo.')
                return response

            response['result'] = {'saldo': saldo_nasabah}

            return response
        except Exception as e:
            return setError("(99) Gagal mendapatkan saldo tabungan!")
        # --

    def mutasi(self, data):
        try:
            response = setSuccess("", "Berhasil mendapatkan mutasi")
            
            if data.no_rekening in [None, "", 0]:
                response = setFailed('field no_rekening masih kosong!')
                return response

            count_acc_no = self.nasabah_data.get_account_no_count(data.no_rekening)
            if count_acc_no == 0:
                response = setFailed('(999) No Rekening tidak dikenali.')
                return response

            data_mutasi = self.transaksi_data.get_transaction(data.no_rekening)
            response['result'] = data_mutasi

            return response

        except Exception as e:
            return setError("(99) Gagal mendapatkan mutasi!")
        # --
    # --