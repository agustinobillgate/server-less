DEFINE TEMP-TABLE out-list
    FIELD s-recid       AS INTEGER
    FIELD marked        AS CHARACTER    FORMAT "x(1)" LABEL "M"
    FIELD fibukonto     AS CHARACTER
    FIELD jnr           AS INTEGER      INITIAL 0
    FIELD jtype         AS INTEGER
    FIELD bemerk        AS CHARACTER
    FIELD trans-date    AS DATE
    FIELD bezeich       AS CHARACTER
    FIELD number1       AS CHARACTER /*wenni*/
    FIELD debit         AS DECIMAL
    FIELD credit        AS DECIMAL
    FIELD balance       AS DECIMAL
    FIELD debit-str     AS CHARACTER
    FIELD credit-str    AS CHARACTER
    FIELD balance-str   AS CHARACTER
    FIELD refno         AS CHARACTER
    FIELD uid           AS CHARACTER
    FIELD created       AS DATE
    FIELD chgID         AS CHARACTER
    FIELD chgDate       AS DATE
    /*gst for penang*/
    FIELD tax-code    AS CHAR
    FIELD tax-amount  AS CHAR
    FIELD tot-amt     AS CHAR
    FIELD approved    AS LOGICAL INIT NO
    FIELD prev-bal    AS CHARACTER. /* add by gerald budget awal 080420 */


DEFINE TEMP-TABLE g-list
    FIELD grecid    AS INTEGER
    FIELD fibu      AS CHARACTER
    INDEX fibu_ix fibu.

DEFINE TEMP-TABLE j-list
    FIELD grecid    AS INTEGER
    FIELD fibu      AS CHARACTER
    FIELD datum     AS DATE
    INDEX fibu_ix fibu.

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER last-2yr     AS DATE.
DEFINE INPUT PARAMETER close-year   AS DATE.
DEFINE INPUT PARAMETER journaltype  AS INT.
DEFINE INPUT PARAMETER excl-other   AS LOGICAL.
DEFINE INPUT PARAMETER other-dept   AS LOGICAL.
DEFINE INPUT PARAMETER summ-date    AS LOGICAL.
DEFINE INPUT PARAMETER from-fibu    AS CHAR.
DEFINE INPUT PARAMETER to-fibu      AS CHAR.
DEFINE INPUT PARAMETER sorttype     AS INT.
DEFINE INPUT PARAMETER from-dept    AS INT.
DEFINE INPUT PARAMETER journaltype1 AS INT.
DEFINE INPUT PARAMETER cashflow     AS LOGICAL.
DEFINE INPUT PARAMETER f-note       AS CHAR.   
DEFINE INPUT PARAMETER from-main    AS INTEGER.  /*FD*/ 
DEFINE OUTPUT PARAMETER TABLE FOR out-list.

DEFINE VARIABLE datum1 AS DATE NO-UNDO.
DEFINE VARIABLE datum2 AS DATE NO-UNDO.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

/*IF from-date LE last-2yr AND to-date GE last-2yr THEN 
DO:
    RUN create-dlist.
    RUN create-djlist.
END.
ELSE*/ IF YEAR(to-date) LE YEAR(last-2yr) THEN 
DO:
    RUN create-hglist.
    RUN create-hlist.
END.
ELSE 
DO: 
    RUN create-glist.
    RUN create-list. 
END.

PROCEDURE create-dlist:
    FOR EACH j-list:
        DELETE j-list.
    END.

    /*ASSIGN datum1 = last-2yr
           datum2 = last-2yr + 1.*/

    ASSIGN datum1 = DATE(12, 31, YEAR(last-2yr))
           datum2 = datum1 + 1.

    FOR EACH vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.datum GE from-date
        AND vhp.gl-jhdrhis.datum LE datum1 NO-LOCK BY vhp.gl-jhdrhis.datum:
        IF journaltype EQ 0 AND excl-other AND gl-jhdrhis.jtype NE 0 THEN 
            NEXT.
        ELSE IF journaltype NE 0 AND NOT other-dept 
          AND vhp.gl-jhdrhis.jtype NE journaltype THEN NEXT.
        FOR EACH gl-jourhis WHERE gl-jourhis.jnr = vhp.gl-jhdrhis.jnr
            AND gl-jourhis.fibukonto GE from-fibu
            AND gl-jourhis.fibukonto LE to-fibu NO-LOCK 
            BY gl-jourhis.fibukonto:
            CREATE j-list.
            ASSIGN
                j-list.grecid = RECID(gl-jourhis)
                j-list.fibu   = gl-jourhis.fibukonto
                j-list.datum  = gl-jhdrhis.datum
                .
        END.
    END.

     FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE datum2
        AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:         /*gerald 240820*/
        IF journaltype EQ 0 AND excl-other AND gl-jouhdr.jtype NE 0 THEN 
            NEXT.
        ELSE IF journaltype NE 0 AND other-dept 
          AND gl-jouhdr.jtype EQ 0 THEN NEXT. 
        ELSE IF journaltype NE 0 AND NOT other-dept 
          AND gl-jouhdr.jtype NE journaltype 
          AND gl-jouhdr.jtype NE journaltype1 THEN NEXT.
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
            AND gl-journal.fibukonto GE from-fibu
            AND gl-journal.fibukonto LE to-fibu NO-LOCK 
            BY gl-journal.fibukonto:
            CREATE j-list.
            ASSIGN
                j-list.grecid = RECID(gl-journal)
                j-list.fibu   = gl-journal.fibukonto
                j-list.datum  = gl-jouhdr.datum
                .
        END.
    END.   
END.

PROCEDURE create-djlist: 
DEFINE VARIABLE debit       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE credit      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE balance     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE c           AS CHAR. 
DEFINE VARIABLE bezeich     AS CHAR. 
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE refno       AS CHAR. 
DEFINE VARIABLE h-bezeich   AS CHAR. 
DEFINE VARIABLE id          AS CHAR FORMAT "x(2)". 
DEFINE VARIABLE chgdate     AS DATE. 
DEFINE VARIABLE beg-date    AS DATE. 
DEFINE VARIABLE beg-day     AS INTEGER. 

DEFINE VARIABLE date1       AS DATE.
DEFINE VARIABLE ddebit      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE dcredit     AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE dbalance    AS DECIMAL FORMAT "->>>,>>>,>>9.99".
 
DEFINE VARIABLE t-debit     LIKE debit  INITIAL 0. 
DEFINE VARIABLE t-credit    LIKE credit INITIAL 0. 
DEFINE VARIABLE tot-debit   LIKE debit  INITIAL 0. 
DEFINE VARIABLE tot-credit  LIKE credit INITIAL 0. 
 
DEFINE VARIABLE e-bal AS DECIMAL INITIAL 0. 
DEFINE VARIABLE delta AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fdate AS DATE. 
DEFINE VARIABLE tdate AS DATE. 
 
DEFINE buffer gl-account FOR gl-acct. 
DEFINE buffer gl-jour1   FOR gl-jourhis. 
DEFINE buffer gl-jouh1   FOR gl-jhdrhis. 
 
DEFINE VARIABLE prev-mm  AS INTEGER. 
DEFINE VARIABLE prev-yr  AS INTEGER.
DEFINE VARIABLE prev-bal AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE end-bal  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
 
