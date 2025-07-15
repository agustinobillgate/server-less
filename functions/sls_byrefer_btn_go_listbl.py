#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Guest, Akthdr, Akt_kont

def sls_byrefer_btn_go_listbl(pvilanguage:int, next_date:date, to_date:date, all_flag:bool, usr_init:string):
    slrefer_list_data = []
    lvcarea:string = "sls-byrefer"
    akt_code = guest = akthdr = akt_kont = None

    p_list = slrefer_list = None

    p_list_data, P_list = create_model("P_list", {"pnr":int, "sflag":int, "refer_name":string, "pcomp":string, "pcont":string, "pname":string, "pntot":string, "pnam1":int, "pnam2":int, "pnam3":int, "pnam4":int, "pamt":Decimal, "pamt1":Decimal, "pamt2":Decimal, "pamt3":Decimal, "pamt4":Decimal, "patot":Decimal, "pamt_str":string, "stnr":int, "stage":string, "proz":string, "popen":date, "pfnsh":date, "pmain1":string, "pmain2":string, "pmain3":string, "reason":string, "refer":int, "pid":string, "pcid":string, "ctotal":int})
    slrefer_list_data, Slrefer_list = create_model("Slrefer_list", {"pnr":int, "sflag":int, "refer_name":string, "pcomp":string, "pcont":string, "pname":string, "pntot":string, "pnam1":int, "pnam2":int, "pnam3":int, "pnam4":int, "pamt":Decimal, "pamt1":Decimal, "pamt2":Decimal, "pamt3":Decimal, "pamt4":Decimal, "patot":Decimal, "pamt_str":string, "stnr":int, "stage":string, "proz":string, "popen":date, "pfnsh":date, "pmain1":string, "pmain2":string, "pmain3":string, "reason":string, "refer":int, "pid":string, "pcid":string, "ctotal":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slrefer_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slrefer_list
        nonlocal p_list_data, slrefer_list_data

        return {"slrefer-list": slrefer_list_data}

    def browse_open1():

        nonlocal slrefer_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slrefer_list
        nonlocal p_list_data, slrefer_list_data

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:Decimal = to_decimal("0.0")
        amt:Decimal = to_decimal("0.0")
        flag:bool = True
        lname:string = ""
        kname:string = ""
        akt_code1 = None
        buf_aktcode = None
        guest1 = None
        akthdr1 = None
        akt_kont1 = None
        buf_akthdr = None
        Akt_code1 =  create_buffer("Akt_code1",Akt_code)
        Buf_aktcode =  create_buffer("Buf_aktcode",Akt_code)
        Guest1 =  create_buffer("Guest1",Guest)
        Akthdr1 =  create_buffer("Akthdr1",Akthdr)
        Akt_kont1 =  create_buffer("Akt_kont1",Akt_kont)
        Buf_akthdr =  create_buffer("Buf_akthdr",Akthdr)
        p_list_data.clear()
        slrefer_list_data.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.referred == Akt_code1.aktionscode) & (Buf_akthdr.referred != 0)).filter(
                     (Akt_code1.aktiongrup == 6)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.refer_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.referred == akt_code1.aktionscode)).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pnam1 = akthdr1.product[0]
                        p_list.pnam2 = akthdr1.product[1]
                        p_list.pnam3 = akthdr1.product[2]
                        p_list.pnam4 = akthdr1.product[3]
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
                        p_list.refer = akthdr1.referred
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == akthdr1.grund)).first()
                            p_list.reason = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_refer()
        else:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.referred == Akt_code1.aktionscode) & (Buf_akthdr.referred != 0) & (Buf_akthdr.userinit == (usr_init).lower())).filter(
                     (Akt_code1.aktiongrup == 6)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.refer_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.referred == akt_code1.aktionscode) & (Akthdr1.userinit == (usr_init).lower())).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pnam1 = akthdr1.product[0]
                        p_list.pnam2 = akthdr1.product[1]
                        p_list.pnam3 = akthdr1.product[2]
                        p_list.pnam4 = akthdr1.product[3]
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
                        p_list.refer = akthdr1.referred
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == akthdr1.grund)).first()
                            p_list.reason = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_refer()


    def browse_open2():

        nonlocal slrefer_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slrefer_list
        nonlocal p_list_data, slrefer_list_data

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:Decimal = to_decimal("0.0")
        amt:Decimal = to_decimal("0.0")
        flag:bool = True
        lname:string = ""
        kname:string = ""
        akt_code1 = None
        buf_aktcode = None
        guest1 = None
        akthdr1 = None
        akt_kont1 = None
        buf_akthdr = None
        Akt_code1 =  create_buffer("Akt_code1",Akt_code)
        Buf_aktcode =  create_buffer("Buf_aktcode",Akt_code)
        Guest1 =  create_buffer("Guest1",Guest)
        Akthdr1 =  create_buffer("Akthdr1",Akthdr)
        Akt_kont1 =  create_buffer("Akt_kont1",Akt_kont)
        Buf_akthdr =  create_buffer("Buf_akthdr",Akthdr)
        p_list_data.clear()
        slrefer_list_data.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.referred == Akt_code1.aktionscode) & (Buf_akthdr.referred != 0) & (Buf_akthdr.next_datum >= next_date) & (Buf_akthdr.next_datum <= to_date)).filter(
                     (Akt_code1.aktiongrup == 6)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.refer_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.referred == akt_code1.aktionscode) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pnam1 = akthdr1.product[0]
                        p_list.pnam2 = akthdr1.product[1]
                        p_list.pnam3 = akthdr1.product[2]
                        p_list.pnam4 = akthdr1.product[3]
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
                        p_list.refer = akthdr1.referred
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == akthdr1.grund)).first()
                            p_list.reason = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_refer()
        else:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, buf_akthdr in db_session.query(Akt_code1, Buf_akthdr).join(Buf_akthdr,(Buf_akthdr.referred == Akt_code1.aktionscode) & (Buf_akthdr.referred != 0) & (Buf_akthdr.userinit == (usr_init).lower()) & (Buf_akthdr.next_datum >= next_date) & (Buf_akthdr.next_datum <= to_date)).filter(
                     (Akt_code1.aktiongrup == 6)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.refer_name = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    akthdr1_obj_list = {}
                    for akthdr1, guest1, akt_kont1 in db_session.query(Akthdr1, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Akthdr1.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Akthdr1.kontakt_nr)).filter(
                             (Akthdr1.referred == akt_code1.aktionscode) & (Akthdr1.userinit == (usr_init).lower()) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).order_by(Akthdr1.stufe, Guest1.name).all():
                        if akthdr1_obj_list.get(akthdr1._recid):
                            continue
                        else:
                            akthdr1_obj_list[akthdr1._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

                        p_list.pnr = akthdr1.aktnr
                        p_list.sflag = akthdr1.flag
                        p_list.pcomp = guest1.name + ", " + guest1.anredefirma
                        p_list.pcont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
                        p_list.pname = akthdr1.bezeich
                        p_list.pntot = akthdr1.stichwort
                        p_list.pnam1 = akthdr1.product[0]
                        p_list.pnam2 = akthdr1.product[1]
                        p_list.pnam3 = akthdr1.product[2]
                        p_list.pnam4 = akthdr1.product[3]
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
                        p_list.refer = akthdr1.referred
                        p_list.pid = akthdr1.userinit
                        p_list.pcid = akthdr1.chg_id


                        hnr = hnr + 1
                        amt =  to_decimal(p_list.pamt)
                        tamt =  to_decimal(tamt) + to_decimal(amt)

                        if akthdr1.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == akthdr1.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if akthdr1.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if akthdr1.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if akthdr1.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == akthdr1.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if akthdr1.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == akthdr1.grund)).first()
                            p_list.reason = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_refer()


    def fill_refer():

        nonlocal slrefer_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slrefer_list
        nonlocal p_list_data, slrefer_list_data

        for p_list in query(p_list_data):
            slrefer_list = Slrefer_list()
            slrefer_list_data.append(slrefer_list)

            buffer_copy(p_list, slrefer_list)


    IF next_date != None and to_date != NoneTHEN RUN browse_open2
    else:
        browse_open1()

    return generate_output()