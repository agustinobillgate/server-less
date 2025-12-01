#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Kellner, Bill_line, H_bill_line, Reservation, Artikel, H_journal, Hoteldpt

t_bediener_data, T_bediener = create_model_like(Bediener)

def write_bedienerbl(case_type:int, t_bediener_data:[T_bediener]):

    prepare_cache ([Hoteldpt])

    success_flag = False
    prevname:string = ""
    existflag:bool = False
    ct:string = ""
    curr_i:int = 0
    st:string = ""
    curr_j:int = 0
    deptnr:int = 0
    mkey:bool = False
    crartno:int = 0
    toartno:int = 0
    bediener = kellner = bill_line = h_bill_line = reservation = artikel = h_journal = hoteldpt = None

    t_bediener = dept_list = kbuff = None

    dept_list_data, Dept_list = create_model("Dept_list", {"deptno":int})

    Kbuff = create_buffer("Kbuff",Kellner)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, deptnr, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal case_type
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal dept_list_data

        return {"success_flag": success_flag}

    def update_kellner():

        nonlocal success_flag, prevname, existflag, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal case_type
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal dept_list_data

        ct:string = ""
        curr_i:int = 0
        st:string = ""
        curr_j:int = 0
        deptnr:int = 0
        mkey:bool = False
        crartno:int = 0
        toartno:int = 0
        kbuff = None
        Kbuff =  create_buffer("Kbuff",Kellner)
        ct = bediener.mapi_profile
        for curr_i in range(1,num_entries(bediener.mapi_profile, ";")  + 1) :
            ct = trim(entry(curr_i - 1, bediener.mapi_profile, ";"))

            if ct != "":

                if substring(ct, 0, 2) == "$1":
                    pass
                elif substring(ct, 0, 2) == "$2":
                    ct = substring(ct, 2)
                    for curr_j in range(1,num_entries(ct, ",")  + 1) :
                        st = trim(entry(curr_j - 1, ct, ","))

                        if st != "":
                            deptnr = to_int(entry(0, st, "/"))
                            mkey = to_int(entry(1, st, "/")) == 1


                            dept_list = Dept_list()
                            dept_list_data.append(dept_list)

                            dept_list.deptno = deptnr

                            # kellner = get_cache (Kellner, {"departement": [(eq, deptnr)],"kellner_nr": [(eq, to_int(bediener.userinit))]})
                            kellner = db_session.query(Kellner).filter(
                                     (Kellner.departement == deptnr) &
                                     (Kellner.kellner_nr == to_int(bediener.userinit))).with_for_update().first()

                            if kellner and kellner.masterkey != mkey:
                                pass
                                kellner.masterkey = mkey


                                pass

                            elif not kellner:

                                artikel = db_session.query(Artikel).filter(
                                         (Artikel.departement == 0) & (Artikel.artart == 1) & (substring(Artikel.bezeich, 0, 4) == ("CR" + to_string(deptnr, "99").lower()))).first()

                                if artikel:
                                    crartno = artikel.artnr
                                else:
                                    crartno = create_crartikel(deptnr)

                                artikel = get_cache (Artikel, {"departement": [(eq, deptnr)],"artart": [(eq, 1)],"bezeich": [(eq, "t/o-" + bediener.userinit)]})

                                if artikel:
                                    toartno = artikel.artnr
                                else:
                                    crartno = create_toartikel(deptnr, bediener.userinit)
                                kellner = Kellner()
                                db_session.add(kellner)

                                kellner.departement = deptnr
                                kellner.kellner_nr = to_int(bediener.userinit)
                                kellner.kellnername = bediener.username
                                kellner.kumsatz_nr = toartno
                                kellner.kcredit_nr = crartno
                                kellner.masterkey = mkey


                                pass

                    for kellner in db_session.query(Kellner).filter(
                             (Kellner.kellner_nr == to_int(bediener.userinit))).order_by(Kellner._recid).all():

                        dept_list = query(dept_list_data, filters=(lambda dept_list: dept_list.deptno == kellner.departement), first=True)

                        if not dept_list:

                            h_journal = get_cache (H_journal, {"kellner_nr": [(eq, kellner.kellner_nr)],"departement": [(eq, kellner.departement)]})

                            if not h_journal:

                                kbuff = db_session.query(Kbuff).filter(
                                         (Kbuff._recid == kellner._recid)).with_for_update().first()
                                db_session.delete(kbuff)
                                pass


    def create_crartikel(deptnr:int):

        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal case_type
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal dept_list_data

        artno = 0

        def generate_inner_output():
            return (artno)

        artno = 3000 + deptnr

        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, artno)]})
        while None != artikel:
            artno = artno + 1

            curr_recid = artikel._recid
            artikel = db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & (Artikel.artnr == artno) & (Artikel._recid > curr_recid)).first()

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, deptnr)]})
        artikel = Artikel()
        db_session.add(artikel)

        artikel.departement = 0
        artikel.artnr = artno
        artikel.bezeich = "CR" + to_string(hoteldpt.num, "99") + "-" +\
                hoteldpt.depart.upper()
        artikel.artart = 1
        artikel.activeflag = True

        return generate_inner_output()


    def create_toartikel(deptnr:int, userinit:string):

        nonlocal success_flag, prevname, existflag, ct, curr_i, st, curr_j, mkey, crartno, toartno, bediener, kellner, bill_line, h_bill_line, reservation, artikel, h_journal, hoteldpt
        nonlocal case_type
        nonlocal kbuff


        nonlocal t_bediener, dept_list, kbuff
        nonlocal dept_list_data

        artno = 0

        def generate_inner_output():
            return (artno)

        artno = 3000 + deptnr

        artikel = get_cache (Artikel, {"departement": [(eq, deptnr)],"artnr": [(eq, artno)]})
        while None != artikel:
            artno = artno + 1

            curr_recid = artikel._recid
            artikel = db_session.query(Artikel).filter(
                     (Artikel.departement == deptnr) & (Artikel.artnr == artno) & (Artikel._recid > curr_recid)).first()
        artikel = Artikel()
        db_session.add(artikel)

        artikel.departement = deptnr
        artikel.artnr = artno
        artikel.bezeich = "T/O" + "-" + userinit
        artikel.artart = 1
        artikel.activeflag = True

        return generate_inner_output()

    t_bediener = query(t_bediener_data, first=True)

    if not t_bediener:

        return generate_output()

    if case_type == 1:
        bediener = Bediener()
        db_session.add(bediener)

        buffer_copy(t_bediener, bediener)
        pass
        success_flag = True


    elif case_type == 2:

        # bediener = get_cache (Bediener, {"userinit": [(eq, t_bediener.userinit)]})
        bediener = db_session.query(Bediener).filter(
                 (Bediener.userinit == t_bediener.userinit)).with_for_update

        if bediener:
            buffer_copy(t_bediener, bediener)
            pass
            success_flag = True


    elif case_type == 3:

        # bediener = get_cache (Bediener, {"nr": [(eq, t_bediener.nr)]})
        bediener = db_session.query(Bediener).filter(
                 (Bediener.nr == t_bediener.nr)).with_for_update().first()

        if bediener:
            prevname = bediener.username
            buffer_copy(t_bediener, bediener)
            pass

            if prevname != t_bediener.username:

                kellner = get_cache (Kellner, {"kellner_nr": [(eq, to_int(bediener.userinit))]})
                while None != kellner:

                    kbuff = db_session.query(Kbuff).filter(
                             (Kbuff._recid == kellner._recid)).with_for_update().first()
                    kbuff.kellnername = t_bediener.username


                    pass
                    pass

                    curr_recid = kellner._recid
                    kellner = db_session.query(Kellner).filter(
                             (Kellner.kellner_nr == to_int(bediener.userinit)) & (Kellner._recid > curr_recid)).first()
            update_kellner()
            success_flag = True


    elif case_type == 4:

        # bediener = get_cache (Bediener, {"nr": [(eq, t_bediener.nr)]})
        bediener = db_session.query(Bediener).filter(
                 (Bediener.nr == t_bediener.nr)).with_for_update().first

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
        pass

        if existflag:
            bediener.flag = 1


            pass
        else:

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, to_int(bediener.userinit))]})
            while None != kellner:

                # artikel = get_cache (Artikel, {"artnr": [(eq, kellner.kumsatz_nr)],"departement": [(eq, kellner.departement)]})
                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == kellner.kumsatz_nr) &
                         (Artikel.departement == kellner.departement)).with_for_update().first()

                if artikel:
                    db_session.delete(artikel)
                    pass

                kbuff = db_session.query(Kbuff).filter(
                         (Kbuff.kcredit_nr == kellner.kcredit_nr) & (Kbuff._recid != kellner._recid)).first()

                if not kbuff:

                    # artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, kellner.kcredit_nr)]})
                    artikel = db_session.query(Artikel).filter(
                             (Artikel.departement == 0) & (Artikel.artnr == kellner.kcredit_nr)).with_for_update().first()

                    if artikel:
                        db_session.delete(artikel)
                        pass

                kbuff = db_session.query(Kbuff).filter(
                         (Kbuff._recid == kellner._recid)).with_for_update().first()
                db_session.delete(kbuff)
                pass

                curr_recid = kellner._recid
                kellner = db_session.query(Kellner).filter(
                         (Kellner.kellner_nr == to_int(bediener.userinit)) & (Kellner._recid > curr_recid)).first()
            db_session.delete(bediener)
            success_flag = True
        pass
    elif case_type == 5:

        for t_bediener in query(t_bediener_data):
            bediener = Bediener()
            db_session.add(bediener)

            buffer_copy(t_bediener, bediener)
            pass
            ct = t_bediener.mapi_profile
            for curr_i in range(1,num_entries(t_bediener.mapi_profile, ";")  + 1) :
                ct = trim(entry(curr_i - 1, t_bediener.mapi_profile, ";"))

                if ct != "":

                    if substring(ct, 0, 2) == "$1":
                        pass
                    elif substring(ct, 0, 2) == "$2":
                        ct = substring(ct, 2)
                        for curr_j in range(1,num_entries(ct, ",")  + 1) :
                            st = trim(entry(curr_j - 1, ct, ","))

                            if st != "":
                                deptnr = to_int(entry(0, st, "/"))
                                mkey = to_int(entry(1, st, "/")) == 1

                                artikel = db_session.query(Artikel).filter(
                                         (Artikel.departement == 0) & (Artikel.artart == 1) & (substring(Artikel.bezeich, 0, 4) == ("CR" + to_string(deptnr, "99").lower()))).first()

                                if artikel:
                                    crartno = artikel.artnr
                                else:
                                    crartno = create_crartikel(deptnr)

                                artikel = get_cache (Artikel, {"departement": [(eq, deptnr)],"artart": [(eq, 1)],"bezeich": [(eq, "t/o-" + bediener.userinit)]})

                                if artikel:
                                    toartno = artikel.artnr
                                else:
                                    toartno = create_toartikel(deptnr, bediener.userinit)
                                kellner = Kellner()
                                db_session.add(kellner)

                                kellner.kellner_nr = to_int(bediener.userinit)
                                kellner.departement = deptnr
                                kellner.kellnername = bediener.username
                                kellner.kumsatz_nr = toartno
                                kellner.kcredit_nr = crartno
                                kellner.masterkey = mkey


                                pass
        success_flag = True

    return generate_output()