DEFINE VARIABLE blankchar AS CHAR FORMAT "x(70)" INITIAL "". 
DEFINE VARIABLE acc-bez   AS CHAR FORMAT "x(24)" INITIAL "".

  DO i = 1 TO 72: 
    blankchar = blankchar + " ". 
  END. 
 
  ASSIGN
    prev-mm = MONTH(from-date) - 1
    prev-yr = YEAR(from-date)
  .
  IF prev-mm = 0 THEN 
  ASSIGN
    prev-mm = 12
    prev-yr = prev-yr - 1
  .
 
  beg-date = DATE(MONTH(from-date), 1, YEAR(from-date)). 

  FOR EACH out-list:
      DELETE out-list.
  END.

  DO:
      IF sorttype = 2 THEN
      DO:
          FOR EACH j-list NO-LOCK BY j-list.fibu BY j-list.datum:

            FIND FIRST vhp.gl-jourhis WHERE RECID(vhp.gl-jourhis) = j-list.grecid NO-LOCK NO-ERROR.
            IF AVAILABLE vhp.gl-jourhis THEN DO:
                FIND FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr NO-LOCK NO-ERROR.
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto NO-LOCK NO-ERROR.
                DELETE j-list.
                
                IF vhp.gl-jourhis.chgdate = ? THEN chgdate = ?. 
                ELSE chgdate = vhp.gl-jourhis.chgdate. 
    
                IF konto = "" THEN 
                DO:
                  RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr, OUTPUT prev-bal, 
                                  OUTPUT balance, OUTPUT dbalance).
                  
                  CREATE out-list.
                  RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
  
                  ASSIGN
                      out-list.fibukonto = c
                      out-list.refno     = STRING(c, "x(15)")
                      out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                      out-list.bemerk    = STRING(gl-acct.bezeich) + " "+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") .
  
                  IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99").
                  ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99").
  
                  ASSIGN
                      konto   = gl-acct.fibukonto
                      acc-bez = gl-acct.bezeich.
                END.
    
    
                IF konto NE gl-acct.fibukonto THEN
                DO:
                    IF summ-date THEN
                    DO:
                      CREATE out-list.
                      ASSIGN
                          out-list.s-recid        = INTEGER(RECID(gl-journal))
                          out-list.fibukonto      = konto
                          out-list.trans-date     = date1
                          out-list.bezeich        = STRING(acc-bez, "x(40)")
                          out-list.bemerk         = STRING(acc-bez, "x(40)")
                          out-list.debit          = ddebit
                          out-list.credit         = dcredit
                          out-list.balance        = dbalance
                          out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                          out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                          out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99")
                          /*out-list.jnr = gl-jhdrhis.jnr*/
                          .

                      IF AVAILABLE gl-journal THEN
                      DO:
                         IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                         out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                      END.

                      IF AVAILABLE gl-acct THEN DO:
                          IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                      out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                          IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                          ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
                      END.
  
                      ASSIGN
                          ddebit  = 0
                          dcredit = 0
                          date1   = gl-jhdrhis.datum.
                    END.
    
                    CREATE out-list.
                    ASSIGN
                        out-list.bezeich        = "T O T A L " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                        out-list.debit          = t-debit
                        out-list.credit         = t-credit
                        out-list.balance        = balance
                        out-list.debit-str      = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
                        out-list.credit-str     = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
                        out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").
                    
                    CREATE out-list.
    
                    ASSIGN
                        balance     = 0
                        t-debit     = 0
                        t-credit    = 0.
    
                    RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                      OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                    CREATE out-list.
                    RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                    ASSIGN
                        out-list.refno      = STRING(c, "x(15)")
                        out-list.fibukonto  = STRING(c, "x(15)")
                        out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                        out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                        acc-bez             = gl-acct.bezeich
                        konto               = gl-acct.fibukonto.
                END.
    
                
                IF summ-date THEN
                DO:
                    IF date1 NE ? AND date1 NE gl-jhdrhis.datum THEN
                    DO:
                        CREATE out-list.
                        ASSIGN
                            out-list.fibukonto      = konto
                            out-list.trans-date     = date1
                            out-list.bezeich        = acc-bez
                            out-list.debit          = ddebit
                            out-list.credit         = dcredit
                            out-list.balance        = dbalance
                            out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                            out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                            out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99").
    
                        IF AVAILABLE gl-acct THEN DO:
                            IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                            IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                            ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
                        END.
    
                        ASSIGN
                            ddebit = 0
                            dcredit = 0.
                    END.
                END.
                
                FIND FIRST gl-account WHERE gl-account.fibukonto = vhp.gl-jourhis.fibukonto NO-LOCK. 
                IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    ASSIGN
                    balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
                ELSE ASSIGN
                   balance      = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                    /*balance = balance + gl-jourhis.debit - gl-jourhis.credit. */
                
                ASSIGN 
                    t-debit     = t-debit + vhp.gl-jourhis.debit
                    t-credit    = t-credit + vhp.gl-jourhis.credit
                    tot-debit   = tot-debit + vhp.gl-jourhis.debit
                    tot-credit  = tot-credit + vhp.gl-jourhis.credit. 
                
                IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    ASSIGN
                       dbalance = dbalance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
                ELSE ASSIGN
                   dbalance = dbalance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                ASSIGN
                   ddebit   = ddebit  + vhp.gl-jourhis.debit
                   dcredit  = dcredit + vhp.gl-jourhis.credit
                   date1    = gl-jhdrhis.datum.
                
                IF NOT summ-date THEN
                DO:
                    CREATE out-list.
                    ASSIGN
                        out-list.s-recid        = INTEGER(RECID(gl-jourhis))
                        out-list.fibukonto      = gl-jourhis.fibukonto
                        out-list.jnr            = gl-jhdrhis.jnr
                        out-list.jtype          = gl-jhdrhis.jtype
                        out-list.trans-date     = gl-jhdrhis.datum
                        out-list.refno          = gl-jhdrhis.refno
                        out-list.bezeich        = gl-jhdrhis.bezeich
                        out-list.debit          = gl-jourhis.debit
                        out-list.credit         = gl-jourhis.credit
                        out-list.uid            = gl-jourhis.userinit
                        out-list.created        = gl-jourhis.sysdate
                        out-list.chgID          = gl-jourhis.chginit
                        out-list.chgDate        = chgdate
                        out-list.bemerk         = STRING(get-bemerk(gl-jourhis.bemerk), "x(50)")
                        out-list.balance        = balance
                        out-list.debit-str      = STRING(gl-jourhis.debit, "->>>,>>>,>>>,>>9.99")
                        out-list.credit-str     = STRING(gl-jourhis.credit, "->>>,>>>,>>>,>>9.99")
                        out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").
    
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
    
                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).       
                END.
            END.
            ELSE DO:
                  FIND FIRST gl-journal WHERE RECID(gl-journal) = j-list.grecid NO-LOCK NO-ERROR.
                  IF AVAILABLE gl-journal THEN DO:
                     FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                     FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK NO-ERROR.
                     DELETE j-list.
            
                     IF gl-journal.chgdate = ? THEN chgdate = ?. 
                     ELSE chgdate = gl-journal.chgdate. 
            
                     IF konto = "" THEN
                     DO:
                        RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                          OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                        CREATE out-list.
                        RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                        
                        ASSIGN
                            out-list.fibukonto  = STRING(c, "x(15)")
                            out-list.refno      = STRING(c, "x(15)")
                            out-list.bezeich    = STRING(gl-acct.bezeich) + " " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                            out-list.bemerk     = STRING(gl-acct.bezeich) + " " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99").
                        ASSIGN
                            konto   = gl-acct.fibukonto
                            acc-bez = gl-acct.bezeich.
                     END.
            
                     IF konto NE gl-acct.fibukonto THEN
                     DO:
                        IF summ-date THEN
                        DO:
                            CREATE out-list.
                            ASSIGN
                                out-list.s-recid        = INTEGER(RECID(gl-journal))
                                out-list.fibukonto      = konto
                                out-list.trans-date     = date1
                                out-list.bezeich        = acc-bez
                                out-list.bemerk         = acc-bez
                                out-list.debit          = ddebit
                                out-list.credit         = dcredit
                                out-list.balance        = dbalance
                                out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                                out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                                out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99")
                                .

                            IF AVAILABLE gl-journal THEN
                            DO:
                               IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                               out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                            END.
            
                            IF AVAILABLE gl-acct THEN DO:                                                  
                                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                            END.                             

                            ASSIGN
                                ddebit  = 0
                                dcredit = 0
                                date1   = gl-jouhdr.datum.
                        END.
            
                        CREATE out-list.
                        ASSIGN
                            out-list.bezeich        = STRING("T O T A L ") /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                            out-list.debit          = t-debit
                            out-list.credit         = t-credit
                            out-list.balance        = balance
                            out-list.debit-str      = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
                            out-list.credit-str     = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
                            out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").
            
                        CREATE out-list.
                        ASSIGN
                            balance = 0
                            t-debit = 0 
                            t-credit = 0.
            
                        RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                          OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
            
                        CREATE out-list.
                        RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                        ASSIGN
                            out-list.refno      = STRING(c, "x(15)")
                            out-list.fibukonto  = STRING(c, "x(15)")
                            out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                            out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                            acc-bez             = gl-acct.bezeich
                            konto               = gl-acct.fibukonto.
                     END.
                     IF summ-date THEN
                     DO:
                        IF date1 NE ? AND date1 NE gl-jouhdr.datum THEN
                        DO:
                            CREATE out-list.
                            ASSIGN
                                out-list.fibukonto      = konto
                                out-list.trans-date     = date1
                                out-list.debit          = ddebit
                                out-list.credit         = dcredit
                                out-list.balance        = dbalance
                                out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                                out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                                out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99").
            
                            IF AVAILABLE gl-acct THEN DO:                                                  
                                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                            END.                                                                           

                            ASSIGN
                                ddebit = 0
                                dcredit = 0.
                        END.
                     END.
            
                     FIND FIRST gl-account WHERE gl-account.fibukonto = gl-journal.fibukonto NO-LOCK NO-ERROR.
                    
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                        ASSIGN
                         balance = balance - gl-journal.debit + gl-journal.credit.
                     ELSE 
                        ASSIGN
                            balance     = balance + gl-journal.debit - gl-journal.credit.
                            
                     t-debit     = t-debit + gl-journal.debit.
                     t-credit    = t-credit + gl-journal.credit.
                     tot-debit   = tot-debit + gl-journal.debit.
                     tot-credit  = tot-credit + gl-journal.credit. 
            
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                        ASSIGN dbalance = dbalance - gl-journal.debit + gl-journal.credit.
                     ELSE ASSIGN dbalance = dbalance + gl-journal.debit - gl-journal.credit.
                     ASSIGN
                       ddebit   = ddebit  + gl-journal.debit
                       dcredit  = dcredit + gl-journal.credit
                       date1    = gl-jouhdr.datum.
            
                     IF NOT summ-date THEN
                     DO:
                        CREATE out-list.
                        ASSIGN
                            out-list.s-recid        = INTEGER(RECID(gl-journal))
                            out-list.fibukonto      = gl-journal.fibukonto
                            out-list.jnr            = gl-jouhdr.jnr
                            out-list.jtype          = gl-jouhdr.jtype
                            out-list.trans-date     = gl-jouhdr.datum
                            out-list.refno          = gl-jouhdr.refno
                            out-list.bezeich        = gl-jouhdr.bezeich
                            out-list.debit          = gl-journal.debit
                            out-list.credit         = gl-journal.credit
                            out-list.refno          = gl-jouhdr.refno
                            out-list.uid            = gl-journal.userinit
                            out-list.created        = gl-journal.sysdate
                            out-list.chgID          = gl-journal.chginit
                            out-list.chgDate        = chgdate
                            out-list.bemerk         = STRING(get-bemerk(gl-journal.bemerk), "x(50)")
                            out-list.balance        = balance
                            out-list.debit-str      = STRING(gl-journal.debit, "->>>,>>>,>>>,>>9.99") /*dd*/
                            out-list.credit-str     = STRING(gl-journal.credit, "->>>,>>>,>>>,>>9.99")
                            out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").

                        IF AVAILABLE gl-journal THEN
                        DO:
                           IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                           out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                        END.
            
                        IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                              out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
            
                        IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(50)").
                        ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(50)").                                                 
                     END.                                             
                  END.                                  
            END. /*end-do*/                        
          END. /*end for*/

          IF summ-date THEN
          DO:
              CREATE out-list.
              ASSIGN
                  out-list.s-recid          = INTEGER(RECID(gl-journal))
                  out-list.fibukonto        = konto
                  out-list.trans-date       = date1
                  out-list.bezeich          = acc-bez
                  out-list.debit            = ddebit
                  out-list.credit           = dcredit
                  out-list.balance          = dbalance
                  out-list.debit-str        = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                  out-list.credit-str       = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                  out-list.balance-str      = STRING(dbalance, "->>>,>>>,>>>,>>9.99").

             IF AVAILABLE gl-journal THEN
             DO:
                IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
             END.

             ASSIGN
                  ddebit = 0
                  dcredit = 0.
          END.

          CREATE out-list.
          ASSIGN
              out-list.bezeich      = "T O T A L " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
              out-list.debit        = t-debit
              out-list.credit       = t-credit
              out-list.balance      = balance
              out-list.debit-str    = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
              out-list.credit-str   = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
              out-list.balance-str  = STRING(balance, "->>>,>>>,>>>,>>9.99").

          
          CREATE out-list.
          CREATE out-list.

          ASSIGN
              out-list.bezeich      = "GRAND T O T A L               " 
              out-list.debit        = tot-debit
              out-list.credit       = tot-credit
              out-list.debit-str    = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
              out-list.credit-str   = STRING(tot-credit, "->>>,>>>,>>>,>>9.99").

          
      END.
      ELSE IF sorttype = 1 THEN
      DO:
         FOR EACH j-list NO-LOCK BY j-list.fibu BY j-list.datum:
            FIND FIRST vhp.gl-jourhis WHERE RECID(vhp.gl-jourhis) = j-list.grecid NO-LOCK NO-ERROR.
            IF AVAILABLE gl-jourhis THEN DO:
                FIND FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr NO-LOCK NO-ERROR.
                FIND FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto AND gl-acct.main-nr = from-main NO-LOCK NO-ERROR.
                DELETE j-list.
                
                IF vhp.gl-jourhis.chgdate = ? THEN chgdate = ?. 
                ELSE chgdate = vhp.gl-jourhis.chgdate. 
                IF konto = "" THEN 
                DO:    
                  RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                      OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                  CREATE out-list. 
                  RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                  ASSIGN
                      out-list.fibukonto = STRING(c, "x(15)") 
                      out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                      /*FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/.
    
                  ASSIGN
                      konto = gl-acct.fibukonto
                      acc-bez = gl-acct.bezeich.
                END.
    
                IF konto NE gl-acct.fibukonto THEN
                DO:
                    IF summ-date THEN
                    DO:
                        CREATE out-list.
                        ASSIGN
                            out-list.s-recid          = INTEGER(RECID(gl-journal))
                            out-list.fibukonto      = konto
                            out-list.trans-date     = date1
                            out-list.bezeich        = acc-bez
                            out-list.debit          = ddebit
                            out-list.credit         = dcredit
                            out-list.balance        = dbalance
                            out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                            out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                            out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99").

                        IF AVAILABLE gl-journal THEN
                        DO:
                           IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                           out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                        END.
    
                        IF AVAILABLE gl-acct THEN DO:                                                  
                            IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                            IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                            ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                        END.  

                        ASSIGN
                            ddebit  = 0
                            dcredit = 0
                            date1   = gl-jhdrhis.datum.
                    END.
                    CREATE out-list.
                    ASSIGN
                        out-list.bezeich        = "T O T A L  " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                        out-list.debit          = t-debit
                        out-list.credit         = t-credit
                        out-list.balance        = balance
                        out-list.debit-str      = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
                        out-list.credit-str     = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
                        out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").
    
                    CREATE out-list.
                    ASSIGN
                        balance  = 0
                        t-debit  = 0
                        t-credit = 0.
    
                    RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                      OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
    
                    CREATE out-list.
                    RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                    ASSIGN
                        out-list.fibukonto = STRING(c, "x(15)")
                        out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") .
    
                    ASSIGN
                        acc-bez = gl-acct.bezeich
                        konto   = gl-acct.fibukonto.
                END.
    
                IF summ-date THEN
                DO:
                    IF date1 NE ? AND date1 NE gl-jhdrhis.datum THEN
                    DO:
                        CREATE out-list.
                        ASSIGN
                            out-list.fibukonto      = konto
                            out-list.trans-date     = date1
                            out-list.bezeich        = acc-bez
                            out-list.debit          = ddebit
                            out-list.credit         = dcredit
                            out-list.balance        = dbalance
                            out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                            out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                            out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99").
                            
                        IF AVAILABLE gl-acct THEN DO:                                                  
                            IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                            IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                            ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                        END.                                                                           
    
                        ASSIGN
                            ddebit  = 0
                            dcredit = 0.
                    END.
                END.
    
                FIND FIRST gl-account WHERE gl-account.fibukonto 
                  = vhp.gl-jourhis.fibukonto NO-LOCK. 
                IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                   balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
                ELSE
                balance = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                
                    t-debit = t-debit + vhp.gl-jourhis.debit.
                    t-credit = t-credit + vhp.gl-jourhis.credit.
                    tot-debit = tot-debit + vhp.gl-jourhis.debit.
                    tot-credit = tot-credit + vhp.gl-jourhis.credit. 
    
                IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    ASSIGN
                       dbalance = dbalance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
                ELSE ASSIGN
                   dbalance = dbalance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                ASSIGN
                   ddebit   = ddebit  + vhp.gl-jourhis.debit
                   dcredit  = dcredit + vhp.gl-jourhis.credit
                   date1    = vhp.gl-jhdrhis.datum.
    
                IF NOT summ-date THEN
                DO:
                    CREATE out-list.
                    ASSIGN
                        out-list.s-recid        = INTEGER(RECID(gl-journal))
                        out-list.fibukonto      = gl-jourhis.fibukonto
                        out-list.jnr            = gl-jhdrhis.jnr
                        out-list.jtype          = gl-jhdrhis.jtype
                        out-list.trans-date     = gl-jhdrhis.datum
                        out-list.refno          = gl-jhdrhis.refno
                        out-list.bezeich        = gl-jhdrhis.bezeich
                        out-list.debit          = gl-jourhis.debit
                        out-list.credit         = gl-jourhis.credit
                        out-list.uid            = gl-jourhis.userinit
                        out-list.created        = gl-jourhis.sysdate
                        out-list.chgID          = gl-jourhis.chginit
                        out-list.chgDate        = chgdate
                        out-list.bemerk         = STRING(get-bemerk(gl-jourhis.bemerk), "x(50)")
                        out-list.balance        = balance
                        out-list.debit-str      = STRING(gl-jourhis.debit, "->>>,>>>,>>>,>>9.99")
                        out-list.credit-str     = STRING(gl-jourhis.credit, "->>>,>>>,>>>,>>9.99")
                        out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").
    
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
    
                END.
            END.
            ELSE DO:
                 FIND FIRST gl-journal WHERE RECID(gl-journal) = j-list.grecid NO-LOCK NO-ERROR.
                 IF AVAILABLE gl-journal THEN DO:
                        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                        FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto AND gl-acct.main-nr = from-main NO-LOCK NO-ERROR.
                        DELETE j-list.
                     
                        IF gl-journal.chgdate = ? THEN chgdate = ?. 
                        ELSE chgdate = gl-journal.chgdate. 
                        IF konto = "" THEN 
                        DO:    
                          RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                              OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                          CREATE out-list. 
                          RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                          ASSIGN
                              out-list.fibukonto   = STRING(c, "x(15)") 
                              out-list.refno       = STRING(c, "x(15)")
                              out-list.bezeich     = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                              out-list.bemerk      = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") . 
        
                          ASSIGN
                              konto = gl-acct.fibukonto
                              acc-bez = gl-acct.bezeich.
                        END.
        
                        IF konto NE gl-acct.fibukonto THEN
                        DO:
                            IF summ-date THEN
                            DO:
                                CREATE out-list.
                                ASSIGN
                                    out-list.s-recid        = INTEGER(RECID(gl-journal))
                                    out-list.fibukonto      = konto
                                    out-list.trans-date     = date1
                                    out-list.bezeich        = acc-bez
                                    out-list.bemerk         = acc-bez
                                    out-list.debit          = ddebit
                                    out-list.credit         = dcredit
                                    out-list.balance        = dbalance
                                    out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                                    out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                                    out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99")
                                    .

                                IF AVAILABLE gl-journal THEN
                                DO:
                                   IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                                   out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                                END.
        
                                IF AVAILABLE gl-acct THEN DO:                                                  
                                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                                out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                                END.                                                                           
        
                                ASSIGN
                                    ddebit     = 0
                                    dcredit    = 0
                                    date1      = gl-jouhdr.datum.
                            END.
                            CREATE out-list.
                            ASSIGN
                                out-list.bezeich       = "T O T A L  " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                                out-list.debit         = t-debit
                                out-list.credit        = t-credit
                                out-list.balance       = balance
                                out-list.debit-str     = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
                                out-list.credit-str    = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
                                out-list.balance-str   = STRING(balance, "->>>,>>>,>>>,>>9.99").
        
                            CREATE out-list.
                            ASSIGN
                                balance  = 0
                                t-debit  = 0
                                t-credit = 0.
        
                            RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
        
                            CREATE out-list.
                            RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                            ASSIGN
                                out-list.refno      = STRING(c, "x(15)")
                                out-list.fibukonto  = STRING(c, "x(15)")
                                out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                                out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") .
        
                            ASSIGN
                                acc-bez    = gl-acct.bezeich
                                konto      = gl-acct.fibukonto.
                        END.
        
                        IF summ-date THEN
                        DO:
                            IF date1 NE ? AND date1 NE gl-jouhdr.datum THEN
                            DO:
                                CREATE out-list.
                                ASSIGN
                                    out-list.fibukonto     = konto
                                    out-list.trans-date    = date1
                                    out-list.bezeich       = acc-bez
                                    out-list.bemerk        = acc-bez
                                    out-list.debit         = ddebit
                                    out-list.credit        = dcredit
                                    out-list.balance       = dbalance
                                    out-list.debit-str     = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                                    out-list.credit-str    = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                                    out-list.balance-str   = STRING(dbalance, "->>>,>>>,>>>,>>9.99").
        
                                IF AVAILABLE gl-acct THEN DO:                                                  
                                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                                out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                                END.                                                                           
        
                                ASSIGN
                                    ddebit = 0
                                    dcredit = 0.
                            END.
                        END.
        
                        FIND FIRST gl-account WHERE gl-account.fibukonto = gl-journal.fibukonto NO-LOCK NO-ERROR. 
                        IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                           balance = balance - gl-journal.debit + gl-journal.credit.
                        ELSE
                            balance    = balance + gl-journal.debit - gl-journal.credit.
                        
                        ASSIGN
                            t-debit    = t-debit + gl-journal.debit
                            t-credit   = t-credit + gl-journal.credit
                            tot-debit  = tot-debit + gl-journal.debit
                            tot-credit = tot-credit + gl-journal.credit. 
        
                        IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                            ASSIGN
                               dbalance = dbalance - gl-journal.debit + gl-journal.credit.
                        ELSE ASSIGN
                           dbalance = dbalance + gl-journal.debit - gl-journal.credit.

                        ASSIGN
                           ddebit   = ddebit  + gl-journal.debit
                           dcredit  = dcredit + gl-journal.credit
                           date1    = gl-jouhdr.datum.
        
                        IF NOT summ-date THEN
                        DO:
                            CREATE out-list.
                            ASSIGN
                                out-list.s-recid       = INTEGER(RECID(gl-journal))
                                out-list.fibukonto     = gl-journal.fibukonto
                                out-list.jnr           = gl-jouhdr.jnr
                                out-list.jtype         = gl-jouhdr.jtype
                                out-list.trans-date    = gl-jouhdr.datum
                                out-list.refno         = gl-jouhdr.refno
                                out-list.bezeich       = gl-jouhdr.bezeich
                                out-list.debit         = gl-journal.debit
                                out-list.credit        = gl-journal.credit
                                out-list.uid           = gl-journal.userinit
                                out-list.created       = gl-journal.sysdate
                                out-list.chgID         = gl-journal.chginit
                                out-list.chgDate       = chgdate
                                out-list.bemerk        = STRING(get-bemerk(gl-journal.bemerk), "x(50)")
                                out-list.balance       = balance
                                out-list.debit-str     = STRING(gl-journal.debit, "->>>,>>>,>>>,>>9.99")
                                out-list.credit-str    = STRING(gl-journal.credit, "->>>,>>>,>>>,>>9.99")
                                out-list.balance-str   = STRING(balance, "->>>,>>>,>>>,>>9.99").

                                IF AVAILABLE gl-journal THEN
                                DO:
                                   IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                                   out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                                END.                                                     
        
                                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                       out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
        
                                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(50)").
                                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(50)").
                        END.                               
                 END.                             
            END. /*end do*/                         
          END. /*end for each*/

          IF summ-date THEN
          DO:
              CREATE out-list.
              ASSIGN
                  out-list.s-recid          = INTEGER(RECID(gl-journal))
                  out-list.fibukonto    = konto
                  out-list.trans-date   = date1
                  out-list.bezeich      = acc-bez
                  out-list.debit        = ddebit
                  out-list.credit       = dcredit
                  out-list.balance      = dbalance
                  out-list.debit-str    = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                  out-list.credit-str   = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                  out-list.balance-str  = STRING(dbalance, "->>>,>>>,>>>,>>9.99").

              IF AVAILABLE gl-journal THEN
              DO:
                 IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                 out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
              END.

              IF AVAILABLE gl-acct THEN DO:                                                  
                  IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                              out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                  IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                  ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
              END.                                                                      

              ASSIGN
                  ddebit = 0
                  dcredit = 0.
          END.

          CREATE out-list.
          ASSIGN
              out-list.bezeich      =  "T O T A L  " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
              out-list.debit        = tot-debit
              out-list.credit       = tot-credit
              out-list.debit-str    = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
              out-list.credit-str   = STRING(tot-credit, "->>>,>>>,>>>,>>9.99").

          
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
        FOR EACH j-list NO-LOCK BY j-list.fibu BY j-list.datum:
          FIND FIRST vhp.gl-jourhis WHERE RECID(vhp.gl-jourhis) = j-list.grecid NO-LOCK NO-ERROR.
          IF AVAILABLE gl-jourhis THEN DO:
              FIND FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr NO-LOCK NO-ERROR.
              FIND FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto 
                    AND gl-acct.deptnr = from-dept NO-LOCK NO-ERROR.
              DELETE j-list.
              
              IF vhp.gl-jourhis.chgdate = ? THEN chgdate = ?. 
              ELSE chgdate = vhp.gl-jourhis.chgdate. 
              IF konto = "" THEN 
              DO:    
                RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                    OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                CREATE out-list. 
                RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                ASSIGN
                    out-list.fibukonto = STRING(c, "x(15)") 
                    out-list.bezeich = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") /*+
                    FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                ASSIGN 
                    acc-bez = gl-acct.bezeich
                    konto = gl-acct.fibukonto.
              END.
    
              IF konto NE gl-acct.fibukonto THEN
              DO:
                  IF summ-date THEN
                  DO:
                      CREATE out-list.
                      ASSIGN
                          out-list.s-recid      = INTEGER(RECID(gl-journal))
                          out-list.fibukonto    = konto
                          out-list.trans-date   = date1
                          out-list.bezeich      = acc-bez
                          out-list.debit        = ddebit
                          out-list.credit       = dcredit
                          out-list.balance      = dbalance
                          out-list.debit-str    = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                          out-list.credit-str   = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                          out-list.balance-str  = STRING(dbalance, "->>>,>>>,>>>,>>9.99").

                      IF AVAILABLE gl-journal THEN
                      DO:
                         IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                         out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                      END.
    
                      IF AVAILABLE gl-acct THEN DO:                                                  
                          IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                      out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                          IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                          ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                      END.                                                                        

                      ASSIGN
                          ddebit = 0
                          dcredit = 0
                          date1 = gl-jhdrhis.datum.
                  END.

                  CREATE out-list.
                  ASSIGN
                      out-list.bezeich      = "T O T A L  " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                      out-list.debit        = t-debit
                      out-list.credit       = t-credit
                      out-list.balance      = balance
                      out-list.debit-str    = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
                      out-list.credit-str   = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
                      out-list.balance-str  = STRING(balance, "->>>,>>>,>>>,>>9.99").
    
                  CREATE out-list.
                  ASSIGN
                      balance = 0
                      t-debit = 0
                      t-credit = 0.
    
                  RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                    OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
    
                  CREATE out-list.
                  RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                  ASSIGN
                      out-list.fibukonto    = STRING(c, "x(15)")
                      out-list.bezeich      = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") .
    
                  ASSIGN
                      acc-bez   = gl-acct.bezeich
                      konto     = gl-acct.fibukonto.
              END.                          
    
              IF summ-date THEN
              DO:
                  IF date1 NE ? AND date1 NE gl-jhdrhis.datum THEN
                  DO:
                      CREATE out-list.
                      ASSIGN
                          out-list.fibukonto    = konto
                          out-list.trans-date   = date1
                          out-list.bezeich      = acc-bez
                          out-list.debit        = ddebit
                          out-list.credit       = dcredit
                          out-list.balance      = dbalance
                          out-list.debit-str    = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                          out-list.credit-str   = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                          out-list.balance-str  = STRING(dbalance, "->>>,>>>,>>>,>>9.99").
    
                      IF AVAILABLE gl-acct THEN DO:                                                  
                          IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                      out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                          IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                          ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).              
                      END.                            

                      ASSIGN
                          ddebit = 0
                          dcredit = 0.
                  END.
              END.
    
              FIND FIRST gl-account WHERE gl-account.fibukonto 
                = vhp.gl-jourhis.fibukonto NO-LOCK. 
              IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                 balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
              ELSE
              balance = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
              
                  t-debit = t-debit + vhp.gl-jourhis.debit.
                  t-credit = t-credit + vhp.gl-jourhis.credit.
                  tot-debit = tot-debit + vhp.gl-jourhis.debit.
                  tot-credit = tot-credit + vhp.gl-jourhis.credit. 
    
              IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                  ASSIGN
                     dbalance = dbalance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
              ELSE ASSIGN
                 dbalance = dbalance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
              ASSIGN
                 ddebit   = ddebit  + vhp.gl-jourhis.debit
                 dcredit  = dcredit + vhp.gl-jourhis.credit
                 date1    = vhp.gl-jhdrhis.datum.
    
    
              IF NOT summ-date THEN
              DO:
                  CREATE out-list.
                  ASSIGN
                      out-list.s-recid      = INTEGER(RECID(gl-jourhis))
                      out-list.fibukonto    = gl-jourhis.fibukonto
                      out-list.jnr          = gl-jhdrhis.jnr
                      out-list.jtype          = gl-jhdrhis.jtype
                      out-list.trans-date   = gl-jhdrhis.datum
                      out-list.refno        = gl-jhdrhis.refno
                      out-list.bezeich      = gl-jhdrhis.bezeich
                      out-list.debit        = gl-jourhis.debit
                      out-list.credit       = gl-jourhis.credit
                      out-list.uid          = gl-jourhis.userinit
                      out-list.created      = gl-jourhis.sysdate
                      out-list.chgID        = gl-jourhis.chginit
                      out-list.chgDate      = chgdate
                      out-list.bemerk       = STRING(get-bemerk(gl-jourhis.bemerk), "x(50)")
                      out-list.balance      = balance
                      out-list.debit-str    = STRING(gl-jourhis.debit, "->>>,>>>,>>>,>>9.99")
                      out-list.credit-str   = STRING(gl-jourhis.credit, "->>>,>>>,>>>,>>9.99")
                      out-list.balance-str  = STRING(balance, "->>>,>>>,>>>,>>9.99").
    
                  IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
    
                  IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                  ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).
                  
              END.
          END.                   
          ELSE DO:
              FIND FIRST gl-journal WHERE RECID(gl-journal) = j-list.grecid NO-LOCK NO-ERROR.
              IF AVAILABLE gl-journal THEN DO:
                 FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                 FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto 
                        AND gl-acct.deptnr = from-dept NO-LOCK NO-ERROR.
                 DELETE j-list.
               
                 IF gl-journal.chgdate = ? THEN chgdate = ?. 
                 ELSE chgdate = gl-journal.chgdate. 
                 IF konto = "" THEN 
                 DO:    
                   RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                       OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                   CREATE out-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   ASSIGN
                       out-list.refno      = STRING(c, "x(15)")
                       out-list.fibukonto  = STRING(c, "x(15)") 
                       out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                       out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") . 
        
                   ASSIGN 
                       acc-bez = gl-acct.bezeich
                       konto = gl-acct.fibukonto.
                 END.
        
                 IF konto NE gl-acct.fibukonto THEN
                 DO:
                     IF summ-date THEN
                     DO:
                         CREATE out-list.
                         ASSIGN
                             out-list.s-recid       = INTEGER(RECID(gl-journal))
                             out-list.fibukonto     = konto
                             out-list.trans-date    = date1
                             out-list.bezeich       = acc-bez
                             out-list.bemerk        = acc-bez
                             out-list.debit         = ddebit
                             out-list.credit        = dcredit
                             out-list.balance       = dbalance
                             out-list.debit-str     = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                             out-list.credit-str    = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                             out-list.balance-str   = STRING(dbalance, "->>>,>>>,>>>,>>9.99").

                         IF AVAILABLE gl-journal THEN
                         DO:
                            IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                            out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                         END.
        
                         IF AVAILABLE gl-acct THEN DO:                                                  
                             IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                         out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                             IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                             ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                         END.               

                         ASSIGN
                             ddebit = 0
                             dcredit = 0
                             date1 = gl-jouhdr.datum.
                     END.

                     CREATE out-list.
                     ASSIGN
                         out-list.bezeich       = "T O T A L  " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                         out-list.debit         = t-debit
                         out-list.credit        = t-credit
                         out-list.balance       = balance
                         out-list.debit-str     = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
                         out-list.credit-str    = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
                         out-list.balance-str   = STRING(balance, "->>>,>>>,>>>,>>9.99").
        
                     CREATE out-list.
                     ASSIGN
                         balance = 0
                         t-debit = 0
                         t-credit = 0.
        
                     RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                       OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
        
                     CREATE out-list.
                     RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                     ASSIGN
                         out-list.refno     = STRING(c, "x(15)")
                         out-list.fibukonto = STRING(c, "x(15)")
                         out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                         out-list.bemerk    = STRING(gl-acct.bezeich, "x(40)") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") .
        
                     ASSIGN
                         acc-bez    = gl-acct.bezeich
                         konto      = gl-acct.fibukonto.
                 END.
        
                 IF summ-date THEN
                 DO:
                     IF date1 NE ? AND date1 NE gl-jouhdr.datum THEN
                     DO:
                         CREATE out-list.
                         ASSIGN
                             out-list.fibukonto     = konto
                             out-list.trans-date    = date1
                             out-list.bezeich       = acc-bez
                             out-list.bemerk        = acc-bez
                             out-list.debit         = ddebit
                             out-list.credit        = dcredit
                             out-list.balance       = dbalance
                             out-list.debit-str     = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                             out-list.credit-str    = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                             out-list.balance-str   = STRING(dbalance, "->>>,>>>,>>>,>>9.99").
        
                         IF AVAILABLE gl-acct THEN DO:                                                  
                             IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                         out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                             IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                             ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                         END.                                       

                         ASSIGN
                             ddebit = 0
                             dcredit = 0.
                     END.
                 END.
                 FIND FIRST gl-account WHERE gl-account.fibukonto 
                   = gl-journal.fibukonto NO-LOCK. 
                 IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    balance = balance - gl-journal.debit + gl-journal.credit.
                 ELSE
                     balance    = balance + gl-journal.debit - gl-journal.credit.
        
                         t-debit    = t-debit + gl-journal.debit.
                         t-credit   = t-credit + gl-journal.credit.
                         tot-debit  = tot-debit + gl-journal.debit.
                         tot-credit = tot-credit + gl-journal.credit. 
        
                 IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     ASSIGN
                        dbalance = dbalance - gl-journal.debit + gl-journal.credit.
                 ELSE ASSIGN
                    dbalance = dbalance + gl-journal.debit - gl-journal.credit.
                 ASSIGN
                    ddebit   = ddebit  + gl-journal.debit
                    dcredit  = dcredit + gl-journal.credit
                    date1    = gl-jouhdr.datum.
        
                 IF NOT summ-date THEN
                 DO:
                     CREATE out-list.
                     ASSIGN
                         out-list.s-recid       = INTEGER(RECID(gl-journal))
                         out-list.fibukonto     = gl-journal.fibukonto
                         out-list.jnr           = gl-jouhdr.jnr
                         out-list.jtype         = gl-jouhdr.jtype
                         out-list.trans-date    = gl-jouhdr.datum
                         out-list.refno         = gl-jouhdr.refno
                         out-list.bezeich       = gl-jouhdr.bezeich
                         out-list.debit         = gl-journal.debit
                         out-list.credit        = gl-journal.credit
                         out-list.uid           = gl-journal.userinit
                         out-list.created       = gl-journal.sysdate
                         out-list.chgID         = gl-journal.chginit
                         out-list.chgDate       = chgdate
                         out-list.bemerk        = STRING(get-bemerk(gl-journal.bemerk), "x(50)")
                         out-list.balance       = balance
                         out-list.debit-str     = STRING(gl-journal.debit, "->>>,>>>,>>>,>>9.99")
                         out-list.credit-str    = STRING(gl-journal.credit, "->>>,>>>,>>>,>>9.99")
                         out-list.balance-str   = STRING(balance, "->>>,>>>,>>>,>>9.99")
                     .

                     IF AVAILABLE gl-journal THEN
                     DO:
                        IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                        out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                     END.
        
                     IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
        
                     IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(50)").
                     ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(50)").                         
                 END.                        
              END.
          END. /*end do*/
        END. /*end for ech*/

        IF summ-date THEN
        DO:
            CREATE out-list.
            ASSIGN
                out-list.s-recid        = INTEGER(RECID(gl-journal))
                out-list.fibukonto      = konto
                out-list.trans-date     = date1
                out-list.bezeich        = acc-bez
                out-list.debit          = ddebit
                out-list.credit         = dcredit
                out-list.balance        = dbalance
                out-list.debit-str      = STRING(ddebit, "->>>,>>>,>>>,>>9.99")
                out-list.credit-str     = STRING(dcredit, "->>>,>>>,>>>,>>9.99")
                out-list.balance-str    = STRING(dbalance, "->>>,>>>,>>>,>>9.99").

            IF AVAILABLE gl-journal THEN
            DO:
               IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
               out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
            END.

            IF AVAILABLE gl-acct THEN DO:                                                  
                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
            END.                                                      

            ASSIGN
                ddebit = 0
                dcredit = 0.
        END.
        CREATE out-list.
        ASSIGN
            out-list.bezeich        = "T O T A L  " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
            out-list.debit          = t-debit
            out-list.credit         = t-credit
            out-list.balance        = balance
            out-list.debit-str      = STRING(t-debit, "->>>,>>>,>>>,>>9.99")
            out-list.credit-str     = STRING(t-credit, "->>>,>>>,>>>,>>9.99")
            out-list.balance-str    = STRING(balance, "->>>,>>>,>>>,>>9.99").

        CREATE out-list.
        CREATE out-list.

        ASSIGN
            out-list.bezeich        = "GRAND T O T A L               " 
            out-list.debit          = tot-debit
            out-list.credit         = tot-credit
            out-list.debit-str      = STRING(tot-debit, "->>>,>>>,>>>,>>9.99")
            out-list.credit-str     = STRING(tot-credit, "->>>,>>>,>>>,>>9.99").
        END.
  END.
