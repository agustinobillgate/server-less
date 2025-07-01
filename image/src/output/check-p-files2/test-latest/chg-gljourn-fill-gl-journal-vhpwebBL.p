DEF TEMP-TABLE b1-list  
  FIELD fibukonto    AS CHARACTER  
  FIELD debit        AS DECIMAL   
  FIELD credit       AS DECIMAL   
  FIELD bemerk       AS CHAR  
  FIELD bezeich      AS CHARACTER FORMAT "x(36)"   
  FIELD chginit      AS CHARACTER FORMAT "x(3)"   
  FIELD chgdate      AS DATE 
  FIELD sysdate      AS DATE   
  FIELD zeit         AS INTEGER  
  FIELD activeflag   AS INTEGER
  FIELD rec-gl-journ AS INTEGER
  FIELD tax-code     AS CHAR
  FIELD tax-amount   AS CHAR
  FIELD tot-amt      AS CHAR.  
  
DEFINE TEMP-TABLE g-list   
  FIELD jnr        AS INTEGER   
  FIELD fibukonto  AS CHARACTER  
  FIELD debit      AS DECIMAL  
  FIELD credit     AS DECIMAL     
  FIELD userinit   AS CHARACTER   
  FIELD sysdate    AS DATE INITIAL today   
  FIELD zeit       AS INTEGER  
  FIELD chginit    AS CHARACTER  
  FIELD chgdate    AS DATE INITIAL ?   
  FIELD duplicate  AS LOGICAL INITIAL YES
  FIELD bemerk     AS CHARACTER
  FIELD jou-recid  AS INTEGER
  FIELD b1-recid   AS INTEGER
  FIELD flag       AS INTEGER.
 
DEFINE INPUT  PARAMETER jnr AS INTEGER.  
DEFINE INPUT  PARAMETER user-init AS CHAR.  
DEFINE INPUT  PARAMETER t-bezeich AS CHAR.   
DEFINE INPUT  PARAMETER t-refno AS CHAR.  
DEFINE INPUT  PARAMETER TABLE FOR g-list.  
DEFINE OUTPUT PARAMETER debits AS DECIMAL.  
DEFINE OUTPUT PARAMETER credits AS DECIMAL.  
DEFINE OUTPUT PARAMETER remains AS DECIMAL.  
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.  

DEF VAR debitval AS DECIMAL.
DEF VAR creditval AS DECIMAL.
DEF VAR tmp-activeflag AS INTEGER. /* Malik Serverless */

