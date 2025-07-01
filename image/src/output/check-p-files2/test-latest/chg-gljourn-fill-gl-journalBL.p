DEF TEMP-TABLE b1-list  
  FIELD fibukonto    LIKE gl-acct.fibukonto   
  FIELD debit        LIKE gl-journal.debit   
  FIELD credit       LIKE gl-journal.credit   
  FIELD bemerk       AS CHAR  
  FIELD bezeich      LIKE gl-acct.bezeich FORMAT "x(36)"   
  FIELD chginit      LIKE gl-journal.chginit FORMAT "x(3)"   
  FIELD chgdate      LIKE gl-journal.chgdate  
  FIELD sysdate      LIKE gl-journal.sysdate  
  FIELD zeit         LIKE gl-journal.zeit  
  FIELD activeflag   LIKE gl-journal.activeflag  
  FIELD rec-gl-journ AS INTEGER
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS CHAR
  FIELD tot-amt     AS CHAR.  
  
DEFINE TEMP-TABLE g-list   
  FIELD  jnr        LIKE gl-journal.jnr   
  FIELD  fibukonto  LIKE gl-acct.fibukonto   
  FIELD  debit      LIKE gl-journal.debit   
  FIELD  credit     LIKE gl-journal.credit   
  FIELD  userinit   LIKE gl-journal.userinit   
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today   
  FIELD  zeit       LIKE gl-journal.zeit   
  FIELD  chginit    LIKE gl-journal.chginit   
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ?   
  FIELD  duplicate  AS LOGICAL INITIAL YES.  
  
  
DEF INPUT  PARAMETER case-type   AS INTEGER.  
DEF INPUT  PARAMETER jnr         AS INTEGER.  
DEF INPUT  PARAMETER comment     AS CHAR.  
DEF INPUT  PARAMETER user-init   AS CHAR.  
DEF INPUT  PARAMETER jou-recid   AS INTEGER.  
DEF INPUT  PARAMETER b1-recid    AS INTEGER.  
DEF INPUT  PARAMETER t-bezeich   AS CHAR.  
DEF INPUT  PARAMETER t-refno     AS CHAR.  
DEF INPUT  PARAMETER TABLE FOR g-list.  
DEF OUTPUT PARAMETER debits LIKE gl-jouhdr.debit.  
DEF OUTPUT PARAMETER credits LIKE gl-jouhdr.credit.  
DEF OUTPUT PARAMETER remains LIKE gl-jouhdr.remain.  
DEF OUTPUT PARAMETER TABLE FOR b1-list.
/*Naufal - add variable for logfile*/
DEF VAR fibukonto   LIKE gl-acct.fibukonto.
DEF VAR bemerk      AS CHAR.
DEF VAR debit       LIKE gl-journal.debit.
DEF VAR credit      LIKE gl-journal.credit.
DEF VAR datum       LIKE gl-jouhdr.datum.
/*end*/

/*DEF VAR case-type AS INT INIT 1.  
DEF VAR jnr AS INT INIT 4017.  
DEF VAR comment AS CHAR INIT "".  
DEF VAR user-init AS CHAR INIT "01".  
DEF VAR jou-recid AS INT INIT ?.  
DEF VAR b1-recid AS INT INIT ?.  
CREATE g-list.  
ASSIGN  
    g-list.jnr        = gl-journal.jnr   
    g-list.fibukonto  = gl-acct.fibukonto   
    g-list.debit      = gl-journal.debit   
    g-list.credit     = gl-journal.credit   
    g-list.userinit   = gl-journal.userinit   
    g-list.sysdate    = today   
    g-list.zeit       = gl-journal.zeit   
    g-list.chginit    = gl-journal.chginit   
    g-list.chgdate    = gl-journal.chgdate INITIAL ?   
    g-list.duplicate  = YES.*/  