END.

/* Modify by Michael @ 15/10/2018 for La Joya request - ticket no FF10ED */
PROCEDURE create-hglist:
    FOR EACH g-list:
        DELETE g-list.
    END.

    IF f-note NE "" THEN
    DO:
        FOR EACH vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.datum GE from-date
            AND vhp.gl-jhdrhis.datum LE to-date NO-LOCK BY vhp.gl-jhdrhis.datum:
            IF journaltype EQ 0 AND excl-other AND gl-jhdrhis.jtype NE 0 THEN 
                NEXT.
            ELSE IF journaltype NE 0 AND NOT other-dept 
              AND vhp.gl-jhdrhis.jtype NE journaltype THEN NEXT.
            FOR EACH gl-jourhis WHERE gl-jourhis.jnr = vhp.gl-jhdrhis.jnr
                AND gl-jourhis.bemerk MATCHES "*" + f-note + "*"
                AND gl-jourhis.fibukonto GE from-fibu
                AND gl-jourhis.fibukonto LE to-fibu NO-LOCK 
                BY gl-jourhis.fibukonto:
                CREATE g-list.
                ASSIGN
                    g-list.grecid = RECID(gl-jourhis)
                    g-list.fibu   = gl-jourhis.fibukonto.
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.datum GE from-date
            AND vhp.gl-jhdrhis.datum LE to-date NO-LOCK BY vhp.gl-jhdrhis.datum:
            IF journaltype EQ 0 AND excl-other AND gl-jhdrhis.jtype NE 0 THEN 
                NEXT.
            ELSE IF journaltype NE 0 AND NOT other-dept 
              AND vhp.gl-jhdrhis.jtype NE journaltype THEN NEXT.
            FOR EACH gl-jourhis WHERE gl-jourhis.jnr = vhp.gl-jhdrhis.jnr
                AND gl-jourhis.fibukonto GE from-fibu
                AND gl-jourhis.fibukonto LE to-fibu NO-LOCK 
                BY gl-jourhis.fibukonto:
                CREATE g-list.
                ASSIGN
                    g-list.grecid = RECID(gl-jourhis)
                    g-list.fibu   = gl-jourhis.fibukonto.
            END.
        END.
    END.
