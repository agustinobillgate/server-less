DEF TEMP-TABLE f-ratecode
    FIELD foreign-rate      AS LOGICAL
    FIELD double-currency   AS LOGICAL
    FIELD local-nr          AS INTEGER
    FIELD foreign-nr        AS INTEGER INIT 0
.

DEFINE TEMP-TABLE tb1 LIKE queasy
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr  
    FIELD wabkurz       LIKE waehrung.wabkurz  
    FIELD active-flag   AS LOGICAL
    FIELD rcode-element AS CHAR
.

DEF INPUT PARAMETER pvILanguage AS INTEGER      NO-UNDO.
DEF OUTPUT PARAMETER msg-str    AS CHAR INIT "" NO-UNDO.
DEF OUTPUT PARAMETER TABLE      FOR f-ratecode.
DEF OUTPUT PARAMETER TABLE      FOR tb1.

/*
DEF VARIABLE pvILanguage AS INTEGER      NO-UNDO.
DEF VARIABLE msg-str     AS CHAR INIT "" NO-UNDO.
*/

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ratecode-admin". 
DEFINE VARIABLE cidate AS DATE.

DEFINE BUFFER bqueasy FOR queasy.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN cidate = htparam.fdate.

CREATE f-ratecode.

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN f-ratecode.foreign-rate = htparam.flogical.
 

FIND FIRST htparam WHERE htparam.paramnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN ASSIGN f-ratecode.double-currency = htparam.flogical. 

  
FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN 
DO:
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE waehrung THEN 
  DO: 
    msg-str = translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)",lvCAREA,""). 
    RETURN. 
  END. 
  ASSIGN f-ratecode.local-nr = waehrung.waehrungsnr.
END.
 

IF f-ratecode.foreign-rate THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam THEN
  DO:
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE waehrung THEN 
    DO: 
       msg-str = translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)",lvCAREA,"").
      RETURN. 
    END. 
    f-ratecode.foreign-nr = waehrung.waehrungsnr. 
  END.
END.
RUN update-queasy. 
/*RUN update-prtable.*/

FOR EACH queasy WHERE queasy.key = 2 NO-LOCK, 
  FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 
  NO-LOCK BY queasy.logi2 DESC BY queasy.char2: 
  CREATE tb1.
  BUFFER-COPY waehrung TO tb1.
  BUFFER-COPY queasy TO tb1.
  /*add*/
  IF queasy.logi2= NO THEN
  DO:
      FIND FIRST ratecode WHERE ratecode.CODE = queasy.char1 NO-LOCK NO-ERROR.
      IF AVAILABLE ratecode THEN
      DO:
          FIND FIRST ratecode WHERE ratecode.CODE = queasy.char1 AND ratecode.endperiode GE cidate NO-LOCK NO-ERROR.
          IF AVAILABLE ratecode THEN
              tb1.logi3 = YES.
      END.
      ELSE tb1.logi3 = YES.
  END.
  /* Malik Serverless 314 */
  IF queasy.date2 NE ? THEN
  DO:
    IF queasy.date2 LT cidate THEN tb1.logi3 = NO.
  END.
  /* END Malik */
  /* IF queasy.date2 LT cidate THEN tb1.logi3 = NO. */

  FIND FIRST bqueasy WHERE bqueasy.KEY = 264
        AND bqueasy.char1 = queasy.char1 NO-LOCK NO-ERROR.
  IF AVAILABLE bqueasy THEN ASSIGN tb1.active-flag = bqueasy.logi1.
  
  /*Alder - Ticket C0DB81 - Start*/
  FIND FIRST bqueasy WHERE bqueasy.KEY EQ 289
      AND bqueasy.char1 EQ queasy.char1 
      NO-LOCK NO-ERROR.
  IF AVAILABLE bqueasy THEN 
  DO:
      ASSIGN tb1.rcode-element = bqueasy.char2.
  END.
  /*Alder - Ticket C0DB81 - End*/
END.
/*end add*/

PROCEDURE update-queasy: 
DEF BUFFER qsy FOR queasy.  
  FIND FIRST qsy WHERE qsy.key = 18 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE qsy THEN 
  DO: 
    FOR EACH prmarket NO-LOCK BY prmarket.bezeich: 
      CREATE qsy. 
      ASSIGN 
        qsy.key     = 18 
        qsy.number1 = prmarket.nr
      . 
      RELEASE qsy. 
    END. 
  END. 
  FIND FIRST queasy WHERE queasy.key = 2 AND queasy.number1 = 0 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE queasy THEN RETURN. 
  FOR EACH queasy WHERE queasy.key = 2 AND queasy.number1 = 0: 
    IF (NOT f-ratecode.foreign-rate) OR queasy.logi1 THEN 
      queasy.number1 = f-ratecode.local-nr. 
    ELSE queasy.number1 = f-ratecode.foreign-nr. 
  END. 
END. 

PROCEDURE update-prtable:
DEF BUFFER prbuff FOR prtable.
DEF VARIABLE curr-i AS INTEGER NO-UNDO.
    FIND FIRST prbuff NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE prbuff:
      DO TRANSACTION:
        FIND FIRST prtable WHERE RECID(prtable) 
            = RECID(prbuff) EXCLUSIVE-LOCK.
        
        DO curr-i = 1 TO 99:
            ASSIGN
                prtable.zikatnr[curr-i] = 0
                prtable.argtnr[curr-i]  = 0
            .
        END.

        curr-i = 0.
        FOR EACH zimkateg NO-LOCK BY zimkateg.zikatnr:
            curr-i = curr-i + 1.
            ASSIGN prtable.zikatnr[curr-i] = zimkateg.zikatnr.
        END.

        curr-i = 0.
        FOR EACH arrangement WHERE NOT arrangement.weeksplit 
            AND arrangement.segmentcode = 0 NO-LOCK BY arrangement.argtnr:
            curr-i = curr-i + 1.
            ASSIGN prtable.argtnr[curr-i] = arrangement.argtnr.
        END.
        FIND CURRENT prtable NO-LOCK.
      END.
      FIND NEXT prbuff NO-LOCK NO-ERROR.
    END.
END.
