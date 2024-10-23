DEFINE INPUT PARAMETER  case-type      AS INTEGER.
DEFINE INPUT PARAMETER  rechnr         AS INTEGER.
DEFINE OUTPUT PARAMETER error-flag     AS INTEGER NO-UNDO.

DEFINE VARIABLE disc          AS INTEGER NO-UNDO.
DEFINE VARIABLE loopi         AS INTEGER NO-UNDO.

DEFINE BUFFER hbline FOR h-bill-line.

IF case-type = 1 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 557 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN disc = htparam.finteger.

    FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ rechnr NO-LOCK:
        IF h-bill-line.artnr EQ disc THEN
        DO:
            error-flag = 1.
            RETURN.
        END.
    END.
END.

ELSE IF case-type = 2 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 451 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN disc = INTEGER(ENTRY(1, htparam.fchar, ";")).

    FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ rechnr NO-LOCK:
        IF h-bill-line.artnr EQ disc THEN
        DO:
            error-flag = 1.
            RETURN.
        END.
    END.
END.

ELSE IF case-type = 3 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = 451 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN disc = INTEGER(ENTRY(1, htparam.fchar, ";")).

    FIND FIRST h-bill WHERE RECID(h-bill) EQ rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr NO-LOCK:
            IF h-bill-line.artnr EQ disc THEN
            DO:
                error-flag = 1.
                RETURN.
            END.
        END.
    END.    
END.
