from functions.additional_functions import *
import decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from models import Htparam, Res_line, Argt_line, Artikel, Genstat, Billjournal

def argt_betrag_new(res_recid:int, argt_recid:int, curr_date:date):
    argt_betrag = to_decimal("0.0")
    ex_rate = 1
    bill_date:date = None
    tokcounter:int = 0
    count_i:int = 0
    mestoken:str = ""
    mesvalue:str = ""
    curr_artnr:int = 0
    curr_dept:int = 0
    a_betrag:decimal = to_decimal("0.0")
    x_betrag:decimal = to_decimal("0.0")
    htparam = res_line = argt_line = artikel = genstat = billjournal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_betrag, ex_rate, bill_date, tokcounter, count_i, mestoken, mesvalue, curr_artnr, curr_dept, a_betrag, x_betrag, htparam, res_line, argt_line, artikel, genstat, billjournal
        nonlocal res_recid, argt_recid, curr_date

        return {"argt_betrag": argt_betrag, "ex_rate": ex_rate}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    if curr_date == None or (curr_date >= bill_date):
        argt_betrag, ex_rate = get_output(argt_betrag(res_recid, argt_recid))

        return generate_output()

    res_line = db_session.query(Res_line).filter(
             (Res_line._recid == res_recid)).first()

    argt_line = db_session.query(Argt_line).filter(
             (Argt_line._recid == argt_recid)).first()

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()

    genstat = db_session.query(Genstat).filter(
             (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr) & (Genstat.datum == curr_date)).first()

    if genstat and genstat.res_char[3] != "":
        for tokcounter in range(1,num_entries(genstat.res_char[3], ";")  + 1) :
            mestoken = trim(entry(tokcounter - 1, genstat.res_char[3], ";"))

            if mestoken != "":
                curr_artnr = to_int(entry(0, mestoken, ","))
                curr_dept = to_int(entry(1, mestoken, ","))
                a_betrag =  to_decimal(to_decimal(entry(2 , mestoken , ","))) * to_decimal(0.01)
                x_betrag =  to_decimal(to_decimal(entry(3 , mestoken , ","))) * to_decimal(0.01)

                if curr_artnr == artikel.artnr and curr_dept == artikel.departement:
                    argt_betrag =  to_decimal(a_betrag)
                    ex_rate =  to_decimal(x_betrag)

                    return generate_output()

    billjournal = db_session.query(Billjournal).filter(
             (Billjournal.artnr == artikel.artnr) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == curr_date) & (Billjournal.comment == to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr))).first()

    if billjournal:
        argt_betrag =  to_decimal(billjournal.betrag)
        ex_rate =  to_decimal("1")

        return generate_output()
    argt_betrag, ex_rate = get_output(argt_betrag(res_recid, argt_recid))

    return generate_output()