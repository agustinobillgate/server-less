#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel

def prepare_bk_depositbl(blockid:string):
    t_bk_deposit_data = []
    t_bk_deposit_line_data = []
    t_artikel_data = []
    artikel = None

    t_artikel = t_bk_deposit = t_bk_deposit_line = None

    t_artikel_data, T_artikel = create_model_like(Artikel)
    t_bk_deposit_data, T_bk_deposit = create_model("T_bk_deposit", {"blockid":string, "deposit":Decimal, "limitdate":date, "totalpaid":Decimal, "totalrefund":Decimal, "gastnr":int})
    t_bk_deposit_line_data, T_bk_deposit_line = create_model("T_bk_deposit_line", {"blockid":string, "nr":int, "paymentamount":Decimal, "paymentartnr":int, "paymentuserinit":string, "paymentdate":date, "paymenttype":int, "voucherno":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_deposit_data, t_bk_deposit_line_data, t_artikel_data, artikel
        nonlocal blockid


        nonlocal t_artikel, t_bk_deposit, t_bk_deposit_line
        nonlocal t_artikel_data, t_bk_deposit_data, t_bk_deposit_line_data

        return {"t-bk-deposit": t_bk_deposit_data, "t-bk-deposit-line": t_bk_deposit_line_data, "t-artikel": t_artikel_data}

    bk_deposit = db_session.query(Bk_deposit).filter(
             (Bk_deposit.blockid == blockid)).first()

    if bk_deposit:
        t_bk_deposit = T_bk_deposit()
        t_bk_deposit_data.append(t_bk_deposit)

        buffer_copy(bk_deposit, t_bk_deposit)

    for bk_deposit_line in query(bk_deposit_line_data, filters=(lambda bk_deposit_line: bk_deposit_line.blockid == blockid)):
        t_bk_deposit_line = T_bk_deposit_line()
        t_bk_deposit_line_data.append(t_bk_deposit_line)

        buffer_copy(bk_deposit_line, t_bk_deposit_line)

    for artikel in db_session.query(Artikel).filter(
             ((Artikel.artart == 6) | (Artikel.artart == 7))).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    return generate_output()