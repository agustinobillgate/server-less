
DEF INPUT PARAMETER rec-id AS INT.

FIND FIRST fa-lager WHERE RECID(fa-lager) = rec-id NO-LOCK NO-ERROR.
IF AVAILABLE fa-lager THEN
DO:
    FIND CURRENT fa-lager EXCLUSIVE-LOCK.
    delete fa-lager.
    RELEASE fa-lager.
END.
