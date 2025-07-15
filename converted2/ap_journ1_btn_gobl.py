#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Ap_journal, Bediener, Artikel

def ap_journ1_btn_gobl(from_date:date, to_date:date):

    prepare_cache ([L_lieferant, Ap_journal, Artikel])

    output_list_data = []
    l_lieferant = ap_journal = bediener = artikel = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, l_lieferant, ap_journal, bediener, artikel
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_list():

        nonlocal output_list_data, l_lieferant, ap_journal, bediener, artikel
        nonlocal from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        datum:date = None
        tot_saldo:Decimal = to_decimal("0.0")
        tot_netto:Decimal = to_decimal("0.0")
        output_list_data.clear()

        ap_journal_obj_list = {}
        ap_journal = Ap_journal()
        l_lieferant = L_lieferant()
        for ap_journal.userinit, ap_journal.rgdatum, ap_journal.docu_nr, ap_journal.lscheinnr, ap_journal.netto, ap_journal.bemerk, ap_journal.sysdate, ap_journal.zeit, ap_journal.zahlkonto, ap_journal.saldo, ap_journal._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(Ap_journal.userinit, Ap_journal.rgdatum, Ap_journal.docu_nr, Ap_journal.lscheinnr, Ap_journal.netto, Ap_journal.bemerk, Ap_journal.sysdate, Ap_journal.zeit, Ap_journal.zahlkonto, Ap_journal.saldo, Ap_journal._recid, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == Ap_journal.lief_nr)).filter(
                 (Ap_journal.rgdatum >= from_date) & (Ap_journal.rgdatum <= to_date)).order_by(Ap_journal.sysdate, Ap_journal.zeit).all():
            if ap_journal_obj_list.get(ap_journal._recid):
                continue
            else:
                ap_journal_obj_list[ap_journal._recid] = True


            receiver = l_lieferant.firma

            bediener = get_cache (Bediener, {"userinit": [(eq, ap_journal.userinit)]})
            output_list = Output_list()
            output_list_data.append(output_list)


            if ap_journal.zahlkonto == 0:
                output_list.str = to_string(ap_journal.rgdatum) + to_string(receiver, "x(20)") + to_string(ap_journal.docu_nr, "x(11)") + to_string(ap_journal.lscheinnr, "x(11)") + to_string(ap_journal.netto, " ->,>>>,>>>,>>9.99") + to_string("", "x(38)") + to_string(ap_journal.userinit, "x(3)") + to_string(ap_journal.bemerk, "x(12)") + to_string(ap_journal.sysdate) + to_string(ap_journal.zeit, "HH:MM")
                tot_netto =  to_decimal(tot_netto) + to_decimal(ap_journal.netto)


            else:

                artikel = get_cache (Artikel, {"artnr": [(eq, ap_journal.zahlkonto)],"departement": [(eq, 0)]})
                output_list.str = to_string(ap_journal.rgdatum) + to_string(receiver, "x(20)") + to_string(ap_journal.docu_nr, "x(11)") + to_string(ap_journal.lscheinnr, "x(11)") + to_string("", "x(18)") + to_string(ap_journal.saldo, " ->,>>>,>>>,>>9.99") + to_string(ap_journal.zahlkonto, ">>>9") + to_string(artikel.bezeich, "x(16)") + to_string(ap_journal.userinit, "x(3)") + to_string(ap_journal.bemerk, "x(12)") + to_string(ap_journal.sysdate) + to_string(ap_journal.zeit, "HH:MM")
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(ap_journal.saldo)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.str = to_string(" ", "x(8)") + to_string("T O T A L", "x(20)") + to_string(" ", "x(11)") + to_string(" ", "x(11)") + to_string(tot_netto, "->>,>>>,>>>,>>9.99") + to_string(tot_saldo, "->>,>>>,>>>,>>9.99") + to_string(" ", "x(3)") + to_string(" ", "x(12)") + to_string(" ") + to_string(" ")

    create_list()

    return generate_output()