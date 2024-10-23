
DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER str-list-billdate  AS DATE.
DEF INPUT  PARAMETER str-list-lief-nr   AS INT.
DEF INPUT  PARAMETER str-list-docu-nr   AS CHAR.
DEF INPUT  PARAMETER str-list-lscheinnr AS CHAR.
DEF INPUT  PARAMETER str-list-l-recid   AS INT.
DEF INPUT  PARAMETER str-list-artnr     AS INT.
DEF OUTPUT PARAMETER may-delete         AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER msg-str            AS CHAR.
DEF OUTPUT PARAMETER msg-str1           AS CHAR.
DEF OUTPUT PARAMETER msg-str2           AS CHAR.

DEF VARIABLE art-fibu                   AS CHAR NO-UNDO INIT "".

DEF BUFFER incoming-op FOR l-op.
DEF BUFFER l-op FOR l-op.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "supply-inlist".

FIND FIRST l-kredit WHERE l-kredit.lief-nr = str-list-lief-nr 
  AND l-kredit.name = str-list-docu-nr 
  AND l-kredit.lscheinnr = str-list-lscheinnr 
  AND l-kredit.opart GE 1 AND l-kredit.zahlkonto GT 0 NO-LOCK NO-ERROR. 
IF AVAILABLE l-kredit THEN 
DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("The A/P Payment record found.",lvCAREA,"")
            + CHR(10)
            + translateExtended ("Cancel Receiving is no longer possible.",lvCAREA,"").
    RETURN.
END.

FIND FIRST l-artikel WHERE l-artikel.artnr = str-list-artnr NO-LOCK.
FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto
    NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN art-fibu = gl-acct.fibukonto.

IF art-fibu NE "" THEN
DO:
/* search if stock incoming GL journal exists */
  FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE str-list-billdate
    AND gl-jouhdr.jtyp = 6 AND gl-jouhdr.refno MATCHES "RCV*" NO-LOCK:
    FIND FIRST gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
        AND gl-journal.fibukonto = art-fibu NO-LOCK NO-ERROR.
    IF AVAILABLE gl-journal THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Stock receiving records have been transfered to the G/L.",lvCAREA,"")
                + CHR(10)
                + translateExtended ("Cancel Receiving is no longer possible.",lvCAREA,"").
        LEAVE.
    END.
  END.
/* search if stock outgoing GL journal exists */
  FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE str-list-billdate
    AND gl-jouhdr.jtyp = 3 AND gl-jouhdr.refno MATCHES "OUT*" NO-LOCK:
    FIND FIRST gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
        AND gl-journal.fibukonto = art-fibu NO-LOCK NO-ERROR.
    IF AVAILABLE gl-journal THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Stock outgoing records have been transfered to the G/L.",lvCAREA,"")
                + CHR(10)
                + translateExtended ("Cancel outgoing is no longer possible.",lvCAREA,"").
        LEAVE.
    END.
  END.
END.

IF msg-str NE "" THEN RETURN.

RUN check-onhand-after-cancel-receiving. 
IF NOT may-delete THEN RETURN.

/*MT check outgoing transaction */
FIND FIRST l-op WHERE l-op.datum GE str-list-billdate 
    AND l-op.artnr = str-list-artnr
    AND l-op.op-art GE 2 AND l-op.op-art LE 4
    AND NOT l-op.flag NO-LOCK NO-ERROR.
IF AVAILABLE l-op THEN
DO:
    msg-str2 = "&W" 
             + translateExtended ("Stock receiving record(s) exist for this article.",lvCAREA,"")
             + CHR(10)
             + translateExtended ("The stock receiving amount will be adjusted. ",lvCAREA,"").
END.

PROCEDURE check-onhand-after-cancel-receiving: 
DEFINE VARIABLE f-endkum        AS INTEGER  NO-UNDO. 
DEFINE VARIABLE b-endkum        AS INTEGER  NO-UNDO. 
DEFINE VARIABLE m-endkum        AS INTEGER  NO-UNDO. 
DEFINE VARIABLE billdate        AS DATE     NO-UNDO. 
DEFINE VARIABLE fb-closedate    AS DATE     NO-UNDO. 
DEFINE VARIABLE m-closedate     AS DATE     NO-UNDO. 
DEFINE VARIABLE qty             AS DECIMAL  NO-UNDO. 
DEFINE VARIABLE trf-gl          AS DATE     NO-UNDO. /* Add by Michael @ 03/07/2019 for using htparam transfer to G/L date - ticket no 653938 */
 
  IF str-list-l-recid = 0 THEN
  DO:
      msg-str1 = msg-str1 + CHR(2)
               + translateExtended ("Old record(s) can not be deleted,",lvCAREA,"")
               + translateExtended ("Cancel Receiving not possible.",lvCAREA,"").
      RETURN.
  END.

  FIND FIRST l-op WHERE RECID(l-op) = str-list-l-recid NO-LOCK. 
  IF l-op.flag THEN  /* indicates direct issue */ 
  DO: 
      may-delete = YES.
      RETURN.
  END.
 
  /* Add by Michael @ 03/07/2019 for using htparam transfer to G/L date - ticket no 653938 */
  FIND FIRST htparam WHERE htparam.paramnr EQ 269 NO-LOCK NO-ERROR.
  IF AVAILABLE htparam THEN ASSIGN trf-gl = htparam.fdate.
  /* End of add */

  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
  m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
  fb-closedate = htparam.fdate. 
  FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
  m-closedate = htparam.fdate. 

/* check stock onhand */
  IF ((l-artikel.endkum = f-endkum OR l-artikel.endkum = b-endkum) 
    AND str-list-billdate GT fb-closedate) OR (l-artikel.endkum GE m-endkum 
    AND str-list-billdate GT m-closedate) THEN 
  DO: 
      may-delete = YES.
      RETURN. 
  END.
 
  FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
    AND l-bestand.lager-nr = l-op.lager-nr NO-LOCK NO-ERROR. 
  qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang 
    - l-op.anzahl. 
  IF qty LT 0 THEN 
  DO: 
    msg-str1 = msg-str1 + CHR(2)
             + translateExtended ("Onhand QTY in Store ",lvCAREA,"")
             + STRING(l-op.lager-nr,"99")
             + " " + translateExtended ("would become (-) =",lvCAREA,"")
             + " " + TRIM(STRING(qty,"->,>>>,>>>,>>9.99"))
             + CHR(10)
             + translateExtended ("Cancel Receiving not possible.",lvCAREA,""). 
    RETURN.
  END.
  
  may-delete = YES.

  /* Add by Michael @ 03/07/2019 for using htparam transfer to G/L date - ticket no 653938 */
  IF str-list-billdate LE trf-gl THEN
  DO:
      may-delete = NO.
      msg-str1 = msg-str1 + CHR(2)
               + translateExtended ("Receiving have been transfered to the G/L, ",lvCAREA,"")
               + translateExtended ("cancel Receiving not possible.",lvCAREA,"").
      RETURN.
  END.
  /* End of add */
END. 