END.


PROCEDURE create-hlist: 
DEFINE VARIABLE debit       AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*->>>,>>>,>>>,>>9.99*/
DEFINE VARIABLE credit      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*->>>,>>>,>>>,>>9.99*/
DEFINE VARIABLE balance     AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>9.99" INITIAL 0. /*->>>,>>>,>>>,>>9.99*/
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE c           AS CHAR. 
DEFINE VARIABLE bezeich     AS CHAR. 
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE refno       AS CHAR. 
DEFINE VARIABLE h-bezeich   AS CHAR. 
DEFINE VARIABLE id          AS CHAR FORMAT "x(2)". 
DEFINE VARIABLE chgdate     AS DATE. 
DEFINE VARIABLE beg-date    AS DATE. 
DEFINE VARIABLE beg-day     AS INTEGER. 

DEFINE VARIABLE date1       AS DATE.
DEFINE VARIABLE ddebit      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE dcredit     AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE dbalance    AS DECIMAL FORMAT "->>>,>>>,>>9.99".
 
DEFINE VARIABLE t-debit     LIKE debit  INITIAL 0. 
DEFINE VARIABLE t-credit    LIKE credit INITIAL 0. 
DEFINE VARIABLE tot-debit   LIKE debit  INITIAL 0. 
DEFINE VARIABLE tot-credit  LIKE credit INITIAL 0. 
 
DEFINE VARIABLE e-bal AS DECIMAL INITIAL 0. 
DEFINE VARIABLE delta AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fdate AS DATE. 
DEFINE VARIABLE tdate AS DATE. 
 
DEFINE buffer gl-account FOR gl-acct. 
DEFINE buffer gl-jour1   FOR gl-jourhis. 
DEFINE buffer gl-jouh1   FOR gl-jhdrhis. 
 
DEFINE VARIABLE prev-mm  AS INTEGER. 
DEFINE VARIABLE prev-yr  AS INTEGER.
DEFINE VARIABLE prev-bal AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*"->>>,>>>,>>>,>>9.99"*/
DEFINE VARIABLE end-bal  AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*"->>>,>>>,>>>,>>9.99"*/
 
