#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

def read_zimmerbl(case_type:int, rmno:string, zikatno:int, setupno:int):
    t_zimmer_data = []
    counter:int = 0
    str:string = ""
    zimmer = None

    t_zimmer = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimmer_data, counter, str, zimmer
        nonlocal case_type, rmno, zikatno, setupno


        nonlocal t_zimmer
        nonlocal t_zimmer_data

        return {"t-zimmer": t_zimmer_data}

    if case_type == 1:

        if num_entries(rmno, ";") > 1:
            for counter in range(1,num_entries(rmno, ";")  + 1) :
                str = entry(counter - 1, rmno, ";")

                zimmer = get_cache (Zimmer, {"zinr": [(eq, str)]})

                if zimmer:

                    t_zimmer = query(t_zimmer_data, filters=(lambda t_zimmer: t_zimmer.zinr.lower()  == (str).lower()), first=True)

                    if not t_zimmer:
                        t_zimmer = T_zimmer()
                        t_zimmer_data.append(t_zimmer)

                        buffer_copy(zimmer, t_zimmer)
        else:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rmno)]})

            if zimmer:
                t_zimmer = T_zimmer()
                t_zimmer_data.append(t_zimmer)

                buffer_copy(zimmer, t_zimmer)
    elif case_type == 2:

        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zikatno)],"setup": [(eq, setupno)]})

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 3:

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zikatnr == zikatno)).order_by(Zimmer.zinr).all():
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)

    elif case_type == 4:

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.house_status != 0)).order_by(Zimmer.zinr).all():
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)

    elif case_type == 5:

        zimmer = db_session.query(Zimmer).order_by(Zimmer._recid.desc()).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 6:

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zikatnr == zikatno) & (Zimmer.sleeping)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 7:

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 8:

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zistatus >= 2) & (Zimmer.zistatus <= 4)).order_by(Zimmer._recid).all():
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 9:

        zimmer = get_cache (Zimmer, {"typ": [(eq, zikatno)]})

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 10:

        zimmer = db_session.query(Zimmer).filter(
                 ((Zimmer.setup + 9200) == setupno)).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)
    elif case_type == 11:

        # zimmer = get_cache (Zimmer, {"nebenstelle": [(ne, "")]})
        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.nebenstelle != "")).first()

        if zimmer:
            t_zimmer = T_zimmer()
            t_zimmer_data.append(t_zimmer)

            buffer_copy(zimmer, t_zimmer)

    return generate_output()