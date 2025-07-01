DEFINE TEMP-TABLE t-eg-cost LIKE eg-cost
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE t-eg-resources LIKE eg-resources
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE t-eg-budget LIKE eg-budget.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-eg-resources.
DEF OUTPUT PARAMETER TABLE FOR t-eg-cost.
DEF OUTPUT PARAMETER TABLE FOR t-eg-budget.

RUN define-group.
RUN define-engineering.

FOR EACH eg-resources:
    CREATE t-eg-resources.
    BUFFER-COPY eg-resources TO t-eg-resources.
    ASSIGN t-eg-resources.rec-id = RECID(eg-resources).
END.

FOR EACH eg-cost:
    CREATE t-eg-cost.
    BUFFER-COPY eg-cost TO t-eg-cost.
END.

FOR EACH eg-budget:
    CREATE t-eg-budget.
    BUFFER-COPY eg-budget TO t-eg-budget.
END.

PROCEDURE Define-engineering:
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