DEFINE VARIABLE blankchar AS CHAR FORMAT "x(70)" INITIAL "". 
DEFINE VARIABLE acc-bez   AS CHAR FORMAT "x(24)" INITIAL "".

  DO i = 1 TO 72: 
    blankchar = blankchar + " ". 
  END. 
 
  ASSIGN
    prev-mm = MONTH(from-date) - 1
    prev-yr = YEAR(from-date)
  .
  IF prev-mm = 0 THEN 
  ASSIGN
    prev-mm = 12
    prev-yr = prev-yr - 1
  .
 
  beg-date = DATE(MONTH(from-date), 1, YEAR(from-date)). 

  FOR EACH out-list:
      DELETE out-list.
  END.

  DO:
      IF sorttype = 2 THEN
      DO:
          FOR EACH g-list,
            FIRST vhp.gl-jourhis WHERE RECID(vhp.gl-jourhis) = g-list.grecid NO-LOCK,
            FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr NO-LOCK,
            FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto NO-LOCK 
            BY vhp.gl-jourhis.fibukonto BY vhp.gl-jourhis.datum BY vhp.gl-jourhis.zeit
            BY gl-jhdrhis.refno BY SUBSTR(vhp.gl-jourhis.bemerk,1,24): 
            DELETE g-list.
            /*
                  FOR EACH gl-jourhis WHERE  gl-jourhis.fibukonto GE from-fibu 
                    AND gl-jourhis.fibukonto LE to-fibu NO-LOCK,
                    FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr 
                    AND gl-jhdrhis.datum GE from-date AND gl-jhdrhis.datum LE to-date NO-LOCK, 
                    FIRST gl-acct WHERE gl-acct.fibukonto = gl-jourhis.fibukonto NO-LOCK 
                    BY gl-jourhis.fibukonto BY gl-jhdrhis.datum 
                    BY gl-jhdrhis.refno BY SUBSTR(gl-jourhis.bemerk,1,24): 

                    IF journaltype EQ 0 AND excl-other AND gl-jhdrhis.jtype NE 0 THEN 
                        NEXT.
                    ELSE IF journaltype NE 0 AND NOT other-dept 
                        AND gl-jhdrhis.jtype NE journaltype THEN NEXT.
            */
            IF vhp.gl-jourhis.chgdate = ? THEN chgdate = ?. 
            ELSE chgdate = vhp.gl-jourhis.chgdate. 


            IF konto = "" THEN 
            DO:
              RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
				
              IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN
                /*ASSIGN balance = balance - vhp.gl-jourhis.debit 
                  + vhp.gl-jourhis.credit.*/

                  /*fixed bugs discrepancy ending balance, example reference no 250-00-010 (09/2015) -> fadly 22/07/19*/
                  prev-bal = - prev-bal.
              ELSE balance = prev-bal. /*end fadly*/
                /*ASSIGN balance = balance + vhp.gl-jourhis.debit 
                  - vhp.gl-jourhis.credit.*/

                CREATE out-list.
                RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).

                ASSIGN
                    out-list.fibukonto = c
                    out-list.refno     = STRING(c, "x(15)")
                    out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)")
                    out-list.bemerk    = STRING(gl-acct.bezeich)
					out-list.prev-bal  = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */																														 

                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(40)").
                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(40)").

                ASSIGN
                    konto   = gl-acct.fibukonto
                    acc-bez = gl-acct.bezeich.
            END.


            IF konto NE gl-acct.fibukonto THEN
            DO:
                IF summ-date THEN
                DO:
                    CREATE out-list.
                    ASSIGN
                        out-list.s-recid        = INTEGER(RECID(gl-jourhis))
                        out-list.fibukonto      = konto
                        out-list.trans-date     = date1
                        out-list.bezeich        = STRING(acc-bez, "x(40)")
                        out-list.bemerk         = STRING(acc-bez, "x(40)")
                        out-list.debit          = ddebit
                        out-list.credit         = dcredit
                        out-list.balance        = dbalance
                        out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99"*/
                        out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99"*/
                        out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99"*/
                        /*out-list.jnr = gl-jhdrhis.jnr*/
                        .

                    IF AVAILABLE gl-jourhis THEN
                    DO:
                       IF NUM-ENTRIES(gl-jourhis.bemerk, CHR(2)) GT 1 THEN                       
                       out-list.number1 = ENTRY(2,gl-jourhis.bemerk,CHR(2)).   
                    END.

                    IF AVAILABLE gl-acct THEN DO:                                                  
                        IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                    out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                        IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                        ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                    END.                                            

                    ASSIGN
                        ddebit  = 0
                        dcredit = 0
                        date1   = gl-jhdrhis.datum.
                END.

                CREATE out-list.
                ASSIGN
                    out-list.bezeich        = "T O T A L " /*+ STRING(prev-bal, "->>>,>>>,>>>,>>9.99") */
                    out-list.debit          = t-debit
                    out-list.credit         = t-credit
                    out-list.balance        = balance
                    out-list.debit-str      = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99"*/
                    out-list.credit-str     = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99"*/
                    out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99"*/
                    out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
                
                CREATE out-list.

                ASSIGN
                    balance     = 0
                    t-debit     = 0
                    t-credit    = 0.

                RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                  OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
                CREATE out-list.
                RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                ASSIGN
                    out-list.refno      = STRING(c, "x(15)")
                    out-list.fibukonto  = STRING(c, "x(15)")
                    out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)")
                    out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)")
                    acc-bez             = gl-acct.bezeich
                    konto               = gl-acct.fibukonto
                    out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */																														  
            END.

            
            IF summ-date THEN
            DO:
                IF date1 NE ? AND date1 NE gl-jhdrhis.datum THEN
                DO:
                    CREATE out-list.
                    ASSIGN
                        out-list.fibukonto      = konto
                        out-list.trans-date     = date1
                        out-list.bezeich        = acc-bez
                        out-list.debit          = ddebit
                        out-list.credit         = dcredit
                        out-list.balance        = dbalance
                        out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99") /*"->>>,>>>,>>>,>>9.99"*/
                        out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99") /*"->>>,>>>,>>>,>>9.99"*/
                        out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99"). /*"->>>,>>>,>>>,>>9.99"*/

                    IF AVAILABLE gl-acct THEN DO:                                                  
                        IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                    out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                        IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                        ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                    END.          

                    ASSIGN
                        ddebit = 0
                        dcredit = 0.
                END.
            END.
            
            FIND FIRST gl-account WHERE gl-account.fibukonto 
              = vhp.gl-jourhis.fibukonto NO-LOCK. 
            IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                ASSIGN
                balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
            ELSE ASSIGN
               balance      = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                /*balance = balance + gl-jourhis.debit - gl-jourhis.credit. */

            
            ASSIGN 
                t-debit     = t-debit + vhp.gl-jourhis.debit
                t-credit    = t-credit + vhp.gl-jourhis.credit
                tot-debit   = tot-debit + vhp.gl-jourhis.debit
                tot-credit  = tot-credit + vhp.gl-jourhis.credit. 
            
            IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                ASSIGN
                   dbalance = dbalance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
            ELSE ASSIGN
               dbalance = dbalance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
            ASSIGN
               ddebit   = ddebit  + vhp.gl-jourhis.debit
               dcredit  = dcredit + vhp.gl-jourhis.credit
               date1    = gl-jhdrhis.datum.

            
            IF NOT summ-date THEN
            DO:
                CREATE out-list.
                ASSIGN
                    out-list.s-recid        = INTEGER(RECID(gl-jourhis))
                    out-list.fibukonto      = gl-jourhis.fibukonto
                    out-list.jnr            = gl-jhdrhis.jnr
                    out-list.jtype          = gl-jhdrhis.jtype
                    out-list.trans-date     = gl-jhdrhis.datum
                    out-list.refno          = gl-jhdrhis.refno
                    out-list.bezeich        = gl-jhdrhis.bezeich
                    out-list.debit          = gl-jourhis.debit
                    out-list.credit         = gl-jourhis.credit
                    out-list.uid            = gl-jourhis.userinit
                    out-list.created        = gl-jourhis.sysdate
                    out-list.chgID          = gl-jourhis.chginit
                    out-list.chgDate        = chgdate
                    out-list.bemerk         = STRING(get-bemerk(gl-jourhis.bemerk), "x(100)") /*"x(50)" Modified Gerald 240220*/ 
                    out-list.balance        = balance
                    out-list.debit-str      = STRING(gl-jourhis.debit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99"*/
                    out-list.credit-str     = STRING(gl-jourhis.credit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99"*/
                    out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99").           /*->>>,>>>,>>>,>>9.99"*/

                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).
                
            END.
             /*IF NOT too-old THEN 
             DO:
                 IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    e-bal = e-bal - gl-jourhis.debit + gl-jourhis.credit. 
                 ELSE e-bal = e-bal + gl-jourhis.debit - gl-jourhis.credit. 
             END.
             str = str + STRING(e-bal, "->>>,>>>,>>>,>>9.99").*/
             /*IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
               STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
             ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). */
          END. /*end for*/

          IF summ-date THEN
          DO:
              CREATE out-list.
              ASSIGN
                  out-list.s-recid          = INTEGER(RECID(gl-jourhis))
                  out-list.fibukonto        = konto
                  out-list.trans-date       = date1
                  out-list.bezeich          = acc-bez
                  out-list.debit            = ddebit
                  out-list.credit           = dcredit
                  out-list.balance          = dbalance
                  out-list.debit-str        = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*"->>>,>>>,>>>,>>9.99"*/
                  out-list.credit-str       = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*"->>>,>>>,>>>,>>9.99"*/
                  out-list.balance-str      = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*"->>>,>>>,>>>,>>9.99"*/

              IF AVAILABLE gl-jourhis THEN
              DO:
                 IF NUM-ENTRIES(gl-jourhis.bemerk, CHR(2)) GT 1 THEN                       
                 out-list.number1 = ENTRY(2,gl-jourhis.bemerk,CHR(2)).   
              END.

              ASSIGN
                  ddebit = 0
                  dcredit = 0.
          END.

          CREATE out-list.
          ASSIGN
              out-list.bezeich      = "T O T A L " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
              out-list.debit        = t-debit
              out-list.credit       = t-credit
              out-list.balance      = balance
              out-list.debit-str    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")    /*"->>>,>>>,>>>,>>9.99"*/
              out-list.credit-str   = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")   /*"->>>,>>>,>>>,>>9.99"*/
              out-list.balance-str  = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")   /*"->>>,>>>,>>>,>>9.99"*/
              out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
          
          CREATE out-list.
          CREATE out-list.

          ASSIGN
              out-list.bezeich      = "GRAND T O T A L               " 
              out-list.debit        = tot-debit
              out-list.credit       = tot-credit
              out-list.debit-str    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")      /*"->>>,>>>,>>>,>>9.99"*/
              out-list.credit-str   = STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99").    /*"->>>,>>>,>>>,>>9.99"*/

          
      END.
      ELSE IF sorttype = 1 THEN
      DO:
          FOR EACH g-list,
            FIRST vhp.gl-jourhis WHERE RECID(vhp.gl-jourhis) = g-list.grecid NO-LOCK,
            FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr NO-LOCK,
            FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto 
              AND gl-acct.main-nr = /*gl-main.nr*/ from-main NO-LOCK
            BY vhp.gl-jourhis.fibukonto /*BY vhp.gl-jhdrhis.datum*/ BY vhp.gl-jourhis.datum   BY vhp.gl-jourhis.zeit
            BY vhp.gl-jhdrhis.refno BY SUBSTR(vhp.gl-jourhis.bemerk,1,24): 
            DELETE g-list.
            /*
              FOR EACH gl-jourhis WHERE  gl-jourhis.fibukonto GE from-fibu 
                AND gl-jourhis.fibukonto LE to-fibu NO-LOCK, 
                FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr 
                AND gl-jhdrhis.datum GE from-date AND gl-jhdrhis.datum LE to-date NO-LOCK, 
                FIRST gl-acct WHERE gl-acct.fibukonto = gl-jourhis.fibukonto 
                  AND gl-acct.main-nr = gl-main.nr NO-LOCK 
                BY gl-jourhis.fibukonto BY gl-jhdrhis.datum 
                BY gl-jhdrhis.refno BY SUBSTR(gl-jourhis.bemerk,1,24): 

                IF journaltype EQ 0 AND excl-other AND gl-jhdrhis.jtype NE 0 THEN 
                    NEXT.
                ELSE IF journaltype NE 0 AND NOT other-dept 
                    AND gl-jhdrhis.jtype NE journaltype THEN NEXT.
            */
            IF vhp.gl-jourhis.chgdate = ? THEN chgdate = ?. 
            ELSE chgdate = vhp.gl-jourhis.chgdate. 
            IF konto = "" THEN 
            DO:    
              RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                  OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
              CREATE out-list. 
              RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
              ASSIGN
                  out-list.fibukonto = STRING(c, "x(15)") 
                  out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)") 
                  /*FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/
                  out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

              ASSIGN
                  konto = gl-acct.fibukonto
                  acc-bez = gl-acct.bezeich.
            END.

            IF konto NE gl-acct.fibukonto THEN
            DO:
                IF summ-date THEN
                DO:
                    CREATE out-list.
                    ASSIGN
                        out-list.s-recid        = INTEGER(RECID(gl-jourhis))
                        out-list.fibukonto      = konto
                        out-list.trans-date     = date1
                        out-list.bezeich        = acc-bez
                        out-list.debit          = ddebit
                        out-list.credit         = dcredit
                        out-list.balance        = dbalance
                        out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*"->>>,>>>,>>>,>>9.99"*/
                        out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*"->>>,>>>,>>>,>>9.99"*/
                        out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*"->>>,>>>,>>>,>>9.99"*/

                    IF AVAILABLE gl-jourhis THEN
                    DO:
                       IF NUM-ENTRIES(gl-jourhis.bemerk, CHR(2)) GT 1 THEN                       
                       out-list.number1 = ENTRY(2,gl-jourhis.bemerk,CHR(2)).   
                    END.

                    IF AVAILABLE gl-acct THEN DO:                                                  
                        IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                    out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                        IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                        ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                    END.                                          

                    ASSIGN
                        ddebit  = 0
                        dcredit = 0
                        date1   = gl-jhdrhis.datum.
                END.
                CREATE out-list.
                ASSIGN
                    out-list.bezeich        = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                    out-list.debit          = t-debit
                    out-list.credit         = t-credit
                    out-list.balance        = balance
                    out-list.debit-str      = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")    /*"->>>,>>>,>>>,>>9.99"*/
                    out-list.credit-str     = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")   /*"->>>,>>>,>>>,>>9.99"*/
                    out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")   /*"->>>,>>>,>>>,>>9.99"*/
                    out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

                CREATE out-list.
                ASSIGN
                    balance  = 0
                    t-debit  = 0
                    t-credit = 0.

                RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                  OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).

                CREATE out-list.
                RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
                ASSIGN
                    out-list.fibukonto = STRING(c, "x(15)")
                    out-list.bezeich = STRING(gl-acct.bezeich, "x(40)")
                    out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

                ASSIGN
                    acc-bez = gl-acct.bezeich
                    konto   = gl-acct.fibukonto.
            END.

            IF summ-date THEN
            DO:
                IF date1 NE ? AND date1 NE gl-jhdrhis.datum THEN
                DO:
                    CREATE out-list.
                    ASSIGN
                        out-list.fibukonto      = konto
                        out-list.trans-date     = date1
                        out-list.bezeich        = acc-bez
                        out-list.debit          = ddebit
                        out-list.credit         = dcredit
                        out-list.balance        = dbalance
                        out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*"->>>,>>>,>>>,>>9.99"*/
                        out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*"->>>,>>>,>>>,>>9.99"*/
                        out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*"->>>,>>>,>>>,>>9.99"*/
                        
                    IF AVAILABLE gl-acct THEN DO:                                                  
                        IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                    out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                        IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                        ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                    END.                                                                           

                    ASSIGN
                        ddebit  = 0
                        dcredit = 0.
                END.
            END.

            FIND FIRST gl-account WHERE gl-account.fibukonto 
              = vhp.gl-jourhis.fibukonto NO-LOCK. 
            IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
               balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
            ELSE
            balance = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.

            
                t-debit = t-debit + vhp.gl-jourhis.debit.
                t-credit = t-credit + vhp.gl-jourhis.credit.
                tot-debit = tot-debit + vhp.gl-jourhis.debit.
                tot-credit = tot-credit + vhp.gl-jourhis.credit. 

            IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                ASSIGN
                   dbalance = dbalance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
            ELSE ASSIGN
               dbalance = dbalance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
            ASSIGN
               ddebit   = ddebit  + vhp.gl-jourhis.debit
               dcredit  = dcredit + vhp.gl-jourhis.credit
               date1    = vhp.gl-jhdrhis.datum.

            IF NOT summ-date THEN
            DO:
                CREATE out-list.
                ASSIGN
                    out-list.s-recid        = INTEGER(RECID(gl-jourhis))
                    out-list.fibukonto      = gl-jourhis.fibukonto
                    out-list.jnr            = gl-jhdrhis.jnr
                    out-list.jtype          = gl-jhdrhis.jtype
                    out-list.trans-date     = gl-jhdrhis.datum
                    out-list.refno          = gl-jhdrhis.refno
                    out-list.bezeich        = gl-jhdrhis.bezeich
                    out-list.debit          = gl-jourhis.debit
                    out-list.credit         = gl-jourhis.credit
                    out-list.uid            = gl-jourhis.userinit
                    out-list.created        = gl-jourhis.sysdate
                    out-list.chgID          = gl-jourhis.chginit
                    out-list.chgDate        = chgdate
                    out-list.bemerk         = STRING(get-bemerk(gl-jourhis.bemerk), "x(100)") /*"x(50)" modified gerald 240220*/
                    out-list.balance        = balance
                    out-list.debit-str      = STRING(gl-jourhis.debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                    out-list.credit-str     = STRING(gl-jourhis.credit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                    out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/

                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

            END.

             /*
             IF NOT too-old THEN 
             DO:
               IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    e-bal = e-bal - gl-jourhis.debit + gl-jourhis.credit. 
               ELSE e-bal = e-bal + gl-jourhis.debit - gl-jourhis.credit. 
             END.
             STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99").
                 
             IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
               STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
             ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). 
             */

          END.
          IF summ-date THEN
          DO:
              CREATE out-list.
              ASSIGN
                  out-list.s-recid      = INTEGER(RECID(gl-jourhis))
                  out-list.fibukonto    = konto
                  out-list.trans-date   = date1
                  out-list.bezeich      = acc-bez
                  out-list.debit        = ddebit
                  out-list.credit       = dcredit
                  out-list.balance      = dbalance
                  out-list.debit-str    = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                  out-list.credit-str   = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                  out-list.balance-str  = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/

              IF AVAILABLE gl-jourhis THEN
              DO:
                 IF NUM-ENTRIES(gl-jourhis.bemerk, CHR(2)) GT 1 THEN                       
                 out-list.number1 = ENTRY(2,gl-jourhis.bemerk,CHR(2)).   
              END.

              IF AVAILABLE gl-acct THEN DO:                                                  
                  IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                              out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                  IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                  ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
              END.                                                

              ASSIGN
                  ddebit = 0
                  dcredit = 0.
          END.

          CREATE out-list.
          ASSIGN
              out-list.bezeich      =  "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
              out-list.debit        = tot-debit
              out-list.credit       = tot-credit
              out-list.debit-str    = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
              out-list.credit-str   = STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
              out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

          
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
        FOR EACH g-list,
          FIRST vhp.gl-jourhis WHERE RECID(vhp.gl-jourhis) = g-list.grecid NO-LOCK,
          FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr NO-LOCK,
          FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto 
          AND gl-acct.deptnr = from-dept NO-LOCK 
          BY vhp.gl-jourhis.fibukonto BY vhp.gl-jourhis.datum BY vhp.gl-jourhis.zeit
          BY vhp.gl-jhdrhis.refno BY SUBSTR(vhp.gl-jourhis.bemerk,1,24): 
          DELETE g-list.
          /*
            FOR EACH gl-jourhis WHERE  gl-jourhis.fibukonto GE from-fibu 
              AND gl-jourhis.fibukonto LE to-fibu NO-LOCK, 
              FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr 
              AND gl-jhdrhis.datum GE from-date AND gl-jhdrhis.datum LE to-date NO-LOCK, 
              FIRST gl-acct WHERE gl-acct.fibukonto = gl-jourhis.fibukonto 
              AND gl-acct.deptnr = from-dept NO-LOCK 
              BY gl-jourhis.fibukonto BY gl-jhdrhis.datum 
              BY gl-jhdrhis.refno BY SUBSTR(gl-jourhis.bemerk,1,24): 

              IF excl-other AND gl-jhdrhis.jtype NE 0 THEN 
                  NEXT.
          */         
          IF vhp.gl-jourhis.chgdate = ? THEN chgdate = ?. 
          ELSE chgdate = vhp.gl-jourhis.chgdate. 
          IF konto = "" THEN 
          DO:    
            RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
            CREATE out-list. 
            RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
            ASSIGN
                out-list.fibukonto = STRING(c, "x(15)") 
                out-list.bezeich = STRING(gl-acct.bezeich, "x(40)") /*+
                FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/
                out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
            ASSIGN 
                acc-bez = gl-acct.bezeich
                konto = gl-acct.fibukonto.
          END.

          IF konto NE gl-acct.fibukonto THEN
          DO:
              IF summ-date THEN
              DO:
                  CREATE out-list.
                  ASSIGN
                      out-list.s-recid      = INTEGER(RECID(gl-jourhis))
                      out-list.fibukonto    = konto
                      out-list.trans-date   = date1
                      out-list.bezeich      = acc-bez
                      out-list.debit        = ddebit
                      out-list.credit       = dcredit
                      out-list.balance      = dbalance
                      out-list.debit-str    = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                      out-list.credit-str   = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                      out-list.balance-str  = STRING(dbalance, "->,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

                  IF AVAILABLE gl-jourhis THEN
                  DO:
                     IF NUM-ENTRIES(gl-jourhis.bemerk, CHR(2)) GT 1 THEN                       
                     out-list.number1 = ENTRY(2,gl-jourhis.bemerk,CHR(2)).   
                  END.

                  IF AVAILABLE gl-acct THEN DO:                                                  
                      IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                  out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                      IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                      ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
                  END.                                                                           

                  ASSIGN
                      ddebit = 0
                      dcredit = 0
                      date1 = gl-jhdrhis.datum.
              END.
			 
              CREATE out-list.
              ASSIGN
                  out-list.bezeich      = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                  out-list.debit        = t-debit
                  out-list.credit       = t-credit
                  out-list.balance      = balance
                  out-list.debit-str    = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                  out-list.credit-str   = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                  out-list.balance-str  = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                  out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

              CREATE out-list.
              ASSIGN
                  balance = 0
                  t-debit = 0
                  t-credit = 0.

              RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                                OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).

              CREATE out-list.
              RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
              ASSIGN
                  out-list.fibukonto    = STRING(c, "x(15)")
			      out-list.bezeich      = STRING(gl-acct.bezeich, "x(40)")
                  out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */																														

              ASSIGN
                  acc-bez   = gl-acct.bezeich
                  konto     = gl-acct.fibukonto.
          END.                          

          IF summ-date THEN
          DO:
              IF date1 NE ? AND date1 NE gl-jhdrhis.datum THEN
              DO:
                  CREATE out-list.
                  ASSIGN
                      out-list.fibukonto    = konto
                      out-list.trans-date   = date1
                      out-list.bezeich      = acc-bez
                      out-list.debit        = ddebit
                      out-list.credit       = dcredit
                      out-list.balance      = dbalance
                      out-list.debit-str    = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                      out-list.credit-str   = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                      out-list.balance-str  = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/

                  IF AVAILABLE gl-acct THEN DO:                                                  
                      IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                                  out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                      IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                      ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).              
                  END.                      

                  ASSIGN
                      ddebit = 0
                      dcredit = 0.
              END.
          END.


          FIND FIRST gl-account WHERE gl-account.fibukonto 
            = vhp.gl-jourhis.fibukonto NO-LOCK. 
          IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
             balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
          ELSE
          balance = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.

          
              t-debit = t-debit + vhp.gl-jourhis.debit.
              t-credit = t-credit + vhp.gl-jourhis.credit.
              tot-debit = tot-debit + vhp.gl-jourhis.debit.
              tot-credit = tot-credit + vhp.gl-jourhis.credit. 

          IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
              ASSIGN
                 dbalance = dbalance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
          ELSE ASSIGN
             dbalance = dbalance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
          ASSIGN
             ddebit   = ddebit  + vhp.gl-jourhis.debit
             dcredit  = dcredit + vhp.gl-jourhis.credit
             date1    = vhp.gl-jhdrhis.datum.


          IF NOT summ-date THEN
          DO:
              CREATE out-list.
              ASSIGN
                  out-list.s-recid      = INTEGER(RECID(gl-jourhis))
                  out-list.fibukonto    = gl-jourhis.fibukonto
                  out-list.jnr          = gl-jhdrhis.jnr
                  out-list.jtype          = gl-jhdrhis.jtype
                  out-list.trans-date   = gl-jhdrhis.datum
                  out-list.refno        = gl-jhdrhis.refno
                  out-list.bezeich      = gl-jhdrhis.bezeich
                  out-list.debit        = gl-jourhis.debit
                  out-list.credit       = gl-jourhis.credit
                  out-list.uid          = gl-jourhis.userinit
                  out-list.created      = gl-jourhis.sysdate
                  out-list.chgID        = gl-jourhis.chginit
                  out-list.chgDate      = chgdate
                  out-list.bemerk       = STRING(get-bemerk(gl-jourhis.bemerk), "x(100)") /*"x(50)" modified gerald 240220*/
                  out-list.balance      = balance
                  out-list.debit-str    = STRING(gl-jourhis.debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                  out-list.credit-str   = STRING(gl-jourhis.credit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                  out-list.balance-str  = STRING(balance, "->>,>>>,>>>,>>>,>>9.99").          /*->>>,>>>,>>>,>>9.99*/ 

              IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

              IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
              ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).
              
          END.

         /*IF NOT too-old THEN 
         DO:
           IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                e-bal = e-bal - gl-jourhis.debit + gl-jourhis.credit. 
           ELSE e-bal = e-bal + gl-jourhis.debit - gl-jourhis.credit.
         END.
           
         STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99").
         */
         /*IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
           STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
         ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). */
        END.

        IF summ-date THEN
        DO:
            CREATE out-list.
            ASSIGN
                out-list.s-recid        = INTEGER(RECID(gl-jourhis))
                out-list.fibukonto      = konto
                out-list.trans-date     = date1
                out-list.bezeich        = acc-bez
                out-list.debit          = ddebit
                out-list.credit         = dcredit
                out-list.balance        = dbalance
                out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

            IF AVAILABLE gl-jourhis THEN
            DO:
               IF NUM-ENTRIES(gl-jourhis.bemerk, CHR(2)) GT 1 THEN                       
               out-list.number1 = ENTRY(2,gl-jourhis.bemerk,CHR(2)).   
            END.

            IF AVAILABLE gl-acct THEN DO:                                                  
                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN                              
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").             
                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).          
                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).          
            END.                            

            ASSIGN
                ddebit = 0
                dcredit = 0.
        END.
        
        CREATE out-list.
        ASSIGN
            out-list.bezeich        = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
            out-list.debit          = t-debit
            out-list.credit         = t-credit
            out-list.balance        = balance
            out-list.debit-str      = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")      /*->>>,>>>,>>>,>>9.99*/
            out-list.credit-str     = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
            out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
            out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

        CREATE out-list.
        CREATE out-list.

        ASSIGN
            out-list.bezeich        = "GRAND T O T A L               " 
            out-list.debit          = tot-debit
            out-list.credit         = tot-credit
            out-list.debit-str      = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
            out-list.credit-str     = STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/   
        END.
  END.
