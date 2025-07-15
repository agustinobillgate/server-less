#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, Htparam, Waehrung, L_lieferant

def prepare_dml_list3bl(lief_nr:int):

    prepare_cache ([L_orderhdr, Htparam, Waehrung, L_lieferant])

    local_nr = 0
    supplier = ""
    currdate = None
    err_code = 0
    t_l_orderhdr_data = []
    t_l_lieferant_data = []
    l_orderhdr = htparam = waehrung = l_lieferant = None

    t_l_lieferant = t_l_orderhdr = None

    t_l_lieferant_data, T_l_lieferant = create_model("T_l_lieferant", {"lief_nr":int, "firma":string, "telefon":string, "fax":string, "namekontakt":string, "rec_id":int})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, supplier, currdate, err_code, t_l_orderhdr_data, t_l_lieferant_data, l_orderhdr, htparam, waehrung, l_lieferant
        nonlocal lief_nr


        nonlocal t_l_lieferant, t_l_orderhdr
        nonlocal t_l_lieferant_data, t_l_orderhdr_data

        return {"local_nr": local_nr, "supplier": supplier, "currdate": currdate, "err_code": err_code, "t-l-orderhdr": t_l_orderhdr_data, "t-l-lieferant": t_l_lieferant_data}

    def new_po_number():

        nonlocal local_nr, supplier, currdate, err_code, t_l_orderhdr_data, t_l_lieferant_data, l_orderhdr, htparam, waehrung, l_lieferant
        nonlocal lief_nr


        nonlocal t_l_lieferant, t_l_orderhdr
        nonlocal t_l_lieferant_data, t_l_orderhdr_data

        l_orderhdr1 = None
        s:string = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        docu_nr:string = ""
        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        currdate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 973)]})
        l_orderhdr = L_orderhdr()
        db_session.add(l_orderhdr)


        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(currdate)
            yy = get_year(currdate)
            s = "P" + substring(to_string(get_year(currdate)) , 2, 2) + to_string(get_month(currdate) , "99")

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                     (get_month(L_orderhdr1.bestelldatum) == mm) & (get_year(L_orderhdr1.bestelldatum) == yy) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
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
                 (L_orderhdr1.bestelldatum == currdate) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")
            l_orderhdr.docu_nr = docu_nr

            return
        docu_nr = s + to_string(i, "999")
        l_orderhdr.docu_nr = docu_nr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        err_code = 1
    else:
        local_nr = waehrung.waehrungsnr

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
        supplier = l_lieferant.firma
        new_po_number()
        pass
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_data.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
        t_l_orderhdr.rec_id = l_orderhdr._recid


        pass
        t_l_lieferant = T_l_lieferant()
        t_l_lieferant_data.append(t_l_lieferant)

        t_l_lieferant.lief_nr = l_lieferant.lief_nr
        t_l_lieferant.firma = l_lieferant.firma
        t_l_lieferant.rec_id = l_lieferant._recid
        t_l_lieferant.telefon = l_lieferant.telefon
        t_l_lieferant.fax = l_lieferant.fax
        t_l_lieferant.namekontakt = l_lieferant.namekontakt

    return generate_output()