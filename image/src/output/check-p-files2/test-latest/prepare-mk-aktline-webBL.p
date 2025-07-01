
DEF TEMP-TABLE t-akthdr   LIKE akthdr
    FIELD akt-code-bezeich LIKE akt-code.bezeich
    FIELD akt-kont-anrede  LIKE akt-kont.anrede
    FIELD akt-kont-name    LIKE akt-kont.name
    FIELD akt-kont-vorname LIKE akt-kont.vorname.
DEF TEMP-TABLE t-akt-code LIKE akt-code.
DEF TEMP-TABLE akt-line1 LIKE akt-line.

DEF INPUT  PARAMETER aktnr          AS INT.
DEF INPUT  PARAMETER inp-gastnr     AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER lname          AS CHAR.
DEF OUTPUT PARAMETER guest-gastnr   AS INT.
DEF OUTPUT PARAMETER p-400          AS CHAR.
DEF OUTPUT PARAMETER p-405          AS CHAR.
DEF OUTPUT PARAMETER p-406          AS CHAR.
DEF OUTPUT PARAMETER p-407          AS CHAR.
DEF OUTPUT PARAMETER zeit           AS CHAR.
DEF OUTPUT PARAMETER dauer          AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-akthdr.
DEF OUTPUT PARAMETER TABLE FOR t-akt-code.
DEF OUTPUT PARAMETER TABLE FOR akt-line1.

IF aktnr NE 0 THEN
DO:
    FOR EACH akthdr WHERE akthdr.aktnr = aktnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 
        AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr 
              AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK:
        CREATE t-akthdr.
        BUFFER-COPY akthdr TO t-akthdr.
        ASSIGN 
            akt-code-bezeich = akt-code.bezeich
            akt-kont-anrede  = akt-kont.anrede
            akt-kont-name    = akt-kont.name
            akt-kont-vorname = akt-kont.vorname.
    END.    
END.

IF inp-gastnr > 0 THEN
DO:
  FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK.
  lname = guest.NAME + ", " + guest.anredefirma.
  guest-gastnr = guest.gastnr.
END.

FOR EACH akt-code WHERE akt-code.aktiongrup = 1 NO-LOCK BY akt-code.aktionscode:
    CREATE t-akt-code.
    BUFFER-COPY akt-code TO t-akt-code.
END.

FIND FIRST htparam WHERE paramnr = 400 NO-LOCK. 
p-400 = htparam.fchar.
FIND FIRST htparam WHERE paramnr = 405 NO-LOCK. 
p-405 = htparam.fchar.
FIND FIRST htparam WHERE paramnr = 406 NO-LOCK. 
p-406 = htparam.fchar.
FIND FIRST htparam WHERE paramnr = 407 NO-LOCK. 
p-407 = htparam.fchar.

CREATE akt-line1. 
IF aktnr NE 0 THEN
DO:
    FOR EACH t-akthdr NO-LOCK:
        ASSIGN akt-line1.regard = "Follow up on the " + t-akthdr.bezeich 
            + " opportunity, " + akt-code-bezeich + " stage".
        ASSIGN akt-line1.kontakt = akt-kont-name + ", " + akt-kont-vorname 
             + " " + akt-kont-anrede. 
    END.
END.

ASSIGN
    akt-line1.aktnr = aktnr
    akt-line1.userinit = user-init 
    akt-line1.datum = TODAY
    zeit = SUBSTR(STRING(TIME, "HH:MM"), 1, 2)
         + SUBSTR(STRING(TIME, "HH:MM"), 4, 2)
    akt-line1.zeit = INTEGER(SUBSTR(zeit, 1, 2)) * 3600 
         + INTEGER(SUBSTR(zeit, 3, 2)) * 60
    dauer = zeit
    akt-line1.dauer = akt-line1.zeit.

IF inp-gastnr > 0 THEN
DO:
    ASSIGN akt-line1.gastnr = inp-gastnr.
    akt-line1.gastnr = guest-gastnr.  
END.

