DEFINE INPUT PARAMETER ss-artnr1    AS INT  NO-UNDO.
DEFINE INPUT PARAMETER ss-artnr2    AS INT  NO-UNDO.
DEFINE INPUT PARAMETER ss-artnr3    AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER ss-bezeich1 AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER ss-bezeich2 AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER ss-bezeich3 AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER ss-preis1   AS DEC  NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER ss-preis2   AS DEC  NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER ss-preis3   AS DEC  NO-UNDO INIT 0.

IF ss-artnr1 NE 0 THEN 
DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = ss-artnr1 NO-LOCK. 
    IF AVAILABLE l-artikel THEN 
        ASSIGN ss-bezeich1 = l-artikel.bezeich
               ss-preis1 = l-artikel.ek-aktuell. 
END. 
IF ss-artnr2 NE 0 THEN 
DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = ss-artnr2 NO-LOCK. 
    IF AVAILABLE l-artikel THEN 
        ASSIGN ss-bezeich2 = l-artikel.bezeich
               ss-preis2 = l-artikel.ek-aktuell. 
END. 
IF ss-artnr3 NE 0 THEN 
DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = ss-artnr3 NO-LOCK. 
    IF AVAILABLE l-artikel THEN 
        ASSIGN ss-bezeich3 = l-artikel.bezeich
               ss-preis3 = l-artikel.ek-aktuell. 
END. 
