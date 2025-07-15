#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.translateframe import translateframe

def sel_allotorglobal():
    lvcarea:string = "sel-allotorglobal"
    out_type = -1
    whand = None
    rectl1:string = ""
    rectl9:string = ""
    sorttype:int = 0 VIEW_AS RADIO_SET SIZE 30 BY 5 TOOLTIP "Select Allotment or Global Reservation" VERTICAL RADIO_BUTTONS "&A l l o t m e n t", 0, "&Global Reservation", 1 FGCOLOR 1

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, out_type, whand, rectl1, rectl9, sorttype

        return {"out_type": out_type}

    DEFINE BUTTON btn_exit LABEL "&OK" SIZE_CHAR 13 BY 1 TOOLTIP "Confirm Selection"
    DEFINE BUTTON btn_cancel LABEL "&CANCEL" SIZE_CHAR 13 BY 1 TOOLTIP "Cancel Selection"
    DEFINE FRAME Frame1 rectl1 AT ROW 1.5 COLUMN 4 NO_LABELS sorttype AT ROW 3.0 COLUMN 12 NO_LABEL rectl9 AT ROW 10 COLUMN 4.0 NO_LABEL BGCOLOR 7 btn_exit AT ROW 10.3 COLUMN 7 btn_cancel COLON 28 SKIP (0.5) WITH SIDE_LABELS CENTERED OVERLAY WIDTH 47.5 THREE_D VIEW_AS dialog_box TITLE "Allotment / Global Reservation"
    ON F1, F2, F3, F4, F5, F6, F8, F9, F11, F12, cursor_left, cursor_right, page_up, page_down ANYWHERE DO:
    ON F7 OF FRAME frame1 ANYWHERE APPLY "choose" TO btn_cancel IN FRAME frame1
    ON F10 OF FRAME frame1 ANYWHERE APPLY "choose" TO btn_exit IN FRAME frame1
    ON CTRL_T OF FRAME frame1 ANYWHERE DO:
    get_output(translateframe(FRAME frame1:HANDLE, lvcarea))
    APPLY "entry" TO btn_exit
    ON return OF btn_exit APPLY "choose" TO btn_exit
    ON return OF btn_cancel APPLY "choose" TO btn_cancel
    ON CURSOR_DOWN OF FRAME frame1 ANYWHERE DO:

    if sorttype == 1:
        sorttype = 0

    elif sorttype == 0:
        sorttype = 1
    pass
    APPLY "entry" TO btn_exit
    ON CURSOR_UP OF FRAME frame1 ANYWHERE DO:

    if sorttype == 1:
        sorttype = 0

    elif sorttype == 0:
        sorttype = 1
    pass
    APPLY "entry" TO btn_exit
    ON CURSOR_RIGHT OF FRAME frame1 ANYWHERE DO:
    APPLY "entry" TO btn_cancel IN FRAME frame1
    ON cursor_left ANYWHERE DO:
    APPLY "entry" TO btn_exit IN FRAME frame1
    ON VALUE_CHANGED OF sorttype DO:
    sorttype


    APPLY "entry" TO btn_exit
    ON WINDOW_CLOSE OF FRAME frame1 DO:
    APPLY "choose" TO btn_cancel
    ON CHOOSE OF btn_exit DO:
    out_type = sorttype
    translatewidgetwinctx(FRAME frame1:HANDLE, lvcarea)
    VIEW FRAME frame1
    status INPUT ""
    ENABLE btn_exit btn_cancel sorttype WITH FRAME frame1
    FRAME frame1:LOAD_MOUSE_POINTER ("arrow")
    WAIT_FOR CHOOSE OF btn_exit, btn_cancel

    return generate_output()