#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_veran

glist_list, Glist = create_model("Glist", {"gastnr":int, "karteityp":int, "name":string, "telefon":string, "land":string, "plz":string, "wohnort":string, "adresse1":string, "adresse2":string, "adresse3":string, "namekontakt":string, "von_datum":date, "bis_datum":date, "von_zeit":string, "bis_zeit":string, "rstatus":int, "fax":string, "firmen_nr":int})

def main_fs_display_browser1bl(glist_list:[Glist], b1_resnr:int, b1_resline:int, search_str:string, curr_gastnr:int, guestsort:int, rsvsort:int, to_name:string):

    prepare_cache ([Bk_reser, Bk_veran])

    op_flag = 0
    ol_list = []
    bk_reser = bk_veran = None

    glist = ol = None

    ol_list, Ol = create_model("Ol", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal op_flag, ol_list, bk_reser, bk_veran
        nonlocal b1_resnr, b1_resline, search_str, curr_gastnr, guestsort, rsvsort, to_name


        nonlocal glist, ol
        nonlocal ol_list

        return {"op_flag": op_flag, "ol": ol_list}

    ol_list.clear()

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, b1_resnr)],"veran_resnr": [(eq, b1_resline)]})

    if b1_resnr != 0:

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, b1_resnr)]})

        glist = query(glist_list, filters=(lambda glist: glist.gastnr == bk_veran.gastnr), first=True)
        ol = Ol()
        ol_list.append(ol)

        ol.str = to_string(glist.name, "x(40)") + to_string(glist.telefon, "x(15)") + to_string(bk_reser.datum, "99/99/9999") + to_string(bk_reser.bis_datum, "99/99/9999") + to_string(bk_reser.von_zeit, "99:99") + to_string(bk_reser.bis_zeit, "99:99")
        op_flag = 1

        return generate_output()

    if search_str == "" and curr_gastnr == 0:

        if guestsort < 3:

            for glist in query(glist_list, filters=(lambda glist: glist.karteityp == guestsort), sort_by=[("name",False)]):

                for bk_veran in db_session.query(Bk_veran).filter(
                         (Bk_veran.gastnr == glist.gastnr) & (Bk_veran.activeflag == 0)).order_by(Bk_veran._recid).all():

                    for bk_reser in db_session.query(Bk_reser).filter(
                             (Bk_reser.veran_nr == bk_veran.veran_nr) & (Bk_reser.resstatus == rsvsort)).order_by(Bk_reser._recid).all():
                        ol = Ol()
                        ol_list.append(ol)

                        ol.str = to_string(glist.name, "x(40)") + to_string(glist.telefon, "x(15)") + to_string(bk_reser.datum, "99/99/9999") + to_string(bk_reser.bis_datum, "99/99/9999") + to_string(bk_reser.von_zeit, "99:99") + to_string(bk_reser.bis_zeit, "99:99")
        op_flag = 2

    elif search_str != "" and curr_gastnr == 0:

        for glist in query(glist_list, filters=(lambda glist: glist.karteityp == guestsort and glist.name.lower()  >= (search_str).lower()  and glist.name.lower()  <= (to_name).lower()), sort_by=[("name",False)]):

            for bk_veran in db_session.query(Bk_veran).filter(
                     (Bk_veran.gastnr == glist.gastnr) & (Bk_veran.activeflag == 0)).order_by(Bk_veran._recid).all():

                for bk_reser in db_session.query(Bk_reser).filter(
                         (Bk_reser.veran_nr == bk_veran.veran_nr) & (Bk_reser.resstatus == rsvsort)).order_by(Bk_reser._recid).all():
                    ol = Ol()
                    ol_list.append(ol)

                    ol.str = to_string(glist.name, "x(40)") + to_string(glist.telefon, "x(15)") + to_string(bk_reser.datum, "99/99/9999") + to_string(bk_reser.bis_datum, "99/99/9999") + to_string(bk_reser.von_zeit, "99:99") + to_string(bk_reser.bis_zeit, "99:99")
        op_flag = 3

    elif curr_gastnr != 0:

        for glist in query(glist_list, filters=(lambda glist: glist.karteityp == guestsort and glist.gastnr >= curr_gastnr), sort_by=[("name",False)]):

            for bk_veran in db_session.query(Bk_veran).filter(
                     (Bk_veran.gastnr == glist.gastnr) & (Bk_veran.activeflag == 0)).order_by(Bk_veran._recid).all():

                for bk_reser in db_session.query(Bk_reser).filter(
                         (Bk_reser.veran_nr == bk_veran.veran_nr) & (Bk_reser.resstatus == rsvsort)).order_by(Bk_reser._recid).all():
                    ol = Ol()
                    ol_list.append(ol)

                    ol.str = to_string(glist.name, "x(40)") + to_string(glist.telefon, "x(15)") + to_string(bk_reser.datum, "99/99/9999") + to_string(bk_reser.bis_datum, "99/99/9999") + to_string(bk_reser.von_zeit, "99:99") + to_string(bk_reser.bis_zeit, "99:99")
        op_flag = 4

    return generate_output()