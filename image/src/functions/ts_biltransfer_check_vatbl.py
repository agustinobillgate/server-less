from functions.additional_functions import *
import decimal
from models import H_bill, H_bill_line, H_artikel, Htparam

def ts_biltransfer_check_vatbl(rec_id:int, multi_vat:bool, balance:decimal, closed:bool, splitted:bool):
    fl_code = 0
    its_ok = False
    h_bill = h_bill_line = h_artikel = htparam = None

    vat_list = None

    vat_list_list, Vat_list = create_model("Vat_list", {"vat":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, its_ok, h_bill, h_bill_line, h_artikel, htparam


        nonlocal vat_list
        nonlocal vat_list_list
        return {"fl_code": fl_code, "its_ok": its_ok}

    def check_vat():

        nonlocal fl_code, its_ok, h_bill, h_bill_line, h_artikel, htparam


        nonlocal vat_list
        nonlocal vat_list_list

        anz_vat:int = 0
        anz_pay:int = 0
        tot_rev:decimal = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).all():

            if h_bill_line.artnr == 0:
                anz_pay = anz_pay + 1
            else:

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

                if h_artikel.artart != 0:
                    anz_pay = anz_pay + 1
                else:
                    tot_rev = tot_rev + h_bill_line.betrag

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == h_artikel.mwst_code)).first()

                    if not htparam:

                        vat_list = query(vat_list_list, first=True)

                        if not vat_list:
                            vat_list = Vat_list()
                            vat_list_list.append(vat_list)

                            vat_list.vat = 0
                            anz_vat = anz_vat + 1


                    else:

                        vat_list = query(vat_list_list, first=True)

                        if not vat_list:
                            vat_list = Vat_list()
                            vat_list_list.append(vat_list)

                            vat_list.vat = htparam.fdecimal
                            anz_vat = anz_vat + 1

        if anz_vat <= 1 and not multi_vat:

            return

        if (tot_rev == balance) or (tot_rev == - balance) and closed:

            return

        if anz_pay >= 1 and not splitted:
            fl_code = 1
            its_ok = False

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    check_vat()
    vat_list_list.clear()

    return generate_output()