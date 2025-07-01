DEFINE TEMP-TABLE g-list 
  FIELD jnr             LIKE gl-journal.jnr 
  FIELD fibukonto       LIKE gl-journal.fibukonto
  FIELD acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD debit           LIKE gl-journal.debit 
  FIELD credit          LIKE gl-journal.credit 
  FIELD userinit        LIKE gl-journal.userinit 
  FIELD sysdate         LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit            LIKE gl-journal.zeit 
  FIELD chginit         LIKE gl-journal.chginit 
  FIELD chgdate         LIKE gl-journal.chgdate INITIAL ? 
  FIELD bemerk          LIKE gl-journal.bemerk
  FIELD bezeich         LIKE gl-acct.bezeich
  FIELD duplicate       AS LOGICAL INITIAL YES
  /*gst for penang*/
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS CHAR
  FIELD tot-amt     AS CHAR.

DEF INPUT  PARAMETER TABLE FOR g-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER curr-step      AS INTEGER.
DEF INPUT  PARAMETER bezeich        AS CHAR.
DEF INPUT  PARAMETER credits        LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER debits         LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER remains        LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER refno          AS CHAR.
DEF INPUT  PARAMETER datum          AS DATE.
DEF INPUT  PARAMETER adjust-flag    AS LOGICAL.
DEF INPUT  PARAMETER journaltype    AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER curr-jnr       AS INTEGER  INIT 0.
DEF OUTPUT PARAMETER msg-str        AS CHAR     INIT "".
DEF OUTPUT PARAMETER error-flag     AS LOGICAL.

DEF VARIABLE f-date                 AS DATE     NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-postjourn".

IF curr-step = 1 THEN 
DO:
  RUN check-date.
  RETURN.
END. 
ELSE IF curr-step = 2 THEN 
DO: 
    RUN create-header. 
    RUN create-journals.
END. 

PROCEDURE check-date:
DEF VARIABLE acct-date      AS DATE NO-UNDO.
DEF VARIABLE last-acctdate  AS DATE NO-UNDO.
DEF VARIABLE jou-date       AS DATE NO-UNDO.
DEF VARIABLE close-year     AS DATE NO-UNDO.

  IF NOT adjust-flag THEN FIND FIRST htparam WHERE htparam.paramnr = 372 NO-LOCK.   
  /* journal posting DATE */ 
  ELSE FIND FIRST htparam WHERE htparam.paramnr = 795 NO-LOCK.   
  /* LAST year closing DATE */ 
  
  ASSIGN jou-date = htparam.fdate. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK.   /* LAST Accounting Period */ 
  ASSIGN last-acctdate = htparam.fdate. 
  
  FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK.   /* CURRENT Accounting Period */ 
  ASSIGN acct-date = htparam.fdate. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 795 NO-LOCK. 
  ASSIGN close-year = htparam.fdate. 

  IF acct-date = ? OR last-acctdate = ? OR jou-date = ? 
    OR close-year = ? THEN 
  DO:
    ASSIGN msg-str = translateExtended ("Accounting Date is not defined.",lvCAREA,"") 
     + CHR(10)
     + translateExtended ("(ParamNo 372, 558, 597, 975)",lvCAREA,"").
    error-flag = YES.
    RETURN.
  END.
  ELSE 
  DO: 
    IF (datum LE last-acctdate) AND NOT adjust-flag THEN 
    DO: 
      msg-str = translateExtended ("Wrong Posting Date",lvCAREA,"") 
        + CHR(10)
        + translateExtended ("Last Closing Date :",lvCAREA,"") + " " + STRING(last-acctdate) 
        + CHR(10) 
        + translateExtended ("Current Closing Date :",lvCAREA,"") + " " + STRING(acct-date).
      error-flag = YES.
      RETURN.
    END. 
    IF datum GT TODAY THEN 
    DO: 
      msg-str = translateExtended ("Posting Date can not be later then TODAY.",lvCAREA,"").
      error-flag = YES.
      RETURN.
    END. 

    RUN htpdate.p (404, OUTPUT f-date).
    IF f-date NE ? AND journaltype = 5 AND (datum LE f-date) THEN 
    DO: 
      msg-str = translateExtended ("Wrong Posting Date.",lvCAREA,"") + "  " + 
        translateExtended ("Last G/C Closing Date :",lvCAREA,"") + " " + STRING(f-date,"99/99/9999").
      error-flag = YES.
      RETURN. 
    END. 

    IF NOT adjust-flag THEN
    DO:
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jtype = journaltype 
          AND gl-jouhdr.datum GT datum AND gl-jouhdr.activeflag = 0 
              NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-jouhdr THEN 
        ASSIGN 
          msg-str = "&W"
            + translateExtended ("Transaction journal found with LATER posting date :",lvCAREA,"") 
            + CHR(10) 
            + STRING(gl-jouhdr.datum ) + " - " + gl-jouhdr.refno 
            + CHR(10) 
            + translateExtended ("Please re-check the entered posting date.",lvCAREA,"")
        .
    END.
  END. 
END.

PROCEDURE create-header: 
    FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      ASSIGN
        counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,"") + ""
        counters.counter-no  = 25
      . 
    END. 
    counters.counter = counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 
    CREATE gl-jouhdr. 
    ASSIGN 
      gl-jouhdr.jnr     = counters.counter 
      gl-jouhdr.refno   = refno 
      gl-jouhdr.datum   = datum
      gl-jouhdr.bezeich = bezeich 
      gl-jouhdr.jtype   = journaltype 
      gl-jouhdr.batch   = (journaltype GT 0)
      gl-jouhdr.credit  = credits 
      gl-jouhdr.debit   = debits 
      curr-jnr          = counters.counter
    . 
    FIND CURRENT gl-jouhdr NO-LOCK. 

    /*Alder - 958EFC*/
    RUN update-queasy-345( 
        INPUT curr-jnr,
        INPUT datum,
        INPUT bezeich).
END. 

PROCEDURE create-journals: 
  FOR EACH g-list WHERE g-list.duplicate = NO NO-LOCK: 
    CREATE gl-journal. 
    BUFFER-COPY g-list TO gl-journal.
    ASSIGN gl-journal.jnr = curr-jnr.
    FIND CURRENT gl-journal NO-LOCK.
  END. 
END. 

/*Alder - 958EFC - Start*/
PROCEDURE update-queasy-345:
    DEFINE INPUT PARAMETER jnr AS INTEGER NO-UNDO.
    DEFINE INPUT PARAMETER datum AS DATE NO-UNDO.
    DEFINE INPUT PARAMETER bezeich AS CHARACTER NO-UNDO.

    FIND FIRST queasy WHERE queasy.KEY EQ 345
        AND queasy.number1 EQ jnr
        AND queasy.date1 EQ datum
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN
            queasy.logi1 = YES
            queasy.logi2 = NO
            queasy.logi3 = NO.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 345
            queasy.number1 = jnr
            queasy.number2 = TIME
            queasy.char1 = bezeich
            queasy.date1 = datum
            queasy.logi1 = YES
            queasy.logi2 = NO
            queasy.logi3 = NO.
        RELEASE queasy.
    END.
END PROCEDURE.
/*Alder - 958EFC - End*/
