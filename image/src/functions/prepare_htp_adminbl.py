from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Paramtext

def prepare_htp_adminbl():
    rest_flag = False
    s_list_list = []
    htp_list = []
    htgrp_list = []
    htp_list_list = []
    fl_assign:bool = False
    gnr:int = 31
    anz_htp:int = 70
    arr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    htp_arr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    i:int = 0
    htparam = paramtext = None

    s_list = htp_list = htgrp = htp = None

    s_list_list, S_list = create_model("S_list", {"nr":int})
    htp_list_list, Htp_list = create_model_like(Htparam)
    htgrp_list, Htgrp = create_model("Htgrp", {"number":int, "bezeich":str})
    htp_list, Htp = create_model("Htp", {"reihenfolge":int, "number":int, "bezeich":str, "typ":int, "logv":bool, "lupdate":date, "note":str, "wert":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, i, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list
        return {"rest_flag": rest_flag, "s-list": s_list_list, "htp": htp_list, "htgrp": htgrp_list, "htp-list": htp_list_list}

    def create_htplist():

        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, i, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 40)).all():
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            buffer_copy(htparam, htp_list)

    def create_htgrp():

        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, i, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        i:int = 0

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 161)).first()

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 161
            paramtext.number = 35
            paramtext.ptexte = "Centralized Mgmt Reporting System"


        for i in range(1,gnr + 1) :

            if arr[i - 1] != 0:

                paramtext = db_session.query(Paramtext).filter(
                        (Paramtext.txtnr == arr[i - 1])).first()

                if paramtext:
                    htgrp = Htgrp()
                    htgrp_list.append(htgrp)

                    htgrp.number = paramtext.number
                    htgrp.bezeich = paramtext.ptexte

    def create_htp(i:int):

        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, i, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        passwd_ok:bool = True
        do_it:bool = False
        htp_list.clear()

        for htparam in db_session.query(Htparam).filter(
                    (Htparam.paramgruppe == i)).all():
            do_it = True

            if rest_flag:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nr == htparam.paramnr), first=True)

                if s_list:
                    do_it = False

            if do_it:
                htp = Htp()
                htp_list.append(htp)

                htp.reihenfolge = htparam.reihenfolge
                htp.number = htparam.paramnr
                htp.bezeich = htparam.bezeich
                htp.lupdate = htparam.lupdate
                htp.note = htparam.fdefault

                if htparam.feldtyp == 1:
                    htp.wert = to_string(htparam.finteger)

                elif htparam.feldtyp == 2:
                    htp.wert = to_string(htparam.fdecimal)

                elif htparam.feldtyp == 3:
                    htp.wert = to_string(htparam.fdate)

                elif htparam.feldtyp == 4:
                    htp.wert = to_string(htparam.flogical)
                    htp.logv = htparam.flogical

                elif htparam.feldtyp == 5:
                    htp.wert = to_string(htparam.fchar)
                htp.typ = htparam.feldtyp


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 996)).first()

    if not htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1015)).first()

        if not htparam.flogical:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 990)).first()

            if htparam.flogical:
                rest_flag = True
                arr[8] = 0
                arr[13] = 0
                arr[15] = 0
                arr[17] = 0
                arr[18] = 0
                arr[19] = 0
                for i in range(1,anz_htp + 1) :

                    if htp_arr[i - 1] != 0:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.nr = htp_arr[i - 1]

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 981)).first()

    if not htparam.flogical:
        arr[18] = 0
    create_htgrp()

    htgrp = query(htgrp_list, first=True)

    if htgrp and htgrp.number != 10 and htgrp.number != 99 and htgrp.number != 100:
        create_htp(htgrp.number)
    create_htplist()

    return generate_output()