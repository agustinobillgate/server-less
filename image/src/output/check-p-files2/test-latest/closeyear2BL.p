
DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF INPUT PARAMETER curr-yr     AS INTEGER.
DEF INPUT PARAMETER curr-date   AS DATE.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.

DEF BUFFER gl-acc1  FOR gl-acct. 
DEF BUFFER gl-hbuff FOR gl-accthis.

DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE last-2yr AS DATE. 
DEFINE VARIABLE yy AS INTEGER. 

DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 983 EXCLUSIVE-LOCK. 
  htparam.flogical = YES.   /* set running flag */ 
END. 

FOR EACH gl-acct NO-LOCK: 
    CREATE t-gl-acct.
    BUFFER-COPY gl-acct TO t-gl-acct.
END. 

/* !!! */
/*** check if gl-accthis found for curr-yr, delete the records *****/
FIND FIRST gl-accthis WHERE gl-accthis.YEAR = curr-yr NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE gl-accthis: 
  DO TRANSACTION:
    FIND FIRST gl-hbuff WHERE RECID(gl-hbuff) = RECID(gl-accthis)
        EXCLUSIVE-LOCK.
    DELETE gl-hbuff.
    RELEASE gl-hbuff.
  END.
  FIND NEXT gl-accthis WHERE gl-accthis.YEAR = curr-yr NO-LOCK NO-ERROR. 
END.
 
/* !!! */
FIND FIRST gl-acct NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE gl-acct: 
  DO TRANSACTION: 
    CREATE gl-accthis. 
    BUFFER-COPY gl-acct TO gl-accthis. 
    ASSIGN gl-accthis.YEAR = curr-yr. 
    FIND CURRENT gl-accthis NO-LOCK. 
    RELEASE gl-accthis.
    FIND FIRST gl-acc1 WHERE RECID(gl-acc1) = RECID(gl-acct).
    DO i = 1 TO 12: 
      ASSIGN 
        gl-acc1.last-yr[i]   = gl-acc1.actual[i] 
        gl-acc1.actual[i]    = 0 
        gl-acc1.ly-budget[i] = gl-acc1.budget[i] 
        gl-acc1.budget[i]    = gl-acc1.debit[i] 
        gl-acc1.debit[i]     = 0
      . 
    END. 
    FIND CURRENT gl-acc1 NO-LOCK.
  END. 
  FIND NEXT gl-acct NO-LOCK NO-ERROR. 
END. 
 
last-2yr = DATE(1, 1, (curr-yr - 1)). 
FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LT last-2yr NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE gl-jouhdr: 
  DO TRANSACTION:    
/*    
    IF CONNECTED("vhparch") THEN RUN closeyear-arch.p (gl-jouhdr.jnr).
    ELSE 
*/    
    DO:
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr: 
            CREATE vhp.gl-jourhis. 
            BUFFER-COPY gl-journal TO vhp.gl-jourhis. 
            ASSIGN vhp.gl-jourhis.datum = gl-jouhdr.datum. 
            FIND CURRENT vhp.gl-jourhis NO-LOCK. 
            RELEASE vhp.gl-jourhis. 
            DELETE gl-journal. 
        END. 
        CREATE vhp.gl-jhdrhis. 
        BUFFER-COPY gl-jouhdr TO gl-jhdrhis. 
        FIND CURRENT vhp.gl-jhdrhis NO-LOCK. 
        FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
        DELETE gl-jouhdr. 
    END. 
    FIND NEXT gl-jouhdr WHERE gl-jouhdr.datum LT last-2yr NO-LOCK NO-ERROR. 
  END.
END. 
RELEASE gl-journal.
RELEASE gl-jouhdr.

/********* UPDATE NEW closing DATE *****/ 
 
DO TRANSACTION: 
 
  FIND FIRST htparam WHERE paramnr = 983 EXCLUSIVE-LOCK. 
  htparam.flogical = NO. 
  FIND CURRENT htparam NO-LOCK. 
 
  FIND FIRST htparam WHERE paramnr = 795 EXCLUSIVE-LOCK. /* LAST CLOSE year DATE */ 
  ASSIGN 
      curr-date = htparam.fdate
      yy = YEAR(curr-date) + 1 
      htparam.fdate = DATE(month(curr-date), DAY(curr-date), yy)
      htparam.lupdate = TODAY
      htparam.fdefault = user-init + " - " + STRING(TIME, "HH:MM:SS").
  FIND CURRENT htparam NO-LOCK. 
 
/* !!! */
  FIND FIRST htparam WHERE paramnr = 599 NO-LOCK. 
  IF htparam.flogical THEN 
  DO: 
  DEFINE BUFFER gl-acct1 FOR gl-acct. 
  DEFINE BUFFER gbuff    FOR gl-accthis.
  DEFINE BUFFER gbuff1   FOR gl-accthis.

    FIND FIRST htparam WHERE paramnr = 979 NO-LOCK. /* RE accont */
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar EXCLUSIVE-LOCK. 
        
    FIND FIRST htparam WHERE paramnr = 612 NO-LOCK. /* current Year RE acct */
    FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = htparam.fchar EXCLUSIVE-LOCK. 
    
    /* gl-accthis */
    FIND FIRST gbuff WHERE gbuff.fibukonto = gl-acct.fibukonto
        AND gbuff.YEAR = curr-yr EXCLUSIVE-LOCK. 
    FIND FIRST gbuff1 WHERE gbuff1.fibukonto = gl-acct1.fibukonto
        AND gbuff1.YEAR = curr-yr EXCLUSIVE-LOCK. 
    
    DO i = 1 TO 12:
      ASSIGN
        gl-acct1.last-yr[i] = gl-acct1.last-yr[i] + gl-acct.last-yr[i]
        gl-acct.last-yr[i]  = 0
        gbuff1.actual[i]    = gl-acct1.last-yr[i]
        gbuff.actual[i]     = 0
      .
    END. 
    FIND CURRENT gl-acct NO-LOCK. 
    FIND CURRENT gl-acct1 NO-LOCK. 
    FIND CURRENT gbuff NO-LOCK. 
    FIND CURRENT gbuff1 NO-LOCK. 
  END. 

  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
  CREATE res-history.
  ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.aenderung = "Closing Year - " + STRING(yy - 1)              
      res-history.action = "G/L". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 

END. 
