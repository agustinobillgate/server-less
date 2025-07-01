
DEFINE TEMP-TABLE queasy-19
    FIELD number1 LIKE queasy.number1
    FIELD char3 LIKE queasy.char3.

DEFINE TEMP-TABLE Dept
    FIELD dept-nr  AS INTEGER 
    FIELD dept-nm AS CHAR FORMAT "x(36)" COLUMN-LABEL "Department".

DEFINE TEMP-TABLE UserSkill
    FIELD Categ-nr  AS INTEGER
    FIELD Categ-nm  AS CHAR     FORMAT "x(30)"
    FIELD Categ-sel AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE t-eg-staff LIKE eg-staff
    FIELD rec-id AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR Dept.
DEF OUTPUT PARAMETER TABLE FOR UserSkill.
DEF OUTPUT PARAMETER TABLE FOR t-eg-staff.
DEF OUTPUT PARAMETER TABLE FOR queasy-19.

RUN define-group.
RUN define-engineering.

RUN create-dept.
/*RUN create-User.*/
RUN create-Skill.

FOR EACH eg-staff:
    CREATE t-eg-staff.
    BUFFER-COPY eg-staff TO t-eg-staff.
    ASSIGN t-eg-staff.rec-id = RECID(eg-staff).
END.

FOR EACH queasy WHERE queasy.KEY = 19:
    CREATE queasy-19.
    ASSIGN
    queasy-19.number1 = queasy.number1
    queasy-19.char3 = queasy.char3.
END.

PROCEDURE Define-engineering:
/*
    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.CHAR3 = "Engineering" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN EngID = queasy.number1.
    END.
*/
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        ASSIGN EngID = 0.
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION.*/
    END.
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-Skill:
    FOR EACH UserSkill :
        DELETE UserSkill.
    END.

    FOR EACH queasy WHERE queasy.KEY = 132 NO-LOCK BY queasy.number1 :
        CREATE UserSkill.
        ASSIGN  UserSkill.Categ-nr  = queasy.number1
                UserSkill.Categ-nm  = queasy.char1
                UserSkill.Categ-sel = NO.
    END.
END.

PROCEDURE create-dept:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH dept:
        DELETE dept.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 19 NO-LOCK:
        CREATE dept.
        ASSIGN dept.dept-nr = qbuff.number1
            dept.dept-nm = qbuff.char3.
    END.                                    
END.
