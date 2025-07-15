#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Gl_department

def prepare_gl_subdepart_adminbl():
    t_queasy_data = []
    t_gl_depart_data = []
    queasy = gl_department = None

    t_queasy = t_gl_depart = None

    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_gl_depart_data, T_gl_depart = create_model_like(Gl_department)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, t_gl_depart_data, queasy, gl_department


        nonlocal t_queasy, t_gl_depart
        nonlocal t_queasy_data, t_gl_depart_data

        return {"t-queasy": t_queasy_data, "t-gl-depart": t_gl_depart_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 155)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        t_gl_depart = T_gl_depart()
        t_gl_depart_data.append(t_gl_depart)

        buffer_copy(gl_department, t_gl_depart)

    return generate_output()