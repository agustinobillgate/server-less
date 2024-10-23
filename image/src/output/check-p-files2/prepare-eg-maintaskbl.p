DEFINE TEMP-TABLE tCategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR FORMAT "x(30)"
    FIELD str      AS CHAR FORMAT "x".
DEFINE TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-queasy132 LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-queasy132.
DEF OUTPUT PARAMETER TABLE FOR tCategory.

RUN define-group.
RUN define-engineering.
RUN create-categ.
FOR EACH queasy WHERE queasy.KEY = 133 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
    ASSIGN t-queasy.rec-id = RECID(queasy).
END.
FOR EACH queasy WHERE queasy.KEY = 132 NO-LOCK:
    CREATE t-queasy132.
    BUFFER-COPY queasy TO t-queasy132.
    ASSIGN t-queasy132.rec-id = RECID(queasy).
END.

PROCEDURE create-categ:
    DEFINE BUFFER qbuff FOR queasy.

    FOR EACH tcategory:
        DELETE tcategory.
    END.
    
    CREATE tcategory.
    ASSIGN tcategory.categ-nr = 0
           tcategory.categ-nm = "".

    FOR EACH qbuff WHERE qbuff.KEY = 132 NO-LOCK:
        CREATE tcategory.
        ASSIGN tcategory.categ-nr = qbuff.number1
            tcategory.categ-nm    = qbuff.CHAR1.
    END.
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


