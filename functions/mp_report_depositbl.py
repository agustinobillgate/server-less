#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def mp_report_depositbl():
    t_deposit_data = []

    t_deposit = None

    t_deposit_data, T_deposit = create_model("T_deposit", {"blockid":string, "startdate":date, "gname":string, "depositamount":Decimal, "limitdate":date, "paidamount":Decimal, "refundamount":Decimal, "remainbalance":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_deposit_data


        nonlocal t_deposit
        nonlocal t_deposit_data

        return {"t-deposit": t_deposit_data}

    for bk_deposit in query(bk_deposit_data):

        bk_master = db_session.query(Bk_master).filter(
                 (Bk_master.block_id == bk_deposit.blockId)).first()

        if bk_master:
            t_deposit = T_deposit()
            t_deposit_data.append(t_deposit)

            t_deposit.blockid = bk_master.block_id
            t_deposit.startdate = bk_master.startdate
            t_deposit.gname = bk_master.name
            t_deposit.depositamount =  to_decimal(bk_deposit.deposit)
            t_deposit.limitdate = bk_deposit.limitDate
            t_deposit.paidamount =  to_decimal(bk_deposit.totalPaid)
            t_deposit.refundamount =  to_decimal(bk_deposit.totalRefund)
            t_deposit.remainbalance =  to_decimal(bk_deposit.deposit) - to_decimal(bk_deposit.totalPaid) + to_decimal(bk_deposit.totalRefund)

    return generate_output()