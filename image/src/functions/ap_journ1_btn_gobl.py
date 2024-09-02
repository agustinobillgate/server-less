from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lieferant, Ap_journal, Bediener, Artikel

def ap_journ1_btn_gobl(from_date:date, to_date:date):
    output_list_list = []
    l_lieferant = ap_journal = bediener = artikel = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, l_lieferant, ap_journal, bediener, artikel


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, l_lieferant, ap_journal, bediener, artikel


        nonlocal output_list
        nonlocal output_list_list

        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        receiver:str = ""
        datum:date = None
        tot_saldo:decimal = 0
        tot_netto:decimal = 0
        output_list_list.clear()

        ap_journal_obj_list = []
        for ap_journal, l_lieferant in db_session.query(Ap_journal, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Ap_journal.lief_nr)).filter(
                (Ap_journal.rgdatum >= from_date) &  (Ap_journal.rgdatum <= to_date)).all():
            if ap_journal._recid in ap_journal_obj_list:
                continue
            else:
                ap_journal_obj_list.append(ap_journal._recid)


            receiver = l_lieferant.firma

            bediener = db_session.query(Bediener).filter(
                    (Bediener.userinit == ap_journal.userinit)).first()
            output_list = Output_list()
            output_list_list.append(output_list)


            if ap_journal.zahlkonto == 0:
                output_list.str = to_string(ap_journal.rgdatum) + to_string(receiver, "x(20)") + to_string(ap_journal.docu_nr, "x(11)") + to_string(ap_journal.lscheinnr, "x(11)") + to_string(ap_journal.netto, " ->,>>>,>>>,>>9.99") + to_string("", "x(38)") + to_string(ap_journal.userinit, "x(3)") + to_string(ap_journal.bemerk, "x(12)") + to_string(ap_journal.sysdate) + to_string(ap_journal.zeit, "HH:MM")
                tot_netto = tot_netto + ap_journal.netto


            else:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == ap_journal.zahlkonto) &  (Artikel.departement == 0)).first()
                output_list.str = to_string(ap_journal.rgdatum) + to_string(receiver, "x(20)") + to_string(ap_journal.docu_nr, "x(11)") + to_string(ap_journal.lscheinnr, "x(11)") + to_string("", "x(18)") + to_string(ap_journal.saldo, " ->,>>>,>>>,>>9.99") + to_string(ap_journal.zahlkonto, ">>>9") + to_string(artikel.bezeich, "x(16)") + to_string(ap_journal.userinit, "x(3)") + to_string(ap_journal.bemerk, "x(12)") + to_string(ap_journal.sysdate) + to_string(ap_journal.zeit, "HH:MM")
                tot_saldo = tot_saldo + ap_journal.saldo


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = to_string(" ", "x(8)") + to_string("T O T A L", "x(20)") + to_string(" ", "x(11)") + to_string(" ", "x(11)") + to_string(tot_netto, "->>,>>>,>>>,>>9.99") + to_string(tot_saldo, "->>,>>>,>>>,>>9.99") + to_string(" ", "x(3)") + to_string(" ", "x(12)") + to_string(" ") + to_string(" ")


    create_list()

    return generate_output()