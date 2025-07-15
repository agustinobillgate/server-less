#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Dml_artdep, Dml_art, L_artikel, L_untergrup, L_bestand, Queasy, L_lieferant

def dml_list_modifybl(user_init:string, dml_no:string, curr_dept:int, selected_date:date):

    prepare_cache ([Reslin_queasy, Dml_artdep, Dml_art, L_artikel, L_untergrup, L_bestand, Queasy, L_lieferant])

    c_list_data = []
    counter:int = 0
    fill_dml_nr:string = ""
    reslin_queasy = dml_artdep = dml_art = l_artikel = l_untergrup = l_bestand = queasy = l_lieferant = None

    c_list = breslin = bdml_artdep = bdml_art = None

    c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})

    Breslin = create_buffer("Breslin",Reslin_queasy)
    Bdml_artdep = create_buffer("Bdml_artdep",Dml_artdep)
    Bdml_art = create_buffer("Bdml_art",Dml_art)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_data, counter, fill_dml_nr, reslin_queasy, dml_artdep, dml_art, l_artikel, l_untergrup, l_bestand, queasy, l_lieferant
        nonlocal user_init, dml_no, curr_dept, selected_date
        nonlocal breslin, bdml_artdep, bdml_art


        nonlocal c_list, breslin, bdml_artdep, bdml_art
        nonlocal c_list_data

        return {"c-list": c_list_data}

    def modify_dml():

        nonlocal c_list_data, counter, fill_dml_nr, reslin_queasy, dml_artdep, dml_art, l_artikel, l_untergrup, l_bestand, queasy, l_lieferant
        nonlocal user_init, dml_no, curr_dept, selected_date
        nonlocal breslin, bdml_artdep, bdml_art


        nonlocal c_list, breslin, bdml_artdep, bdml_art
        nonlocal c_list_data

        liefno:int = 0

        if curr_dept == 0:

            dml_art_obj_list = {}
            dml_art = Dml_art()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for dml_art.anzahl, dml_art.einzelpreis, dml_art.geliefert, dml_art.userinit, dml_art.chginit, dml_art.artnr, dml_art.datum, dml_art._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Dml_art.anzahl, Dml_art.einzelpreis, Dml_art.geliefert, Dml_art.userinit, Dml_art.chginit, Dml_art.artnr, Dml_art.datum, Dml_art._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == Dml_art.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (Dml_art.datum == selected_date)).order_by(Dml_art._recid).all():
                if dml_art_obj_list.get(dml_art._recid):
                    continue
                else:
                    dml_art_obj_list[dml_art._recid] = True


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
                c_list.content =  to_decimal(l_artikel.lief_einheit)
                c_list.deliver =  to_decimal(dml_art.geliefert)
                c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                c_list.qty1 =  to_decimal(c_list.qty)
                c_list.price1 =  to_decimal(c_list.price)
                c_list.id = entry(0, dml_art.userinit, ";")
                c_list.dept = curr_dept

                if num_entries(dml_art.chginit, ";") > 1:
                    c_list.cid = entry(0, dml_art.chginit, ";")
                    c_list.dml_nr = entry(1, dml_art.chginit, ";")


                else:
                    c_list.cid = dml_art.chginit

                if num_entries(dml_art.chginit, ";") > 2:
                    c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_art.chginit , ";")))

                if dml_art.chginit != "" and substring(dml_art.chginit, length(dml_art.chginit) - 1) == ("!").lower() :
                    c_list.approved = True
                liefno = 0
                liefno = to_int(entry(1, dml_art.userinit, ";"))

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_art.artnr)],"lager_nr": [(eq, 0)]})

                if l_bestand:
                    c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, dml_art.artnr)],"number3": [(eq, counter)],"date1": [(eq, dml_art.datum)]})

                if queasy:
                    c_list.remark = queasy.char1


                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, dml_art.artnr)],"number3": [(eq, 0)],"date1": [(eq, dml_art.datum)]})

                    if queasy:
                        c_list.remark = queasy.char1

                if liefno != 0:

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                    if l_lieferant:
                        c_list.supplier = l_lieferant.firma
                        c_list.lief_nr = liefno

            l_artikel_obj_list = {}
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_artikel.bestellt)).order_by(L_artikel._recid).all():
                if l_artikel_obj_list.get(l_artikel._recid):
                    continue
                else:
                    l_artikel_obj_list[l_artikel._recid] = True

                c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == l_artikel.artnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_data.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.grp = l_untergrup.bezeich
                    c_list.zwkum = l_untergrup.zwkum
                    c_list.bezeich = l_artikel.bezeich
                    c_list.price =  to_decimal(l_artikel.ek_aktuell) * to_decimal(l_artikel.lief_einheit)
                    c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                    c_list.unit = l_artikel.traubensorte
                    c_list.content =  to_decimal(l_artikel.lief_einheit)
                    c_list.price1 =  to_decimal(c_list.price)
                    c_list.id = user_init
                    c_list.dept = curr_dept

                    l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

                    if l_bestand:
                        c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
        else:

            breslin = db_session.query(Breslin).filter(
                     (Breslin.key == ("DML").lower()) & (Breslin.date1 == selected_date) & (entry(1, Breslin.char3, ";") == (dml_no).lower())).first()

            if breslin:

                reslin_queasy_obj_list = {}
                reslin_queasy = Reslin_queasy()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for reslin_queasy.char1, reslin_queasy.deci2, reslin_queasy.deci1, reslin_queasy.number3, reslin_queasy.char2, reslin_queasy.char3, reslin_queasy.date1, reslin_queasy._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Reslin_queasy.char1, Reslin_queasy.deci2, Reslin_queasy.deci1, Reslin_queasy.number3, Reslin_queasy.char2, Reslin_queasy.char3, Reslin_queasy.date1, Reslin_queasy._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == to_int(entry(0, Reslin_queasy.char1, ";")))).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower())).order_by(Reslin_queasy._recid).all():
                    if reslin_queasy_obj_list.get(reslin_queasy._recid):
                        continue
                    else:
                        reslin_queasy_obj_list[reslin_queasy._recid] = True


                    c_list = C_list()
                    c_list_data.append(c_list)

                    c_list.artnr = to_int(entry(0, reslin_queasy.char1, ";"))
                    c_list.grp = l_untergrup.bezeich
                    c_list.zwkum = l_untergrup.zwkum
                    c_list.bezeich = l_artikel.bezeich
                    c_list.qty =  to_decimal(reslin_queasy.deci2)
                    c_list.price =  to_decimal(reslin_queasy.deci1)
                    c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                    c_list.unit = l_artikel.traubensorte
                    c_list.content =  to_decimal(l_artikel.lief_einheit)
                    c_list.deliver =  to_decimal(reslin_queasy.number3)
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

                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"number2": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))],"number3": [(eq, counter)],"date1": [(eq, reslin_queasy.date1)]})

                    if queasy:
                        c_list.remark = queasy.char1


                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"number2": [(eq, to_int(entry(0, reslin_queasy.char1, ";")))],"number3": [(eq, 0)],"date1": [(eq, reslin_queasy.date1)]})

                        if queasy:
                            c_list.remark = queasy.char1

                    if liefno != 0:

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                        if l_lieferant:
                            c_list.supplier = l_lieferant.firma
                            c_list.lief_nr = liefno

                l_artikel_obj_list = {}
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_artikel.bestellt)).order_by(L_artikel._recid).all():
                    if l_artikel_obj_list.get(l_artikel._recid):
                        continue
                    else:
                        l_artikel_obj_list[l_artikel._recid] = True

                    c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == l_artikel.artnr), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.grp = l_untergrup.bezeich
                        c_list.zwkum = l_untergrup.zwkum
                        c_list.bezeich = l_artikel.bezeich
                        c_list.price =  to_decimal(l_artikel.ek_aktuell) * to_decimal(l_artikel.lief_einheit)
                        c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                        c_list.unit = l_artikel.traubensorte
                        c_list.content =  to_decimal(l_artikel.lief_einheit)
                        c_list.price1 =  to_decimal(c_list.price)
                        c_list.id = user_init
                        c_list.dept = curr_dept

                        l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

                        if l_bestand:
                            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            else:

                dml_artdep_obj_list = {}
                dml_artdep = Dml_artdep()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for dml_artdep.departement, dml_artdep.datum, dml_artdep.anzahl, dml_artdep.einzelpreis, dml_artdep.geliefert, dml_artdep.userinit, dml_artdep.chginit, dml_artdep.artnr, dml_artdep._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Dml_artdep.departement, Dml_artdep.datum, Dml_artdep.anzahl, Dml_artdep.einzelpreis, Dml_artdep.geliefert, Dml_artdep.userinit, Dml_artdep.chginit, Dml_artdep.artnr, Dml_artdep._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == Dml_artdep.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (Dml_artdep.datum == selected_date) & (Dml_artdep.departement == curr_dept)).order_by(Dml_artdep._recid).all():
                    if dml_artdep_obj_list.get(dml_artdep._recid):
                        continue
                    else:
                        dml_artdep_obj_list[dml_artdep._recid] = True


                    fill_dml_nr = "D" + to_string(dml_artdep.departement, "99") + substring(to_string(get_year(dml_artdep.datum)) , 2, 2) + to_string(get_month(dml_artdep.datum) , "99") + to_string(get_day(dml_artdep.datum) , "99")
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
                    c_list.content =  to_decimal(l_artikel.lief_einheit)
                    c_list.deliver =  to_decimal(dml_artdep.geliefert)
                    c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                    c_list.qty1 =  to_decimal(c_list.qty)
                    c_list.price1 =  to_decimal(c_list.price)
                    c_list.id = entry(0, dml_artdep.userinit, ";")
                    c_list.dept = curr_dept

                    if num_entries(dml_artdep.chginit, ";") > 1:
                        c_list.cid = entry(0, dml_artdep.chginit, ";")
                        c_list.dml_nr = entry(1, dml_artdep.chginit, ";")

                    if c_list.dml_nr == "" or c_list.dml_nr == None:
                        c_list.dml_nr = fill_dml_nr + to_string(1, "999")
                    else:
                        c_list.cid = dml_artdep.chginit
                        c_list.dml_nr = fill_dml_nr + to_string(1, "999")

                    if num_entries(dml_artdep.chginit, ";") > 2:
                        c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_artdep.chginit , ";")))

                    if dml_artdep.chginit != "" and substring(dml_artdep.chginit, length(dml_artdep.chginit) - 1) == ("!").lower() :
                        c_list.approved = True
                    liefno = 0
                    liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                    l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_artdep.artnr)],"lager_nr": [(eq, 0)]})

                    if l_bestand:
                        c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"number3": [(eq, counter)],"date1": [(eq, dml_artdep.datum)]})

                    if queasy:
                        c_list.remark = queasy.char1


                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"number3": [(eq, 0)],"date1": [(eq, dml_artdep.datum)]})

                        if queasy:
                            c_list.remark = queasy.char1

                    if liefno != 0:

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, liefno)]})

                        if l_lieferant:
                            c_list.supplier = l_lieferant.firma
                            c_list.lief_nr = liefno

                l_artikel_obj_list = {}
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel.ek_aktuell, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel.ek_aktuell, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_artikel.bestellt)).order_by(L_artikel._recid).all():
                    if l_artikel_obj_list.get(l_artikel._recid):
                        continue
                    else:
                        l_artikel_obj_list[l_artikel._recid] = True

                    c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == l_artikel.artnr), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.grp = l_untergrup.bezeich
                        c_list.zwkum = l_untergrup.zwkum
                        c_list.bezeich = l_artikel.bezeich
                        c_list.price =  to_decimal(l_artikel.ek_aktuell) * to_decimal(l_artikel.lief_einheit)
                        c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                        c_list.unit = l_artikel.traubensorte
                        c_list.content =  to_decimal(l_artikel.lief_einheit)
                        c_list.price1 =  to_decimal(c_list.price)
                        c_list.id = user_init
                        c_list.dept = curr_dept

                        l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

                        if l_bestand:
                            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


    if dml_no == None:
        dml_no = ""

    if dml_no != "" and dml_no != None:
        counter = to_int(substring(dml_no, 10, 2))
    else:
        counter = 1
    modify_dml()

    return generate_output()