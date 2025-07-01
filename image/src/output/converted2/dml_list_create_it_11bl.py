#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Dml_art, L_artikel, L_untergrup, L_bestand, Queasy, L_lieferant, Dml_artdep

def dml_list_create_it_11bl(curr_dept:int, selected_date:date, dml_no:string):

    prepare_cache ([L_artikel, L_untergrup, L_bestand, Queasy, L_lieferant])

    supply_list_list = []
    c_list_list = []
    dml_art = l_artikel = l_untergrup = l_bestand = queasy = l_lieferant = dml_artdep = None

    supply_list = c_list = None

    supply_list_list, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":string, "telefon":string, "fax":string, "namekontakt":string})
    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal supply_list_list, c_list_list, dml_art, l_artikel, l_untergrup, l_bestand, queasy, l_lieferant, dml_artdep
        nonlocal curr_dept, selected_date, dml_no


        nonlocal supply_list, c_list
        nonlocal supply_list_list, c_list_list

        return {"supply-list": supply_list_list, "c-list": c_list_list}

    def create_it():

        nonlocal supply_list_list, c_list_list, dml_art, l_artikel, l_untergrup, l_bestand, queasy, l_lieferant, dml_artdep
        nonlocal curr_dept, selected_date, dml_no


        nonlocal supply_list, c_list
        nonlocal supply_list_list, c_list_list

        dept:int = 0
        liefno:int = 0
        c_list_list.clear()
        supply_list_list.clear()
        supply_list = Supply_list()
        supply_list_list.append(supply_list)


        if curr_dept == 0:

            dml_art = get_cache (Dml_art, {"datum": [(eq, selected_date)]})
            while None != dml_art:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_art.artnr)]})

                if l_artikel:

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                    if l_untergrup:
                        c_list = C_list()
                        c_list_list.append(c_list)

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
                        c_list.cid = replace_str(dml_art.chginit, "!", "")
                        c_list.dept = curr_dept

                        if dml_art.chginit != "" and substring(dml_art.chginit, length(dml_art.chginit) - 1) == ("!").lower() :
                            c_list.approved = True
                        liefno = 0
                        liefno = to_int(entry(1, dml_art.userinit, ";"))

                        l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_art.artnr)],"lager_nr": [(eq, 0)]})

                        if l_bestand:
                            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, dml_art.artnr)],"date1": [(eq, dml_art.datum)]})

                        if queasy:
                            c_list.remark = queasy.char1

                        if liefno != 0:

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                            if l_lieferant:
                                c_list.supplier = l_lieferant.firma
                                c_list.lief_nr = liefno

                                supply_list = query(supply_list_list, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_list.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                curr_recid = dml_art._recid
                dml_art = db_session.query(Dml_art).filter(
                         (Dml_art.datum == selected_date) & (Dml_art._recid > curr_recid)).first()
        else:

            dml_artdep = get_cache (Dml_artdep, {"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})
            while None != dml_artdep:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, dml_artdep.artnr)]})

                if l_artikel:

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                    if l_untergrup:
                        c_list = C_list()
                        c_list_list.append(c_list)

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
                        c_list.cid = dml_artdep.chginit
                        c_list.dept = curr_dept

                        if dml_artdep.chginit != "" and substring(dml_artdep.chginit, length(dml_artdep.chginit) - 1) == ("!").lower() :
                            c_list.approved = True
                        liefno = 0
                        liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                        l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_artdep.artnr)],"lager_nr": [(eq, 0)]})

                        if l_bestand:
                            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"date1": [(eq, dml_artdep.datum)]})

                        if queasy:
                            c_list.remark = queasy.char1

                        if liefno != 0:

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                            if l_lieferant:
                                c_list.supplier = l_lieferant.firma
                                c_list.lief_nr = liefno

                            supply_list = query(supply_list_list, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                            if not supply_list:
                                supply_list = Supply_list()
                                supply_list_list.append(supply_list)

                                supply_list.lief_nr = l_lieferant.lief_nr
                                supply_list.supplier = l_lieferant.firma
                                supply_list.telefon = l_lieferant.telefon
                                supply_list.fax = l_lieferant.fax
                                supply_list.namekontakt = l_lieferant.namekontakt

                curr_recid = dml_artdep._recid
                dml_artdep = db_session.query(Dml_artdep).filter(
                         (Dml_artdep.datum == selected_date) & (Dml_artdep.departement == curr_dept) & (Dml_artdep._recid > curr_recid)).first()


    create_it()

    return generate_output()