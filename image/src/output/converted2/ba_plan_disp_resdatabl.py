#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Bk_reser, Guest, Bediener, Bk_setup, Bk_rset, Bk_func

def ba_plan_disp_resdatabl(rml_raum:string, t_resnr:int, t_reslinnr:int):

    prepare_cache ([Bk_veran, Bk_reser, Guest, Bediener, Bk_setup, Bk_rset, Bk_func])

    info1 = ""
    info2 = ""
    info3 = ""
    rsl_list = []
    stat:List[string] = ["Fix", "Tentative", "", "WaitingList", "", "", "", "Actual", "Cancel"]
    bk_veran = bk_reser = guest = bediener = bk_setup = bk_rset = bk_func = None

    rsl = mainres = resline = gast = bbuff = None

    rsl_list, Rsl = create_model("Rsl", {"resnr":int, "reslinnr":int, "resstatus":int, "sdate":date, "ndate":date, "stime":string, "ntime":string, "created_date":date, "venue":string, "userinit":string})

    Mainres = create_buffer("Mainres",Bk_veran)
    Resline = create_buffer("Resline",Bk_reser)
    Gast = create_buffer("Gast",Guest)
    Bbuff = create_buffer("Bbuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal info1, info2, info3, rsl_list, stat, bk_veran, bk_reser, guest, bediener, bk_setup, bk_rset, bk_func
        nonlocal rml_raum, t_resnr, t_reslinnr
        nonlocal mainres, resline, gast, bbuff


        nonlocal rsl, mainres, resline, gast, bbuff
        nonlocal rsl_list

        return {"info1": info1, "info2": info2, "info3": info3, "rsl": rsl_list}

    bk_rset_obj_list = {}
    bk_rset = Bk_rset()
    bk_setup = Bk_setup()
    for bk_rset.groesse, bk_rset.personen, bk_rset.preis, bk_rset._recid, bk_setup.bezeichnung, bk_setup._recid in db_session.query(Bk_rset.groesse, Bk_rset.personen, Bk_rset.preis, Bk_rset._recid, Bk_setup.bezeichnung, Bk_setup._recid).join(Bk_setup,(Bk_setup.setup_id == Bk_rset.setup_id)).filter(
             (Bk_rset.raum == (rml_raum).lower())).order_by(Bk_rset._recid).all():
        if bk_rset_obj_list.get(bk_rset._recid):
            continue
        else:
            bk_rset_obj_list[bk_rset._recid] = True


        info1 = info1 + bk_setup.bezeich + ": Sz: " + to_string(bk_rset.groesse) + " Cp: " + to_string(bk_rset.personen) + " P:" + to_string(bk_rset.preis, ">>>,>>>,>>9.99") + chr_unicode(10)

    mainres = get_cache (Bk_veran, {"veran_nr": [(eq, t_resnr)]})

    if mainres:

        resline = get_cache (Bk_reser, {"veran_nr": [(eq, mainres.veran_nr)],"veran_resnr": [(eq, t_reslinnr)]})

        gast = get_cache (Guest, {"gastnr": [(eq, mainres.gastnr)]})

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, t_resnr)],"veran_seite": [(eq, t_reslinnr)]})
        info3 = gast.name + " " + gast.vorname1 + ", " + gast.anrede1 + gast.anredefirma + chr_unicode(10) + "RefNo: " + to_string(resline.veran_nr) + "-" + to_string(resline.veran_resnr) + " Status: " + stat[resline.resstatus - 1] + " InvNo: " + to_string(mainres.rechnr) + chr_unicode(10) + "Date: " + to_string(resline.datum) + " - " + to_string(resline.bis_datum) + " Time: " + to_string(resline.von_zeit, "99:99") + " - " + to_string(resline.bis_zeit, "99:99") + chr_unicode(10) + "Weekday: " + to_string(bk_func.wochentag) + " Total Pax: " + to_string(bk_func.rpersonen[0])

        if bk_func.raumbezeichnung[7] != "":
            info3 = info3 + chr_unicode(10) + "Event: " + to_string(bk_func.raumbezeichnung[7])

    for resline in db_session.query(Resline).filter(
             (Resline.veran_nr == mainres.veran_nr) & ((Resline.resstatus <= 4) | (Resline.resstatus == 8))).order_by(Resline._recid).all():

        bbuff = get_cache (Bediener, {"nr": [(eq, resline.bediener_nr)]})
        rsl = Rsl()
        rsl_list.append(rsl)

        rsl.resnr = resline.veran_nr
        rsl.reslinnr = resline.veran_resnr
        rsl.resstatus = resline.resstatus
        rsl.sdate = resline.datum
        rsl.ndate = resline.bis_datum
        rsl.stime = resline.von_zeit
        rsl.ntime = resline.bis_zeit
        rsl.venue = resline.raum
        rsl.created_date = mainres.kontaktfirst

        if bbuff:
            rsl.userinit = bbuff.userinit

    return generate_output()