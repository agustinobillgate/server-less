from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Kontline, Bediener, Guest, Zimkateg, Guest_pr, Res_line, Reservation, Queasy

def allotm_reviewbl(pvilanguage:int, from_name:str, to_name:str, from_date:date, to_date:date, resflag:bool, gflag:bool, cflag:bool, detailflag:bool, curr_rmtype:str):
    output_list_list = []
    lvcarea:str = "allotm-review"
    kontline = bediener = guest = zimkateg = guest_pr = res_line = reservation = queasy = None

    k_list = res_list = output_list = allot_list = usr = None

    k_list_list, K_list = create_model("K_list", {"gastnr":int, "bediener_nr":int, "kontcode":str, "global_flag":bool, "global_str":str, "ankunft":date, "zikatnr":int, "argt":str, "zimmeranz":[int,31], "erwachs":int, "kind1":int, "ruecktage":int, "overbooking":int, "abreise":date, "useridanlage":str, "resdate":date, "bemerk":str}, {"global_str": ""})
    res_list_list, Res_list = create_model("Res_list", {"resno":int, "reslinnr":int, "flag":str, "count":int, "s1":str})
    output_list_list, Output_list = create_model("Output_list", {"reihe":int, "resno":int, "reslinnr":int, "str":str})
    allot_list_list, Allot_list = create_model_like(Kontline)

    Usr = create_buffer("Usr",Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, lvcarea, kontline, bediener, guest, zimkateg, guest_pr, res_line, reservation, queasy
        nonlocal pvilanguage, from_name, to_name, from_date, to_date, resflag, gflag, cflag, detailflag, curr_rmtype
        nonlocal usr


        nonlocal k_list, res_list, output_list, allot_list, usr
        nonlocal k_list_list, res_list_list, output_list_list, allot_list_list
        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, lvcarea, kontline, bediener, guest, zimkateg, guest_pr, res_line, reservation, queasy
        nonlocal pvilanguage, from_name, to_name, from_date, to_date, resflag, gflag, cflag, detailflag, curr_rmtype
        nonlocal usr


        nonlocal k_list, res_list, output_list, allot_list, usr
        nonlocal k_list_list, res_list_list, output_list_list, allot_list_list

        curr_reihe:int = 0
        i:int = 0
        datum:date = None
        ci_date:date = None
        count:int = 0
        anz1:List[int] = create_empty_list(31,0)
        anz2:List[int] = create_empty_list(31,0)
        t_anz0:List[int] = create_empty_list(31,0)
        t_anz1:List[int] = create_empty_list(31,0)
        t_anz2:List[int] = create_empty_list(31,0)
        avail_allotm:List[int] = create_empty_list(31,0)
        totavail_allotm:List[int] = create_empty_list(31,0)
        overbook:List[int] = create_empty_list(31,0)
        wday:List[str] = ["SU", "MO", "TU", "WE", "TH", "FR", "SA", "SU"]
        ci_date = get_output(htpdate(87))
        for i in range(1,31 + 1) :
            t_anz0[i - 1] = 0
            t_anz1[i - 1] = 0
            t_anz2[i - 1] = 0
            avail_allotm[i - 1] = 0
            totavail_allotm[i - 1] = 0
            overbook[i - 1] = 0
        curr_reihe = 0

        if from_name == "" and to_name.lower()  == ("zz").lower() :
            create_alllist()
        else:
            create_alist()

        if not detailflag:
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = translateExtended ("Dates :", lvcarea, "") + " " + to_string(from_date) + " - " +\
                    to_string(to_date)


            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = " "


            datum = from_date
            while datum <= to_date:
                str = str + to_string(get_day(datum) , "99 ")
                datum = datum + timedelta(days=1)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = " "


            datum = from_date
            while datum <= to_date:
                str = str + wday[get_weekday(datum) - 1] + " "
                datum = datum + timedelta(days=1)

        guest_obj_list = []
        for guest, usr in db_session.query(Guest, Usr).join(Usr,(Usr.nr == k_list.bediener_nr)).filter(
                 ((Guest.gastnr.in_(list(set([k_list.gastnr for k_list in k_list_list)]))))).order_by(Guest.name, k_list.ankunft).all():
            if guest._recid in guest_obj_list:
                continue
            else:
                guest_obj_list.append(guest._recid)

            k_list = query(k_list_list, (lambda k_list: (guest.gastnr == k_list.gastnr)), first=True)

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == k_list.zikatnr)).first()
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = translateExtended ("Company Name :", lvcarea, "") + " " + guest.name + ", " + guest.anredefirma

            if not detailflag:
                output_list.str = output_list.str + "; " + translateExtended ("Code:", lvcarea, "") + " " + k_list.kontcode

                if zimkateg:
                    str = str + "; " + translateExtended ("RmType:", lvcarea, "") + " " + zimkateg.kurzbez

                if k_list.argt != "":
                    str = str + "; " + translateExtended ("Arg:", lvcarea, "") + " " + k_list.argt

                if k_list.erwachs > 0:
                    str = str + "; " + translateExtended ("Pax:", lvcarea, "") + " " + to_string(k_list.erwachs)
            else:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = translateExtended ("Address :", lvcarea, "") + " " + guest.adresse1 + " " + guest.adresse2


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = translateExtended ("City :", lvcarea, "") + " " + guest.wohnort + " " + guest.plz


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = translateExtended ("Allotm Code :", lvcarea, "") + " " + k_list.kontcode

                if k_list.global_flag:
                    output_list.str = output_list.str + "[*]"
                output_list.str = output_list.str + " " + translateExtended ("RateCode :", lvcarea, "") + " "

                for guest_pr in db_session.query(Guest_pr).filter(
                         (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr._recid).all():
                    str = str + guest_pr.code + "; "
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe


                str = to_string(translateExtended ("Start ", lvcarea, "") , "x(8)") + to_string(k_list.ankunft) + " Pax " + to_string(k_list.erwachs) + "/" + to_string(k_list.kind1) + " " + translateExtended ("ConfirmDays:", lvcarea, "") + " "
                str = str + to_string(k_list.ruecktage) + " " + translateExtended ("Overbooking:", lvcarea, "") + " " + to_string(k_list.overbooking)
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = to_string(translateExtended ("Ending", lvcarea, "") , "x(8)") + to_string(k_list.abreise) + " RmCat "

                if zimkateg:
                    str = str + to_string(zimkateg.kurzbez, "x(6)")
                else:
                    str = str + " "
                str = str + " " + translateExtended ("Arg", lvcarea, "") + " " + to_string(k_list.argt, "x(5)") + " " + translateExtended ("ID", lvcarea, "") + " " + to_string(usr.userinit) + " " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(k_list.useridanlage, "x(2)") + " " + translateExtended ("Date", lvcarea, "") + " " + to_string(k_list.resdat)

                if k_list.bemerk != "":
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_reihe = curr_reihe + 1
                    output_list.reihe = curr_reihe
                    output_list.str = translateExtended ("Comment :", lvcarea, "") + " " + k_list.bemerk


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = translateExtended ("Dates :", lvcarea, "") + " " + to_string(from_date) + " - " +\
                        to_string(to_date)


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = " "


                datum = from_date
                while datum <= to_date:
                    str = str + to_string(get_day(datum) , "99 ")
                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = " "


                datum = from_date
                while datum <= to_date:
                    str = str + wday[get_weekday(datum) - 1] + " "
                    datum = datum + timedelta(days=1)
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe


                for i in range(1,109 + 1) :
                    str = str + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = to_string(translateExtended ("Allotment Room", lvcarea, "") , "x(16)")


            datum = from_date
            i = 1
            while datum <= to_date:

                if datum >= k_list.ankunft and datum < k_list.abreise and datum >= (ci_date):
                    t_anz0[i - 1] = t_anz0[i - 1] + k_list.zimmeranz[i - 1]
                    str = str + to_string(k_list.zimmeranz[i - 1], "-99")
                else:
                    str = str + " 00"
                i = i + 1
                datum = datum + timedelta(days=1)
            for i in range(1,31 + 1) :
                anz1[i - 1] = 0
                anz2[i - 1] = 0
            count = 0

            res_line_obj_list = []
            for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == k_list.kontcode) & (Kontline.kontstatus == 1)).filter(
                     (Res_line.kontignr > 0) & (Res_line.gastnr == k_list.gastnr) & (Res_line.active_flag < 2) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < from_date)) & (Res_line.resstatus < 11) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft, Res_line.abreise, Res_line.resnr).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                if resflag and res_line.active_flag == 0:
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.flag = "r"
                    count = count + 1
                    res_list.count = count
                    res_list.resno = res_line.resnr
                    res_list.reslinnr = res_line.reslinnr
                    s1 = " " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") +\
                            " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) +\
                            " " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + " Pax " +\
                            to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) +\
                            " " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) +\
                            " " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + " ChgID " +\
                            to_string(res_line.changed_id, "x(2)")


                    res_list.s1 = to_string(reservation.name, "x(22)") + " " + res_list.s1

                    if res_line.bemerk != "":
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        count = count + 1
                        res_list.flag = "r"
                        s1 = translateExtended ("Comment :", lvcarea, "") + " " + res_line.bemerk

                if gflag and res_line.active_flag == 2:
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.resno = res_line.resnr
                    res_list.reslinnr = res_line.reslinnr
                    res_list.flag = "g"
                    count = count + 1
                    res_list.count = count
                    s1 = " " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") +\
                            " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) +\
                            " " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + " Pax " +\
                            to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) +\
                            " " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) +\
                            " " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + " ChgID " +\
                            to_string(res_line.changed_id, "x(2)")

                    if res_line.bemerk != "":
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        count = count + 1
                        res_list.flag = "g"
                        s1 = translateExtended ("Comment :", lvcarea, "") + " " + res_line.bemerk
                datum = from_date
                i = 1
                while datum <= to_date:

                    if datum >= res_line.ankunft and datum < res_line.abreise:
                        anz1[i - 1] = anz1[i - 1] + res_line.zimmeranz
                    i = i + 1
                    datum = datum + timedelta(days=1)
            datum = from_date
            i = 1
            while datum <= to_date:
                anz2[i - 1] = k_list.zimmeranz[i - 1] - anz1[i - 1]
                i = i + 1
                datum = datum + timedelta(days=1)
            i = 1
            datum = from_date
            while datum <= to_date:
                t_anz1[i - 1] = t_anz1[i - 1] + anz1[i - 1]
                t_anz2[i - 1] = t_anz2[i - 1] + anz2[i - 1]
                i = i + 1
                datum = datum + timedelta(days=1)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = to_string(translateExtended ("Used Allotment", lvcarea, "") , "x(16)")


            datum = from_date
            i = 1
            while datum <= to_date:
                str = str + to_string(anz1[i - 1], "-99")
                i = i + 1
                datum = datum + timedelta(days=1)

            if detailflag:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = to_string(translateExtended ("Not used :", lvcarea, "") , "x(16)")


                datum = from_date
                i = 1
                while datum <= to_date:

                    if anz2[i - 1] > 0:
                        str = str + to_string(anz2[i - 1], "-99")
                    else:
                        str = str + " 00"
                    i = i + 1
                    datum = datum + timedelta(days=1)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = to_string(translateExtended ("Available :", lvcarea, "") , "x(16)")


            datum = from_date
            i = 1
            while datum <= to_date:

                if datum >= (ci_date + timedelta(days=k_list.ruecktage)):

                    if anz2[i - 1] > 0:
                        avail_allotm[i - 1] = anz2[i - 1]
                        totavail_allotm[i - 1] = totavail_allotm[i - 1] + anz2[i - 1]
                        str = str + to_string(avail_allotm[i - 1], "-99")
                    else:
                        avail_allotm[i - 1] = 0
                        str = str + " 00"
                else:
                    avail_allotm[i - 1] = 0
                    str = str + " 00"
                i = i + 1
                datum = datum + timedelta(days=1)

            if detailflag:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = to_string(translateExtended ("Overbooking :", lvcarea, "") , "x(16)")


                datum = from_date
                i = 1
                while datum <= to_date:

                    if datum >= (ci_date + timedelta(days=k_list.ruecktage)):

                        if anz2[i - 1] < 0:
                            overbook[i - 1] = - anz2[i - 1]
                            str = str + to_string(overbook[i - 1], "-99")
                        else:
                            overbook[i - 1] = 0
                            str = str + " 00"
                    else:
                        overbook[i - 1] = 0
                        str = str + " 00"
                    i = i + 1
                    datum = datum + timedelta(days=1)

            if resflag:
                i = 1
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = "Reservations:"

                for res_list in query(res_list_list, filters=(lambda res_list: res_list.flag.lower()  == ("r").lower()), sort_by=[("count",False)]):

                    if i > 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        curr_reihe = curr_reihe + 1
                        output_list.reihe = curr_reihe
                        output_list.resno = res_list.resNo
                        output_list.reslinnr = res_list.reslinnr
                        output_list.str = " " + res_list.s1


                    else:
                        output_list.resno = res_list.resNo
                        output_list.reslinnr = res_list.reslinnr
                        output_list.str = output_list.str + res_list.s1


                    i = i + 1

            if gflag:
                i = 1
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = "Residents :"

                for res_list in query(res_list_list, filters=(lambda res_list: res_list.flag.lower()  == ("g").lower()), sort_by=[("count",False)]):

                    if i > 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        curr_reihe = curr_reihe + 1
                        output_list.reihe = curr_reihe
                        output_list.resno = res_list.resNo
                        output_list.reslinnr = res_list.reslinnr
                        output_list.str = " " + res_list.s1


                    else:
                        curr_reihe = curr_reihe + 1
                        output_list.reihe = curr_reihe
                        output_list.resno = res_list.resNo
                        output_list.reslinnr = res_list.reslinnr
                        output_list.str = output_list.str + res_list.s1


                    i = i + 1

            if cflag:

                res_line_obj_list = []
                for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == Res_line.kontignr) & (Kontline.kontcode == k_list.kontcode) & (Kontline.kontstatus == 1)).filter(
                         (Res_line.kontignr > 0) & (Res_line.resstatus == 9) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft, Res_line.abreise, Res_line.resnr).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.flag = "c"
                    count = count + 1
                    res_list.count = count
                    res_list.resno = - res_line.resnr
                    res_list.reslinnr = res_line.reslinnr
                    s1 = " " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") +\
                            " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) +\
                            " " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + " Pax " +\
                            to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) +\
                            " " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) +\
                            " " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + " ChgID " +\
                            to_string(res_line.changed_id, "x(2)")


                    res_list.s1 = to_string(reservation.name, "x(22)") + " " + res_list.s1

                    if res_line.bemerk != "":
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        count = count + 1
                        res_list.flag = "r"
                        s1 = translateExtended ("Comment :", lvcarea, "") + " " + res_line.bemerk
                i = 1
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe
                output_list.str = translateExtended ("Cancelled :", lvcarea, "")

                for res_list in query(res_list_list, filters=(lambda res_list: res_list.flag.lower()  == ("c").lower()), sort_by=[("count",False)]):

                    if i > 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        curr_reihe = curr_reihe + 1
                        output_list.reihe = curr_reihe
                        output_list.resno = res_list.resNo
                        output_list.reslinnr = res_list.reslinnr
                        output_list.str = " " + res_list.s1


                    else:
                        output_list.resno = res_list.resNo
                        output_list.reslinnr = res_list.reslinnr
                        output_list.str = output_list.str + res_list.s1


                    i = i + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            for i in range(1,109 + 1) :
                str = str + "="

            if detailflag:
                output_list = Output_list()
                output_list_list.append(output_list)

                curr_reihe = curr_reihe + 1
                output_list.reihe = curr_reihe


        count = 2
        for i in range(1,31 + 1) :

            if t_anz0[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Total Allotm", lvcarea, "") , "x(12)") + to_string(t_anz0[i - 1], "->>>>9")
                else:
                    str = str + to_string(t_anz0[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 2
            datum = from_date + timedelta(days=1)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = " "


            while datum <= to_date:
                str = str + to_string(t_anz0[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Total Allotm", lvcarea, "") , "x(16)") + to_string(t_anz0[i - 1], "->9")
                else:
                    str = str + to_string(t_anz0[i - 1], "->9")
                i = i + 1
                datum = datum + timedelta(days=1)
        count = 2
        for i in range(1,31 + 1) :

            if t_anz1[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Used Allotm", lvcarea, "") , "x(16)") + to_string(t_anz1[i - 1], "->>>>9")
                else:
                    str = str + to_string(t_anz1[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 2
            datum = from_date + timedelta(days=1)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = " "


            while datum <= to_date:
                str = str + to_string(t_anz1[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Used Allotm :", lvcarea, "") , "x(16)") + to_string(t_anz1[i - 1], "->9")
                else:
                    str = str + to_string(t_anz1[i - 1], "->9")
                i = i + 1
                datum = datum + timedelta(days=1)
        count = 2
        for i in range(1,31 + 1) :

            if t_anz2[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if t_anz2[i - 1] > 0:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used :", lvcarea, "") , "x(16)") + to_string(t_anz2[i - 1], "->>>>9")
                    else:
                        str = str + to_string(t_anz2[i - 1], "->>>>9")
                else:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used :", lvcarea, "") , "x(16)") + to_string(0, "->>>>9")
                    else:
                        str = str + to_string(0, "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 2
            datum = from_date + timedelta(days=1)
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe
            output_list.str = " "


            while datum <= to_date:
                str = str + to_string(t_anz2[i - 1], "->>>>9")
                i = i + 2
                datum = datum + timedelta(days=2)
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Avail Allotm :", lvcarea, "") , "x(15)") + to_string(totavail_allotm[i - 1], "->9")
                else:
                    str = str + to_string(totavail_allotm[i - 1], "->9")
                i = i + 1
                datum = datum + timedelta(days=1)
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if t_anz2[i - 1] > 0:

                    if i <= 1:
                        str = to_string(translateExtended ("Not used :", lvcarea, "") , "x(16)") + to_string(t_anz2[i - 1], "->9")
                    else:
                        str = str + to_string(t_anz2[i - 1], "->9")
                else:
                    str = str + to_string(0, "->9")
                i = i + 1
                datum = datum + timedelta(days=1)
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            curr_reihe = curr_reihe + 1
            output_list.reihe = curr_reihe


            while datum <= to_date:

                if i <= 1:
                    str = to_string(translateExtended ("Avail Allotm :", lvcarea, "") , "x(16)") + to_string(totavail_allotm[i - 1], "->9")
                else:
                    str = str + to_string(totavail_allotm[i - 1], "->9")
                i = i + 1
                datum = datum + timedelta(days=1)


    def create_alllist():

        nonlocal output_list_list, lvcarea, kontline, bediener, guest, zimkateg, guest_pr, res_line, reservation, queasy
        nonlocal pvilanguage, from_name, to_name, from_date, to_date, resflag, gflag, cflag, detailflag, curr_rmtype
        nonlocal usr


        nonlocal k_list, res_list, output_list, allot_list, usr
        nonlocal k_list_list, res_list_list, output_list_list, allot_list_list

        curr_code:str = ""
        d:date = None
        d1:date = None
        d2:date = None
        i:int = 0
        do_it:bool = False

        kontline_obj_list = []
        for kontline, guest, usr in db_session.query(Kontline, Guest, Usr).join(Guest,(Guest.gastnr == Kontline.gastnr)).join(Usr,(Usr.nr == Kontline.bediener_nr)).filter(
                 (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1) & (not_ (Kontline.ankunft > to_date)) & (not_ (Kontline.abreise < from_date))).order_by(Guest.name, Kontline.kontcode, Kontline.ankunft).all():
            if kontline._recid in kontline_obj_list:
                continue
            else:
                kontline_obj_list.append(kontline._recid)


            do_it = True

            if re.match(r".*-ALL-.*",curr_rmtype, re.IGNORECASE):
                pass

            elif kontline.zikatnr == 0:
                pass
            else:

                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.kurzbez == curr_rmtype)).first()
                do_it = kontline.zikatnr == zimkateg.zikatnr

            if do_it:

                if curr_code != kontline.kontcode:
                    curr_code = kontline.kontcode
                    k_list = K_list()
                    k_list_list.append(k_list)

                    k_list.gastnr = guest.gastnr
                    k_list.bediener_nr = usr.nr
                    k_list.kontcode = curr_code
                    k_list.ankunft = kontline.ankunft
                    k_list.zikatnr = kontline.zikatnr
                    k_list.argt = kontline.arrangement
                    k_list.erwachs = kontline.erwachs
                    k_list.kind1 = kontline.kind1
                    k_list.ruecktage = kontline.ruecktage
                    k_list.overbooking = kontline.overbooking
                    k_list.abreise = kontline.abreise
                    k_list.useridanlage = kontline.useridanlage
                    k_list.resdat = kontline.resdat
                    k_list.bemerk = kontline.bemerk

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 147) & (Queasy.number1 == kontline.gastnr) & (Queasy.char1 == kontline.kontcode)).first()

                    if queasy:
                        k_list.global_flag = True
                        k_list.global_str = queasy.char3


                else:
                    k_list.abreise = kontline.abreise

                if from_date > kontline.ankunft:
                    d1 = from_date
                else:
                    d1 = kontline.ankunft

                if to_date < kontline.abreise:
                    d2 = to_date
                else:
                    d2 = kontline.abreise
                i = d1 - from_date
                for d in date_range(d1,d2) :
                    i = i + 1

                    if d >= kontline.ankunft and d <= kontline.abreise:
                        k_list.zimmeranz[i - 1] = kontline.zimmeranz


    def create_alist():

        nonlocal output_list_list, lvcarea, kontline, bediener, guest, zimkateg, guest_pr, res_line, reservation, queasy
        nonlocal pvilanguage, from_name, to_name, from_date, to_date, resflag, gflag, cflag, detailflag, curr_rmtype
        nonlocal usr


        nonlocal k_list, res_list, output_list, allot_list, usr
        nonlocal k_list_list, res_list_list, output_list_list, allot_list_list

        curr_code:str = ""
        d:date = None
        d1:date = None
        d2:date = None
        i:int = 0
        do_it:bool = False

        kontline_obj_list = []
        for kontline, guest, usr in db_session.query(Kontline, Guest, Usr).join(Guest,(Guest.gastnr == Kontline.gastnr) & (func.lower(Guest.name) >= (from_name).lower()) & (func.lower(Guest.name) <= (to_name).lower())).join(Usr,(Usr.nr == Kontline.bediener_nr)).filter(
                 (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1) & (not_ (Kontline.ankunft > to_date)) & (not_ (Kontline.abreise < from_date))).order_by(Guest.name, Kontline.kontcode, Kontline.ankunft).all():
            if kontline._recid in kontline_obj_list:
                continue
            else:
                kontline_obj_list.append(kontline._recid)


            do_it = True

            if re.match(r".*-ALL-.*",curr_rmtype, re.IGNORECASE):
                pass

            elif kontline.zikatnr == 0:
                pass
            else:

                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.kurzbez == curr_rmtype)).first()
                do_it = kontline.zikatnr == zimkateg.zikatnr

            if do_it:

                if curr_code != kontline.kontcode:
                    curr_code = kontline.kontcode
                    k_list = K_list()
                    k_list_list.append(k_list)

                    k_list.gastnr = guest.gastnr
                    k_list.bediener_nr = usr.nr
                    k_list.kontcode = curr_code
                    k_list.ankunft = kontline.ankunft
                    k_list.zikatnr = kontline.zikatnr
                    k_list.argt = kontline.arrangement
                    k_list.erwachs = kontline.erwachs
                    k_list.kind1 = kontline.kind1
                    k_list.ruecktage = kontline.ruecktage
                    k_list.overbooking = kontline.overbooking
                    k_list.abreise = kontline.abreise
                    k_list.useridanlage = kontline.useridanlage
                    k_list.resdat = kontline.resdat
                    k_list.bemerk = kontline.bemerk

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 147) & (Queasy.number1 == kontline.gastnr) & (Queasy.char1 == kontline.kontcode)).first()

                    if queasy:
                        k_list.global_flag = True
                        k_list.global_str = queasy.char3


                else:
                    k_list.abreise = kontline.abreise

                if from_date > kontline.ankunft:
                    d1 = from_date
                else:
                    d1 = kontline.ankunft

                if to_date < kontline.abreise:
                    d2 = to_date
                else:
                    d2 = kontline.abreise
                i = d1 - from_date
                for d in date_range(d1,d2) :
                    i = i + 1

                    if d >= kontline.ankunft and d <= kontline.abreise:
                        k_list.zimmeranz[i - 1] = kontline.zimmeranz


    create_list()

    return generate_output()