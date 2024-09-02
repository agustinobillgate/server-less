from functions.additional_functions import *
import decimal
from datetime import date
from models import L_orderhdr, Htparam, Waehrung, L_lieferant

def prepare_dml_list3bl(lief_nr:int):
    local_nr = 0
    supplier = ""
    currdate = None
    err_code = 0
    t_l_orderhdr_list = []
    t_l_lieferant_list = []
    l_orderhdr = htparam = waehrung = l_lieferant = None

    t_l_lieferant = t_l_orderhdr = l_orderhdr1 = None

    t_l_lieferant_list, T_l_lieferant = create_model("T_l_lieferant", {"lief_nr":int, "firma":str, "telefon":str, "fax":str, "namekontakt":str, "rec_id":int})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    L_orderhdr1 = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, supplier, currdate, err_code, t_l_orderhdr_list, t_l_lieferant_list, l_orderhdr, htparam, waehrung, l_lieferant
        nonlocal l_orderhdr1


        nonlocal t_l_lieferant, t_l_orderhdr, l_orderhdr1
        nonlocal t_l_lieferant_list, t_l_orderhdr_list
        return {"local_nr": local_nr, "supplier": supplier, "currdate": currdate, "err_code": err_code, "t-l-orderhdr": t_l_orderhdr_list, "t-l-lieferant": t_l_lieferant_list}

    def new_po_number():

        nonlocal local_nr, supplier, currdate, err_code, t_l_orderhdr_list, t_l_lieferant_list, l_orderhdr, htparam, waehrung, l_lieferant
        nonlocal l_orderhdr1


        nonlocal t_l_lieferant, t_l_orderhdr, l_orderhdr1
        nonlocal t_l_lieferant_list, t_l_orderhdr_list

        s:str = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        docu_nr:str = ""
        L_orderhdr1 = L_orderhdr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        currdate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 973)).first()
        l_orderhdr = L_orderhdr()
        db_session.add(l_orderhdr)


        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(currdate)
            yy = get_year(currdate)
            s = "P" + substring(to_string(get_year(currdate)) , 2, 2) + to_string(get_month(currdate) , "99")

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                    (get_month(L_orderhdr1.bestelldatum) == mm) &  (get_year(L_orderhdr1.bestelldatum) == yy) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
                i = to_int(substring(l_orderhdr1.docu_nr, 5, 5))
                i = i + 1
                docu_nr = s + to_string(i, "99999")
                l_orderhdr.docu_nr = docu_nr

                return
            docu_nr = s + to_string(i, "99999")
            l_orderhdr.docu_nr = docu_nr

            return
        s = "P" + substring(to_string(get_year(currdate)) , 2, 2) + to_string(get_month(currdate) , "99") + to_string(get_day(currdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                (L_orderhdr1.bestelldatum == currdate) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")
            l_orderhdr.docu_nr = docu_nr

            return
        docu_nr = s + to_string(i, "999")
        l_orderhdr.docu_nr = docu_nr


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        err_code = 1
    else:
        local_nr = waehrungsnr

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == lief_nr)).first()
        supplier = l_lieferant.firma
        new_po_number()

        l_orderhdr = db_session.query(L_orderhdr).first()
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_list.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
        t_l_orderhdr.rec_id = l_orderhdr._recid

        l_lieferant = db_session.query(L_lieferant).first()
        t_l_lieferant = T_l_lieferant()
        t_l_lieferant_list.append(t_l_lieferant)

        t_l_lieferant.lief_nr = l_lieferant.lief_nr
        t_l_lieferant.firma = l_lieferant.firma
        t_l_lieferant.rec_id = l_lieferant._recid
        t_l_lieferant.telefon = l_lieferant.telefon
        t_l_lieferant.fax = l_lieferant.fax
        t_l_lieferant.namekontakt = l_lieferant.namekontakt

    return generate_output()