DEFINE TEMP-TABLE staff LIKE eg-staff
    FIELD staff-SELECTED AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER engid AS INT.
DEF INPUT PARAMETER m-PIC AS INT.
DEF OUTPUT PARAMETER avail-eg-staff AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER e-nr AS INT.
DEF OUTPUT PARAMETER e-name AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR staff.

FIND FIRST eg-staff WHERE 
    eg-staff.usergroup = engid AND 
    eg-staff.activeflag = YES AND 
    eg-staff.nr = m-PIC NO-LOCK NO-ERROR.
IF AVAILABLE eg-staff THEN
DO:
    avail-eg-staff = YES.
    e-nr = eg-staff.nr.
    e-name = eg-staff.NAME.
    RUN create-staff.
END.

PROCEDURE create-Staff:
    DEF BUFFER qbuff FOR eg-staff.

    FOR EACH staff :
        DELETE staff.
    END.

    FOR EACH qbuff WHERE qbuff.usergroup = engid  AND qbuff.activeflag = YES NO-LOCK:
        CREATE staff.
        ASSIGN staff.nr = qbuff.nr
           staff.NAME = qbuff.NAME
           staff.staff-SELECTED = NO.
    END.                                    
END.

