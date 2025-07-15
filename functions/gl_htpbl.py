#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Paramtext

def gl_htpbl(grpnr:int):

    prepare_cache ([Paramtext])

    t_htparam_data = []
    htgrp_data = []
    htparam = paramtext = None

    t_htparam = htgrp = None

    t_htparam_data, T_htparam = create_model_like(Htparam)
    htgrp_data, Htgrp = create_model("Htgrp", {"number":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_htparam_data, htgrp_data, htparam, paramtext
        nonlocal grpnr


        nonlocal t_htparam, htgrp
        nonlocal t_htparam_data, htgrp_data

        return {"t-htparam": t_htparam_data, "htgrp": htgrp_data}

    def create_htgrp():

        nonlocal t_htparam_data, htgrp_data, htparam, paramtext
        nonlocal grpnr


        nonlocal t_htparam, htgrp
        nonlocal t_htparam_data, htgrp_data

        arr:List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 158, 0, 0, 0, 0, 0]
        i:int = 0

        if grpnr == 20:
            arr[14] = 143
            arr[15] = 0

        elif grpnr == 21:
            arr[14] = 144
            arr[15] = 0
        for i in range(1,20 + 1) :

            if arr[i - 1] != 0:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, arr[i - 1])]})
                htgrp = Htgrp()
                htgrp_data.append(htgrp)

                htgrp.number = paramtext.number
                htgrp.bezeich = paramtext.ptexte


    def create_htparam():

        nonlocal t_htparam_data, htgrp_data, htparam, paramtext
        nonlocal grpnr


        nonlocal t_htparam, htgrp
        nonlocal t_htparam_data, htgrp_data

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == htgrp.number)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)


    create_htgrp()

    for htgrp in query(htgrp_data):
        create_htparam()

    return generate_output()