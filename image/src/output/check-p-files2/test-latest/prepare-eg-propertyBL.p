DEFINE TEMP-TABLE queasy-133 LIKE queasy.

DEFINE TEMP-TABLE Maintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm AS CHAR FORMAT "x(36)" COLUMN-LABEL "Object".

DEFINE TEMP-TABLE Location
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm AS CHAR FORMAT "x(36)" COLUMN-LABEL "Location".

DEFINE TEMP-TABLE t-eg-property LIKE eg-property.
DEFINE TEMP-TABLE t-eg-location LIKE eg-location.
DEFINE TEMP-TABLE t-zimmer LIKE zimmer.

DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER EngId      AS INT.
DEF OUTPUT PARAMETER GroupID    AS INT.
DEF OUTPUT PARAMETER TABLE FOR Maintask.
DEF OUTPUT PARAMETER TABLE FOR Location.
DEF OUTPUT PARAMETER TABLE FOR t-eg-property.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR queasy-133.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.


RUN define-group.
RUN define-engineering.

RUN create-Location.
RUN create-maintask.

FOR EACH eg-location:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.

FOR EACH eg-property NO-LOCK:
    CREATE t-eg-property.
    BUFFER-COPY eg-property TO t-eg-property.
END.

FOR EACH queasy WHERE queasy.KEY = 133:
    CREATE queasy-133.
    BUFFER-COPY queasy TO queasy-133.
END.

FOR EACH zimmer:
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
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
            VIEW-AS ALERT-BOX INFORMATION. 
        */
    END.
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-Location:
    DEF BUFFER qbuff FOR eg-location.

    FOR EACH Location:
        DELETE Location.
    END.

    FOR EACH qbuff NO-LOCK:
        CREATE Location.
        ASSIGN Location.loc-nr = qbuff.nr
            Location.loc-nm = qbuff.bezeich.
    END.                                    
END.

PROCEDURE create-maintask:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH Maintask:
        DELETE Maintask.
    END.

    FOR EACH qbuff WHERE qbuff.KEY= 133 NO-LOCK:
        CREATE Maintask.
        ASSIGN Maintask.Main-nr = qbuff.number1
            Maintask.Main-nm = qbuff.char1.
    END.                                    
END.


