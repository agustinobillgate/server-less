#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Guest, Akthdr, Akt_kont

def sls_bystatus_btn_go_listbl(pvilanguage:int, next_date:date, to_date:date, all_flag:bool, usr_init:string):
    slstatus_list_list = []
    s_flag:List[string] = create_empty_list(4,"")
    lvcarea:string = "sls-bystatus"
    akt_code = guest = akthdr = akt_kont = None

    p_list = slstatus_list = None

    p_list_list, P_list = create_model("P_list", {"pnr":int, "sflag":int, "pcomp":string, "pcont":string, "pname":string, "pntot":string, "pnam1":string, "pnam2":string, "pnam3":string, "pnam4":string, "pamt":Decimal, "pamt1":Decimal, "pamt2":Decimal, "pamt3":Decimal, "pamt4":Decimal, "patot":Decimal, "pamt_str":string, "stnr":int, "stage":string, "proz":string, "popen":date, "pfnsh":date, "pmain1":string, "pmain2":string, "pmain3":string, "reason":string, "refer":string, "pid":string, "pcid":string, "ctotal":int, "stat_flag":string})
    slstatus_list_list, Slstatus_list = create_model("Slstatus_list", {"pnr":int, "sflag":int, "pcomp":string, "pcont":string, "pname":string, "pntot":string, "pnam1":string, "pnam2":string, "pnam3":string, "pnam4":string, "pamt":Decimal, "pamt1":Decimal, "pamt2":Decimal, "pamt3":Decimal, "pamt4":Decimal, "patot":Decimal, "pamt_str":string, "stnr":int, "stage":string, "proz":string, "popen":date, "pfnsh":date, "pmain1":string, "pmain2":string, "pmain3":string, "reason":string, "refer":string, "pid":string, "pcid":string, "ctotal":int, "stat_flag":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slstatus_list_list, s_flag, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slstatus_list
        nonlocal p_list_list, slstatus_list_list

        return {"slstatus-list": slstatus_list_list}

    def browse_open1():

        nonlocal slstatus_list_list, s_flag, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slstatus_list
        nonlocal p_list_list, slstatus_list_list

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:Decimal = to_decimal("0.0")
        amt:Decimal = to_decimal("0.0")
        akt_code1 = None
        guest1 = None
        akthdr1 = None
        akt_kont1 = None
        buf_akthdr = None
        Akt_code1 =  create_buffer("Akt_code1",Akt_code)
        Guest1 =  create_buffer("Guest1",Guest)
        Akthdr1 =  create_buffer("Akthdr1",Akthdr)
        Akt_kont1 =  create_buffer("Akt_kont1",Akt_kont)
        Buf_akthdr =  create_buffer("Buf_akthdr",Akthdr)
        p_list_list.clear()
        slstatus_list_list.clear()

        if all_flag:
            nr = 0
            for i in range(1,4 + 1) :
                s_flag[i - 1]

                akthdr1 = db_session.query(Akthdr1).filter(
                         (Akthdr1.flag == i)).first()

                if akthdr1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.stat_flag = to_string(nr, ">9") + " - " + s_flag[i - 1]


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.flag == i)).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 =  to_decimal(akthdr1.amount[0])
                        p_list.pamt2 =  to_decimal(akthdr1.amount[1])
                        p_list.pamt3 =  to_decimal(akthdr1.amount[2])
                        p_list.pamt4 =  to_decimal(akthdr1.amount[3])
                        p_list.pamt =  to_decimal(p_list.pamt1) + to_decimal(p_list.pamt2) + to_decimal(p_list.pamt3)
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot =  to_decimal(akthdr1.t_betrag)
                        p_list.stnr = akthdr1.stufe
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 2) & (Akt_code1.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = akt_code1.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = akt_code1.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = akt_code1.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = akt_code1.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = akt_code1.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = akt_code1.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = akt_code1.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = akt_code1.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 5) & (Akt_code1.aktionscode == akthdr1.grund)).first()
                            p_list.reason = akt_code1.bezeich

                        if akthdr1.referred != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 6) & (Akt_code1.aktionscode == akthdr1.referred)).first()
                            p_list.refer = akt_code1.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(s_flag[i - 1], "x(10)") + " Opportunity : " + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_status()
        else:
            nr = 0
            for i in range(1,4 + 1) :
                s_flag[i - 1]

                akthdr1 = db_session.query(Akthdr1).filter(
                         (Akthdr1.flag == i) & (Akthdr1.userinit == (usr_init).lower())).first()

                if akthdr1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.stat_flag = to_string(nr, ">9") + " - " + s_flag[i - 1]


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.flag == i) & (Akthdr1.userinit == (usr_init).lower())).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 =  to_decimal(akthdr1.amount[0])
                        p_list.pamt2 =  to_decimal(akthdr1.amount[1])
                        p_list.pamt3 =  to_decimal(akthdr1.amount[2])
                        p_list.pamt4 =  to_decimal(akthdr1.amount[3])
                        p_list.pamt =  to_decimal(p_list.pamt1) + to_decimal(p_list.pamt2) + to_decimal(p_list.pamt3)
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot =  to_decimal(akthdr1.t_betrag)
                        p_list.stnr = akthdr1.stufe
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 2) & (Akt_code1.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = akt_code1.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = akt_code1.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = akt_code1.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = akt_code1.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = akt_code1.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = akt_code1.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = akt_code1.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = akt_code1.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 5) & (Akt_code1.aktionscode == akthdr1.grund)).first()
                            p_list.reason = akt_code1.bezeich

                        if akthdr1.referred != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 6) & (Akt_code1.aktionscode == akthdr1.referred)).first()
                            p_list.refer = akt_code1.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(s_flag[i - 1], "x(10)") + " Opportunity : " + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_status()


    def browse_open2():

        nonlocal slstatus_list_list, s_flag, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slstatus_list
        nonlocal p_list_list, slstatus_list_list

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:Decimal = to_decimal("0.0")
        amt:Decimal = to_decimal("0.0")
        akt_code1 = None
        guest1 = None
        akthdr1 = None
        akt_kont1 = None
        buf_akthdr = None
        Akt_code1 =  create_buffer("Akt_code1",Akt_code)
        Guest1 =  create_buffer("Guest1",Guest)
        Akthdr1 =  create_buffer("Akthdr1",Akthdr)
        Akt_kont1 =  create_buffer("Akt_kont1",Akt_kont)
        Buf_akthdr =  create_buffer("Buf_akthdr",Akthdr)
        p_list_list.clear()
        slstatus_list_list.clear()

        if all_flag:
            nr = 0
            for i in range(1,4 + 1) :
                s_flag[i - 1]

                akthdr1 = db_session.query(Akthdr1).filter(
                         (Akthdr1.flag == i) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).first()

                if akthdr1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.stat_flag = to_string(nr, ">9") + " - " + s_flag[i - 1]


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.flag == i) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 =  to_decimal(akthdr1.amount[0])
                        p_list.pamt2 =  to_decimal(akthdr1.amount[1])
                        p_list.pamt3 =  to_decimal(akthdr1.amount[2])
                        p_list.pamt4 =  to_decimal(akthdr1.amount[3])
                        p_list.pamt =  to_decimal(p_list.pamt1) + to_decimal(p_list.pamt2) + to_decimal(p_list.pamt3)
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot =  to_decimal(akthdr1.t_betrag)
                        p_list.stnr = akthdr1.stufe
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 2) & (Akt_code1.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = akt_code1.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = akt_code1.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = akt_code1.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = akt_code1.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = akt_code1.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = akt_code1.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = akt_code1.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = akt_code1.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 5) & (Akt_code1.aktionscode == akthdr1.grund)).first()
                            p_list.reason = akt_code1.bezeich

                        if akthdr1.referred != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 6) & (Akt_code1.aktionscode == akthdr1.referred)).first()
                            p_list.refer = akt_code1.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(s_flag[i - 1], "x(10)") + " Opportunity : " + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_status()
        else:
            nr = 0
            for i in range(1,4 + 1) :
                s_flag[i - 1]

                akthdr1 = db_session.query(Akthdr1).filter(
                         (Akthdr1.flag == i) & (Akthdr1.userinit == (usr_init).lower()) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).first()

                if akthdr1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.stat_flag = to_string(nr, ">9") + " - " + s_flag[i - 1]


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.flag == i) & (Akthdr1.userinit == (usr_init).lower()) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pamt1 =  to_decimal(akthdr1.amount[0])
                        p_list.pamt2 =  to_decimal(akthdr1.amount[1])
                        p_list.pamt3 =  to_decimal(akthdr1.amount[2])
                        p_list.pamt4 =  to_decimal(akthdr1.amount[3])
                        p_list.pamt =  to_decimal(p_list.pamt1) + to_decimal(p_list.pamt2) + to_decimal(p_list.pamt3)
                        p_list.pamt_str = to_string(p_list.pamt, ">,>>>,>>>,>>9.99")
                        p_list.patot =  to_decimal(akthdr1.t_betrag)
                        p_list.stnr = akthdr1.stufe
                        p_list.proz = to_string(akthdr1.prozent, ">>9%")
                        p_list.popen = akthdr1.next_datum
                        p_list.pfnsh = akthdr1.erl_datum
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 2) & (Akt_code1.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = akt_code1.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.product[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[0])).first()
                            p_list.pnam1 = akt_code1.bezeich
                        else:
                            p_list.pnam1 = " "

                        if akthdr1.product[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[1])).first()
                            p_list.pnam2 = akt_code1.bezeich
                        else:
                            p_list.pnam2 = " "

                        if akthdr1.product[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[2])).first()
                            p_list.pnam3 = akt_code1.bezeich
                        else:
                            p_list.pnam3 = " "

                        if akthdr1.product[3] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 3) & (Akt_code1.aktionscode == akthdr1.product[3])).first()
                            p_list.pnam4 = akt_code1.bezeich
                        else:
                            p_list.pnam4 = " "

                        if akthdr1.mitbewerber[0] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = akt_code1.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = akt_code1.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 4) & (Akt_code1.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = akt_code1.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 5) & (Akt_code1.aktionscode == akthdr1.grund)).first()
                            p_list.reason = akt_code1.bezeich

                        if akthdr1.referred != 0:

                            akt_code1 = db_session.query(Akt_code1).filter(
                                     (Akt_code1.aktiongrup == 6) & (Akt_code1.aktionscode == akthdr1.referred)).first()
                            p_list.refer = akt_code1.bezeich
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(s_flag[i - 1], "x(10)") + " Opportunity : " + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_list.append(p_list)

            fill_status()


    def fill_status():

        nonlocal slstatus_list_list, s_flag, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slstatus_list
        nonlocal p_list_list, slstatus_list_list

        for p_list in query(p_list_list):
            slstatus_list = Slstatus_list()
            slstatus_list_list.append(slstatus_list)

            buffer_copy(p_list, slstatus_list)


    s_flag[0] = "Open"
    s_flag[1] = "Close-Won"
    s_flag[2] = "Close-Lost"
    s_flag[3] = "Inactive"

    if next_date != None and to_date != None:
        browse_open2()
    else:
        browse_open1()

    return generate_output()