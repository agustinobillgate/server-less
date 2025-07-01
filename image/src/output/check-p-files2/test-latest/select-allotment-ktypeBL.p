DEF TEMP-TABLE kline LIKE kontline.

DEF INPUT PARAMETER         kontignr    AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER  gastnr      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER         zikatno     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER        ktype       AS INTEGER NO-UNDO INIT -1.
DEF OUTPUT PARAMETER        rmtype      AS CHAR    NO-UNDO INIT "".
DEF OUTPUT PARAMETER TABLE FOR kline.

FIND FIRST zimkateg WHERE zimkateg.zikatnr = zikatno NO-LOCK.
ASSIGN rmtype = zimkateg.kurzbez.

FIND FIRST kontline WHERE kontline.gastnr = gastnr 
  AND kontline.betriebsnr = 0 
  AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE kontline THEN ktype = 0. 

FIND FIRST kontline WHERE kontline.gastnr = gastnr 
  AND kontline.betriebsnr = 1 
  AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE kontline THEN ktype = ktype + 2. 
 
IF ktype = -1 THEN /* check if defined as member of global allotment */
DO:
DEF VAR tokcounter AS INTEGER NO-UNDO.
DEF VAR mesValue   AS CHAR    NO-UNDO.
  FOR EACH queasy WHERE queasy.KEY = 147 NO-LOCK:
    DO tokcounter = 1 TO NUM-ENTRIES(queasy.char3, ","):
      mesValue = ENTRY(tokcounter, queasy.char3, ",").
      IF INTEGER(mesValue) = gastnr THEN
      DO:
        ASSIGN
            ktype  = 0
            gastnr = queasy.number1
        .
        LEAVE.
      END.
    END.
  END.
END.

FIND FIRST kontline WHERE kontline.kontignr = kontignr 
  AND kontline.kontstat = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE kontline THEN 
DO: 
  CREATE kline.
  BUFFER-COPY kontline TO kline.
END.
