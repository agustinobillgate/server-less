#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Htparam, Fa_artikel, Mathis

def prepare_fa_upgradebl(p_nr:int, nr:int):

    prepare_cache ([Htparam, Fa_artikel, Mathis])

    name_mathis = ""
    asset_no = ""
    last_close = None
    datum = None
    amt = to_decimal("0.0")
    gl_jouhdr1_list = []
    gl_jouhdr = htparam = fa_artikel = mathis = None

    gl_jouhdr1 = None

    gl_jouhdr1_list, Gl_jouhdr1 = create_model_like(Gl_jouhdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal name_mathis, asset_no, last_close, datum, amt, gl_jouhdr1_list, gl_jouhdr, htparam, fa_artikel, mathis
        nonlocal p_nr, nr


        nonlocal gl_jouhdr1
        nonlocal gl_jouhdr1_list

        return {"name_mathis": name_mathis, "asset_no": asset_no, "last_close": last_close, "datum": datum, "amt": amt, "gl-jouhdr1": gl_jouhdr1_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_close = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 372)]})
    datum = htparam.fdate

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, p_nr)]})
    amt =  to_decimal(fa_artikel.warenwert)

    mathis = get_cache (Mathis, {"nr": [(eq, nr)]})
    name_mathis = mathis.name
    asset_no = mathis.asset

    for gl_jouhdr in db_session.query(Gl_jouhdr).order_by(Gl_jouhdr._recid).all():
        gl_jouhdr1 = Gl_jouhdr1()
        gl_jouhdr1_list.append(gl_jouhdr1)

        buffer_copy(gl_jouhdr, gl_jouhdr1)

    return generate_output()