END.

/* Modify by Michael @ 15/10/2018 for La Joya request - ticket no FF10ED */
PROCEDURE create-glist:
    FOR EACH g-list:
        DELETE g-list.
    END.

    IF f-note NE "" THEN
    DO:
        FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date
            AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:
            IF journaltype EQ 0 AND excl-other AND gl-jouhdr.jtype NE 0 THEN 
                NEXT.
            ELSE IF journaltype NE 0 AND other-dept 
              AND gl-jouhdr.jtype EQ 0 THEN NEXT. 
            ELSE IF journaltype NE 0 AND NOT other-dept 
              AND gl-jouhdr.jtype NE journaltype 
              AND gl-jouhdr.jtype NE journaltype1 THEN NEXT.
            FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
                AND gl-journal.bemerk MATCHES "*" + f-note + "*"
                AND gl-journal.fibukonto GE from-fibu
                AND gl-journal.fibukonto LE to-fibu NO-LOCK 
                BY gl-journal.fibukonto:
                CREATE g-list.
                ASSIGN
                    g-list.grecid = RECID(gl-journal)
                    g-list.fibu   = gl-journal.fibukonto.
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date
            AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:
            IF journaltype EQ 0 AND excl-other AND gl-jouhdr.jtype NE 0 THEN 
                NEXT.
            ELSE IF journaltype NE 0 AND other-dept 
              AND gl-jouhdr.jtype EQ 0 THEN NEXT. 
            ELSE IF journaltype NE 0 AND NOT other-dept 
              AND gl-jouhdr.jtype NE journaltype 
              AND gl-jouhdr.jtype NE journaltype1 THEN NEXT.
            FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
                AND gl-journal.fibukonto GE from-fibu
                AND gl-journal.fibukonto LE to-fibu NO-LOCK 
                BY gl-journal.fibukonto:
                CREATE g-list.
                ASSIGN
                    g-list.grecid = RECID(gl-journal)
                    g-list.fibu   = gl-journal.fibukonto.
            END.
        END.
    END.
END.
/* End of modify */

PROCEDURE create-list: 
DEFINE VARIABLE debit       AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*->>>,>>>,>>>,>>9.99*/
DEFINE VARIABLE credit      AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*->>>,>>>,>>>,>>9.99*/
DEFINE VARIABLE balance     AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INITIAL 0. /*->>>,>>>,>>>,>>9.99*/
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE c           AS CHAR. 
DEFINE VARIABLE bezeich     AS CHAR.
DEFINE VARIABLE refno       AS CHAR.
DEFINE VARIABLE datum       AS DATE. 

DEFINE VARIABLE h-bezeich   AS CHAR.
DEFINE VARIABLE id          AS CHAR FORMAT "x(2)".
DEFINE VARIABLE chgdate     AS DATE.
DEFINE VARIABLE beg-date    AS DATE.
DEFINE VARIABLE beg-day     AS INTEGER.
DEFINE VARIABLE date1       AS DATE.
DEFINE VARIABLE fdate       AS DATE. 
DEFINE VARIABLE tdate       AS DATE. 
DEFINE VARIABLE ddebit      AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE dcredit     AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE dbalance    AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE e-bal       AS DECIMAL INITIAL 0.
DEFINE VARIABLE delta       AS DECIMAL INITIAL 0.

DEFINE VARIABLE prev-mm     AS INTEGER. 
DEFINE VARIABLE prev-yr     AS INTEGER.
DEFINE VARIABLE prev-bal    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE end-bal     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0.
DEFINE VARIABLE blankchar   AS CHAR FORMAT "x(70)" INITIAL "". 
DEFINE VARIABLE acc-bez     AS CHAR FORMAT "x(24)" INITIAL "".

DEFINE VARIABLE t-debit    LIKE debit  INITIAL 0.
DEFINE VARIABLE t-credit   LIKE credit INITIAL 0.
DEFINE VARIABLE tot-debit  LIKE debit  INITIAL 0.
DEFINE VARIABLE tot-credit LIKE credit INITIAL 0.
DEFINE VARIABLE konto      LIKE gl-acct.fibukonto INITIAL "".

DEFINE buffer gl-account FOR gl-acct.
DEFINE buffer gl-jour1   FOR gl-journal.
DEFINE buffer gl-jouh1   FOR gl-jouhdr.

