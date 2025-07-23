#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 22/7/2025
# gitlab: 586
# kk=int(k)
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Bk_veran, Bk_reser, Bk_raum

rml_data, Rml = create_model("Rml", {"nr":int, "raum":string, "bezeich":string, "departement":int, "resnr":[int,48], "reslinnr":[int,48], "gstatus":[int,48], "room":[string,48], "blocked":[int,48]})

def ba_plan_create_dlist_prevbl(rml_data:[Rml], from_date:date):

    prepare_cache ([Guest, Bk_veran, Bk_reser, Bk_raum])

    guest = bk_veran = bk_reser = bk_raum = None

    rml = gast = None

    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest, bk_veran, bk_reser, bk_raum
        nonlocal from_date
        nonlocal gast


        nonlocal rml, gast

        return {"rml": rml_data}

    def create_dlist1_prev(parent_rm:string, curr_rm:string):

        nonlocal guest, bk_veran, bk_reser, bk_raum
        nonlocal from_date
        nonlocal gast


        nonlocal rml, gast

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

        rml = query(rml_data, filters=(lambda rml: rml.raum.lower()  == (curr_rm).lower()  and rml.nr == 1), first=True)
        
        # Rd 23/7/2025
        if rml is None:
            return generate_output()
        
        gastname = gast.name

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

            if i > 0 and i < 49:
                rml.gstatus[i - 1] = bk_reser.resstatus

                if bk_reser.resstatus == 8:

                    bk_buff = db_session.query(Bk_buff).filter(
                             ((Bk_buff.datum == from_date) | ((Bk_buff.datum <= from_date) & (Bk_buff.bis_datum >= from_date))) & (Bk_buff.resstatus == 8) & (Bk_buff.raum == bk_reser.raum) & (i <= Bk_buff.bis_i) & (i >= Bk_buff.von_i)).first()

                    if bk_buff:
                        rml.gstatus[i - 1] = 8
                    else:
                        rml.gstatus[i - 1] = bk_reser.resstatus
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
                    # Rd, 22/7/2025
                    # int(k)
                    kk = int(k)
                    for m in range(l - kk,l - 1 + 1) :

                        if m > 0:

                            if rml.gstatus[m - 1] == 0:
                                rml.gstatus[m - 1] = 8
                                rml.resnr[m - 1] = bk_reser.veran_nr
                                rml.reslinnr[m - 1] = bk_reser.veran_resnr


    bk_reser_obj_list = {}
    bk_reser = Bk_reser()
    bk_veran = Bk_veran()
    gast = Guest()
    for bk_reser.bis_datum, bk_reser.von_i, bk_reser.bis_i, bk_reser.resstatus, bk_reser.raum, bk_reser.veran_nr, bk_reser.veran_resnr, bk_reser.datum, bk_reser._recid, bk_veran.bemerkung, bk_veran._recid, gast.name, gast._recid in db_session.query(Bk_reser.bis_datum, Bk_reser.von_i, Bk_reser.bis_i, Bk_reser.resstatus, Bk_reser.raum, Bk_reser.veran_nr, Bk_reser.veran_resnr, Bk_reser.datum, Bk_reser._recid, Bk_veran.bemerkung, Bk_veran._recid, Gast.name, Gast._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_reser.veran_nr)).join(Gast,(Gast.gastnr == Bk_veran.gastnr)).filter(
             ((Bk_reser.datum == from_date) | ((Bk_reser.datum <= from_date) & (Bk_reser.bis_datum >= from_date))) & (Bk_reser.resstatus <= 8)).order_by(Bk_reser._recid).all():
        if bk_reser_obj_list.get(bk_reser._recid):
            continue
        else:
            bk_reser_obj_list[bk_reser._recid] = True


        create_dlist1_prev(bk_reser.raum, bk_reser.raum)

    return generate_output()