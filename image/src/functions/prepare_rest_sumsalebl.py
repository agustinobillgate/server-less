from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Artikel, Hoteldpt

def prepare_rest_sumsalebl(curr_dept:int):
    ldry = 0
    dstore = 0
    clb = 0
    price_decimal = 0
    exchg_rate = 0
    curr_local = ""
    curr_foreign = ""
    anzahl = 0
    sep_line = ""
    dept_name = ""
    from_date = None
    tt_bezeich_list = []
    tt_artnr_list = []
    p_240 = False
    bezeich:[str] = ["", "", "", "", "", ""]
    artnr_list:[int] = [0, 0, 0, 0, 0, 0]
    i:int = 0
    paramnr_list:[int] = [0, 0, 0, 0, 0, 0]
    htparam = waehrung = artikel = hoteldpt = None

    tt_artnr = tt_bezeich = None

    tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "artnr":int})
    tt_bezeich_list, Tt_bezeich = create_model("Tt_bezeich", {"curr_i":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ldry, dstore, clb, price_decimal, exchg_rate, curr_local, curr_foreign, anzahl, sep_line, dept_name, from_date, tt_bezeich_list, tt_artnr_list, p_240, bezeich, artnr_list, i, paramnr_list, htparam, waehrung, artikel, hoteldpt


        nonlocal tt_artnr, tt_bezeich
        nonlocal tt_artnr_list, tt_bezeich_list
        return {"ldry": ldry, "dstore": dstore, "clb": clb, "price_decimal": price_decimal, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "anzahl": anzahl, "sep_line": sep_line, "dept_name": dept_name, "from_date": from_date, "tt-bezeich": tt_bezeich_list, "tt-artnr": tt_artnr_list, "p_240": p_240}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    p_240 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()
    ldry = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1082)).first()
    dstore = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1045)).first()
    clb = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = fchar
    for i in range(1,5 + 1) :

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == paramnr_list[i - 1])).first()
        artnr_list[i - 1] = htparam.finteger

        if htparam.finteger != 0:
            anzahl = anzahl + 1

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 1)).first()

            if artikel:
                bezeich[i - 1] = artikel.bezeich
        tt_artnr = Tt_artnr()
        tt_artnr_list.append(tt_artnr)

        tt_artnr.curr_i = i
        tt_artnr.artnr = artnr_list[i - 1]


        tt_bezeich = Tt_bezeich()
        tt_bezeich_list.append(tt_bezeich)

        tt_bezeich.curr_i = i
        tt_bezeich.bezeich = bezeich[i - 1]


    sep_line = ""
    for i in range(1,116 + 1) :
        sep_line = sep_line + "-"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0) &  (Hoteldpt.num == curr_dept)).first()

    if hoteldpt:
        dept_name = hoteldpt.depart

    return generate_output()