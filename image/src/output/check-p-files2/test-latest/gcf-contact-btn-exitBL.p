
DEF TEMP-TABLE aktkont-list LIKE akt-kont.

DEF INPUT  PARAMETER TABLE FOR aktkont-list.
DEF INPUT  PARAMETER case-type  AS INT.
DEF INPUT  PARAMETER gastnr     AS INT.
DEF OUTPUT PARAMETER kont-nr    AS INTEGER.

DEF BUFFER gbuff FOR guest.  
DEF BUFFER abuff FOR akt-kont.

IF case-type = 1 THEN   /* add */
DO:
    FIND FIRST aktkont-list.
    kont-nr = 1. 
    FOR EACH abuff WHERE abuff.gastnr = gastnr NO-LOCK
        BY abuff.kontakt-nr DESCENDING:
        kont-nr = abuff.kontakt-nr + 1.
        LEAVE.
    END. 
    CREATE akt-kont.
    BUFFER-COPY aktkont-list EXCEPT kontakt-nr gastnr kategorie TO akt-kont.
    akt-kont.kategorie = 1.
    akt-kont.kontakt-nr = kont-nr. 
    akt-kont.gastnr = gastnr.
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
    FIND FIRST aktkont-list.
    FIND FIRST akt-kont WHERE akt-kont.kontakt-nr = aktkont-list.kontakt-nr
        EXCLUSIVE-LOCK.
    BUFFER-COPY aktkont-list EXCEPT kontakt-nr gastnr kategorie TO akt-kont.
END.
