from functions.additional_functions import *
import decimal
from datetime import date
from functions.argt_betrag import argt_betrag
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Res_line, Bill, Arrangement, Argt_line, Artikel, Argtstat

def nt_argtstat():
    bill_date:date = None
    price_decimal:int = 0
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    argt_betrag:decimal = to_decimal("0.0")
    betrag:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    ex_rate:decimal = to_decimal("0.0")
    do_it:bool = False
    rm_serv:bool = False
    rm_vat:bool = False
    serv_taxable:bool = False
    ai_str:str = ""
    htparam = res_line = bill = arrangement = argt_line = artikel = argtstat = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, price_decimal, service, vat, vat2, fact, argt_betrag, betrag, netto, ex_rate, do_it, rm_serv, rm_vat, serv_taxable, ai_str, htparam, res_line, bill, arrangement, argt_line, artikel, argtstat

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 496)).first()
    ai_str = htparam.fchar
    ai_str = replace_str(ai_str, " ", "")
    ai_str = replace_str(ai_str, ",", ";")

    if ai_str != "" and substring(ai_str, len(ai_str) - 1, 1) != (";").lower() :
        ai_str = ai_str + ";"

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 127)).first()
    rm_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    rm_serv = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    for res_line in db_session.query(Res_line).filter(
             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zipreis > 0)).order_by(Res_line.zinr, Res_line.active_flag).all():
        do_it = False

        if res_line.active_flag == 2 and res_line.ankunft == bill_date:

            bill = db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).first()

            if bill and bill.argtumsatz > 0:
                do_it = True
        else:
            do_it = True

        if do_it:

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == res_line.arrangement)).first()

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()

                if artikel:
                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                    betrag = to_decimal(round(argt_betrag * ex_rate , price_decimal))
                    netto =  to_decimal(betrag) / to_decimal(fact)

                    if betrag > 0:

                        argtstat = db_session.query(Argtstat).filter(
                                 (Argtstat.datum == bill_date) & (Argtstat.gastnrmember == res_line.gastnrmember) & (Argtstat.zinr == res_line.zinr) & (Argtstat.artnr == artikel.artnr) & (Argtstat.departement == artikel.departement)).first()

                        if not argtstat:
                            argtstat = Argtstat()
                            db_session.add(argtstat)

                            argtstat.datum = bill_date
                            argtstat.argtnr = arrangement.argtnr
                            argtstat.gastnrmember = res_line.gastnrmember
                            argtstat.zinr = res_line.zinr
                            argtstat.artnr = artikel.artnr
                            argtstat.departement = artikel.departement

                            if re.match(r".*" + res_line.arrangement + r";.*",ai_str, re.IGNORECASE):
                                argtstat.aiflag = True
                        argtstat.netto =  to_decimal(argtstat.netto) + to_decimal(netto)
                        argtstat.betrag =  to_decimal(argtstat.betrag) + to_decimal(betrag)

    return generate_output()