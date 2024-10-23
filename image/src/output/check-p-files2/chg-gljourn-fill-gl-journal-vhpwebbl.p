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
  FIELD  duplicate  AS LOGICAL INITIAL YES
  FIELD  bemerk     AS CHARACTER.  
  
  
DEF INPUT  PARAMETER case-type   AS INTEGER.  
DEF INPUT  PARAMETER jnr         AS INTEGER.  
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


/*DEF INPUT  PARAMETER comment     AS CHAR.*/ 
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
    gl-journal.jnr          = jnr.  
    gl-journal.fibukonto    = g-list.fibukonto.  
    gl-journal.bemerk       = g-list.bemerk.  
    gl-journal.userinit     = user-init.   
    gl-journal.zeit         = time.  
      
    gl-jouhdr.debit         = gl-jouhdr.debit  + g-list.debit.   
    gl-jouhdr.credit        = gl-jouhdr.credit + g-list.credit.   
    gl-jouhdr.remain        = gl-jouhdr.remain + g-list.debit - g-list.credit.  
  
    gl-jouhdr.bezeich       = t-bezeich.  
    gl-jouhdr.refno         = t-refno.  

    /*gl-jouhdr.debit = gl-jouhdr.debit + g-list.debit - gl-journal.debit.   
    gl-jouhdr.credit = gl-jouhdr.credit + g-list.credit - gl-journal.credit.   
    gl-jouhdr.remain = gl-jouhdr.remain + g-list.debit - g-list.credit   
          - gl-journal.debit + gl-journal.credit. */  

    gl-journal.debit        = g-list.debit.   
    gl-journal.credit       = g-list.credit. 


    FIND CURRENT gl-jouhdr  NO-LOCK.  
    FIND CURRENT gl-journal NO-LOCK.  
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto NO-LOCK.  
  
    CREATE b1-list.  
    ASSIGN  
        b1-list.fibukonto    = g-list.fibukonto   
        b1-list.debit        = g-list.debit  
        b1-list.credit       = g-list.credit  
        b1-list.bemerk       = g-list.bemerk  
        b1-list.bezeich      = gl-acct.bezeich  
        b1-list.chginit      = user-init  
        b1-list.chgdate      = today  
        b1-list.activeflag   = gl-journal.activeflag  
        b1-list.rec-gl-journ = RECID(gl-journal). 

    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
        ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
END.  

ELSE IF case-type = 2 THEN  
DO:  
    FIND FIRST g-list.  
    FIND FIRST gl-jouhdr  WHERE gl-jouhdr.jnr  = jnr EXCLUSIVE-LOCK.  
    FIND FIRST gl-journal WHERE RECID(gl-journal) = jou-recid EXCLUSIVE-LOCK.  
  
    gl-journal.chginit      = user-init.   
    gl-journal.chgdate      = today.   
    gl-journal.bemerk       = g-list.bemerk.  
  
    gl-jouhdr.debit         = gl-jouhdr.debit + g-list.debit - gl-journal.debit.   
    gl-jouhdr.credit        = gl-jouhdr.credit + g-list.credit - gl-journal.credit.   
    gl-jouhdr.remain        = gl-jouhdr.remain + g-list.debit - g-list.credit   
                              - gl-journal.debit + gl-journal.credit.   
    gl-jouhdr.bezeich       = t-bezeich.  
    gl-jouhdr.refno         = t-refno.  
  
    gl-journal.fibukonto    = g-list.fibukonto.   
    gl-journal.debit        = g-list.debit.   
    gl-journal.credit       = g-list.credit.  

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
      b1-list.bemerk        = g-list.bemerk  
      b1-list.chginit       = user-init  
      b1-list.chgdate       = today  
      b1-list.activeflag    = gl-journal.activeflag  
      b1-list.rec-gl-journ  = b1-recid
      b1-list.bezeich       = gl-acct.bezeich .  

    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
        ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
END.  

debits      = gl-jouhdr.debit.   
credits     = gl-jouhdr.credit.   
remains     = gl-jouhdr.remain.   