DEFINE VARIABLE curr-recid AS INTEGER NO-UNDO.

  DO i = 1 TO 72: 
    blankchar = blankchar + " ". 
  END. 
 
  ASSIGN
    prev-mm = MONTH(from-date) - 1
    prev-yr = YEAR(from-date)
  .
  IF prev-mm = 0 THEN 
  ASSIGN
    prev-mm = 12
    prev-yr = prev-yr - 1
  .
 
  beg-date = DATE(MONTH(from-date), 1, YEAR(from-date)). 
 
  FOR EACH out-list: 
    DELETE out-list. 
  END. 


  DO: 
     IF sorttype = 2 THEN 
     DO: 
        FOR EACH g-list,
          FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK,
          FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK,
          FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK 
          BY gl-journal.fibukonto BY gl-jouhdr.datum 
          BY gl-jouhdr.refno BY SUBSTR(gl-journal.bemerk,1,24): 
          curr-recid = g-list.grecid.
          DELETE g-list.

       /*
       FOR EACH gl-journal WHERE  gl-journal.fibukonto GE from-fibu 
         AND gl-journal.fibukonto LE to-fibu NO-LOCK,
         FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr 
         AND gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date NO-LOCK, 
         FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK 
         BY gl-journal.fibukonto BY gl-jouhdr.datum 
         BY gl-jouhdr.refno BY SUBSTR(gl-journal.bemerk,1,24): 

         IF journaltype EQ 0 AND excl-other AND gl-jouhdr.jtype NE 0 THEN 
             NEXT.
         ELSE IF journaltype NE 0 AND NOT other-dept 
           AND gl-jouhdr.jtype NE journaltype THEN NEXT.
       */       
         IF gl-journal.chgdate = ? THEN chgdate = ?. 
         ELSE chgdate = gl-journal.chgdate. 

        IF konto = "" THEN
        DO:
            RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                              OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
            CREATE out-list.
            RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
            
            ASSIGN
                out-list.fibukonto  = STRING(c, "x(15)")
                out-list.refno      = STRING(c, "x(15)")
                out-list.bezeich    = STRING(gl-acct.bezeich)
                out-list.bemerk     = STRING(gl-acct.bezeich).
                out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

           ASSIGN
                konto   = gl-acct.fibukonto
                acc-bez = gl-acct.bezeich.
        END.

        IF konto NE gl-acct.fibukonto THEN
        DO:
            IF summ-date THEN
            DO:
                CREATE out-list.
                ASSIGN
                    out-list.s-recid        = /*INTEGER(RECID(gl-journal))*/ curr-recid
                    out-list.fibukonto      = konto
                    out-list.trans-date     = date1
                    out-list.bezeich        = acc-bez
                    out-list.bemerk         = acc-bez
                    out-list.debit          = ddebit
                    out-list.credit         = dcredit
                    out-list.balance        = dbalance
                    out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                    out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                    out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                    .

                IF AVAILABLE gl-journal THEN
                DO:
                   IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                   out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                END.

                IF AVAILABLE gl-acct THEN DO:
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                     
                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).
                END.
                
                ASSIGN
                    ddebit  = 0
                    dcredit = 0
                    date1   = gl-jouhdr.datum.
            END.

            CREATE out-list.
            ASSIGN
                out-list.bezeich        = STRING("T O T A L ") + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                out-list.debit          = t-debit
                out-list.credit         = t-credit
                out-list.balance        = balance
                out-list.debit-str      = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                out-list.credit-str     = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

            CREATE out-list.
            ASSIGN
                balance = 0
                t-debit = 0 
                t-credit = 0.

            RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                              OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).

            CREATE out-list.
            RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
            ASSIGN
                out-list.refno      = STRING(c, "x(15)")
                out-list.fibukonto  = STRING(c, "x(15)")
                out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)")
                out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)")
                acc-bez             = gl-acct.bezeich
                konto               = gl-acct.fibukonto.
                out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
        END.
        
        IF summ-date THEN
        DO:
            IF date1 NE ? AND date1 NE gl-jouhdr.datum THEN
            DO:
                CREATE out-list.
                ASSIGN
                    out-list.fibukonto      = konto
                    out-list.trans-date     = date1
                    out-list.debit          = ddebit
                    out-list.credit         = dcredit
                    out-list.balance        = dbalance
                    out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")      /*->>>,>>>,>>>,>>9.99*/
                    out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                    out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").   /*->>>,>>>,>>>,>>9.99*/

                IF AVAILABLE gl-acct THEN DO:
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                                                                             
                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).
                END.

                ASSIGN
                    ddebit = 0
                    dcredit = 0.
            END.
        END.

        FIND FIRST gl-account WHERE gl-account.fibukonto 
          = gl-journal.fibukonto NO-LOCK NO-ERROR.
        /* 
        IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
            ASSIGN
            balance = balance - gl-journal.debit + gl-journal.credit.
        ELSE 
            ASSIGN
                balance     = balance + gl-journal.debit - gl-journal.credit.
                /*balance = balance + gl-journal.debit - gl-journal.credit. */

                t-debit     = t-debit + gl-journal.debit.
                t-credit    = t-credit + gl-journal.credit.
                tot-debit   = tot-debit + gl-journal.debit.
                tot-credit  = tot-credit + gl-journal.credit. 
        */
        IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
            ASSIGN
            balance = balance - gl-journal.debit + gl-journal.credit.
        ELSE 
            ASSIGN
                balance     = balance + gl-journal.debit - gl-journal.credit.
                
        t-debit     = t-debit + gl-journal.debit.
        t-credit    = t-credit + gl-journal.credit.
        tot-debit   = tot-debit + gl-journal.debit.
        tot-credit  = tot-credit + gl-journal.credit. 

        /*dody start 06/10/16 display 0 for debit
        IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
            DO:
                IF gl-journal.debit NE prev-bal THEN
                DO:
                    balance = balance - gl-journal.debit + gl-journal.credit.
                END.
                ELSE 
                DO:
                    balance = balance - 0 + gl-journal.credit.
                END.
            END.       
            ELSE 
                IF gl-journal.debit NE prev-bal THEN
                DO:
                    balance     = balance    + gl-journal.debit - gl-journal.credit.
                    t-debit     = t-debit    + gl-journal.debit.
                    t-credit    = t-credit   + gl-journal.credit.
                    tot-debit   = tot-debit  + gl-journal.debit.
                    tot-credit  = tot-credit + gl-journal.credit. 
                END.
                ELSE 
                DO:
                    balance     = balance    + 0 - gl-journal.credit.
                    t-debit     = t-debit    + 0.
                    t-credit    = t-credit   + gl-journal.credit.
                    tot-debit   = tot-debit  + 0.
                    tot-credit  = tot-credit + gl-journal.credit. 
                END.
        /*dody end*/*/

        IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
            ASSIGN
               dbalance = dbalance - gl-journal.debit + gl-journal.credit.
        ELSE ASSIGN
           dbalance = dbalance + gl-journal.debit - gl-journal.credit.
        ASSIGN
           ddebit   = ddebit  + gl-journal.debit
           dcredit  = dcredit + gl-journal.credit
           date1    = gl-jouhdr.datum.

        IF NOT summ-date THEN
        DO:
            CREATE out-list.
            ASSIGN
                out-list.s-recid        = /*INTEGER(RECID(gl-journal))*/ curr-recid
                out-list.fibukonto      = gl-journal.fibukonto
                out-list.jnr            = gl-jouhdr.jnr
                out-list.jtype          = gl-jouhdr.jtype
                out-list.trans-date     = gl-jouhdr.datum
                out-list.refno          = gl-jouhdr.refno
                out-list.bezeich        = gl-jouhdr.bezeich
                out-list.debit          = gl-journal.debit
                out-list.credit         = gl-journal.credit
                out-list.refno          = gl-jouhdr.refno
                out-list.uid            = gl-journal.userinit
                out-list.created        = gl-journal.sysdate
                out-list.chgID          = gl-journal.chginit
                out-list.chgDate        = chgdate
                out-list.bemerk         = STRING(get-bemerk(gl-journal.bemerk), "x(100)") /*"x(50)" modified gerald 240220*/
                out-list.balance        = balance
                out-list.debit-str      = STRING(gl-journal.debit, "->,>>>,>>>,>>>,>>9.99") /*dd*/ /*->>>,>>>,>>>,>>9.99*/
                out-list.credit-str     = STRING(gl-journal.credit, "->,>>>,>>>,>>>,>>9.99")       /*->>>,>>>,>>>,>>9.99*/
                out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99").                /*->>>,>>>,>>>,>>9.99*/

            IF AVAILABLE gl-journal THEN
            DO:
               IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
               out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
            END.

            IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                  out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

            IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(100)"). /*"x(50)" modified gerald 240220*/
            ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(100)"). /*"x(50)" modified gerald 240220*/

            /*dody start 06/10/16 display 0 for debit
            IF gl-journal.debit NE prev-bal THEN
            DO:
                out-list.debit-str      = STRING(gl-journal.debit, "->>>,>>>,>>>,>>9.99").
            END.
            ELSE IF gl-journal.debit EQ prev-bal THEN
            DO:
                out-list.debit-str      = "               0.00".                            
            END.
            /*dody end*/*/
        END.
       
         /*IF NOT too-old THEN 
         DO:
             IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                e-bal = e-bal - gl-journal.debit + gl-journal.credit. 
             ELSE e-bal = e-bal + gl-journal.debit - gl-journal.credit. 
         END.
         str = str + STRING(e-bal, "->>>,>>>,>>>,>>9.99").*/
         /*IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
           STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
         ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). */
        END.

        IF summ-date THEN
        DO:
            CREATE out-list.
            ASSIGN
                out-list.s-recid        = /*INTEGER(RECID(gl-journal))*/ curr-recid
                out-list.fibukonto      = konto
                out-list.trans-date     = date1
                out-list.bezeich        = acc-bez
                out-list.bemerk         = acc-bez
                out-list.debit          = ddebit
                out-list.credit         = dcredit
                out-list.balance        = dbalance
                out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

            IF AVAILABLE gl-journal THEN
            DO:
               IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
               out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
            END.

            IF AVAILABLE gl-acct THEN DO:
                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
            END.

            ASSIGN
                ddebit = 0
                dcredit = 0.
        END.
       
        CREATE out-list.
        ASSIGN
            out-list.bezeich        = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
            out-list.debit          = t-debit
            out-list.credit         = t-credit
            out-list.balance        = balance
            out-list.debit-str      = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
            out-list.credit-str     = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
            out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
            out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

        CREATE out-list.
        CREATE out-list.

        ASSIGN
            out-list.bezeich        = "GRAND T O T A L               " 
            out-list.debit          = tot-debit
            out-list.credit         = tot-credit
            out-list.debit-str      = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
            out-list.credit-str     = STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/
     END.

     ELSE IF sorttype = 1 THEN 
     DO: 
       FOR EACH g-list,
         FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK,
         FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK,
         FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto 
           AND gl-acct.main-nr = /*gl-main.nr*/ from-main NO-LOCK 
         BY gl-journal.fibukonto BY gl-jouhdr.datum 
         BY gl-jouhdr.refno BY SUBSTR(gl-journal.bemerk,1,24): 
         curr-recid = g-list.grecid.
         DELETE g-list.
       /*       
       FOR EACH gl-journal WHERE  gl-journal.fibukonto GE from-fibu 
         AND gl-journal.fibukonto LE to-fibu NO-LOCK, 
         FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr 
         AND gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date NO-LOCK, 
         FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto 
           AND gl-acct.main-nr = gl-main.nr NO-LOCK 
         BY gl-journal.fibukonto BY gl-jouhdr.datum 
         BY gl-jouhdr.refno BY SUBSTR(gl-journal.bemerk,1,24): 
 
         IF journaltype EQ 0 AND excl-other AND gl-jouhdr.jtype NE 0 THEN 
             NEXT.
         ELSE IF journaltype NE 0 AND NOT other-dept 
             AND gl-jouhdr.jtype NE journaltype THEN NEXT.
       */
         IF gl-journal.chgdate = ? THEN chgdate = ?. 
         ELSE chgdate = gl-journal.chgdate. 
         IF konto = "" THEN 
         DO:    
           RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
               OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
           CREATE out-list. 
           RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
           ASSIGN
               out-list.fibukonto   = STRING(c, "x(15)") 
               out-list.refno       = STRING(c, "x(15)")
               out-list.bezeich     = STRING(gl-acct.bezeich, "x(40)")
               out-list.bemerk      = STRING(gl-acct.bezeich, "x(40)"). 
               out-list.prev-bal   = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

           ASSIGN
               konto = gl-acct.fibukonto
               acc-bez = gl-acct.bezeich.
         END.
         
         IF konto NE gl-acct.fibukonto THEN
         DO:
             IF summ-date THEN
             DO:
                 CREATE out-list.
                 ASSIGN
                     out-list.s-recid        = /*INTEGER(RECID(gl-journal))*/ curr-recid
                     out-list.fibukonto      = konto
                     out-list.trans-date     = date1
                     out-list.bezeich        = acc-bez
                     out-list.bemerk         = acc-bez
                     out-list.debit          = ddebit
                     out-list.credit         = dcredit
                     out-list.balance        = dbalance
                     out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")      /*->>>,>>>,>>>,>>9.99*/
                     out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                     out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                     .

                 IF AVAILABLE gl-journal THEN
                 DO:
                    IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                    out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                 END.

                 IF AVAILABLE gl-acct THEN DO:
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
                 END.
                 
                 ASSIGN
                     ddebit     = 0
                     dcredit    = 0
                     date1      = gl-jouhdr.datum.
             END.
             
             CREATE out-list.
             ASSIGN
                 out-list.bezeich       = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                 out-list.debit         = t-debit
                 out-list.credit        = t-credit
                 out-list.balance       = balance
                 out-list.debit-str     = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")        /*->>>,>>>,>>>,>>9.99*/
                 out-list.credit-str    = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")       /*->>>,>>>,>>>,>>9.99*/
                 out-list.balance-str   = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")       /*->>>,>>>,>>>,>>9.99*/
                 out-list.prev-bal      = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
             CREATE out-list.
             ASSIGN
                 balance  = 0
                 t-debit  = 0
                 t-credit = 0.

             RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                 OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).

             CREATE out-list.
             RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
             ASSIGN
                 out-list.refno      = STRING(c, "x(15)")
                 out-list.fibukonto  = STRING(c, "x(15)")
                 out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)")
                 out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)")
                 out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

             ASSIGN
                 acc-bez    = gl-acct.bezeich
                 konto      = gl-acct.fibukonto.
         END.
         
         IF summ-date THEN
         DO:
             IF date1 NE ? AND date1 NE gl-jouhdr.datum THEN
             DO:
                 CREATE out-list.
                 ASSIGN
                     out-list.fibukonto     = konto
                     out-list.trans-date    = date1
                     out-list.bezeich       = acc-bez
                     out-list.bemerk        = acc-bez
                     out-list.debit         = ddebit
                     out-list.credit        = dcredit
                     out-list.balance       = dbalance
                     out-list.debit-str     = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                     out-list.credit-str    = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                     out-list.balance-str   = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

                 IF AVAILABLE gl-acct THEN DO:
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
                 END.

                 ASSIGN
                     ddebit = 0
                     dcredit = 0.
             END.
         END.
         
         FIND FIRST gl-account WHERE gl-account.fibukonto 
           = gl-journal.fibukonto NO-LOCK NO-ERROR. 
         IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
            balance = balance - gl-journal.debit + gl-journal.credit.
         ELSE
             balance    = balance + gl-journal.debit - gl-journal.credit.

                 t-debit    = t-debit + gl-journal.debit.
                 t-credit   = t-credit + gl-journal.credit.
                 tot-debit  = tot-debit + gl-journal.debit.
                 tot-credit = tot-credit + gl-journal.credit. 
         
         IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
             ASSIGN
                dbalance = dbalance - gl-journal.debit + gl-journal.credit.
         ELSE ASSIGN
            dbalance = dbalance + gl-journal.debit - gl-journal.credit.
         ASSIGN
            ddebit   = ddebit  + gl-journal.debit
            dcredit  = dcredit + gl-journal.credit
            date1    = gl-jouhdr.datum.

         IF NOT summ-date THEN
         DO:
             CREATE out-list.
             ASSIGN
                 out-list.s-recid       = /*INTEGER(RECID(gl-journal))*/ curr-recid
                 out-list.fibukonto     = gl-journal.fibukonto
                 out-list.jnr           = gl-jouhdr.jnr
                 out-list.jtype         = gl-jouhdr.jtype
                 out-list.trans-date    = gl-jouhdr.datum
                 out-list.refno         = gl-jouhdr.refno
                 out-list.bezeich       = gl-jouhdr.bezeich
                 out-list.debit         = gl-journal.debit
                 out-list.credit        = gl-journal.credit
                 out-list.uid           = gl-journal.userinit
                 out-list.created       = gl-journal.sysdate
                 out-list.chgID         = gl-journal.chginit
                 out-list.chgDate       = chgdate
                 out-list.bemerk        = STRING(get-bemerk(gl-journal.bemerk), "x(100)") /*"x(50)" modified gerald 240220*/
                 out-list.balance       = balance
                 out-list.debit-str     = STRING(gl-journal.debit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                 out-list.credit-str    = STRING(gl-journal.credit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                 out-list.balance-str   = STRING(balance, "->>,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

                 IF AVAILABLE gl-journal THEN
                 DO:
                    IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                    out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                 END.
               
                 IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

                 IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(100)"). /*"x(50)" modified gerald 240220*/
                 ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(100)"). /*"x(50)" modified gerald 240220*/
         END.
        
         /*
         IF NOT too-old THEN 
         DO:
           IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                e-bal = e-bal - gl-journal.debit + gl-journal.credit. 
           ELSE e-bal = e-bal + gl-journal.debit - gl-journal.credit. 
         END.
         STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99").
             
         IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
           STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
         ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). 
         */
       END.

       IF summ-date THEN
       DO:
           CREATE out-list.
           ASSIGN
               out-list.s-recid     = /*INTEGER(RECID(gl-journal))*/ curr-recid
               out-list.fibukonto   = konto
               out-list.trans-date  = date1
               out-list.bezeich     = acc-bez
               out-list.bemerk      = acc-bez
               out-list.debit       = ddebit
               out-list.credit      = dcredit
               out-list.balance     = dbalance
               out-list.debit-str   = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
               out-list.credit-str  = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
               out-list.balance-str = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/

            IF AVAILABLE gl-journal THEN
            DO:
               IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
               out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
            END.

           IF AVAILABLE gl-acct THEN DO:
              IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                          out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
              IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
              ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
           END.

           ASSIGN
               ddebit = 0
               dcredit = 0.
       END.
       
       CREATE out-list.
       ASSIGN
           out-list.bezeich = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
           out-list.debit       = t-debit
           out-list.credit      = t-credit
           out-list.balance     = balance
           out-list.debit-str   = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")      /*->>>,>>>,>>>,>>9.99*/
           out-list.credit-str  = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
           out-list.balance-str = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
           out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
       
       CREATE out-list.
       CREATE out-list.
       ASSIGN
           out-list.bezeich     = "GRAND T O T A L               " 
           out-list.debit       = tot-debit
           out-list.credit      = tot-credit
           out-list.debit-str   = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99")      /*->>>,>>>,>>>,>>9.99*/
           out-list.credit-str  = STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99").    /*->>>,>>>,>>>,>>9.99*/
     END.
     ELSE IF sorttype = 3 THEN 
     DO: 
        FOR EACH g-list,
          FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK,
          FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK,
          FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto 
          AND gl-acct.deptnr = from-dept NO-LOCK 
          BY gl-journal.fibukonto BY gl-jouhdr.datum 
          BY gl-jouhdr.refno BY SUBSTR(gl-journal.bemerk,1,24):
          curr-recid = g-list.grecid.
          DELETE g-list.
       /*
       FOR EACH gl-journal WHERE  gl-journal.fibukonto GE from-fibu 
         AND gl-journal.fibukonto LE to-fibu NO-LOCK, 
         FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr 
         AND gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date NO-LOCK, 
         FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto 
         AND gl-acct.deptnr = from-dept NO-LOCK 
         BY gl-journal.fibukonto BY gl-jouhdr.datum 
         BY gl-jouhdr.refno BY SUBSTR(gl-journal.bemerk,1,24): 
 
         IF excl-other AND gl-jouhdr.jtype NE 0 THEN 
             NEXT.
       */
         IF gl-journal.chgdate = ? THEN chgdate = ?. 
         ELSE chgdate = gl-journal.chgdate. 
         IF konto = "" THEN 
         DO:    
           RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
               OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).
           CREATE out-list. 
           RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
           ASSIGN
               out-list.refno      = STRING(c, "x(15)")
               out-list.fibukonto  = STRING(c, "x(15)") 
               out-list.bezeich    = STRING(gl-acct.bezeich, "x(40)")
               out-list.bemerk     = STRING(gl-acct.bezeich, "x(40)")
               out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

           ASSIGN 
               acc-bez = gl-acct.bezeich
               konto = gl-acct.fibukonto.
         END.
         
         IF konto NE gl-acct.fibukonto THEN
         DO:
             IF summ-date THEN
             DO:
                 CREATE out-list.
                 ASSIGN
                     out-list.s-recid       = /*INTEGER(RECID(gl-journal))*/ curr-recid
                     out-list.fibukonto     = konto
                     out-list.trans-date    = date1
                     out-list.bezeich       = acc-bez
                     out-list.bemerk        = acc-bez
                     out-list.debit         = ddebit
                     out-list.credit        = dcredit
                     out-list.balance       = dbalance
                     out-list.debit-str     = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                     out-list.credit-str    = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                     out-list.balance-str   = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

                 IF AVAILABLE gl-journal THEN
                 DO:
                    IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                    out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
                 END.

                 IF AVAILABLE gl-acct THEN DO:
                     IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                 out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                     IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                     ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
                 END.
                 
                 ASSIGN
                     ddebit = 0
                     dcredit = 0
                     date1 = gl-jouhdr.datum.
             END.
           
             CREATE out-list.
             ASSIGN
                 out-list.bezeich       = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
                 out-list.debit         = t-debit
                 out-list.credit        = t-credit
                 out-list.balance       = balance
                 out-list.debit-str     = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                 out-list.credit-str    = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                 out-list.balance-str   = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")   /*->>>,>>>,>>>,>>9.99*/
                 out-list.prev-bal      = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
             CREATE out-list.
             ASSIGN
                 balance = 0
                 t-debit = 0
                 t-credit = 0.

             RUN calc-prev-bal(gl-acct.fibukonto, prev-mm, prev-yr,
                               OUTPUT prev-bal, OUTPUT balance, OUTPUT dbalance).

             CREATE out-list.
             RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).
             ASSIGN
                 out-list.refno     = STRING(c, "x(15)")
                 out-list.fibukonto = STRING(c, "x(15)")
                 out-list.bezeich   = STRING(gl-acct.bezeich, "x(40)")
                 out-list.bemerk    = STRING(gl-acct.bezeich, "x(40)")
                 out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */

             ASSIGN
                 acc-bez    = gl-acct.bezeich
                 konto      = gl-acct.fibukonto.
         END.
         
         IF summ-date THEN
         DO:
             IF date1 NE ? AND date1 NE gl-jouhdr.datum THEN
             DO:
                 CREATE out-list.
                 ASSIGN
                     out-list.fibukonto     = konto
                     out-list.trans-date    = date1
                     out-list.bezeich       = acc-bez
                     out-list.bemerk        = acc-bez
                     out-list.debit         = ddebit
                     out-list.credit        = dcredit
                     out-list.balance       = dbalance
                     out-list.debit-str     = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99")     /*->>>,>>>,>>>,>>9.99*/
                     out-list.credit-str    = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99")    /*->>>,>>>,>>>,>>9.99*/
                     out-list.balance-str   = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99").  /*->>>,>>>,>>>,>>9.99*/

                 IF AVAILABLE gl-acct THEN DO:
                    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                                out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                    IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                    ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
                 END.   

                 ASSIGN
                     ddebit = 0
                     dcredit = 0.
             END.
         END.
         
         FIND FIRST gl-account WHERE gl-account.fibukonto 
           = gl-journal.fibukonto NO-LOCK NO-ERROR. 
         IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
            balance = balance - gl-journal.debit + gl-journal.credit.
         ELSE
             balance    = balance + gl-journal.debit - gl-journal.credit.

                 t-debit    = t-debit + gl-journal.debit.
                 t-credit   = t-credit + gl-journal.credit.
                 tot-debit  = tot-debit + gl-journal.debit.
                 tot-credit = tot-credit + gl-journal.credit. 

         IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
             ASSIGN
                dbalance = dbalance - gl-journal.debit + gl-journal.credit.
         ELSE ASSIGN
            dbalance = dbalance + gl-journal.debit - gl-journal.credit.
         ASSIGN
            ddebit   = ddebit  + gl-journal.debit
            dcredit  = dcredit + gl-journal.credit
            date1    = gl-jouhdr.datum.

         IF NOT summ-date THEN
         DO:
             CREATE out-list.
             ASSIGN
                 out-list.s-recid       = /*INTEGER(RECID(gl-journal))*/ curr-recid
                 out-list.fibukonto     = gl-journal.fibukonto
                 out-list.jnr           = gl-jouhdr.jnr
                 out-list.jtype         = gl-jouhdr.jtype
                 out-list.trans-date    = gl-jouhdr.datum
                 out-list.refno         = gl-jouhdr.refno
                 out-list.bezeich       = gl-jouhdr.bezeich
                 out-list.debit         = gl-journal.debit
                 out-list.credit        = gl-journal.credit
                 out-list.uid           = gl-journal.userinit
                 out-list.created       = gl-journal.sysdate
                 out-list.chgID         = gl-journal.chginit
                 out-list.chgDate       = chgdate
                 out-list.bemerk        = STRING(get-bemerk(gl-journal.bemerk), "x(100)") /*"x(50)" modified gerald 240220*/
                 out-list.balance       = balance
                 out-list.debit-str     = STRING(gl-journal.debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
                 out-list.credit-str    = STRING(gl-journal.credit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                 out-list.balance-str   = STRING(balance, "->>,>>>,>>>,>>>,>>9.99")          /*->>>,>>>,>>>,>>9.99*/
             .

             IF AVAILABLE gl-journal THEN
             DO:
                IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
                out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
             END.

             IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                        out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").

             IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk, "x(100)"). /*"x(50)" modified gerald 240220*/
             ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2)), "x(100)"). /*"x(50)" modified gerald 240220*/
                 
         END.
         
         /*IF NOT too-old THEN 
         DO:
           IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                e-bal = e-bal - gl-journal.debit + gl-journal.credit. 
           ELSE e-bal = e-bal + gl-journal.debit - gl-journal.credit.
         END.
           
         STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99").
         */
         /*IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
           STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
         ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). */
        END.
        IF summ-date THEN
        DO:
            CREATE out-list.
            ASSIGN
                out-list.s-recid        = /*INTEGER(RECID(gl-journal))*/ curr-recid
                out-list.fibukonto      = konto
                out-list.trans-date     = date1
                out-list.bezeich        = acc-bez
                out-list.bemerk         = acc-bez
                out-list.debit          = ddebit
                out-list.credit         = dcredit
                out-list.balance        = dbalance
                out-list.debit-str      = STRING(ddebit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                out-list.credit-str     = STRING(dcredit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
                out-list.balance-str    = STRING(dbalance, "->>,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/

            IF AVAILABLE gl-journal THEN
            DO:
               IF NUM-ENTRIES(gl-journal.bemerk, CHR(2)) GT 1 THEN                       
               out-list.number1 = ENTRY(2,gl-journal.bemerk,CHR(2)).   
            END.

            IF AVAILABLE gl-acct THEN DO:
                IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
                            out-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
                IF cashflow = YES THEN out-list.bemerk = STRING(out-list.bemerk).
                ELSE out-list.bemerk = STRING(ENTRY(1, out-list.bemerk, CHR(2))).  
            END.

            ASSIGN
                ddebit = 0
                dcredit = 0.
        END.
        
        CREATE out-list.
        ASSIGN
            out-list.bezeich        = "T O T A L  " + STRING(prev-bal, "->>>,>>>,>>>,>>9.99") 
            out-list.debit          = t-debit
            out-list.credit         = t-credit
            out-list.balance        = balance
            out-list.debit-str      = STRING(t-debit, "->,>>>,>>>,>>>,>>9.99")  /*->>>,>>>,>>>,>>9.99*/
            out-list.credit-str     = STRING(t-credit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
            out-list.balance-str    = STRING(balance, "->>,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
            out-list.prev-bal       = STRING(prev-bal, "->>>,>>>,>>>,>>9.99").  /* add by gerald budget awal 080420 */
        CREATE out-list.
        CREATE out-list.
        ASSIGN
            out-list.bezeich        = "GRAND T O T A L               " 
            out-list.debit          = tot-debit
            out-list.credit         = tot-credit
            out-list.debit-str      = STRING(tot-debit, "->,>>>,>>>,>>>,>>9.99") /*->>>,>>>,>>>,>>9.99*/
            out-list.credit-str     = STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /*->>>,>>>,>>>,>>9.99*/
     END.
  END.
END.

PROCEDURE calc-prev-bal:
DEF INPUT  PARAMETER fibu       AS CHAR.
DEF INPUT  PARAMETER prev-mm    AS INTEGER.
DEF INPUT  PARAMETER prev-yr    AS INTEGER.
DEF OUTPUT PARAMETER prev-bal   AS DECIMAL.
DEF OUTPUT PARAMETER balance    AS DECIMAL.
DEF OUTPUT PARAMETER dbalance   AS DECIMAL.

DEF VAR curr-datum              AS DATE      NO-UNDO.
DEF BUFFER gl-account FOR gl-acct.
DEF BUFFER hdrbuff    FOR gl-jouhdr.
DEF BUFFER joubuff    FOR gl-journal.

    prev-bal = 0. 
    FIND FIRST gl-account WHERE gl-account.fibukonto = fibu NO-LOCK NO-ERROR.
    IF prev-yr LT YEAR(close-year) THEN
    DO:
        FIND FIRST gl-accthis WHERE 
          gl-accthis.fibukonto = gl-account.fibukonto AND
          gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
        IF AVAILABLE gl-accthis THEN 
          prev-bal = gl-accthis.actual[prev-mm].
    END.
    ELSE IF prev-yr = YEAR(close-year) THEN 
        prev-bal = gl-account.actual[prev-mm].
    DO:    
        IF (gl-account.acc-type = 3 OR gl-account.acc-type = 4) 
            AND DAY(from-date) GT 1 THEN
        DO curr-datum = DATE(MONTH(from-date), 1, YEAR(from-date)) TO
           DATE(MONTH(from-date), DAY(from-date) - 1, YEAR(from-date)):
            FOR EACH hdrbuff WHERE hdrbuff.datum = curr-datum 
                AND hdrbuff.activeflag LE 1 NO-LOCK:
                FOR EACH joubuff WHERE joubuff.jnr = hdrbuff.jnr
                    AND joubuff.fibukonto = fibu NO-LOCK:
                    ASSIGN prev-bal = prev-bal + joubuff.debit - joubuff.credit.
                END.
            END.
        END.
    END.
      
    IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
    DO:
        prev-bal = - prev-bal.
    END.  
    IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
    ASSIGN
        balance = prev-bal
        dbalance = prev-bal
    .
    ELSE 
    ASSIGN 
        balance = 0
        dbalance = 0
    .
END.


PROCEDURE convert-fibu: 
DEFINE INPUT  PARAMETER konto   AS CHAR. 
DEFINE OUTPUT PARAMETER s       AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 


