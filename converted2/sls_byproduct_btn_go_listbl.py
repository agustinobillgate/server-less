#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Guest, Akthdr, Akt_kont

def sls_byproduct_btn_go_listbl(pvilanguage:int, next_date:date, to_date:date, all_flag:bool, usr_init:string):
    slprod_list_data = []
    lvcarea:string = "sls-byproduct"
    akt_code = guest = akthdr = akt_kont = None

    p_list = slprod_list = None

    p_list_data, P_list = create_model("P_list", {"pnr":int, "sflag":int, "product":string, "pcomp":string, "pcont":string, "pname":string, "pntot":string, "pnam1":int, "pnam2":int, "pnam3":int, "pnam4":int, "pamt":Decimal, "pamt1":Decimal, "pamt2":Decimal, "pamt3":Decimal, "pamt4":Decimal, "patot":Decimal, "pamt_str":string, "stnr":int, "stage":string, "proz":string, "popen":date, "pfnsh":date, "pmain1":string, "pmain2":string, "pmain3":string, "reason":string, "refer":string, "pid":string, "pcid":string, "ctotal":int})
    slprod_list_data, Slprod_list = create_model("Slprod_list", {"pnr":int, "sflag":int, "product":string, "pcomp":string, "pcont":string, "pname":string, "pntot":string, "pnam1":int, "pnam2":int, "pnam3":int, "pnam4":int, "pamt":Decimal, "pamt1":Decimal, "pamt2":Decimal, "pamt3":Decimal, "pamt4":Decimal, "patot":Decimal, "pamt_str":string, "stnr":int, "stage":string, "proz":string, "popen":date, "pfnsh":date, "pmain1":string, "pmain2":string, "pmain3":string, "reason":string, "refer":string, "pid":string, "pcid":string, "ctotal":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slprod_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slprod_list
        nonlocal p_list_data, slprod_list_data

        return {"slprod-list": slprod_list_data}

    def browse_open1():

        nonlocal slprod_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slprod_list
        nonlocal p_list_data, slprod_list_data

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:Decimal = to_decimal("0.0")
        flag:bool = True
        lname:string = ""
        kname:string = ""
        amt:Decimal = to_decimal("0.0")
        amt1:Decimal = to_decimal("0.0")
        amt2:Decimal = to_decimal("0.0")
        amt3:Decimal = to_decimal("0.0")
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
        slprod_list_data.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[inc_value(0)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(1)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(2)] == Akt_code1.aktionscode)) & ((Akthdr1.product[inc_value(0)] != 0) | (Akthdr1.product[inc_value(1)] != 0) | (Akthdr1.product[inc_value(2)] != 0))).filter(
                     (Akt_code1.aktiongrup == 3)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    buf_akthdr_obj_list = {}
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                             ((Buf_akthdr.product[inc_value(0)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(1)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(2)] == akt_code1.aktionscode))).order_by(Buf_akthdr.stufe, Guest1.name).all():
                        if buf_akthdr_obj_list.get(buf_akthdr._recid):
                            continue
                        else:
                            buf_akthdr_obj_list[buf_akthdr._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

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
                        p_list.pamt1 =  to_decimal(buf_akthdr.amount[0])
                        p_list.pamt2 =  to_decimal(buf_akthdr.amount[1])
                        p_list.pamt3 =  to_decimal(buf_akthdr.amount[2])
                        p_list.pamt4 =  to_decimal(buf_akthdr.amount[3])
                        p_list.patot =  to_decimal(buf_akthdr.t_betrag)
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 =  to_decimal(p_list.pamt1)
                        else:
                            amt1 =  to_decimal("0")

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 =  to_decimal(p_list.pamt2)
                        else:
                            amt2 =  to_decimal("0")

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 =  to_decimal(p_list.pamt3)
                        else:
                            amt3 =  to_decimal("0")
                        hnr = hnr + 1
                        amt =  to_decimal(amt1) + to_decimal(amt2) + to_decimal(amt3)
                        tamt =  to_decimal(tamt) + to_decimal(amt)
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 6) & (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_prod()
        else:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[inc_value(0)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(1)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(2)] == Akt_code1.aktionscode)) & ((Akthdr1.product[inc_value(0)] != 0) | (Akthdr1.product[inc_value(1)] != 0) | (Akthdr1.product[inc_value(2)] != 0)) & (Akthdr1.userinit == (usr_init).lower())).filter(
                     (Akt_code1.aktiongrup == 3)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    buf_akthdr_obj_list = {}
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                             ((Buf_akthdr.product[inc_value(0)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(1)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(2)] == akt_code1.aktionscode)) & (Buf_akthdr.userinit == (usr_init).lower())).order_by(Buf_akthdr.stufe, Guest1.name).all():
                        if buf_akthdr_obj_list.get(buf_akthdr._recid):
                            continue
                        else:
                            buf_akthdr_obj_list[buf_akthdr._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

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
                        p_list.pamt1 =  to_decimal(buf_akthdr.amount[0])
                        p_list.pamt2 =  to_decimal(buf_akthdr.amount[1])
                        p_list.pamt3 =  to_decimal(buf_akthdr.amount[2])
                        p_list.pamt4 =  to_decimal(buf_akthdr.amount[3])
                        p_list.patot =  to_decimal(buf_akthdr.t_betrag)
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 =  to_decimal(p_list.pamt1)
                        else:
                            amt1 =  to_decimal("0")

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 =  to_decimal(p_list.pamt2)
                        else:
                            amt2 =  to_decimal("0")

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 =  to_decimal(p_list.pamt3)
                        else:
                            amt3 =  to_decimal("0")
                        hnr = hnr + 1
                        amt =  to_decimal(amt1) + to_decimal(amt2) + to_decimal(amt3)
                        tamt =  to_decimal(tamt) + to_decimal(amt)
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 6) & (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_prod()


    def browse_open2():

        nonlocal slprod_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slprod_list
        nonlocal p_list_data, slprod_list_data

        i:int = 0
        nr:int = 0
        hnr:int = 0
        tamt:Decimal = to_decimal("0.0")
        flag:bool = True
        lname:string = ""
        kname:string = ""
        amt:Decimal = to_decimal("0.0")
        amt1:Decimal = to_decimal("0.0")
        amt2:Decimal = to_decimal("0.0")
        amt3:Decimal = to_decimal("0.0")
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
        slprod_list_data.clear()

        if all_flag:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[inc_value(0)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(1)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(2)] == Akt_code1.aktionscode)) & ((Akthdr1.product[inc_value(0)] != 0) | (Akthdr1.product[inc_value(1)] != 0) | (Akthdr1.product[inc_value(2)] != 0)) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).filter(
                     (Akt_code1.aktiongrup == 3)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    buf_akthdr_obj_list = {}
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                             ((Buf_akthdr.product[inc_value(0)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(1)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(2)] == akt_code1.aktionscode)) & (Buf_akthdr.next_datum >= next_date) & (Buf_akthdr.next_datum <= to_date)).order_by(Buf_akthdr.stufe, Guest1.name).all():
                        if buf_akthdr_obj_list.get(buf_akthdr._recid):
                            continue
                        else:
                            buf_akthdr_obj_list[buf_akthdr._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

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
                        p_list.pamt1 =  to_decimal(buf_akthdr.amount[0])
                        p_list.pamt2 =  to_decimal(buf_akthdr.amount[1])
                        p_list.pamt3 =  to_decimal(buf_akthdr.amount[2])
                        p_list.pamt4 =  to_decimal(buf_akthdr.amount[3])
                        p_list.patot =  to_decimal(buf_akthdr.t_betrag)
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 =  to_decimal(p_list.pamt1)
                        else:
                            amt1 =  to_decimal("0")

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 =  to_decimal(p_list.pamt2)
                        else:
                            amt2 =  to_decimal("0")

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 =  to_decimal(p_list.pamt3)
                        else:
                            amt3 =  to_decimal("0")
                        hnr = hnr + 1
                        amt =  to_decimal(amt1) + to_decimal(amt2) + to_decimal(amt3)
                        tamt =  to_decimal(tamt) + to_decimal(amt)
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 6) & (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_prod()
        else:
            nr = 0

            akt_code1_obj_list = {}
            for akt_code1, akthdr1 in db_session.query(Akt_code1, Akthdr1).join(Akthdr1,((Akthdr1.product[inc_value(0)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(1)] == Akt_code1.aktionscode) | (Akthdr1.product[inc_value(2)] == Akt_code1.aktionscode)) & ((Akthdr1.product[inc_value(0)] != 0) | (Akthdr1.product[inc_value(1)] != 0) | (Akthdr1.product[inc_value(2)] != 0)) & (Akthdr1.userinit == (usr_init).lower()) & (Akthdr1.next_datum >= next_date) & (Akthdr1.next_datum <= to_date)).filter(
                     (Akt_code1.aktiongrup == 3)).order_by(Akt_code1.aktionscode).all():
                if akt_code1_obj_list.get(akt_code1._recid):
                    continue
                else:
                    akt_code1_obj_list[akt_code1._recid] = True

                if akt_code1:
                    nr = nr + 1
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.product = to_string(nr, ">9") + " - " + akt_code1.bezeich


                    hnr = 0
                    amt =  to_decimal("0")
                    tamt =  to_decimal("0")

                    buf_akthdr_obj_list = {}
                    for buf_akthdr, guest1, akt_kont1 in db_session.query(Buf_akthdr, Guest1, Akt_kont1).join(Guest1,(Guest1.gastnr == Buf_akthdr.gastnr)).join(Akt_kont1,(Akt_kont1.gastnr == Guest1.gastnr) & (Akt_kont1.kontakt_nr == Buf_akthdr.kontakt_nr)).filter(
                             ((Buf_akthdr.product[inc_value(0)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(1)] == akt_code1.aktionscode) | (Buf_akthdr.product[inc_value(2)] == akt_code1.aktionscode)) & (Buf_akthdr.userinit == (usr_init).lower()) & (Buf_akthdr.next_datum >= next_date) & (Buf_akthdr.next_datum <= to_date)).order_by(Buf_akthdr.stufe, Guest1.name).all():
                        if buf_akthdr_obj_list.get(buf_akthdr._recid):
                            continue
                        else:
                            buf_akthdr_obj_list[buf_akthdr._recid] = True


                        p_list = P_list()
                        p_list_data.append(p_list)

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
                        p_list.pamt1 =  to_decimal(buf_akthdr.amount[0])
                        p_list.pamt2 =  to_decimal(buf_akthdr.amount[1])
                        p_list.pamt3 =  to_decimal(buf_akthdr.amount[2])
                        p_list.pamt4 =  to_decimal(buf_akthdr.amount[3])
                        p_list.patot =  to_decimal(buf_akthdr.t_betrag)
                        p_list.stnr = buf_akthdr.stufe
                        p_list.proz = to_string(buf_akthdr.prozent, ">>9%")
                        p_list.popen = buf_akthdr.next_datum
                        p_list.pfnsh = buf_akthdr.erl_datum
                        p_list.pid = buf_akthdr.userinit
                        p_list.pcid = buf_akthdr.chg_id

                        if p_list.pnam1 == akt_code1.aktionscode:
                            amt1 =  to_decimal(p_list.pamt1)
                        else:
                            amt1 =  to_decimal("0")

                        if p_list.pnam2 == akt_code1.aktionscode:
                            amt2 =  to_decimal(p_list.pamt2)
                        else:
                            amt2 =  to_decimal("0")

                        if p_list.pnam3 == akt_code1.aktionscode:
                            amt3 =  to_decimal(p_list.pamt3)
                        else:
                            amt3 =  to_decimal("0")
                        hnr = hnr + 1
                        amt =  to_decimal(amt1) + to_decimal(amt2) + to_decimal(amt3)
                        tamt =  to_decimal(tamt) + to_decimal(amt)
                        p_list.pamt_str = to_string(amt, ">,>>>,>>>,>>9.99")

                        if buf_akthdr.stufe != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 2) & (Buf_aktcode.aktionscode == buf_akthdr.stufe)).first()
                            p_list.stage = buf_aktcode.bezeich
                        else:
                            p_list.stage = " "

                        if buf_akthdr.mitbewerber[0] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[0])).first()
                            p_list.pmain1 = buf_aktcode.bezeich
                        else:
                            p_list.pmain1 = " "

                        if buf_akthdr.mitbewerber[1] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[1])).first()
                            p_list.pmain2 = buf_aktcode.bezeich
                        else:
                            p_list.pmain2 = " "

                        if buf_akthdr.mitbewerber[2] != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 4) & (Buf_aktcode.aktionscode == buf_akthdr.mitbewerber[2])).first()
                            p_list.pmain3 = buf_aktcode.bezeich
                        else:
                            p_list.pmain3 = " "

                        if buf_akthdr.grund != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 5) & (Buf_aktcode.aktionscode == buf_akthdr.grund)).first()
                            p_list.reason = buf_aktcode.bezeich

                        if buf_akthdr.referred != 0:

                            buf_aktcode = db_session.query(Buf_aktcode).filter(
                                     (Buf_aktcode.aktiongrup == 6) & (Buf_aktcode.aktionscode == buf_akthdr.referred)).first()
                            p_list.refer = buf_aktcode.bezeich
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.pcomp = "TOTAL " + to_string(akt_code1.bezeich, "x(25)") + ":" + to_string(hnr, ">>>>")
                    p_list.pname = "TOTAL Amount : "
                    p_list.pamt_str = to_string(tamt, ">,>>>,>>>,>>9.99")


                    p_list = P_list()
                    p_list_data.append(p_list)

            fill_prod()


    def fill_prod():

        nonlocal slprod_list_data, lvcarea, akt_code, guest, akthdr, akt_kont
        nonlocal pvilanguage, next_date, to_date, all_flag, usr_init


        nonlocal p_list, slprod_list
        nonlocal p_list_data, slprod_list_data

        for p_list in query(p_list_data):
            slprod_list = Slprod_list()
            slprod_list_data.append(slprod_list)

            buffer_copy(p_list, slprod_list)

    if next_date != None and to_date != None:
        browse_open2()
    else:
        browse_open1()

    return generate_output()