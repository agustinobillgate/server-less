#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Guest, Bk_veran, Bk_reser

rml_list, Rml = create_model("Rml", {"nr":int, "raum":string, "bezeich":string, "departement":int, "resnr":[int,48], "reslinnr":[int,48], "gstatus":[int,48], "room":[string,48], "blocked":[int,48]})

def ba_plan_create_wlistbl(rml_list:[Rml], from_date:date):

    prepare_cache ([Guest, Bk_reser])

    bk_raum = guest = bk_veran = bk_reser = None

    rml = rmbuff = childrm = gast = None

    Rmbuff = create_buffer("Rmbuff",Bk_raum)
    Childrm = create_buffer("Childrm",Bk_raum)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_raum, guest, bk_veran, bk_reser
        nonlocal from_date
        nonlocal rmbuff, childrm, gast


        nonlocal rml, rmbuff, childrm, gast

        return {"rml": rml_list}

    def create_wlist1(parent_rm:string, curr_rm:string):

        nonlocal bk_raum, guest, bk_veran, bk_reser
        nonlocal from_date
        nonlocal rmbuff, childrm, gast


        nonlocal rml, rmbuff, childrm, gast

        i:int = 0
        j:int = 0
        k:int = 0
        l:int = 0
        from_time:int = 0
        to_time:int = 0
        bk_buff = None
        rmbuff = None
        Bk_buff =  create_buffer("Bk_buff",Bk_reser)
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)

        rml = query(rml_list, filters=(lambda rml: rml.raum.lower()  == (curr_rm).lower()  and rml.nr == bk_reser.resstatus), first=True)
        j = (bk_reser.datum - from_date).days
        k = (bk_reser.bis_datum - from_date).days

        if bk_reser.von_i < 13:
            from_time = (j * 4) + 1

        elif bk_reser.von_i < 25:
            from_time = (j * 4) + 2

        elif bk_reser.von_i < 37:
            from_time = (j * 4) + 3

        elif bk_reser.von_i < 49:
            from_time = (j * 4) + 4

        if bk_reser.datum == bk_reser.bis_datum:

            if bk_reser.bis_i < 13:
                to_time = (j * 4) + 1

            elif bk_reser.bis_i < 25:
                to_time = (j * 4) + 2

            elif bk_reser.bis_i < 37:
                to_time = (j * 4) + 3

            elif bk_reser.bis_i < 49:
                to_time = (j * 4) + 4

        elif bk_reser.bis_datum > bk_reser.datum:

            if bk_reser.bis_i < 13:
                to_time = (k * 4) + 1

            elif bk_reser.bis_i < 25:
                to_time = (k * 4) + 2

            elif bk_reser.bis_i < 37:
                to_time = (k * 4) + 3

            elif bk_reser.bis_i < 49:
                to_time = (k * 4) + 4
        l = 1
        for i in range(from_time,to_time + 1) :
            rml.gstatus[i - 1] = bk_reser.resstatus

            if bk_reser.resstatus == 2:

                bk_buff = get_cache (Bk_reser, {"datum": [(eq, bk_reser.datum)],"resstatus": [(eq, 3)],"raum": [(eq, bk_reser.raum)]})

                if bk_buff:

                    if (i % 4 == 1) and bk_buff.von_i < 13:
                        rml.gstatus[i - 1] = -1

                    elif (i % 4 == 2) and bk_buff.von_i < 25:
                        rml.gstatus[i - 1] = -1

                    elif (i % 4 == 3) and bk_buff.von_i < 31:
                        rml.gstatus[i - 1] = -1

                    elif (i % 4 == 1) and bk_buff.von_i < 37:
                        rml.gstatus[i - 1] = -1
            rml.room[i - 1] = substring(gast.name, l - 1, 1)
            rml.resnr[i - 1] = bk_reser.veran_nr
            rml.reslinnr[i - 1] = bk_reser.veran_resnr
            l = l + 1

            if parent_rm.lower()  != (curr_rm).lower() :
                rml.blocked[i - 1] = 1

        for rmbuff in db_session.query(Rmbuff).filter(
                 (rmBuff.lu_raum == (curr_rm).lower())).order_by(Rmbuff._recid).all():
            create_wlist1(bk_reser.raum, rmBuff.raum)


    def create_wlist2(parent_rm:string, curr_rm:string):

        nonlocal bk_raum, guest, bk_veran, bk_reser
        nonlocal from_date
        nonlocal rmbuff, childrm, gast


        nonlocal rml, rmbuff, childrm, gast

        i:int = 0
        j:int = 0
        k:int = 0
        l:int = 0
        from_time:int = 0
        to_time:int = 0
        bk_buff = None
        rmbuff = None
        childrm = None
        Bk_buff =  create_buffer("Bk_buff",Bk_reser)
        Rmbuff =  create_buffer("Rmbuff",Bk_raum)
        Childrm =  create_buffer("Childrm",Bk_raum)

        rml = query(rml_list, filters=(lambda rml: rml.raum.lower()  == (curr_rm).lower()  and rml.nr == bk_reser.resstatus), first=True)
        j = (bk_reser.datum - from_date).days
        k = (bk_reser.bis_datum - from_date).days

        if bk_reser.von_i < 13:
            from_time = (j * 4) + 1

        elif bk_reser.von_i < 25:
            from_time = (j * 4) + 2

        elif bk_reser.von_i < 37:
            from_time = (j * 4) + 3

        elif bk_reser.von_i < 49:
            from_time = (j * 4) + 4

        if bk_reser.datum == bk_reser.bis_datum:

            if bk_reser.bis_i < 13:
                to_time = (j * 4) + 1

            elif bk_reser.bis_i < 25:
                to_time = (j * 4) + 2

            elif bk_reser.bis_i < 37:
                to_time = (j * 4) + 3

            elif bk_reser.bis_i < 49:
                to_time = (j * 4) + 4

        elif bk_reser.bis_datum > bk_reser.datum:

            if bk_reser.bis_i < 13:
                to_time = (k * 4) + 1

            elif bk_reser.bis_i < 25:
                to_time = (k * 4) + 2

            elif bk_reser.bis_i < 37:
                to_time = (k * 4) + 3

            elif bk_reser.bis_i < 49:
                to_time = (k * 4) + 4
        l = 1
        for i in range(from_time,to_time + 1) :
            rml.gstatus[i - 1] = bk_reser.resstatus

            if bk_reser.resstatus == 2:

                bk_buff = get_cache (Bk_reser, {"datum": [(eq, bk_reser.datum)],"resstatus": [(eq, 3)],"raum": [(eq, bk_reser.raum)]})

                if bk_buff:

                    if (i % 4 == 1) and bk_buff.von_i < 13:
                        rml.gstatus[i - 1] = -1

                    elif (i % 4 == 2) and bk_buff.von_i < 25:
                        rml.gstatus[i - 1] = -1

                    elif (i % 4 == 3) and bk_buff.von_i < 31:
                        rml.gstatus[i - 1] = -1

                    elif (i % 4 == 1) and bk_buff.von_i < 37:
                        rml.gstatus[i - 1] = -1
            rml.room[i - 1] = substring(gast.name, l - 1, 1)
            rml.resnr[i - 1] = bk_reser.veran_nr
            rml.reslinnr[i - 1] = bk_reser.veran_resnr
            l = l + 1

            if parent_rm.lower()  != (curr_rm).lower() :
                rml.blocked[i - 1] = 1

        childrm = db_session.query(Childrm).filter(
                 (childRM.raum == (curr_rm).lower())).first()

        for rmbuff in db_session.query(Rmbuff).filter(
                 (rmBuff.raum == childRM.lu_raum)).order_by(Rmbuff._recid).all():
            create_wlist2(bk_reser.raum, rmBuff.raum)


    bk_reser_obj_list = {}
    for bk_reser, bk_veran, gast in db_session.query(Bk_reser, Bk_veran, Gast).join(Bk_veran,(Bk_veran.veran_nr == Bk_reser.veran_nr)).join(Gast,(Gast.gastnr == Bk_veran.gastnr)).filter(
             ((Bk_reser.datum >= from_date) & (Bk_reser.datum <= from_date + timedelta(days=11))) & (Bk_reser.resstatus <= 2)).order_by(Bk_reser._recid).all():
        if bk_reser_obj_list.get(bk_reser._recid):
            continue
        else:
            bk_reser_obj_list[bk_reser._recid] = True


        create_wlist1(bk_reser.raum, bk_reser.raum)

        childrm = db_session.query(Childrm).filter(
                 (childRM.raum == bk_reser.raum)).first()

        for rmbuff in db_session.query(Rmbuff).filter(
                 (rmBuff.raum == childRM.lu_raum)).order_by(Rmbuff._recid).all():
            create_wlist2(bk_reser.raum, rmBuff.raum)

    return generate_output()