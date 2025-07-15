#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Dml_art, Dml_artdep, Reslin_queasy, Queasy, L_artikel, L_untergrup, L_bestand, L_lieferant

def dml_list_copy_articles_11_webbl(user_init:string, curr_dept:int, selected_date:date, dml_no:string):

    prepare_cache ([Dml_art, Dml_artdep, Reslin_queasy, Queasy, L_artikel, L_untergrup, L_bestand, L_lieferant])

    approve_flag = False
    c_list_data = []
    supply_list_data = []
    dml_counter:int = 0
    copy_mode:string = ""
    liefno:int = 0
    dml_art = dml_artdep = reslin_queasy = queasy = l_artikel = l_untergrup = l_bestand = l_lieferant = None

    c_list = supply_list = d_art = d_artdep = breslin = buff_queasy = None

    c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})
    supply_list_data, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":string, "telefon":string, "fax":string, "namekontakt":string})

    D_art = create_buffer("D_art",Dml_art)
    D_artdep = create_buffer("D_artdep",Dml_artdep)
    Breslin = create_buffer("Breslin",Reslin_queasy)
    Buff_queasy = create_buffer("Buff_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal approve_flag, c_list_data, supply_list_data, dml_counter, copy_mode, liefno, dml_art, dml_artdep, reslin_queasy, queasy, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal user_init, curr_dept, selected_date, dml_no
        nonlocal d_art, d_artdep, breslin, buff_queasy


        nonlocal c_list, supply_list, d_art, d_artdep, breslin, buff_queasy
        nonlocal c_list_data, supply_list_data

        return {"approve_flag": approve_flag, "c-list": c_list_data, "supply-list": supply_list_data}

    def copy_articles():

        nonlocal approve_flag, c_list_data, supply_list_data, dml_counter, copy_mode, dml_art, dml_artdep, reslin_queasy, queasy, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal user_init, curr_dept, selected_date, dml_no
        nonlocal d_art, d_artdep, breslin, buff_queasy


        nonlocal c_list, supply_list, d_art, d_artdep, breslin, buff_queasy
        nonlocal c_list_data, supply_list_data

        liefno:int = 0
        c_list_data.clear()
        supply_list_data.clear()

        if curr_dept == 0:

            dml_art_obj_list = {}
            dml_art = Dml_art()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for dml_art.anzahl, dml_art.einzelpreis, dml_art.geliefert, dml_art.userinit, dml_art.chginit, dml_art.artnr, dml_art._recid, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Dml_art.anzahl, Dml_art.einzelpreis, Dml_art.geliefert, Dml_art.userinit, Dml_art.chginit, Dml_art.artnr, Dml_art._recid, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == Dml_art.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (Dml_art.datum == (selected_date - timedelta(days=1)))).order_by(Dml_art._recid).all():
                if dml_art_obj_list.get(dml_art._recid):
                    continue
                else:
                    dml_art_obj_list[dml_art._recid] = True


                copy_from_dml_art()
        else:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     ((num_entries(Reslin_queasy.char3, ";") >= 2) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower())) & (Reslin_queasy.date1 == (selected_date - timedelta(days=1))) & ((num_entries(Reslin_queasy.char1, ";") >= 2) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept))).first()

            if reslin_queasy:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))]})

                if l_artikel:

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                    if l_untergrup:
                        copy_mode = "reslin-queasy"

            if copy_mode == "":

                dml_artdep = db_session.query(Dml_artdep).filter(
                         (((num_entries(Dml_artdep.chginit, ";") >= 2) & (entry(1, Dml_artdep.chginit, ";") == (dml_no).lower())) | ((num_entries(Dml_artdep.chginit, ";") >= 2) & (entry(1, Dml_artdep.chginit, ";") == "")) | ((num_entries(Dml_artdep.chginit, ";") == 1))) & (Dml_artdep.datum == (selected_date - timedelta(days=1))) & (Dml_artdep.departement == curr_dept)).first()

                if dml_artdep:
                    copy_mode = "dml-artdep"

            if copy_mode.lower()  == ("reslin-queasy").lower() :
                copy_from_reslin_queasy()

            elif copy_mode.lower()  == ("dml-artdep").lower() :
                copy_from_dml_artdep()
        approve_flag = False


    def copy_from_dml_art():

        nonlocal approve_flag, c_list_data, supply_list_data, dml_counter, copy_mode, liefno, dml_art, dml_artdep, reslin_queasy, queasy, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal user_init, curr_dept, selected_date, dml_no
        nonlocal d_art, d_artdep, breslin, buff_queasy


        nonlocal c_list, supply_list, d_art, d_artdep, breslin, buff_queasy
        nonlocal c_list_data, supply_list_data


        c_list = C_list()
        c_list_data.append(c_list)

        c_list.artnr = l_artikel.artnr
        c_list.grp = l_untergrup.bezeich
        c_list.zwkum = l_untergrup.zwkum
        c_list.bezeich = l_artikel.bezeich
        c_list.qty =  to_decimal(dml_art.anzahl)
        c_list.price =  to_decimal(dml_art.einzelpreis)
        c_list.l_price =  to_decimal(l_artikel.ek_letzter)
        c_list.unit = l_artikel.traubensorte
        c_list.content =  to_decimal(l_artikel.inhalt)
        c_list.deliver =  to_decimal(dml_art.geliefert)
        c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
        c_list.qty1 =  to_decimal(c_list.qty)
        c_list.price1 =  to_decimal(c_list.price)
        c_list.id = entry(0, dml_art.userinit, ";")
        c_list.cid = replace_str(entry(0, dml_art.chginit, ";") , "!", "")
        c_list.dept = curr_dept

        if num_entries(dml_art.chginit, ";") > 1:
            c_list.dml_nr = entry(1, dml_art.chginit, ";")

        if num_entries(dml_art.chginit, ";") > 2:
            c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_art.chginit , ";")))

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_art.artnr)],"lager_nr": [(eq, 0)]})

        if l_bestand:
            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


    def copy_from_reslin_queasy():

        nonlocal approve_flag, c_list_data, supply_list_data, dml_counter, copy_mode, liefno, dml_art, dml_artdep, reslin_queasy, queasy, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal user_init, curr_dept, selected_date, dml_no
        nonlocal d_art, d_artdep, breslin, buff_queasy


        nonlocal c_list, supply_list, d_art, d_artdep, breslin, buff_queasy
        nonlocal c_list_data, supply_list_data


        dml_counter = to_int(substring(dml_no, 9, 3))

        reslin_queasy_obj_list = {}
        reslin_queasy = Reslin_queasy()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for reslin_queasy.char1, reslin_queasy.deci2, reslin_queasy.deci1, reslin_queasy.deci3, reslin_queasy.char2, reslin_queasy.char3, reslin_queasy.date1, reslin_queasy._recid, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Reslin_queasy.char1, Reslin_queasy.deci2, Reslin_queasy.deci1, Reslin_queasy.deci3, Reslin_queasy.char2, Reslin_queasy.char3, Reslin_queasy.date1, Reslin_queasy._recid, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == to_int(entry(0, Reslin_queasy.char1, ";")))).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == (selected_date - timedelta(days=1))) & ((num_entries(Reslin_queasy.char1, ";") >= 2) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept)) & (Reslin_queasy.number2 == dml_counter)).order_by(Reslin_queasy._recid).all():
            if reslin_queasy_obj_list.get(reslin_queasy._recid):
                continue
            else:
                reslin_queasy_obj_list[reslin_queasy._recid] = True


            c_list = C_list()
            c_list_data.append(c_list)

            c_list.zwkum = l_untergrup.zwkum
            c_list.grp = l_untergrup.bezeich
            c_list.artnr = l_artikel.artnr
            c_list.bezeich = l_artikel.bezeich
            c_list.qty =  to_decimal(reslin_queasy.deci2)
            c_list.price =  to_decimal(reslin_queasy.deci1)
            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
            c_list.unit = l_artikel.traubensorte
            c_list.content =  to_decimal(l_artikel.inhalt)
            c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
            c_list.deliver =  to_decimal(reslin_queasy.deci3)
            c_list.dept = curr_dept
            c_list.id = entry(0, reslin_queasy.char2, ";")
            c_list.cid = entry(0, reslin_queasy.char3, ";")
            c_list.price1 =  to_decimal(c_list.price)
            c_list.qty1 =  to_decimal(c_list.qty)

            if num_entries(reslin_queasy.char3, ";") > 2:
                c_list.qty2 =  to_decimal(to_decimal(entry(2 , reslin_queasy.char3 , ";")))

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))],"lager_nr": [(eq, 0)]})

            if l_bestand:
                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"number2": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))],"number3": [(eq, dml_counter)],"date1": [(eq, reslin_queasy.date1)]})

            if queasy:
                c_list.remark = queasy.char1


            liefno = 0
            liefno = to_int(entry(1, reslin_queasy.char2, ";"))

            if liefno != 0:

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                if l_lieferant:
                    c_list.supplier = l_lieferant.firma
                    c_list.lief_nr = liefno


    def copy_from_dml_artdep():

        nonlocal approve_flag, c_list_data, supply_list_data, dml_counter, copy_mode, liefno, dml_art, dml_artdep, reslin_queasy, queasy, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal user_init, curr_dept, selected_date, dml_no
        nonlocal d_art, d_artdep, breslin, buff_queasy


        nonlocal c_list, supply_list, d_art, d_artdep, breslin, buff_queasy
        nonlocal c_list_data, supply_list_data


        dml_counter = 1

        dml_artdep_obj_list = {}
        dml_artdep = Dml_artdep()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for dml_artdep.anzahl, dml_artdep.einzelpreis, dml_artdep.geliefert, dml_artdep.userinit, dml_artdep.chginit, dml_artdep.artnr, dml_artdep.departement, dml_artdep.datum, dml_artdep._recid, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Dml_artdep.anzahl, Dml_artdep.einzelpreis, Dml_artdep.geliefert, Dml_artdep.userinit, Dml_artdep.chginit, Dml_artdep.artnr, Dml_artdep.departement, Dml_artdep.datum, Dml_artdep._recid, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == Dml_artdep.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (Dml_artdep.datum == (selected_date - timedelta(days=1))) & (Dml_artdep.departement == curr_dept)).order_by(Dml_artdep._recid).all():
            if dml_artdep_obj_list.get(dml_artdep._recid):
                continue
            else:
                dml_artdep_obj_list[dml_artdep._recid] = True


            c_list = C_list()
            c_list_data.append(c_list)

            c_list.zwkum = l_untergrup.zwkum
            c_list.grp = l_untergrup.bezeich
            c_list.artnr = l_artikel.artnr
            c_list.bezeich = l_artikel.bezeich
            c_list.qty =  to_decimal(dml_artdep.anzahl)
            c_list.price =  to_decimal(dml_artdep.einzelpreis)
            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
            c_list.unit = l_artikel.traubensorte
            c_list.content =  to_decimal(l_artikel.inhalt)
            c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
            c_list.deliver =  to_decimal(dml_artdep.geliefert)
            c_list.dept = curr_dept
            c_list.id = entry(0, dml_artdep.userinit, ";")
            c_list.price1 =  to_decimal(c_list.price)
            c_list.qty1 =  to_decimal(c_list.qty)

            if num_entries(dml_artdep.chginit, ";") > 1:
                c_list.cid = replace_str(entry(0, dml_artdep.chginit, ";") , "!", "")
            else:
                c_list.cid = replace_str(dml_artdep.chginit, "!", "")

            if num_entries(dml_artdep.chginit, ";") > 2:
                c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_artdep.chginit , ";")))

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_artdep.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"number3": [(eq, dml_counter)],"date1": [(eq, dml_artdep.datum)]})

            if queasy:
                c_list.remark = queasy.char1


            liefno = 0
            liefno = to_int(entry(1, dml_artdep.userinit, ";"))

            if liefno != 0:

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                if l_lieferant:
                    c_list.supplier = l_lieferant.firma
                    c_list.lief_nr = liefno

    if dml_no == None or dml_no == " ":
        dml_no = "D" + to_string(curr_dept, "99") + substring(to_string(get_year((selected_date - 1)) , "9999") , 2, 2) + to_string(get_month((selected_date - 1)) , "99") + to_string(get_day((selected_date - 1)) , "99") + to_string(1, "999")
    copy_articles()

    return generate_output()