from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Htparam, Fa_artikel, Mathis

def prepare_fa_upgradebl(p_nr:int, nr:int):
    name_mathis = ""
    asset_no = ""
    last_close = None
    datum = None
    amt = 0
    gl_jouhdr1_list = []
    gl_jouhdr = htparam = fa_artikel = mathis = None

    gl_jouhdr1 = None

    gl_jouhdr1_list, Gl_jouhdr1 = create_model_like(Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal name_mathis, asset_no, last_close, datum, amt, gl_jouhdr1_list, gl_jouhdr, htparam, fa_artikel, mathis


        nonlocal gl_jouhdr1
        nonlocal gl_jouhdr1_list
        return {"name_mathis": name_mathis, "asset_no": asset_no, "last_close": last_close, "datum": datum, "amt": amt, "gl-jouhdr1": gl_jouhdr1_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    last_close = fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 372)).first()
    datum = htparam.fdate

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == p_nr)).first()
    amt = fa_artikel.warenwert

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == nr)).first()
    name_mathis = mathis.name
    asset_no = mathis.asset

    for gl_jouhdr in db_session.query(Gl_jouhdr).all():
        gl_jouhdr1 = Gl_jouhdr1()
        gl_jouhdr1_list.append(gl_jouhdr1)

        buffer_copy(gl_jouhdr, gl_jouhdr1)

    return generate_output()