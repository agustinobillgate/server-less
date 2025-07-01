#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Dml_art, Dml_artdep, L_artikel, L_untergrup, L_bestand, Queasy

def dml_list_copy_articles_11bl(user_init:string, curr_dept:int, selected_date:date):

    prepare_cache ([Dml_art, Dml_artdep, L_artikel, L_untergrup, L_bestand, Queasy])

    approve_flag = False
    c_list_list = []
    supply_list_list = []
    dml_art = dml_artdep = l_artikel = l_untergrup = l_bestand = queasy = None

    c_list = supply_list = None

    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string})
    supply_list_list, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":string, "telefon":string, "fax":string, "namekontakt":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal approve_flag, c_list_list, supply_list_list, dml_art, dml_artdep, l_artikel, l_untergrup, l_bestand, queasy
        nonlocal user_init, curr_dept, selected_date


        nonlocal c_list, supply_list
        nonlocal c_list_list, supply_list_list

        return {"approve_flag": approve_flag, "c-list": c_list_list, "supply-list": supply_list_list}

    def copy_articles():

        nonlocal approve_flag, c_list_list, supply_list_list, dml_art, dml_artdep, l_artikel, l_untergrup, l_bestand, queasy
        nonlocal user_init, curr_dept, selected_date


        nonlocal c_list, supply_list
        nonlocal c_list_list, supply_list_list

        liefno:int = 0
        d_art = None
        d_art1 = None
        D_art =  create_buffer("D_art",Dml_art)
        D_art1 =  create_buffer("D_art1",Dml_artdep)
        c_list_list.clear()
        supply_list_list.clear()

        if curr_dept == 0:

            dml_art_obj_list = {}
            dml_art = Dml_art()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for dml_art.anzahl, dml_art.einzelpreis, dml_art.userinit, dml_art.artnr, dml_art.datum, dml_art._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Dml_art.anzahl, Dml_art.einzelpreis, Dml_art.userinit, Dml_art.artnr, Dml_art.datum, Dml_art._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == Dml_art.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (Dml_art.datum == (selected_date - timedelta(days=1)))).order_by(Dml_art._recid).all():
                if dml_art_obj_list.get(dml_art._recid):
                    continue
                else:
                    dml_art_obj_list[dml_art._recid] = True


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.grp = l_untergrup.bezeich
                c_list.zwkum = l_untergrup.zwkum
                c_list.bezeich = l_artikel.bezeich
                c_list.qty =  to_decimal(dml_art.anzahl)
                c_list.price =  to_decimal(dml_art.einzelpreis)
                c_list.unit = l_artikel.masseinheit
                c_list.content =  to_decimal(l_artikel.inhalt)
                c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                c_list.qty1 =  to_decimal(c_list.qty)
                c_list.price1 =  to_decimal(c_list.price)
                c_list.id = entry(0, dml_art.userinit, ";")

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_art.artnr)],"lager_nr": [(eq, 0)]})

                if l_bestand:
                    c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, dml_art.artnr)],"date1": [(eq, dml_art.datum)]})

                if queasy:
                    c_list.remark = queasy.char1


                d_art = Dml_art()
                db_session.add(d_art)

                d_art.artnr = dml_art.artnr
                d_art.datum = selected_date
                d_art.userinit = user_init
                d_art.anzahl =  to_decimal(dml_art.anzahl)
                d_art.einzelpreis =  to_decimal(dml_art.einzelpreis)

        else:

            dml_artdep_obj_list = {}
            dml_artdep = Dml_artdep()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for dml_artdep.anzahl, dml_artdep.einzelpreis, dml_artdep.geliefert, dml_artdep.userinit, dml_artdep.artnr, dml_artdep.departement, dml_artdep.datum, dml_artdep._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(Dml_artdep.anzahl, Dml_artdep.einzelpreis, Dml_artdep.geliefert, Dml_artdep.userinit, Dml_artdep.artnr, Dml_artdep.departement, Dml_artdep.datum, Dml_artdep._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == Dml_artdep.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (Dml_artdep.datum == (selected_date - timedelta(days=1))) & (Dml_artdep.departement == curr_dept)).order_by(Dml_artdep._recid).all():
                if dml_artdep_obj_list.get(dml_artdep._recid):
                    continue
                else:
                    dml_artdep_obj_list[dml_artdep._recid] = True


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.grp = l_untergrup.bezeich
                c_list.zwkum = l_untergrup.zwkum
                c_list.bezeich = l_artikel.bezeich
                c_list.qty =  to_decimal(dml_artdep.anzahl)
                c_list.price =  to_decimal(dml_artdep.einzelpreis)
                c_list.unit = l_artikel.masseinheit
                c_list.content =  to_decimal(l_artikel.inhalt)
                c_list.deliver =  to_decimal(dml_artdep.geliefert)
                c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                c_list.qty1 =  to_decimal(c_list.qty)
                c_list.price1 =  to_decimal(c_list.price)
                c_list.id = entry(0, dml_artdep.userinit, ";")
                c_list.dept = curr_dept

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, dml_artdep.artnr)],"lager_nr": [(eq, 0)]})

                if l_bestand:
                    c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"date1": [(eq, dml_artdep.datum)]})

                if queasy:
                    c_list.remark = queasy.char1


                d_art1 = Dml_artdep()
                db_session.add(d_art1)

                d_art1.artnr = dml_artdep.artnr
                d_art1.datum = selected_date
                d_art1.userinit = user_init
                d_art1.anzahl =  to_decimal(dml_artdep.anzahl)
                d_art1.einzelpreis =  to_decimal(dml_artdep.einzelpreis)
                d_art1.departement = curr_dept

        approve_flag = False


    copy_articles()

    return generate_output()