IF case-type = 1 THEN  
DO :  
    FIND FIRST g-list.  
    FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = jnr EXCLUSIVE-LOCK.  
    CREATE gl-journal.  
    gl-journal.jnr = jnr.  
    gl-journal.fibukonto = g-list.fibukonto.  
    gl-journal.bemerk = comment.  
    gl-journal.userinit = user-init.   
    gl-journal.zeit = time.

    ASSIGN
        fibukonto   = g-list.fibukonto        
        bemerk      = comment        
        debit       = g-list.debit        
        credit      = g-list.credit
        datum       = gl-jouhdr.datum.                
  
    gl-jouhdr.debit  = gl-jouhdr.debit  + g-list.debit.   
    gl-jouhdr.credit = gl-jouhdr.credit + g-list.credit.   
    gl-jouhdr.remain = gl-jouhdr.remain + g-list.debit - g-list.credit.  
  
    gl-jouhdr.bezeich = t-bezeich.  
    gl-jouhdr.refno = t-refno.  
    /*gl-jouhdr.debit = gl-jouhdr.debit + g-list.debit - gl-journal.debit.   
    gl-jouhdr.credit = gl-jouhdr.credit + g-list.credit - gl-journal.credit.   
    gl-jouhdr.remain = gl-jouhdr.remain + g-list.debit - g-list.credit   
          - gl-journal.debit + gl-journal.credit. */  
    gl-journal.debit = g-list.debit.   
    gl-journal.credit = g-list.credit.  
    FIND CURRENT gl-jouhdr NO-LOCK.  
    FIND CURRENT gl-journal NO-LOCK.  
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto NO-LOCK.  
  
    CREATE b1-list.  
    ASSIGN  
        b1-list.fibukonto = g-list.fibukonto   
        b1-list.debit     = g-list.debit  
        b1-list.credit    = g-list.credit  
        b1-list.bemerk    = comment  
        b1-list.bezeich   = gl-acct.bezeich  
        b1-list.chginit   = user-init  
        b1-list.chgdate   = today  
        b1-list.activeflag = gl-journal.activeflag  
        b1-list.rec-gl-journ = RECID(gl-journal). 

    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
        ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
    /*Naufal - create log when add journal transaction*/
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Add Journal, Date: " + STRING(datum) + ", AcctNo: " + STRING(fibukonto) + ", Remark: " + STRING(comment) + ", Debit: " + STRING(debit) + ", Credit: " + STRING(credit)
            res-history.action      = "G/L".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
    /*end*/

    /*Alder - 958EFC*/
    RUN update-queasy-345(
        INPUT jnr,
        INPUT datum,
        INPUT gl-jouhdr.bezeich).
END.  
ELSE IF case-type = 2 THEN  
DO: 
    FIND FIRST g-list.  
    FIND FIRST gl-jouhdr  WHERE gl-jouhdr.jnr  = jnr EXCLUSIVE-LOCK.  
    FIND FIRST gl-journal WHERE RECID(gl-journal) = jou-recid EXCLUSIVE-LOCK.  
    /*naufal - assign variable for logfile*/
    ASSIGN
        fibukonto = gl-journal.fibukonto
        bemerk    = gl-journal.bemerk
        debit     = gl-journal.debit
        credit    = gl-journal.credit
        datum     = gl-jouhdr.datum.

    gl-journal.chginit = user-init.   
    gl-journal.chgdate = today.   
    gl-journal.bemerk = comment.  
  
    gl-jouhdr.debit = gl-jouhdr.debit + g-list.debit - gl-journal.debit.   
    gl-jouhdr.credit = gl-jouhdr.credit + g-list.credit - gl-journal.credit.   
    gl-jouhdr.remain = gl-jouhdr.remain + g-list.debit - g-list.credit   
          - gl-journal.debit + gl-journal.credit.   
    gl-jouhdr.bezeich = t-bezeich.  
    gl-jouhdr.refno = t-refno.  
  
    gl-journal.fibukonto = g-list.fibukonto.   
    gl-journal.debit = g-list.debit.   
    gl-journal.credit = g-list.credit.  
    FIND CURRENT gl-journal NO-LOCK.   
    FIND CURRENT gl-jouhdr NO-LOCK.   
    RUN update-bemerkbl.p(jou-recid). 

    FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto NO-LOCK.  
    CREATE b1-list.  
    ASSIGN  
      b1-list.fibukonto     = g-list.fibukonto   
      /*b1-list.debit       = gl-jouhdr.debit  
      b1-list.credit        = gl-jouhdr.credit*/  
      b1-list.debit         = g-list.debit  
      b1-list.credit        = g-list.credit  
      b1-list.bemerk        = comment  
      b1-list.chginit       = user-init  
      b1-list.chgdate       = today  
      b1-list.activeflag    = gl-journal.activeflag  
      b1-list.rec-gl-journ  = b1-recid
      b1-list.bezeich       = gl-acct.bezeich .  

    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
        ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

    IF gl-journal.fibukonto NE fibukonto THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Modify Journal, Date: " + STRING(datum) + ", AcctNo From: " + fibukonto + " To: " + gl-journal.fibukonto
                res-history.action      = "G/L".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.

    IF gl-journal.bemerk NE bemerk THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Modify Journal, Date: " + STRING(datum) + ", Notes From: " + bemerk + " To: " + gl-journal.bemerk
                res-history.action      = "G/L".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.

    IF gl-journal.debit NE debit THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Modify Journal, Date: " + STRING(datum) + ", Debit From: " + STRING(debit) + " To: " + STRING(gl-journal.debit)
                res-history.action      = "G/L".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.

    IF gl-journal.credit NE credit THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.aenderung   = "Modify Journal, Date: " + STRING(datum) + ", Credit From: " + STRING(credit) + " To: " + STRING(gl-journal.credit)
                res-history.action      = "G/L".
            FIND CURRENT res-history NO-LOCK.
            RELEASE res-history.
        END.
    END.

    /*Alder - 958EFC*/
    RUN update-queasy-345(
        INPUT jnr,
        INPUT datum,
        INPUT gl-jouhdr.bezeich).
END.  
debits = gl-jouhdr.debit.   
credits = gl-jouhdr.credit.   
remains = gl-jouhdr.remain.   

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
