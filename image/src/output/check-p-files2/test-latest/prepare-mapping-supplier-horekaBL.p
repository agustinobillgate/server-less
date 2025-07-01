DEFINE TEMP-TABLE supplier
    FIELD supplier-name AS CHAR
    FIELD lief-nr       AS CHAR
    FIELD supplierid    AS CHAR
.

DEFINE OUTPUT PARAMETER TABLE FOR supplier.

DEFINE BUFFER bqueasy FOR queasy.

FIND FIRST queasy WHERE queasy.KEY = 256 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN DO:
    FOR EACH l-lieferant NO-LOCK:
        CREATE supplier.
        ASSIGN supplier.supplier-name = l-lieferant.firma
               supplier.lief-nr       = STRING(l-lieferant.lief-nr)
        .
    END.
END.
ELSE DO:
    FOR EACH bqueasy WHERE bqueasy.KEY = 256 NO-LOCK:
        CREATE supplier.
        ASSIGN supplier.supplier-name = bqueasy.char1
               supplier.lief-nr       = bqueasy.char2
               supplier.supplierid    = bqueasy.char3
        .
    END.

    FOR EACH l-lieferant NO-LOCK:
        FIND FIRST supplier WHERE supplier.supplier-name = l-lieferant.firma
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE supplier THEN DO:
            CREATE supplier.
            ASSIGN supplier.supplier-name = l-lieferant.firma
                   supplier.lief-nr       = STRING(l-lieferant.lief-nr)
            .
        END.
    END.
END.
