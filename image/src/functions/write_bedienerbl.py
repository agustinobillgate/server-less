from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Kellner, Bill_line, H_bill_line, Reservation, Artikel, H_journal, Hoteldpt

def write_bedienerbl(case_type:int, t_bediener:[T_bediener]):
    success_flag = False
    prevname:str = ""
    existflag:bool = False
    ct:str = ""
    curr_i:int = 0
    st:str = ""
    curr_j:int = 0
    deptnr:int = 0
    mkey:bool = False
    crartno:int = 0
    toartno:int = 0
    bediener = kellner = bill_line = h_bill_line = reservation = artikel = h_journal = hoteldpt = None

    t_bediener = dept_list = kbuff = None

    t_bediener_list, T_bediener = create_model_like(Bediener)
    dept_list_list, Dept_list = create_model("Dept_list", {"deptno":int})

    Kbuff = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, deptnr, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal t_bediener_list, dept_list_list
        return {"success_flag": success_flag}

    def update_kellner():

        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, deptnr, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal t_bediener_list, dept_list_list

        ct:str = ""
        curr_i:int = 0
        st:str = ""
        curr_j:int = 0
        deptnr:int = 0
        mkey:bool = False
        crartno:int = 0
        toartno:int = 0
        Kbuff = Kellner
        ct = bediener.mapi_profile
        for curr_i in range(1,num_entries(bediener.mapi_profile, ";")  + 1) :
            ct = trim(entry(curr_i - 1, bediener.mapi_profile, ";"))

            if ct != "":

                if substring(ct, 0, 2) == "$1":
                    1
                elif substring(ct, 0, 2) == "$2":
                    ct = substring(ct, 2)
                    for curr_j in range(1,num_entries(ct, ",")  + 1) :
                        st = trim(entry(curr_j - 1, ct, ","))

                        if st != "":
                            deptnr = to_int(entry(0, st, "/"))
                            mkey = to_int(entry(1, st, "/")) == 1


                            dept_list = Dept_list()
                            dept_list_list.append(dept_list)

                            dept_list.deptNo = deptnr

                            kellner = db_session.query(Kellner).filter(
                                    (Kellner.departement == deptnr) &  (Kellner_nr == to_int(bediener.userinit))).first()

                            if kellner and kellner.masterkey != mkey:

                                kellner = db_session.query(Kellner).first()
                                kellner.masterkey = mkey

                                kellner = db_session.query(Kellner).first()

                            elif not kellner:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.departement == 0) &  (Artikel.artart == 1) &  (substring(Artikel.bezeich, 0, 4) == "CR" + to_string(deptnr, "99"))).first()

                                if artikel:
                                    crartno = artikel.artnr
                                else:
                                    crartno = create_crartikel(deptnr)

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.departement == deptnr) &  (Artikel.artart == 1) &  (func.lower(Artikel.bezeich) == "T/O-" + bediener.userinit)).first()

                                if artikel:
                                    toartno = artikel.artnr
                                else:
                                    crartno = create_toartikel(deptnr, bediener.userinit)
                                kellner = Kellner()
                                db_session.add(kellner)

                                kellner.departement = deptnr
                                kellner_nr = to_int(bediener.userinit)
                                kellnername = bediener.username
                                kellner.kumsatz_nr = toartno
                                kellner.kcredit_nr = crartno
                                kellner.masterkey = mkey


                    for kellner in db_session.query(Kellner).filter(
                            (Kellner_nr == to_int(bediener.userinit))).all():

                        dept_list = query(dept_list_list, filters=(lambda dept_list :dept_list.deptNo == kellner.departement), first=True)

                        if not dept_list:

                            h_journal = db_session.query(H_journal).filter(
                                    (H_journal.kellner_nr == kellner_nr) &  (H_journal.departement == kellner.departement)).first()

                            if not h_journal:

                                kbuff = db_session.query(Kbuff).filter(
                                        (Kbuff._recid == kellner._recid)).first()
                                db_session.delete(kbuff)


    def create_crartikel(deptnr:int):

        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, deptnr, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal t_bediener_list, dept_list_list

        artno = 0

        def generate_inner_output():
            return artno
        artno = 3000 + deptnr

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artnr == artno)).first()
        while None != artikel:
            artno = artno + 1

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (Artikel.artnr == artno)).first()

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == deptnr)).first()
        artikel = Artikel()
        db_session.add(artikel)

        artikel.departement = 0
        artikel.artnr = artno
        artikel.bezeich = "CR" + to_string(hoteldpt.num, "99") + "-" +\
                hoteldpt.depart.upper()
        artikel.artart = 1
        artikel.activeflag = True


        return generate_inner_output()

    def create_toartikel(deptnr:int, userinit:str):

        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, deptnr, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal t_bediener_list, dept_list_list

        artno = 0

        def generate_inner_output():
            return artno
        artno = 3000 + deptnr

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == deptnr) &  (Artikel.artnr == artno)).first()
        while None != artikel:
            artno = artno + 1

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == deptnr) &  (Artikel.artnr == artno)).first()
        artikel = Artikel()
        db_session.add(artikel)

        artikel.departement = deptnr
        artikel.artnr = artno
        artikel.bezeich = "T/O" + "-" + userinit
        artikel.artart = 1
        artikel.activeflag = True


        return generate_inner_output()


    t_bediener = query(t_bediener_list, first=True)

    if not t_bediener:

        return generate_output()

    if case_type == 1:
        bediener = Bediener()
        db_session.add(bediener)

        buffer_copy(t_bediener, bediener)

        bediener = db_session.query(Bediener).first()
        success_flag = True


    elif case_type == 2:

        bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == t_Bediener.userinit)).first()

        if bediener:
            buffer_copy(t_bediener, bediener)

            bediener = db_session.query(Bediener).first()
            success_flag = True


    elif case_type == 3:

        bediener = db_session.query(Bediener).filter(
                (Bediener.nr == t_Bediener.nr)).first()

        if bediener:
            prevname = bediener.username


            buffer_copy(t_bediener, bediener)

            bediener = db_session.query(Bediener).first()

            if prevname != t_bediener.username:

                kellner = db_session.query(Kellner).filter(
                        (Kellner_nr == to_int(bediener.userinit))).first()
                while None != kellner:

                    kbuff = db_session.query(Kbuff).filter(
                            (Kbuff._recid == kellner._recid)).first()
                    kbuff.kellnername = t_bediener.username

                    kbuff = db_session.query(Kbuff).first()


                    kellner = db_session.query(Kellner).filter(
                            (Kellner_nr == to_int(bediener.userinit))).first()
            update_kellner()
            success_flag = True


    elif case_type == 4:

        bediener = db_session.query(Bediener).filter(
                (Bediener.nr == t_Bediener.nr)).first()

        if not bediener:

            return generate_output()

        bill_line = db_session.query(Bill_line).first()
        existflag = None != bill_line
        existflag = None != bill_line

        if not existflag:

            h_bill_line = db_session.query(H_bill_line).first()
            existflag = None != h_bill_line

        if not existflag:

            reservation = db_session.query(Reservation).first()
            existflag = None != reservation

        bediener = db_session.query(Bediener).first()

        if existflag:
            bediener.flag = 1

            bediener = db_session.query(Bediener).first()
        else:

            kellner = db_session.query(Kellner).filter(
                    (Kellner_nr == to_int(bediener.userinit))).first()
            while None != kellner:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == kellner.kumsatz_nr) &  (Artikel.departement == kellner.departement)).first()

                if artikel:
                    db_session.delete(artikel)


                kbuff = db_session.query(Kbuff).filter(
                        (Kbuff.kcredit_nr == kellner.kcredit_nr) &  (Kbuff._recid != kellner._recid)).first()

                if not kbuff:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.departement == 0) &  (Artikel.artnr == kellner.kcredit_nr)).first()

                    if artikel:
                        db_session.delete(artikel)


                kbuff = db_session.query(Kbuff).filter(
                        (Kbuff._recid == kellner._recid)).first()
                db_session.delete(kbuff)


                kellner = db_session.query(Kellner).filter(
                        (Kellner_nr == to_int(bediener.userinit))).first()
            db_session.delete(bediener)
            success_flag = True

    elif case_type == 5:

        for t_bediener in query(t_bediener_list):
            bediener = Bediener()
            db_session.add(bediener)

            buffer_copy(t_bediener, bediener)

            bediener = db_session.query(Bediener).first()
            ct = t_bediener.mapi_profile
            for curr_i in range(1,num_entries(t_bediener.mapi_profile, ";")  + 1) :
                ct = trim(entry(curr_i - 1, t_bediener.mapi_profile, ";"))

                if ct != "":

                    if substring(ct, 0, 2) == "$1":
                        1
                    elif substring(ct, 0, 2) == "$2":
                        ct = substring(ct, 2)
                        for curr_j in range(1,num_entries(ct, ",")  + 1) :
                            st = trim(entry(curr_j - 1, ct, ","))

                            if st != "":
                                deptnr = to_int(entry(0, st, "/"))
                                mkey = to_int(entry(1, st, "/")) == 1

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.departement == 0) &  (Artikel.artart == 1) &  (substring(Artikel.bezeich, 0, 4) == "CR" + to_string(deptnr, "99"))).first()

                                if artikel:
                                    crartno = artikel.artnr
                                else:
                                    crartno = create_crartikel(deptnr)

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.departement == deptnr) &  (Artikel.artart == 1) &  (func.lower(Artikel.bezeich) == "T/O-" + bediener.userinit)).first()

                                if artikel:
                                    toartno = artikel.artnr
                                else:
                                    toartno = create_toartikel(deptnr, bediener.userinit)
                                kellner = Kellner()
                                db_session.add(kellner)

                                kellner_nr = to_int(bediener.userinit)
                                kellner.departement = deptnr
                                kellnername = bediener.username
                                kellner.kumsatz_nr = toartno
                                kellner.kcredit_nr = crartno
                                kellner.masterkey = mkey

        success_flag = True

    return generate_output()