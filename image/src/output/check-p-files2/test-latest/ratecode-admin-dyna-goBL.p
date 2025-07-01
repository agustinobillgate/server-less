DEFINE TEMP-TABLE dynaRate-list
  FIELD s-recid AS INTEGER
  FIELD counter AS INTEGER
  FIELD w-day   AS INTEGER FORMAT "9"     LABEL "WeekDay" INIT 0 /* week day 0=ALL, 1=Mon..7=Sun */
  FIELD rmType  AS CHAR    FORMAT "x(10)" LABEL "Room Type"
  FIELD fr-room AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1   AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2   AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD rCode   AS CHAR    FORMAT "x(18)" LABEL "RateCode"
.
DEFINE TEMP-TABLE drBuff LIKE dynaRate-list.

DEF INPUT PARAMETER curr-select AS CHAR NO-UNDO.
DEF INPUT PARAMETER inp-str      AS CHAR NO-UNDO.
DEF INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEF INPUT PARAMETER TABLE FOR drBuff.
DEF OUTPUT PARAMETER error-code  AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER TABLE FOR dynaRate-list.

DEF VARIABLE prcode     AS CHAR    NO-UNDO.
DEF VARIABLE bookengID  AS INTEGER NO-UNDO.
DEF VARIABLE a          AS CHAR    NO-UNDO.
DEF VARIABLE i          AS INTEGER NO-UNDO.

IF NUM-ENTRIES(inp-str,";") GT 1 THEN
    ASSIGN
        prcode = ENTRY(1,inp-str,";")
        bookengID = INT(ENTRY(2,inp-str,";"))
    .
ELSE prcode = inp-str.

IF bookengID = 0 THEN bookengID = 1.

FIND FIRST drBuff.
a = drBuff.rcode.
/*NAUFAL 100321 - perbaikan validasi agar tidak me replace ratcode yang ada spasi ditengahnya*/
IF SUBSTRING(a, LENGTH(a), 1) EQ " " THEN
DO:
    a = SUBSTRING(a, 1, LENGTH(a) - 1).
END.

/* SY 20/09/2014 */
IF drBuff.rmType NE "*" THEN 
DO:
  FIND FIRST zimkateg WHERE zimkateg.kurzbez = drBuff.rmType NO-LOCK NO-ERROR.
  IF NOT AVAILABLE zimkateg THEN
  DO: 
    error-code = 1.
    RETURN.
  END.
END.

FIND FIRST queasy WHERE queasy.KEY = 2 AND trim(queasy.char1) = /*drBuff.rCode*/ TRIM(a) NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
  error-code = 2.
  RETURN.
END.

/* SY 20/09/2014 */
IF drBuff.rmType EQ "*" THEN FIND FIRST ratecode WHERE trim(ratecode.CODE) = trim(queasy.char1) NO-LOCK NO-ERROR.
ELSE
FIND FIRST ratecode WHERE trim(ratecode.CODE) = trim(queasy.char1) AND ratecode.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE ratecode THEN
DO:
  error-code = 3.
  RETURN.
END.

IF curr-select = "add-rate" THEN curr-select = "insert".
IF curr-select = "insert"  THEN 
DO: 
  CREATE ratecode.
  CREATE dynaRate-list.
  RUN fill-dynamic-ratecode (prCode, YES). 
  FIND CURRENT ratecode NO-LOCK.
  RELEASE ratecode.

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:
        CREATE res-history.
        ASSIGN 
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Insert Dynamic RateCode, Code: " + prcode.
            res-history.action      = "RateCode".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END. 
ELSE IF curr-select = "chg-rate" THEN 
DO: 
  FIND FIRST ratecode WHERE RECID(ratecode) = drBuff.s-recid EXCLUSIVE-LOCK. 
  RUN fill-dynamic-ratecode(prCode, NO). 
  FIND CURRENT ratecode NO-LOCK. 

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:
        CREATE res-history.
        ASSIGN 
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Modify Dynamic RateCode, Code: " + prcode.
            res-history.action      = "RateCode".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END. 

