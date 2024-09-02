from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_code, Guest, Akthdr, Akt_kont

def sls_byproduct_btn_go_listbl(pvilanguage:int, next_date:date, to_date:date, all_flag:bool, usr_init:str):
    slprod_list_list = []
    lvcarea:str = "sls_byproduct"
    akt_code = guest = akthdr = akt_kont = None

    p_list = slprod_list = akt_code1 = buf_aktcode = guest1 = akthdr1 = akt_kont1 = buf_akthdr = None

    p_list_list, P_list = create_model("P_list", {"pnr":int, "sflag":int, "product":str, "pcomp":str, "pcont":str, "pname":str, "pntot":str, "pnam1":int, "pnam2":int, "pnam3":int, "pnam4":int, "pamt":decimal, "pamt1":decimal, "pamt2":decimal, "pamt3":decimal, "pamt4":decimal, "patot":decimal, "pamt_str":str, "stnr":int, "stage":str, "proz":str, "popen":date, "pfnsh":date, "pmain1":str, "pmain2":str, "pmain3":str, "reason":str, "refer":str, "pid":str, "pcid":str, "ctotal":int})
    slprod_list_list, Slprod_list = create_model("Slprod_list", {"pnr":int, "sflag":int, "product":str, "pcomp":str, "pcont":str, "pname":str, "pntot":str, "pnam1":int, "pnam2":int, "pnam3":int, "pnam4":int, "pamt":decimal, "pamt1":decimal, "pamt2":decimal, "pamt3":decimal, "pamt4":decimal, "patot":decimal, "pamt_str":str, "stnr":int, "stage":str, "proz":str, "popen":date, "pfnsh":date, "pmain1":str, "pmain2":str, "pmain3":str, "reason":str, "refer":str, "pid":str, "pcid":str, "ctotal":int})

    Akt_code1 = Akt_code
    Buf_aktcode = Akt_code
    Guest1 = Guest
    Akthdr1 = Akthdr
    Akt_kont1 = Akt_kont
    Buf_akthdr = Akthdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slprod_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slprod_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slprod_list_list
        return {"slprod-list": slprod_list_list}

    def browse_open1():

        nonlocal slprod_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slprod_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slprod_list_list

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:decimal = 0
        flag:bool = True
        lname:str = ""
        kname:str = ""
        amt:decimal = 0
        amt1:decimal = 0
        amt2:decimal = 0
        amt3:decimal = 0
        Akt_code1 = Akt_code
        Buf_aktcode = Akt_code
        Guest1 = Guest
        Akthdr1 = Akthdr
        Akt_kont1 = Akt_kont
        Buf_akthdr = Akthdr
        p_list_list.clear()
        slprod_list_list.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[0] == Akt_code1.aktionscode) |  (Akthdr1.product[1] == Akt_code1.aktionscode) |  (Akthdr1.product[2] == Akt_code1.aktionscode)) &  ((Akthdr1.product[0] != 0) |  (Akthdr1.product[1] != 0) |  (Akthdr1.product[2] != 0))).filter(
                    (Akt_code1.aktiongrup == 3)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    buf_akthdr_obj_list = []
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                            ((Buf_akthdr.product[0] == akt_code1.aktionscode) |  (Buf_akthdr.product[1] == akt_code1.aktionscode) |  (Buf_akthdr.product[2] == akt_code1.aktionscode))).all():
                        if buf_akthdr._recid in buf_akthdr_obj_list:
                            continue
                        else:
                            buf_akthdr_obj_list.append(buf_akthdr._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = buf_akthdr.aktnr
                        p_list.sflag = buf_akthdr.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = buf_akthdr.bezeich
                        p_list.pntot = buf_akthdr.stichwort
                        p_list.pnam1 = buf_akthdr.product[0]
                        p_list.pnam2 = buf_akthdr.product[1]
                        p_list.pnam3 = buf_akthdr.product[2]
                        p_list.pnam4 = buf_akthdr.product[3]
                        p_list.pamt1 = buf_akthdr.amount[0]
                        p_list.pamt2 = buf_akthdr.amount[1]
                        p_list.pamt3 = buf_akthdr.amount[2]
                        p_list.pamt4 = buf_akthdr.amount[3]
                        p_list.patot = buf_akthdr.t_betrag
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 = p_list.pamt1
                        else:
                            amt1 = 0

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 = p_list.pamt2
                        else:
                            amt2 = 0

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 = p_list.pamt3
                        else:
                            amt3 = 0
                        hnr = hnr + 1
                        amt = amt1 + amt2 + amt3
                        tamt = tamt + amt
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 5) &  (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_prod()
        else:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[0] == Akt_code1.aktionscode) |  (Akthdr1.product[1] == Akt_code1.aktionscode) |  (Akthdr1.product[2] == Akt_code1.aktionscode)) &  ((Akthdr1.product[0] != 0) |  (Akthdr1.product[1] != 0) |  (Akthdr1.product[2] != 0)) &  (func.lower(Akthdr1.userinit) == (usr_init).lower())).filter(
                    (Akt_code1.aktiongrup == 3)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    buf_akthdr_obj_list = []
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                            ((Buf_akthdr.product[0] == akt_code1.aktionscode) |  (Buf_akthdr.product[1] == akt_code1.aktionscode) |  (Buf_akthdr.product[2] == akt_code1.aktionscode)) &  (func.lower(Buf_akthdr.userinit) == (usr_init).lower())).all():
                        if buf_akthdr._recid in buf_akthdr_obj_list:
                            continue
                        else:
                            buf_akthdr_obj_list.append(buf_akthdr._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = buf_akthdr.aktnr
                        p_list.sflag = buf_akthdr.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = buf_akthdr.bezeich
                        p_list.pntot = buf_akthdr.stichwort
                        p_list.pnam1 = buf_akthdr.product[0]
                        p_list.pnam2 = buf_akthdr.product[1]
                        p_list.pnam3 = buf_akthdr.product[2]
                        p_list.pnam4 = buf_akthdr.product[3]
                        p_list.pamt1 = buf_akthdr.amount[0]
                        p_list.pamt2 = buf_akthdr.amount[1]
                        p_list.pamt3 = buf_akthdr.amount[2]
                        p_list.pamt4 = buf_akthdr.amount[3]
                        p_list.patot = buf_akthdr.t_betrag
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 = p_list.pamt1
                        else:
                            amt1 = 0

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 = p_list.pamt2
                        else:
                            amt2 = 0

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 = p_list.pamt3
                        else:
                            amt3 = 0
                        hnr = hnr + 1
                        amt = amt1 + amt2 + amt3
                        tamt = tamt + amt
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 5) &  (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_prod()

    def browse_open2():

        nonlocal slprod_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slprod_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slprod_list_list

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:decimal = 0
        flag:bool = True
        lname:str = ""
        kname:str = ""
        amt:decimal = 0
        amt1:decimal = 0
        amt2:decimal = 0
        amt3:decimal = 0
        Akt_code1 = Akt_code
        Buf_aktcode = Akt_code
        Guest1 = Guest
        Akthdr1 = Akthdr
        Akt_kont1 = Akt_kont
        Buf_akthdr = Akthdr
        p_list_list.clear()
        slprod_list_list.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[0] == Akt_code1.aktionscode) |  (Akthdr1.product[1] == Akt_code1.aktionscode) |  (Akthdr1.product[2] == Akt_code1.aktionscode)) &  ((Akthdr1.product[0] != 0) |  (Akthdr1.product[1] != 0) |  (Akthdr1.product[2] != 0)) &  (Akthdr1.next_datum >= next_date) &  (Akthdr1.next_datum <= to_date)).filter(
                    (Akt_code1.aktiongrup == 3)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    buf_akthdr_obj_list = []
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                            ((Buf_akthdr.product[0] == akt_code1.aktionscode) |  (Buf_akthdr.product[1] == akt_code1.aktionscode) |  (Buf_akthdr.product[2] == akt_code1.aktionscode)) &  (Buf_akthdr.next_datum >= next_date) &  (Buf_akthdr.next_datum <= to_date)).all():
                        if buf_akthdr._recid in buf_akthdr_obj_list:
                            continue
                        else:
                            buf_akthdr_obj_list.append(buf_akthdr._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = buf_akthdr.aktnr
                        p_list.sflag = buf_akthdr.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = buf_akthdr.bezeich
                        p_list.pntot = buf_akthdr.stichwort
                        p_list.pnam1 = buf_akthdr.product[0]
                        p_list.pnam2 = buf_akthdr.product[1]
                        p_list.pnam3 = buf_akthdr.product[2]
                        p_list.pnam4 = buf_akthdr.product[3]
                        p_list.pamt1 = buf_akthdr.amount[0]
                        p_list.pamt2 = buf_akthdr.amount[1]
                        p_list.pamt3 = buf_akthdr.amount[2]
                        p_list.pamt4 = buf_akthdr.amount[3]
                        p_list.patot = buf_akthdr.t_betrag
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 = p_list.pamt1
                        else:
                            amt1 = 0

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 = p_list.pamt2
                        else:
                            amt2 = 0

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 = p_list.pamt3
                        else:
                            amt3 = 0
                        hnr = hnr + 1
                        amt = amt1 + amt2 + amt3
                        tamt = tamt + amt
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 5) &  (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_prod()
        else:
            nr = 0

            akt_code1_obj_list = []
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[0] == Akt_code1.aktionscode) |  (Akthdr1.product[1] == Akt_code1.aktionscode) |  (Akthdr1.product[2] == Akt_code1.aktionscode)) &  ((Akthdr1.product[0] != 0) |  (Akthdr1.product[1] != 0) |  (Akthdr1.product[2] != 0)) &  (func.lower(Akthdr1.userinit) == (usr_init).lower()) &  (Akthdr1.next_datum >= next_date) &  (Akthdr1.next_datum <= to_date)).filter(
                    (Akt_code1.aktiongrup == 3)).all():
                if akt_code1._recid in akt_code1_obj_list:
                    continue
                else:
                    akt_code1_obj_list.append(akt_code1._recid)

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt = 0
                    tamt = 0

                    buf_akthdr_obj_list = []
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == guest1.gastnr) &  (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                            ((Buf_akthdr.product[0] == akt_code1.aktionscode) |  (Buf_akthdr.product[1] == akt_code1.aktionscode) |  (Buf_akthdr.product[2] == akt_code1.aktionscode)) &  (func.lower(Buf_akthdr.userinit) == (usr_init).lower()) &  (Buf_akthdr.next_datum >= next_date) &  (Buf_akthdr.next_datum <= to_date)).all():
                        if buf_akthdr._recid in buf_akthdr_obj_list:
                            continue
                        else:
                            buf_akthdr_obj_list.append(buf_akthdr._recid)


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = buf_akthdr.aktnr
                        p_list.sflag = buf_akthdr.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = buf_akthdr.bezeich
                        p_list.pntot = buf_akthdr.stichwort
                        p_list.pnam1 = buf_akthdr.product[0]
                        p_list.pnam2 = buf_akthdr.product[1]
                        p_list.pnam3 = buf_akthdr.product[2]
                        p_list.pnam4 = buf_akthdr.product[3]
                        p_list.pamt1 = buf_akthdr.amount[0]
                        p_list.pamt2 = buf_akthdr.amount[1]
                        p_list.pamt3 = buf_akthdr.amount[2]
                        p_list.pamt4 = buf_akthdr.amount[3]
                        p_list.patot = buf_akthdr.t_betrag
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 = p_list.pamt1
                        else:
                            amt1 = 0

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 = p_list.pamt2
                        else:
                            amt2 = 0

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 = p_list.pamt3
                        else:
                            amt3 = 0
                        hnr = hnr + 1
                        amt = amt1 + amt2 + amt3
                        tamt = tamt + amt
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 2) &  (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 4) &  (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 5) &  (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                    (Buf_aktcode.aktiongrup == 6) &  (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_prod()

    def fill_prod():

        nonlocal slprod_list_list, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr


        nonlocal p_list, slprod_list, akt_code1, buf_aktcode, guest1, akthdr1, akt_kont1, buf_akthdr
        nonlocal p_list_list, slprod_list_list

        for p_list in query(p_list_list):
            slprod_list = Slprod_list()
            slprod_list_list.append(slprod_list)

            buffer_copy(p_list, slprod_list)


    if next_date != None and to_date != None:
        browse_open2()
    else:
        browse_open1()

    return generate_output()