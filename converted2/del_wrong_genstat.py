from functions.additional_functions import *
import decimal
from models import Genstat

def del_wrong_genstat():
    i:int = 0
    j:int = 0
    genstat = None

    gbuff = None

    Gbuff = create_buffer("Gbuff",Genstat)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, genstat
        nonlocal gbuff


        nonlocal gbuff

        return {}


    genstat = db_session.query(Genstat).filter(
             (Genstat.res_date[inc_value(0)] < Genstat.datum) & (Genstat.res_date[inc_value(1)] == Genstat.datum) & (Genstat.resstatus == 8)).first()
    while None != genstat:

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff._recid == genstat._recid)).first()
        gbuff_list.remove(gbuff)
        pass
        i = i + 1
        j = j + 1

        if i == 100:
            pass
            i = 0

        curr_recid = genstat._recid
        genstat = db_session.query(Genstat).filter(
                 (Genstat.res_date[inc_value(0)] < Genstat.datum) & (Genstat.res_date[inc_value(1)] == Genstat.datum) & (Genstat.resstatus == 8) & (Genstat._recid > curr_recid)).first()

    return generate_output()