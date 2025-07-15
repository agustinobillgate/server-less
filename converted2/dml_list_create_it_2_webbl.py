#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Dml_artdep, Reslin_queasy, Queasy, Dml_art, L_artikel, L_untergrup, L_bestand, L_lieferant

def dml_list_create_it_2_webbl(curr_dept:int, selected_date:date, dml_no:string):

    prepare_cache ([Queasy, L_artikel, L_untergrup, L_bestand, L_lieferant])

    dml_hdr_remark = ""
    supply_list_data = []
    c_list_data = []
    dml_counter:int = 0
    fill_dml_nr:string = ""
    dml_no_remark:string = ""
    dml_artdep = reslin_queasy = queasy = dml_art = l_artikel = l_untergrup = l_bestand = l_lieferant = None

    supply_list = c_list = dml_list = None

    supply_list_data, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":string, "telefon":string, "fax":string, "namekontakt":string})
    c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})
    dml_list_data, Dml_list = create_model("Dml_list", {"counter":int, "dept":string, "id":string, "approved":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_hdr_remark, supply_list_data, c_list_data, dml_counter, fill_dml_nr, dml_no_remark, dml_artdep, reslin_queasy, queasy, dml_art, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal curr_dept, selected_date, dml_no


        nonlocal supply_list, c_list, dml_list
        nonlocal supply_list_data, c_list_data, dml_list_data

        return {"dml_hdr_remark": dml_hdr_remark, "supply-list": supply_list_data, "c-list": c_list_data}

    def create_it():

        nonlocal dml_hdr_remark, supply_list_data, c_list_data, dml_counter, fill_dml_nr, dml_no_remark, dml_artdep, reslin_queasy, queasy, dml_art, l_artikel, l_untergrup, l_bestand, l_lieferant
        nonlocal curr_dept, selected_date, dml_no


        nonlocal supply_list, c_list, dml_list
        nonlocal supply_list_data, c_list_data, dml_list_data

        dept:int = 0
        liefno:int = 0
        chginit:string = ""
        b_artdep = None
        breslin = None
        B_artdep =  create_buffer("B_artdep",Dml_artdep)
        Breslin =  create_buffer("Breslin",Reslin_queasy)
        c_list_data.clear()
        supply_list_data.clear()
        supply_list = Supply_list()
        supply_list_data.append(supply_list)


        if dml_no == None:
            dml_no_remark = "D" + to_string(curr_dept, "99") + substring(to_string(get_year(selected_date)) , 2, 2) + to_string(get_month(selected_date) , "99") + to_string(get_day(selected_date) , "99") + to_string(1, "999")
        else:
            dml_no_remark = dml_no

        queasy = get_cache (Queasy, {"key": [(eq, 342)],"char1": [(eq, dml_no_remark)],"number1": [(eq, curr_dept)]})

        if queasy:
            dml_hdr_remark = queasy.char2
        else:
            dml_hdr_remark = ""

        if curr_dept == 0:

            dml_art = get_cache (Dml_art, {"datum": [(eq, selected_date)]})
            while None != dml_art:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_art.artnr)]})

                if l_artikel:

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                    if l_untergrup:
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

                        if num_entries(dml_art.chginit, ";") > 1 and entry(0, dml_art.chginit, ";") != "" and substring(entry(0, dml_art.chginit, ";") , length(entry(0, dml_art.chginit, ";")) - 1) == ("!").lower() :
                            c_list.approved = True

                        elif dml_art.chginit != "" and substring(dml_art.chginit, length(dml_art.chginit) - 1) == ("!").lower() :
                            c_list.approved = True
                        liefno = 0
                        liefno = to_int(entry(1, dml_art.userinit, ";"))

                        l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_art.artnr)],"lager_nr": [(eq, 0)]})

                        if l_bestand:
                            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, dml_art.artnr)],"number3": [(eq, dml_counter)],"date1": [(eq, dml_art.datum)]})

                        if queasy:
                            c_list.remark = queasy.char1

                        if liefno != 0:

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                            if l_lieferant:
                                c_list.supplier = l_lieferant.firma
                                c_list.lief_nr = liefno

                                supply_list = query(supply_list_data, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_data.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                curr_recid = dml_art._recid
                dml_art = db_session.query(Dml_art).filter(
                         (Dml_art.datum == selected_date) & (substring(Dml_art.chginit, length(Dml_art.chginit) - 1) != ("*").lower()) & (Dml_art._recid > curr_recid)).first()
        else:

            breslin = db_session.query(Breslin).filter(
                     (Breslin.key == ("DML").lower()) & (Breslin.date1 == selected_date) & (to_int(entry(1, Breslin.char1, ";")) == curr_dept) & (entry(1, Breslin.char3, ";") == (dml_no).lower())).first()

            if breslin:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower())).first()
                while None != reslin_queasy:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))]})

                    if l_artikel:

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                        if l_untergrup:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = l_artikel.artnr
                            c_list.grp = l_untergrup.bezeich
                            c_list.zwkum = l_untergrup.zwkum
                            c_list.bezeich = l_artikel.bezeich
                            c_list.qty =  to_decimal(reslin_queasy.deci2)
                            c_list.price =  to_decimal(reslin_queasy.deci1)
                            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                            c_list.unit = l_artikel.traubensorte
                            c_list.content =  to_decimal(l_artikel.inhalt)
                            c_list.deliver =  to_decimal(reslin_queasy.deci3)
                            c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                            c_list.qty1 =  to_decimal(c_list.qty)
                            c_list.price1 =  to_decimal(c_list.price)
                            c_list.id = entry(0, reslin_queasy.char2, ";")
                            c_list.cid = entry(0, reslin_queasy.char3, ";")
                            c_list.dept = curr_dept
                            c_list.dml_nr = entry(1, reslin_queasy.char3, ";")

                            if num_entries(reslin_queasy.char3, ";") > 2:
                                c_list.qty2 =  to_decimal(to_decimal(entry(2 , reslin_queasy.char3 , ";")))

                            if entry(0, reslin_queasy.char3, ";") != "" and substring(entry(0, reslin_queasy.char3, ";") , length(entry(0, reslin_queasy.char3, ";")) - 1) == ("!").lower() :
                                c_list.approved = True
                            liefno = 0
                            liefno = to_int(entry(1, reslin_queasy.char2, ";"))

                            l_bestand = get_cache (L_bestand, {"artnr": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))],"lager_nr": [(eq, 0)]})

                            if l_bestand:
                                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"number2": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))],"number3": [(eq, dml_counter)],"date1": [(eq, reslin_queasy.date1)]})

                            if queasy:
                                c_list.remark = queasy.char1

                            if liefno != 0:

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                                if l_lieferant:
                                    c_list.supplier = l_lieferant.firma
                                    c_list.lief_nr = liefno

                                supply_list = query(supply_list_data, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_data.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                    curr_recid = reslin_queasy._recid
                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower()) & (Reslin_queasy._recid > curr_recid)).first()
            else:

                dml_artdep = get_cache (Dml_artdep, {"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})
                while None != dml_artdep:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_artdep.artnr)]})

                    if l_artikel:

                        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                        if l_untergrup:

                            if num_entries(dml_artdep.chginit, ";") > 1:

                                if entry(1, dml_artdep.chginit, ";") != "":
                                    fill_dml_nr = entry(1, dml_artdep.chginit, ";")
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = l_artikel.artnr
                            c_list.grp = l_untergrup.bezeich
                            c_list.zwkum = l_untergrup.zwkum
                            c_list.bezeich = l_artikel.bezeich
                            c_list.qty =  to_decimal(dml_artdep.anzahl)
                            c_list.price =  to_decimal(dml_artdep.einzelpreis)
                            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                            c_list.unit = l_artikel.traubensorte
                            c_list.content =  to_decimal(l_artikel.inhalt)
                            c_list.deliver =  to_decimal(dml_artdep.geliefert)
                            c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                            c_list.qty1 =  to_decimal(c_list.qty)
                            c_list.price1 =  to_decimal(c_list.price)
                            c_list.id = entry(0, dml_artdep.userinit, ";")
                            c_list.dept = curr_dept

                            if num_entries(dml_artdep.chginit, ";") > 1:
                                c_list.cid = replace_str(entry(0, dml_artdep.chginit, ";") , "!", "")
                                c_list.dml_nr = entry(1, dml_artdep.chginit, ";")

                                if c_list.dml_nr == "" or c_list.dml_nr == None:
                                    c_list.dml_nr = fill_dml_nr
                            else:
                                c_list.cid = replace_str(dml_artdep.chginit, "!", "")
                                c_list.dml_nr = fill_dml_nr

                            if num_entries(dml_artdep.chginit, ";") > 2:
                                c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_artdep.chginit , ";")))

                            if num_entries(dml_artdep.chginit, ";") > 1 and entry(0, dml_artdep.chginit, ";") != "" and substring(entry(0, dml_artdep.chginit, ";") , length(entry(0, dml_artdep.chginit, ";")) - 1) == ("!").lower() :
                                c_list.approved = True

                            elif dml_artdep.chginit != "" and substring(dml_artdep.chginit, length(dml_artdep.chginit) - 1) == ("!").lower() :
                                c_list.approved = True
                            liefno = 0
                            liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                            l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_artdep.artnr)],"lager_nr": [(eq, 0)]})

                            if l_bestand:
                                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"number3": [(eq, dml_counter)],"date1": [(eq, dml_artdep.datum)]})

                            if queasy:
                                c_list.remark = queasy.char1

                            if liefno != 0:

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                                if l_lieferant:
                                    c_list.supplier = l_lieferant.firma
                                    c_list.lief_nr = liefno

                                supply_list = query(supply_list_data, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_data.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                    curr_recid = dml_artdep._recid
                    dml_artdep = db_session.query(Dml_artdep).filter(
                             (Dml_artdep.datum == selected_date) & (Dml_artdep.departement == curr_dept) & (Dml_artdep._recid > curr_recid)).first()


    if dml_no != None:
        dml_counter = to_int(substring(dml_no, 10, 2))
    else:
        dml_counter = 1
    create_it()

    return generate_output()