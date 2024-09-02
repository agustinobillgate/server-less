from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_code, Guest, Akthdr, Akt_kont

def sls_byreason_btn_go_listbl(pvilanguage:int, next_date:date, to_date:date, all_flag:bool, usr_init:str):
    slreas_list_list = []
    lvcarea:str = "sls_byreason"
    akt_code = guest = akthdr = akt_kont = None

    p_list = slreas_list = akt_code1 = buf_aktcode = guest1 = akthdr1 = akt_kont1 = buf_akthdr = None

    p_list_list, P_list = create_model("P_list", {"pnr":int, "sflag":int, "reason_name":str, "pcomp":str, "pcont":str, "pname":str, "pntot":str, "pnam1":str, "pnam2":str, "pnam3":str, "pnam4":str, "pamt":decimal, "pamt1":decimal, "pamt2":decimal, "pamt3":decimal, "pamt4":decimal, "patot":decimal, "pamt_str":str, "stnr":int, "stage":str, "proz":str, "popen":date, "pfnsh":date, "pmain1":str, "pmain2":str, "pmain3":str, "reason":int, "refer":str, "pid":str, "pcid":str, "ctotal":int})
    slreas_list_list, Slreas_list = create_model("Slreas_list", {"pnr":int, "sflag":int, "reason_name":str, "pcomp":str, "pcont":str, "pname":str, "pntot":str, "pnam1":str, "pnam2":str, "pnam3":str, "pnam4":str, "pamt":decimal, "pamt1":decimal, "pamt2":decimal, "pamt3":decimal, "pamt4":decimal, "patot":decimal, "pamt_str":str, "stnr":int, "stage":str, "proz":str, "popen":date, "pfnsh":date, "pmain1":str, "pmain2":str, "pmain3":str, "reason":int, "refer":str, "pid":str, "pcid":str, "ctotal":int})

    Akt_code1 = Akt_code
    Buf_aktcode = Akt_code
    Guest1 = Guest
    Akthdr1 = Akthdr
    Akt_kont1 = Akt_kont
    Buf_akthdr = Akthdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slreas_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slreas_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slreas_list_list
        return {"slreas-list": slreas_list_list}

    def browse_open1():

        nonlocal slreas_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slreas_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slreas_list_list

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:decimal = 0
        amt:decimal = 0
        flag:bool = True
        lname:str = ""
        kname:str = ""
        Akt_code1 = Akt_code
        Buf_aktcode = Akt_code
        Guest1 = Guest
        Akthdr1 = Akthdr
        Akt_kont1 = Akt_kont
        Buf_akthdr = Akthdr
        p_list_list.clear()
        slreas_list_list.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.grund == Akt_code1.aktionscode) &  (Buf_akthdr.flag == 3) &  (Buf_akthdr.grund != 0)).filter(
                    (Akt_code1.aktiongrup == 5)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.reason_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    akthdr1_obj_list = []
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                            (Akthdr1.grund == akt_code1.aktionscode) &  (Akthdr1.flag == 3)).all():
                        if akthdr1._recid in akthdr1_obj_list:
                            continue
                        else:
                            akthdr1_obj_list.append(akthdr1._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 = akthdr1.amount[0]
                        p_list.pamt2 = akthdr1.amount[1]
                        p_list.pamt3 = akthdr1.amount[2]
                        p_list.pamt4 = akthdr1.amount[3]
                        p_list.pamt = p_list.pamt1 + p_list.pamt2 + p_list.pamt3
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot = akthdr1.t_betrag
                        p_list.stnr = akthdr1.stufe
                        p_list.reason = akthdr1.grund
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt = p_list.pamt
                        tamt = tamt + amt

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = buf_aktcode.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = buf_aktcode.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = buf_aktcode.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = buf_aktcode.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == akthdr1.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(12)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_reason()
        else:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.grund == Akt_code1.aktionscode) &  (Buf_akthdr.flag == 3) &  (Buf_akthdr.grund != 0) &  (func.lower(Buf_akthdr.userinit) == (usr_init).lower())).filter(
                    (Akt_code1.aktiongrup == 5)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.reason_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    akthdr1_obj_list = []
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                            (Akthdr1.grund == akt_code1.aktionscode) &  (Akthdr1.flag == 3) &  (func.lower(Akthdr1.userinit) == (usr_init).lower())).all():
                        if akthdr1._recid in akthdr1_obj_list:
                            continue
                        else:
                            akthdr1_obj_list.append(akthdr1._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 = akthdr1.amount[0]
                        p_list.pamt2 = akthdr1.amount[1]
                        p_list.pamt3 = akthdr1.amount[2]
                        p_list.pamt4 = akthdr1.amount[3]
                        p_list.pamt = p_list.pamt1 + p_list.pamt2 + p_list.pamt3
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot = akthdr1.t_betrag
                        p_list.stnr = akthdr1.stufe
                        p_list.reason = akthdr1.grund
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt = p_list.pamt
                        tamt = tamt + amt

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = buf_aktcode.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = buf_aktcode.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = buf_aktcode.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = buf_aktcode.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == akthdr1.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(12)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_reason()

    def browse_open2():

        nonlocal slreas_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slreas_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slreas_list_list

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:decimal = 0
        amt:decimal = 0
        flag:bool = True
        lname:str = ""
        kname:str = ""
        Akt_code1 = Akt_code
        Buf_aktcode = Akt_code
        Guest1 = Guest
        Akthdr1 = Akthdr
        Akt_kont1 = Akt_kont
        Buf_akthdr = Akthdr
        p_list_list.clear()
        slreas_list_list.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.grund == Akt_code1.aktionscode) &  (Buf_akthdr.flag == 3) &  (Buf_akthdr.grund != 0) &  (Buf_akthdr.erl_datum >= next_date) &  (Buf_akthdr.erl_datum <= to_date)).filter(
                    (Akt_code1.aktiongrup == 5)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.reason_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    akthdr1_obj_list = []
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                            (Akthdr1.grund == akt_code1.aktionscode) &  (Akthdr1.flag == 3) &  (Akthdr1.erl_datum >= next_date) &  (Akthdr1.erl_datum <= to_date)).all():
                        if akthdr1._recid in akthdr1_obj_list:
                            continue
                        else:
                            akthdr1_obj_list.append(akthdr1._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 = akthdr1.amount[0]
                        p_list.pamt2 = akthdr1.amount[1]
                        p_list.pamt3 = akthdr1.amount[2]
                        p_list.pamt4 = akthdr1.amount[3]
                        p_list.pamt = p_list.pamt1 + p_list.pamt2 + p_list.pamt3
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot = akthdr1.t_betrag
                        p_list.stnr = akthdr1.stufe
                        p_list.reason = akthdr1.grund
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt = p_list.pamt
                        tamt = tamt + amt

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = buf_aktcode.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = buf_aktcode.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = buf_aktcode.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = buf_aktcode.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == akthdr1.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(12)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_reason()
        else:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.grund == Akt_code1.aktionscode) &  (Buf_akthdr.flag == 3) &  (Buf_akthdr.grund != 0) &  (func.lower(Buf_akthdr.userinit) == (usr_init).lower()) &  (Buf_akthdr.erl_datum >= next_date) &  (Buf_akthdr.erl_datum <= to_date)).filter(
                    (Akt_code1.aktiongrup == 5)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.reason_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    akthdr1_obj_list = []
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                            (Akthdr1.grund == akt_code1.aktionscode) &  (Akthdr1.flag == 3) &  (func.lower(Akthdr1.userinit) == (usr_init).lower()) &  (Akthdr1.erl_datum >= next_date) &  (Akthdr1.erl_datum <= to_date)).all():
                        if akthdr1._recid in akthdr1_obj_list:
                            continue
                        else:
                            akthdr1_obj_list.append(akthdr1._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 = akthdr1.amount[0]
                        p_list.pamt2 = akthdr1.amount[1]
                        p_list.pamt3 = akthdr1.amount[2]
                        p_list.pamt4 = akthdr1.amount[3]
                        p_list.pamt = p_list.pamt1 + p_list.pamt2 + p_list.pamt3
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot = akthdr1.t_betrag
                        p_list.stnr = akthdr1.stufe
                        p_list.reason = akthdr1.grund
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt = p_list.pamt
                        tamt = tamt + amt

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = buf_aktcode.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = buf_aktcode.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = buf_aktcode.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 3) &  (Buf_aktcode.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = buf_aktcode.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == akthdr1.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(12)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_reason()

    def fill_reason():

        nonlocal slreas_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slreas_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slreas_list_list

        for p_list in query(p_list_list):
            slreas_list = Slreas_list()
            slreas_list_list.append(slreas_list)

            buffer_copy(p_list, slreas_list)

    IF next_date != None and to_date != NoneTHEN RUN browse_open2
    else:
        browse_open1()

    return generate_output()