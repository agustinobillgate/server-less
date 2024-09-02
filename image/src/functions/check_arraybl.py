from functions.additional_functions import *
import decimal
from models import Prmarket, Pricecod, Ratecode, Prtable, Zimkateg, Arrangement

def check_arraybl(rec_id:int):
    margt_list_list = []
    hargt_list_list = []
    hrmcat_list_list = []
    mrmcat_list_list = []
    t_pricecod_list = []
    t_ratecode_list = []
    prmarket = pricecod = ratecode = prtable = zimkateg = arrangement = None

    margt_list = hargt_list = hrmcat_list = mrmcat_list = t_pricecod = t_ratecode = None

    margt_list_list, Margt_list = create_model_like(Prmarket)
    hargt_list_list, Hargt_list = create_model_like(Prmarket)
    hrmcat_list_list, Hrmcat_list = create_model_like(Prmarket)
    mrmcat_list_list, Mrmcat_list = create_model_like(Prmarket)
    t_pricecod_list, T_pricecod = create_model_like(Pricecod)
    t_ratecode_list, T_ratecode = create_model_like(Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, t_pricecod_list, t_ratecode_list, prmarket, pricecod, ratecode, prtable, zimkateg, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, t_pricecod, t_ratecode
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, t_pricecod_list, t_ratecode_list
        return {"margt-list": margt_list_list, "hargt-list": hargt_list_list, "hrmcat-list": hrmcat_list_list, "mrmcat-list": mrmcat_list_list, "t-pricecod": t_pricecod_list, "t-ratecode": t_ratecode_list}

    def check_array():

        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, t_pricecod_list, t_ratecode_list, prmarket, pricecod, ratecode, prtable, zimkateg, arrangement


        nonlocal margt_list, hargt_list, hrmcat_list, mrmcat_list, t_pricecod, t_ratecode
        nonlocal margt_list_list, hargt_list_list, hrmcat_list_list, mrmcat_list_list, t_pricecod_list, t_ratecode_list

        i:int = 0
        array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hrmcat_list_list.clear()
        mrmcat_list_list.clear()
        for i in range(1,99 + 1) :
            array[i - 1] = prtable.zikatnr[i - 1]

        for zimkateg in db_session.query(Zimkateg).all():
            hrmcat_list = Hrmcat_list()
            hrmcat_list_list.append(hrmcat_list)

            hrmcat_list.nr = zimkateg.zikatnr
            hrmcat_list.bezeich = zimkateg.bezeich
        for i in range(1,99 + 1) :

            if array[i - 1] != 0:

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == array[i - 1])).first()

                if zimkateg:
                    mrmcat_list = Mrmcat_list()
                    mrmcat_list_list.append(mrmcat_list)

                    mrmcat_list.nr = zimkateg.zikatnr
                    mrmcat_list.bezeich = zimkateg.bezeich

                hrmcat_list = query(hrmcat_list_list, filters=(lambda hrmcat_list :hrmcat_list.nr == mrmcat_list.nr), first=True)

                if hrmcat_list:
                    hrmcat_list_list.remove(hrmcat_list)
        hargt_list_list.clear()
        margt_list_list.clear()
        for i in range(1,99 + 1) :
            array[i - 1] = prtable.argtnr[i - 1]

        for arrangement in db_session.query(Arrangement).filter(
                (Arrangement.segmentcode == 0)).all():
            hargt_list = Hargt_list()
            hargt_list_list.append(hargt_list)

            hargt_list.nr = arrangement.argtnr
            hargt_list.bezeich = arrangement.argt_bez
        for i in range(1,99 + 1) :

            if array[i - 1] != 0:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement.argtnr == array[i - 1])).first()

                if arrangement:
                    margt_list = Margt_list()
                    margt_list_list.append(margt_list)

                    margt_list.nr = arrangement.argtnr
                    margt_list.bezeich = arrangement.argt_bez

                hargt_list = query(hargt_list_list, filters=(lambda hargt_list :hargt_list.nr == margt_list.nr), first=True)

                if hargt_list:
                    hargt_list_list.remove(hargt_list)


    prtable = db_session.query(Prtable).filter(
            (Prtable._recid == rec_id)).first()

    if not prtable:

        return generate_output()
    check_array()

    for pricecod in db_session.query(Pricecod).filter(
            (Pricecod.marknr == prtable.nr)).all():
        t_pricecod = T_pricecod()
        t_pricecod_list.append(t_pricecod)

        buffer_copy(pricecod, t_pricecod)

    for ratecode in db_session.query(Ratecode).filter(
            (Ratecode.marknr == prtable.nr)).all():
        t_ratecode = T_ratecode()
        t_ratecode_list.append(t_ratecode)

        buffer_copy(ratecode, t_ratecode)

    return generate_output()