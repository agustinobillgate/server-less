#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 25/7/2025
# gitlab: 
# 
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Guest, Bk_veran, Bk_reser

rml_data, Rml = create_model("Rml", {"nr":int, "raum":string, "bezeich":string, "departement":int, "resnr":[int,48], "reslinnr":[int,48], "gstatus":[int,48], "room":[string,48], "blocked":[int,48]})

def ba_plan_create_dlistbl(rml_data:[Rml], from_date:date):

    prepare_cache ([Bk_raum, Guest, Bk_veran, Bk_reser])

    i:int = 0
    maxpar:int = 0
    bk_raum = guest = bk_veran = bk_reser = None

    rml = rmbuff = childrm = gast = None

    Rmbuff = create_buffer("Rmbuff",Bk_raum)
    Childrm = create_buffer("Childrm",Bk_raum)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, maxpar, bk_raum, guest, bk_veran, bk_reser
        nonlocal from_date
        nonlocal rmbuff, childrm, gast


        nonlocal rml, rmbuff, childrm, gast

        return {"rml": rml_data}

    def create_dlist1(parent_rm:string, curr_rm:string):

        nonlocal maxpar, bk_raum, guest, bk_veran, bk_reser
        nonlocal from_date
        nonlocal rmbuff, childrm, gast


        nonlocal rml, rmbuff, childrm, gast

        i:int = 0
        j:int = 0
        k:int = 0
        l:int = 0
        m:int = 0
        start:int = 0
        finish:int = 0
        gastname:string = ""
        bk_buff = None
        rmbuff = None
        childrm = None
        Bk_buff =  create_buffer("Bk_buff",Bk_reser)
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)

        rml = query(rml_data, filters=(lambda rml: rml.raum.lower()  == (curr_rm).lower()  and rml.nr == bk_reser.resstatus), first=True)

        if rml:

            if gast:
                gastname = gast.name


            else:
                gastname = "Please re-attach guest."

            if bk_veran.bemerkung != "":
                gastname = "*" + gastname
            j = 1

            if bk_reser.datum == bk_reser.bis_datum:
                start = bk_reser.von_i
                finish = bk_reser.bis_i

            elif bk_reser.datum == from_date and bk_reser.bis_datum > from_date:
                start = bk_reser.von_i
                finish = 48

            elif bk_reser.datum < from_date and bk_reser.bis_datum == from_date:
                start = 1
                finish = bk_reser.bis_i

            elif bk_reser.datum < from_date and bk_reser.bis_datum > from_date:
                start = 1
                finish = 48

            if start == 0:
                start = 1

            if finish == 49:
                finish = 48


            for i in range(start,finish + 1) :
                rml.gstatus[i - 1] = bk_reser.resstatus

                if bk_reser.resstatus == 2:
                    rml.gstatus[i - 1] = bk_reser.resstatus

                if bk_reser.resstatus == 3:
                    rml.gstatus[i - 1] = -1
                rml.room[i - 1] = substring(gastname, j - 1, 1)
                rml.resnr[i - 1] = bk_reser.veran_nr
                rml.reslinnr[i - 1] = bk_reser.veran_resnr
                j = j + 1

                if parent_rm.lower()  != (curr_rm).lower() :
                    rml.blocked[i - 1] = 1

            bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

            if bk_raum:

                if bk_raum.vorbereit != 0:
                    k = bk_raum.vorbereit / 30

                    if bk_raum.vorbereit > k * 30:
                        k = k + 1
                    l = start

                    if l - 1 > 0:
                        for m in range(l - k,l - 1 + 1) :

                            if m > 0:

                                if rml.gstatus[m - 1] == 0:
                                    rml.gstatus[m - 1] = 3
                                    rml.resnr[m - 1] = bk_reser.veran_nr
                                    rml.reslinnr[m - 1] = bk_reser.veran_resnr

        for rmbuff in db_session.query(Rmbuff).filter(
                 (entry(0 , rmBuff.lu_raum , ";") == (curr_rm).lower())).order_by(Rmbuff._recid).all():
            create_dlist1(bk_reser.raum, rmBuff.raum)


    def create_dlist2(parent_rm:string, curr_rm:string):

        nonlocal maxpar, bk_raum, guest, bk_veran, bk_reser
        nonlocal from_date
        nonlocal rmbuff, childrm, gast


        nonlocal rml, rmbuff, childrm, gast

        i:int = 0
        j:int = 0
        k:int = 0
        l:int = 0
        m:int = 0
        start:int = 0
        finish:int = 0
        gastname:string = ""
        bk_buff = None
        rmbuff = None
        childrm = None
        Bk_buff =  create_buffer("Bk_buff",Bk_reser)
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)

        rml = query(rml_data, filters=(lambda rml: rml.raum.lower()  == (curr_rm).lower()  and rml.nr == bk_reser.resstatus), first=True)

        if rml:

            if gast:
                gastname = gast.name


            else:
                gastname = "Please re-attach guest."

            if bk_veran.bemerkung != "":
                gastname = "*" + gastname
            j = 1

            if bk_reser.datum == bk_reser.bis_datum:
                start = bk_reser.von_i
                finish = bk_reser.bis_i

            elif bk_reser.datum == from_date and bk_reser.bis_datum > from_date:
                start = bk_reser.von_i
                finish = 48

            elif bk_reser.datum < from_date and bk_reser.bis_datum == from_date:
                start = 1
                finish = bk_reser.bis_i

            elif bk_reser.datum < from_date and bk_reser.bis_datum > from_date:
                start = 1
                finish = 48

            if start == 0:
                start = 1

            if finish == 49:
                finish = 48


            for i in range(start,finish + 1) :
                rml.gstatus[i - 1] = bk_reser.resstatus

                if bk_reser.resstatus == 2:
                    rml.gstatus[i - 1] = bk_reser.resstatus

                if bk_reser.resstatus == 3:
                    rml.gstatus[i - 1] = -1
                rml.room[i - 1] = substring(gastname, j - 1, 1)
                rml.resnr[i - 1] = bk_reser.veran_nr
                rml.reslinnr[i - 1] = bk_reser.veran_resnr
                j = j + 1

                if parent_rm.lower()  != (curr_rm).lower() :
                    rml.blocked[i - 1] = 2

            bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

            if bk_raum:

                if bk_raum.vorbereit != 0:
                    k = bk_raum.vorbereit / 30

                    if bk_raum.vorbereit > k * 30:
                        k = k + 1
                    l = start

                    if l - 1 > 0:
                        for m in range(l - k,l - 1 + 1) :

                            if m > 0:

                                if rml.gstatus[m - 1] == 0:
                                    rml.gstatus[m - 1] = 3
                                    rml.resnr[m - 1] = bk_reser.veran_nr
                                    rml.reslinnr[m - 1] = bk_reser.veran_resnr

        childrm = get_cache (Bk_raum, {"raum": [(eq, curr_rm)]})

        for rmbuff in db_session.query(Rmbuff).filter(
                 (rmBuff.raum == childRM.lu_raum)).order_by(Rmbuff._recid).all():
            create_dlist2(bk_reser.raum, rmBuff.raum)


    bk_reser_obj_list = {}
    bk_reser = Bk_reser()
    bk_veran = Bk_veran()
    for bk_reser.resstatus, bk_reser.bis_datum, bk_reser.von_i, bk_reser.bis_i, bk_reser.veran_nr, bk_reser.veran_resnr, bk_reser.raum, bk_reser.datum, bk_reser._recid, bk_veran.gastnr, bk_veran.bemerkung, bk_veran._recid in db_session.query(Bk_reser.resstatus, Bk_reser.bis_datum, Bk_reser.von_i, Bk_reser.bis_i, Bk_reser.veran_nr, Bk_reser.veran_resnr, Bk_reser.raum, Bk_reser.datum, Bk_reser._recid, Bk_veran.gastnr, Bk_veran.bemerkung, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_reser.veran_nr)).filter(
             ((Bk_reser.datum == from_date) | ((Bk_reser.datum <= from_date) & (Bk_reser.bis_datum >= from_date))) & (Bk_reser.resstatus <= 3)).order_by(Bk_reser._recid).all():
        if bk_reser_obj_list.get(bk_reser._recid):
            continue
        else:
            bk_reser_obj_list[bk_reser._recid] = True

        gast = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})
        create_dlist1(bk_reser.raum, bk_reser.raum)

        childrm = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

        if matches(childRM.lu_raum,r"*;*"):
            maxpar = num_entries(childRM.lu_raum, ";")
            for i in range(1,maxpar + 1) :

                rmbuff = get_cache (Bk_raum, {"raum": [(eq, entry(i - 1, childrm.lu_raum, ";"))]})
                create_dlist2(bk_reser.raum, rmBuff.raum)
        else:

            for rmbuff in db_session.query(Rmbuff).filter(
                     (rmBuff.raum == childRM.lu_raum)).order_by(Rmbuff._recid).all():
                create_dlist2(bk_reser.raum, rmBuff.raum)

    return generate_output()