DEFINE BUFFER buffglhdr FOR gl-jouhdr.
FOR EACH g-list NO-LOCK:
    IF g-list.flag EQ 1 THEN
    DO:
        FOR EACH gl-jouhdr WHERE gl-jouhdr.jnr EQ jnr NO-LOCK.
            FIND FIRST buffglhdr WHERE RECID(buffglhdr) EQ RECID(gl-jouhdr) NO-LOCK NO-ERROR.
            IF AVAILABLE buffglhdr THEN
            DO:
                FIND CURRENT buffglhdr EXCLUSIVE-LOCK.
                CREATE gl-journal. 
                ASSIGN
                    gl-journal.jnr          = jnr.  
                    gl-journal.fibukonto    = g-list.fibukonto.  
                    gl-journal.bemerk       = g-list.bemerk.  
                    gl-journal.userinit     = user-init.   
                    gl-journal.zeit         = time.  
                    
                    buffglhdr.debit         = buffglhdr.debit  + g-list.debit.   
                    buffglhdr.credit        = buffglhdr.credit + g-list.credit.   
                    buffglhdr.remain        = buffglhdr.remain + g-list.debit - g-list.credit.
                    
                    debitval                = debitval  + g-list.debit.
                    creditval               = creditval + g-list.credit.
                    
                    buffglhdr.bezeich       = t-bezeich.  
                    buffglhdr.refno         = t-refno.  
                    
                    gl-journal.debit        = g-list.debit.   
                    gl-journal.credit       = g-list.credit. 
                    
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
                    
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
    
                FIND CURRENT buffglhdr NO-LOCK.
                RELEASE buffglhdr.
            END.
             debits  = debits + gl-jouhdr.debit.   
             credits = credits + gl-jouhdr.credit.   
             remains = remains + gl-jouhdr.remain.
        END.        
    END.
    ELSE IF g-list.flag EQ 2 THEN
    DO:
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr EQ jnr NO-LOCK NO-ERROR.
        IF AVAILABLE gl-jouhdr THEN
        DO:
            FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.jou-recid NO-LOCK NO-ERROR.
            IF AVAILABLE gl-journal THEN
            DO:
                FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
                FIND CURRENT gl-journal EXCLUSIVE-LOCK.

                gl-journal.chginit   = user-init.   
                gl-journal.chgdate   = today.   
                gl-journal.bemerk    = g-list.bemerk.  
                                     
                gl-jouhdr.debit      = gl-jouhdr.debit + g-list.debit - gl-journal.debit.   
                gl-jouhdr.credit     = gl-jouhdr.credit + g-list.credit - gl-journal.credit.   
                gl-jouhdr.remain     = gl-jouhdr.remain + g-list.debit - g-list.credit - gl-journal.debit + gl-journal.credit.   
                                     
                gl-jouhdr.bezeich    = t-bezeich.  
                gl-jouhdr.refno      = t-refno.  
                                     
                gl-journal.fibukonto = g-list.fibukonto.   
                gl-journal.debit     = g-list.debit.   
                gl-journal.credit    = g-list.credit.
                                     
                debitval             = debitval + g-list.debit.
                creditval            = creditval + g-list.credit.
                tmp-activeflag       = gl-journal.activeflag. /* Malik Serverless */
                FIND CURRENT gl-jouhdr NO-LOCK.                
                RELEASE gl-journal. /* Malik */
                FIND CURRENT gl-jouhdr NO-LOCK.
            END.
            /* Malik Serverless */
            ELSE
            DO:
                tmp-activeflag = 0.
            END.
            /* END Malik */

           
            debits  = gl-jouhdr.debit.   
            credits = gl-jouhdr.credit.   
            remains = gl-jouhdr.remain. 
            RELEASE gl-jouhdr. /* Malik */            
        END.  
        RUN update-bemerkbl.p(g-list.jou-recid). /* Malik Serverless : jou-recid -> g-list.jou-recid */
        
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-acct THEN
        DO:
            CREATE b1-list.  
            ASSIGN  
                b1-list.fibukonto    = g-list.fibukonto   
                b1-list.debit        = g-list.debit  
                b1-list.credit       = g-list.credit  
                b1-list.bemerk       = g-list.bemerk  
                b1-list.chginit      = user-init  
                b1-list.chgdate      = today  
                b1-list.activeflag   = tmp-activeflag  /* Malik Serverless : gl-journal.activeflag -> tmp-activeflag */
                b1-list.rec-gl-journ = g-list.b1-recid
                b1-list.bezeich      = gl-acct.bezeich.  
    
            IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
        END.
    END.
    ELSE IF g-list.flag EQ 3 THEN
    DO:
        FIND FIRST gl-journal WHERE RECID(gl-journal) EQ g-list.b1-recid NO-LOCK NO-ERROR. /* Malik Serverless : b1-recid -> g-list.b1-recid */
        IF AVAILABLE gl-journal THEN
        DO:
            FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr EQ jnr NO-LOCK NO-ERROR.
            IF AVAILABLE gl-jouhdr THEN
            DO:
                FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
                FIND CURRENT gl-journal EXCLUSIVE-LOCK.

                gl-jouhdr.debit  = gl-jouhdr.debit - gl-journal.debit. 
                gl-jouhdr.credit = gl-jouhdr.credit - gl-journal.credit. 
                gl-jouhdr.remain = gl-jouhdr.debit - gl-jouhdr.credit. 
                
                credits = gl-jouhdr.credit. 
                remains = gl-jouhdr.remain. 
                
                DELETE gl-journal. 
                FIND CURRENT gl-jouhdr NO-LOCK. 
                debits  = gl-jouhdr.debit.   
                credits = gl-jouhdr.credit.   
                remains = gl-jouhdr.remain. 
                RELEASE gl-jouhdr. /* Malik */
                RELEASE gl-journal. /* Malik */
            END.
        END.
    END.
END. 