PROCEDURE fill-dynamic-ratecode:
DEF INPUT PARAMETER prCode AS CHAR NO-UNDO.
DEF INPUT PARAMETER new-flag    AS LOGICAL  NO-UNDO.
DEF VARIABLE curr-counter       AS INTEGER  NO-UNDO.
    IF new-flag THEN
    DO:
      FIND FIRST counters WHERE counters.counter-no = 50 NO-ERROR.
      IF NOT AVAILABLE counters THEN
      DO:
        CREATE counters.
        ASSIGN
            counters.counter-no  = 50
            counters.counter-bez = "Counter for Dynamic Ratecode"
            counters.counter     = 0
        .
      END.
      counters.counter = counters.counter + 1.
      FIND CURRENT counters NO-LOCK.
      curr-counter = counters.counter.
    END.
    ELSE curr-counter = drbuff.counter.
    
   ASSIGN 
        ratecode.CODE     = prCode
        ratecode.char1[5] = "CN" + STRING(curr-counter)   + ";"
                          + "RT" + STRING(drBuff.rmType)  + ";"
                          + "WD" + STRING(drBuff.w-day)   + ";"
                          + "FR" + STRING(drBuff.fr-room) + ";"
                          + "TR" + STRING(drBuff.to-room) + ";"
                          + "D1" + STRING(drBuff.days1  ) + ";"
                          + "D2" + STRING(drBuff.days2)   + ";"
                          + "RC" + STRING(drBuff.rCode)   + ";".
    BUFFER-COPY drBuff EXCEPT drBuff.s-recid drBuff.rCode TO dynaRate-list.
    ASSIGN 
        dynaRate-list.s-recid = INTEGER(RECID(ratecode))
        dynaRate-list.rCode = a.

    IF bookengID NE 0 THEN RUN update-bookengine-config.
END.

PROCEDURE update-bookengine-config:
    DEFINE VARIABLE cm-gastno AS INT NO-UNDO INIT 0.
    DEFINE BUFFER qsy FOR queasy.
    DEFINE BUFFER bqueasy FOR queasy.
    DEFINE BUFFER qsy170 FOR queasy.

    DEFINE VARIABLE ifTask      AS CHAR INIT "".
    DEFINE VARIABLE mesToken    AS CHAR INIT "".
    DEFINE VARIABLE mesValue    AS CHAR INIT "".
    DEFINE VARIABLE tokcounter  AS INT  INIT 0.
    
    FIND FIRST qsy WHERE qsy.KEY = 159 AND qsy.number1 = bookengID NO-LOCK NO-ERROR.
    IF AVAILABLE qsy THEN 
    DO:
        FIND FIRST guest WHERE guest.gastnr = qsy.number2 NO-LOCK NO-ERROR.
        FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest-pr THEN
        DO:
            cm-gastno = guest.gastnr.
        END.
        ELSE RETURN.
    END.

    FOR EACH guest-pr WHERE guest-pr.gastnr = cm-gastno NO-LOCK,
        FIRST bqueasy WHERE bqueasy.KEY = 2 
        AND bqueasy.char1 = guest-pr.CODE 
        AND bqueasy.logi2 NO-LOCK 
        BY bqueasy.number3 DESCENDING /* min advance booking */
        BY bqueasy.deci3 DESCENDING   /* max advance booking */:

        IF prcode = guest-pr.CODE THEN
        DO:
            FIND FIRST qsy170 WHERE qsy170.KEY = 170 AND qsy170.char1 = prcode 
                AND qsy170.logi1 = NO AND qsy170.logi2 = NO NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE qsy170:
                FIND FIRST qsy WHERE RECID(qsy) = RECID(qsy170) EXCLUSIVE-LOCK NO-ERROR.
                IF AVAILABLE qsy THEN
                DO:
                    ASSIGN qsy.logi2 = YES.
                    FIND CURRENT qsy NO-LOCK.
                    RELEASE qsy.
                END.            
                FIND NEXT qsy170 WHERE qsy170.KEY = 170 AND qsy170.char1 = prcode 
                    AND qsy170.logi1 = NO AND qsy170.logi2 = NO NO-LOCK NO-ERROR.
            END.                                                                                   
            /*RUN update-bookengine-configbl.p (9,bookengID,YES,"").*/
            LEAVE.
        END. 
    END.
END.


