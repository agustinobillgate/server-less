DEFINE INPUT PARAMETER mathis-nr AS INTEGER NO-UNDO.

FIND FIRST mathis WHERE mathis.nr = mathis-nr NO-LOCK NO-ERROR.
IF AVAILABLE mathis THEN DO:
    FIND CURRENT mathis EXCLUSIVE-LOCK. 
    DELETE mathis.
    RELEASE mathis.
END.

FIND FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr NO-LOCK NO-ERROR.
IF AVAILABLE fa-artikel THEN DO:
    FIND CURRENT fa-artikel EXCLUSIVE-LOCK. 
    DELETE fa-artikel. 
    RELEASE fa-artikel.
END.

FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = mathis.nr NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK. 
    DELETE queasy. 
    RELEASE queasy.
END.
