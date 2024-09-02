from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Zimkateg

def view_reservationbl(resnr:int):
    tot_pax = 0
    tot_com = 0
    tot_ch1 = 0
    tot_ch2 = 0
    tot_rm = 0
    do_it1 = False
    s_list_list = []
    res_line = zimkateg = None

    s_list = s1_list = None

    s_list_list, S_list = create_model("S_list", {"flag":int, "pos":int, "s_ankunft":str, "ankunft":date, "abreise":date, "rmcat":str, "zimmeranz":int, "erwachs":int, "gratis":int, "kind1":int, "kind2":int, "str":str})

    S1_list = S_list
    s1_list_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_pax, tot_com, tot_ch1, tot_ch2, tot_rm, do_it1, s_list_list, res_line, zimkateg
        nonlocal s1_list


        nonlocal s_list, s1_list
        nonlocal s_list_list
        return {"tot_pax": tot_pax, "tot_com": tot_com, "tot_ch1": tot_ch1, "tot_ch2": tot_ch2, "tot_rm": tot_rm, "do_it1": do_it1, "s-list": s_list_list}

    def cal_revenue():

        nonlocal tot_pax, tot_com, tot_ch1, tot_ch2, tot_rm, do_it1, s_list_list, res_line, zimkateg
        nonlocal s1_list


        nonlocal s_list, s1_list
        nonlocal s_list_list

        pos:int = 0
        l_ankunft:date = None
        l_abreise:date = None
        l_rmcat:str = ""
        do_it:bool = False
        t_qty:int = 0
        t_pax:int = 0
        t_ch1:int = 0
        t_ch2:int = 0
        S1_list = S_list
        s_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12)).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 0 and s_list.rmcat == zimkateg.kurzbez and s_list.ankunft == res_line.ankunft and s_list.abreise == res_line.abreise and s_list.erwachs == res_line.erwachs and s_list.gratis == res_line.gratis and s_list.kind1 == res_line.kind1 and s_list.kind2 == res_line.kind2), first=True)
            tot_pax = tot_pax + res_line.zimmeranz * res_line.erwachs
            tot_com = tot_com + res_line.zimmeranz * res_line.gratis
            tot_ch1 = tot_ch1 + res_line.zimmeranz * res_line.kind1
            tot_ch2 = tot_ch2 + res_line.zimmeranz * res_line.kind2

            if res_line.resstatus != 11 and res_line.resstatus != 13:
                tot_rm = tot_rm + res_line.zimmeranz

            if res_line.resstatus != 11 and res_line.resstatus != 13:

                if not s_list and res_line.resstatus <= 6:
                    pos = pos + 1
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.pos = pos
                    s_list.ankunft = res_line.ankunft
                    s_list.s_ankunft = to_string(s_list.ankunft)
                    s_list.abreise = res_line.abreise
                    s_list.rmcat = zimkateg.kurzbez

            if res_line.resstatus <= 6 and s_list:
                s_list.zimmeranz = s_list.zimmeranz + res_line.zimmeranz
            t_pax = t_pax + (res_line.erwachs + res_line.gratis) * res_line.zimmeranz
            t_ch1 = t_ch1 + res_line.kind1 * res_line.zimmeranz
            t_ch2 = t_ch2 + res_line.kind2 * res_line.zimmeranz

            if s_list:
                s_list.erwachs = res_line.erwachs
                s_list.gratis = res_line.gratis
                s_list.kind1 = res_line.kind1
                s_list.kind2 = res_line.kind2

        for s_list in query(s_list_list):

            if l_ankunft == None:
                l_ankunft = s_list.ankunft
                l_abreise = s_list.abreise
                l_rmcat = s_list.rmcat
            else:

                if l_ankunft == s_list.ankunft and l_abreise == s_list.abreise and l_rmcat == s_list.rmcat:
                    do_it = True
                else:
                    l_ankunft = s_list.ankunft
                    l_abreise = s_list.abreise
                    l_rmcat = s_list.rmcat

        if not do_it:
            do_it1 = True

            return
        s_list = S_list()
        s_list_list.append(s_list)

        pos = pos + 1
        s_list.pos = pos
        s_list.flag = 1
        s_list = S_list()
        s_list_list.append(s_list)

        pos = pos + 1
        s_list.pos = pos
        s_list.flag = 1
        s_list.s_ankunft = "SUMMARY"

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 0)):
            t_qty = t_qty + s_list.zimmeranz

            s1_list = query(s1_list_list, filters=(lambda s1_list :s1_list.flag == 2 and s1_list.rmcat == s_list.rmcat and s1_list.ankunft == s_list.ankunft and s1_list.abreise == s_list.abreise), first=True)

            if not s1_list:
                pos = pos + 1
                s1_list = S1_list()
                s1_list_list.append(s1_list)

                s1_list.pos = pos
                s1_list.flag = 2
                s1_list.ankunft = s_list.ankunft
                s1_list.s_ankunft = to_string(s1_list.ankunft)
                s1_list.abreise = s_list.abreise
                s1_list.rmcat = s_list.rmcat
            s1_list.zimmeranz = s1_list.zimmeranz + s_list.zimmeranz
        pos = pos + 1
        s1_list = S1_list()
        s1_list_list.append(s1_list)

        s1_list.pos = pos
        s1_list.flag = 2
        s1_list.s_ankunft = "TOT ROOM"
        s1_list.zimmeranz = t_qty
        pos = pos + 1
        s1_list = S1_list()
        s1_list_list.append(s1_list)

        s1_list.pos = pos
        s1_list.flag = 3
        s1_list.s_ankunft = "TOT PAX"
        s1_list.zimmeranz = t_pax

        if t_ch1 > 0:
            pos = pos + 1
            s1_list = S1_list()
            s1_list_list.append(s1_list)

            s1_list.pos = pos
            s1_list.flag = 4
            s1_list.s_ankunft = "TOT CH1"
            s1_list.zimmeranz = t_ch1

        if t_ch2 > 0:
            pos = pos + 1
            s1_list = S1_list()
            s1_list_list.append(s1_list)

            s1_list.pos = pos
            s1_list.flag = 5
            s1_list.s_ankunft = "TOT CH2"
            s1_list.zimmeranz = t_ch2


    cal_revenue()

    return generate_output()