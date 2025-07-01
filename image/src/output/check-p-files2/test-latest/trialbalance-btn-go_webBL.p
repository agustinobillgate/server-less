DEFINE TEMP-TABLE output-list 
  FIELD gop-flag AS LOGICAL INITIAL NO 
  FIELD nr       AS INTEGER 
  FIELD STR      AS CHAR 
  FIELD budget   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"      
  FIELD proz     AS DECIMAL FORMAT "->>>>>" LABEL "(%)"
  FIELD mark     AS LOGICAL INITIAL NO FORMAT "Yes/No"
  FIELD ch       AS CHAR FORMAT "x(2)"  
  INDEX nr_idx nr
 .

DEFINE TEMP-TABLE output-listhis 
  FIELD gop-flag AS LOGICAL INITIAL NO 
  FIELD nr       AS INTEGER 
  FIELD STR      AS CHAR 
  FIELD budget   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"      
  FIELD proz     AS DECIMAL FORMAT "->>>>>" LABEL "(%)"
  FIELD mark     AS LOGICAL INITIAL NO FORMAT "Yes/No"
  FIELD ch       AS CHAR FORMAT "x(2)"  
  INDEX nr_idx nr  
  .

DEFINE TEMP-TABLE result-list 
  FIELD gop-flag AS LOGICAL INITIAL NO 
  FIELD nr       AS INTEGER 
  FIELD STR      AS CHAR 
  FIELD budget   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"      
  FIELD proz     AS DECIMAL FORMAT "->>>>>" LABEL "(%)"
  FIELD mark     AS LOGICAL INITIAL NO FORMAT "Yes/No"
  FIELD ch       AS CHAR FORMAT "x(2)"  
  INDEX nr_idx nr  
  .

DEFINE TEMP-TABLE t-res-list
    FIELD grp-nr AS CHARACTER
    FIELD acc-no AS CHARACTER
    FIELD t-date AS DATE
    FIELD f1     AS CHARACTER
    FIELD f2     AS CHARACTER
    FIELD f3     AS INT64
    FIELD f4     AS INT64
    FIELD f5     AS INT64
    FIELD f6     AS INT64
    FIELD f7     AS INT64
    FIELD f8     AS INT64
    FIELD f9     AS INT64
    FIELD f10    AS INT64
    FIELD note   AS CHARACTER.

DEFINE TEMP-TABLE t-res-listhis 
    FIELD grp-nr AS CHARACTER
    FIELD acc-no AS CHARACTER
    FIELD t-date AS DATE
    FIELD f1     AS CHARACTER
    FIELD f2     AS CHARACTER
    FIELD f3     AS INT64
    FIELD f4     AS INT64
    FIELD f5     AS INT64
    FIELD f6     AS INT64
    FIELD f7     AS INT64
    FIELD f8     AS INT64
    FIELD f9     AS INT64
    FIELD f10    AS INT64
    FIELD note   AS CHARACTER.


DEFINE TEMP-TABLE g-list
    FIELD datum  AS DATE    INITIAL ?
    FIELD grecid AS INTEGER INITIAL 0
    FIELD fibu   AS CHAR
    INDEX fibu_ix fibu.

DEFINE TEMP-TABLE g-listpre 
    FIELD datum  AS DATE    INITIAL ?
    FIELD grecid AS INTEGER INITIAL 0
    FIELD fibu   AS CHAR
    INDEX fibu_ix fibu.

DEFINE TEMP-TABLE g-listhis 
    FIELD datum  AS DATE    INITIAL ?
    FIELD grecid AS INTEGER INITIAL 0
    FIELD fibu   AS CHAR
    INDEX fibu_ix fibu. /*Eko*/

DEF INPUT PARAMETER acct-type    AS INT.
DEF INPUT PARAMETER from-fibu   AS CHAR.
DEF INPUT PARAMETER to-fibu     AS CHAR.
DEF INPUT PARAMETER sorttype    AS INT.
DEF INPUT PARAMETER from-dept   AS INT.
DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER close-month AS INT.
DEF INPUT PARAMETER close-date  AS DATE.
DEF INPUT PARAMETER pnl-acct    AS CHAR.
DEF INPUT PARAMETER close-year  AS DATE.
DEF INPUT PARAMETER prev-month  AS INT.
DEF INPUT PARAMETER show-longbal AS LOGICAL.
DEF INPUT PARAMETER pbal-flag   AS LOGICAL.
DEF INPUT PARAMETER ASremoteFlag AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE num-acctype     AS INTEGER.
DEFINE VARIABLE sales           AS DECIMAL. 
DEFINE VARIABLE cost            AS DECIMAL. 
DEFINE VARIABLE gop-credit      AS DECIMAL. 
DEFINE VARIABLE gop-debit       AS DECIMAL. 
DEFINE VARIABLE tot-diff        AS DECIMAL. 
DEFINE VARIABLE curr-i          AS INT.
DEFINE VARIABLE in-procedure    AS LOGICAL  NO-UNDO.
DEF VARIABLE numSend        AS INTEGER INITIAL 30 NO-UNDO.
/* Begin Eko */
DEFINE VARIABLE last-acct-close-priod AS DATE       NO-UNDO. 
DEFINE VARIABLE t-from-date           AS DATE       NO-UNDO.
DEFINE VARIABLE t-to-date             AS DATE       NO-UNDO.
DEFINE VARIABLE t-strgrp              AS CHARACTER  NO-UNDO.
DEFINE VARIABLE t-str                 AS CHARACTER  NO-UNDO.
DEFINE VARIABLE t-int                 AS INTEGER    NO-UNDO.
DEFINE VARIABLE t-date                AS DATE       NO-UNDO.
DEFINE VARIABLE from-datehis          AS DATE       NO-UNDO.
DEFINE VARIABLE to-datehis            AS DATE       NO-UNDO.
DEFINE VARIABLE readFlag              AS INTEGER    NO-UNDO. /*1 present 2 archive + present 3 archive*/
DEFINE VARIABLE coa-format            AS CHAR       NO-UNDO.
DEFINE VARIABLE counter               AS INTEGER INIT 0.
DEF VAR tt-pbal2 AS DECIMAL.

RUN htpdate.p(795, OUTPUT last-acct-close-priod).
RUN htpchar.p(977, OUTPUT coa-format).
/* End Eko */
DEF VARIABLE hHandle AS HANDLE NO-UNDO.
hHandle = THIS-PROCEDURE.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END.

FUNCTION lastDay RETURNS DATE ( INPUT d AS DATE ):
    RETURN ADD-INTERVAL( DATE( MONTH( d ), 1, YEAR( d )), 1, "month" ) - 1.
END FUNCTION.

num-accType = 0.
FIND FIRST gl-acct WHERE gl-acct.fibukonto GE from-fibu
  AND gl-acct.fibukonto LE to-fibu
  AND (gl-acct.acc-type = 1 OR gl-acct.acc-type = 2 OR gl-acct.acc-type = 5)
  NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN num-accType = 1.
FIND FIRST gl-acct WHERE gl-acct.fibukonto GE from-fibu
  AND gl-acct.fibukonto LE to-fibu
  AND gl-acct.acc-type = 3 NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN num-accType = num-accType + 1.
FIND FIRST gl-acct WHERE gl-acct.fibukonto GE from-fibu
  AND gl-acct.fibukonto LE to-fibu
  AND gl-acct.acc-type = 4 NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN num-accType = num-accType + 1.

ASSIGN
    t-from-date = from-date
    t-to-date = to-date
    from-date = ?
    t-date = ?.    

EMPTY TEMP-TABLE g-list.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE lastDay(t-from-date) NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN DO: /*Data only available on present datastore*/
    ASSIGN
        from-date = t-from-date
        to-date = t-to-date.
    RUN create-glist.
END.
ELSE DO:
    FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE t-to-date NO-LOCK NO-ERROR.
    IF AVAILABLE gl-jouhdr THEN DO: /*Data available in archive and present datastore*/
        DO t-date = t-from-date TO t-to-date:
            FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE t-date NO-LOCK NO-ERROR.
            IF AVAILABLE gl-jouhdr THEN DO:
               ASSIGN
                    from-datehis = t-from-date
                    to-datehis   = t-date - 1.
                RUN create-glisthis.
                ASSIGN
                    from-date = t-date
                    to-date   = t-to-date.
                RUN create-glist.
                LEAVE.
             END.
        END.
    END.
    ELSE DO: /*Data only available on archive datastore*/
        ASSIGN
            from-datehis = t-from-date
            to-datehis = t-to-date.
        RUN create-glisthis.
    END.
END.

IF sorttype = 1 THEN RUN create-list1. 
ELSE 
DO: 
  IF from-dept = 0 THEN RUN create-list2. 
  ELSE RUN create-list2d. 
END. 


PROCEDURE create-glist:
    FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date
        AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
            AND gl-journal.fibukonto GE from-fibu
            AND gl-journal.fibukonto LE to-fibu NO-LOCK 
            BY gl-journal.fibukonto:
            CREATE g-list.
            ASSIGN
                g-list.datum  = gl-jouhdr.datum
                g-list.grecid = RECID(gl-journal)
                g-list.fibu   = gl-journal.fibukonto.
        END.
    END.
END.

PROCEDURE create-glisthis: /*Eko*/
    FOR EACH gl-jhdrhis WHERE gl-jhdrhis.datum GE from-datehis
        AND gl-jhdrhis.datum LE to-datehis NO-LOCK BY gl-jhdrhis.datum:
        FOR EACH gl-jourhis WHERE gl-jourhis.jnr = gl-jhdrhis.jnr
            AND gl-jourhis.fibukonto GE from-fibu
            AND gl-jourhis.fibukonto LE to-fibu NO-LOCK 
            BY gl-jourhis.fibukonto:
            CREATE g-list.
            ASSIGN
                g-list.datum  = gl-jhdrhis.datum
                g-list.grecid = RECID(gl-jourhis)
                g-list.fibu   = gl-jourhis.fibukonto.
        END.
    END.
END PROCEDURE.

PROCEDURE create-list1:
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE curr-month AS INTEGER. 
DEFINE VARIABLE do-it AS LOGICAL. 
 
DEFINE VARIABLE t-debit AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
DEFINE VARIABLE t-credit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE p-bal AS DECIMAL. 
DEFINE VARIABLE t-bal AS DECIMAL. 
DEFINE VARIABLE y-bal AS DECIMAL. 
 
DEFINE VARIABLE tot-debit   LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-credit  LIKE t-credit INITIAL 0. 
DEFINE VARIABLE prev-bal    LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-bal     LIKE t-debit INITIAL 0. 
DEFINE VARIABLE diff        AS DECIMAL. 
DEFINE VARIABLE act-flag    AS INTEGER INITIAL 0. 
DEFINE VARIABLE to-bal      AS DECIMAL.

DEFINE VARIABLE curr-tbal   AS DECIMAL.
DEFINE VARIABLE curr-totbal AS DECIMAL.
DEFINE VARIABLE curr-ttbal AS DECIMAL.

  ASSIGN
    curr-month  = close-month 
    sales       = 0 
    cost        = 0 
    gop-credit  = 0 
    gop-debit   = 0 
    tot-diff    = 0  
    act-flag    = 0
  .
  IF to-date LE DATE(month(close-date), 1, year(close-date)) - 1 THEN 
    act-flag = 1. 
 
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
 
  IF sorttype = 1 THEN 
  DO:
    IF acct-type = 0 THEN DO:
        FOR EACH gl-acct WHERE gl-acct.fibukonto GE from-fibu 
          AND gl-acct.fibukonto LE to-fibu NO-LOCK BY gl-acct.fibukonto: 
          
          ASSIGN
            konto = gl-acct.fibukonto
            do-it = YES
          . 
          IF from-dept GT 0 AND gl-acct.deptnr NE from-dept THEN do-it = NO. 
          IF do-it THEN 
          DO: 
            
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.

            RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
            /*STR = "        " + STRING(c, "x(13)") + SUBSTR(gl-acct.bezeich, 1, 20). */
            STR = "        " + STRING(c, "x(16)") + SUBSTR(gl-acct.bezeich, 1, 20). 
       
            IF LENGTH(gl-acct.bezeich) GT 20 THEN 
              STR = STR + SUBSTR(gl-acct.bezeich, 21, 18). 
            ASSIGN
              t-debit       = 0 
              t-credit      = 0 
              p-bal         = 0 
              t-bal         = 0
              curr-tbal     = 0 
              curr-totbal   = 0 
              curr-ttbal    = 0 
            . 
            IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN 
            DO: 
              RUN calc-prevBalance(konto, OUTPUT p-bal, OUTPUT to-bal).
              ASSIGN
                  prev-bal = prev-bal + p-bal  
                  t-bal    = p-bal    + to-bal
                  /*tot-bal  = tot-bal  + t-bal + to-bal*/
                  tot-bal  = tot-bal  + p-bal + to-bal /*FD*/
              . 
            END. 
            
            FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
                USE-INDEX fibu_ix BY g-list.fibu BY g-list.datum:
                RELEASE gl-journal.
                t-date = g-list.datum.
                IF g-list.grecid NE 0 THEN DO:
                    IF t-date >= from-date AND t-date <= to-date THEN DO:
                        FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
                        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                        DELETE g-list.
                        
                        IF AVAILABLE gl-journal THEN
                        DO:
                            IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                gop-credit = gop-credit + gl-journal.credit. 
                                gop-debit = gop-debit + gl-journal.debit. 
                            END. 
                            
                            IF gl-acct.acc-type = 1 THEN 
                                sales = sales + gl-journal.credit - gl-journal.debit. 
                            ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                cost = cost + gl-journal.debit - gl-journal.credit. 
                            
                            t-debit = t-debit + gl-journal.debit. 
                            t-credit = t-credit + gl-journal.credit. 
                            
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
                            ELSE t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
                            
                            tot-debit = tot-debit + gl-journal.debit. 
                            tot-credit = tot-credit + gl-journal.credit. 
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
                            ELSE 
                                tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
                            
                            CREATE output-list. 
                            ASSIGN counter = counter + 1
                                   output-list.nr = counter.
                            STR = STRING(gl-jouhdr.datum) + STRING(gl-jouhdr.refno, "x(16)"). 
                            DO i = 1 TO 22: 
                                STR = STR + " ". 
                            END. 
                            /* FD Comment
                            STR = STR + STRING(gl-journal.debit, "->>,>>>,>>>,>>9.99") 
                                + STRING(gl-journal.credit, "->>,>>>,>>>,>>9.99").
                            */
                            /*FD July 12, 2021*/
                            IF gl-journal.debit GE 0 THEN
                                STR = STR + STRING(gl-journal.debit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-journal.debit, "->>,>>>,>>>,>>>,>>9.99").
                            IF gl-journal.credit GE 0 THEN
                                STR = STR + STRING(gl-journal.credit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-journal.credit, "->>,>>>,>>>,>>>,>>9.99").
                            STR = STR + STRING("", "x(44) ") 
                                    + STRING(get-bemerk(gl-journal.bemerk), "x(62)"). 
                        END.
                    END. 
                    IF t-date >= from-datehis AND t-date <= to-datehis THEN DO:
                        FIND FIRST gl-jourhis WHERE RECID(gl-jourhis) = g-list.grecid NO-LOCK.
                        FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr NO-LOCK NO-ERROR.
                        DELETE g-list.
                        
                        IF AVAILABLE gl-jourhis THEN
                        DO:
                            IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                gop-credit = gop-credit + gl-jourhis.credit. 
                                gop-debit = gop-debit + gl-jourhis.debit. 
                            END. 
                            
                            IF gl-acct.acc-type = 1 THEN 
                                sales = sales + gl-jourhis.credit - gl-jourhis.debit. 
                            ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                cost = cost + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            t-debit = t-debit + gl-jourhis.debit. 
                            t-credit = t-credit + gl-jourhis.credit. 
                            
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                t-bal = t-bal - gl-jourhis.debit + gl-jourhis.credit. 
                            ELSE t-bal = t-bal + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            tot-debit = tot-debit + gl-jourhis.debit. 
                            tot-credit = tot-credit + gl-jourhis.credit. 
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                tot-bal = tot-bal - gl-jourhis.debit + gl-jourhis.credit. 
                            ELSE 
                                tot-bal = tot-bal + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            CREATE output-list. 
                            ASSIGN counter = counter + 1
                                   output-list.nr = counter.
                            STR = STRING(gl-jhdrhis.datum) + STRING(gl-jhdrhis.refno, "x(13)"). 
                            DO i = 1 TO 22: 
                                STR = STR + " ". 
                            END. 
                            /* FD Comment
                            STR = STR + STRING(gl-journal.debit, "->>,>>>,>>>,>>9.99") 
                                + STRING(gl-journal.credit, "->>,>>>,>>>,>>9.99").
                            */
                            /*FD July 12, 2021*/
                            IF gl-jourhis.debit GE 0 THEN
                                STR = STR + STRING(gl-jourhis.debit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-jourhis.debit, "->>,>>>,>>>,>>>,>>9.99").
                            IF gl-jourhis.credit GE 0 THEN
                                STR = STR + STRING(gl-jourhis.credit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-jourhis.credit, "->>,>>>,>>>,>>>,>>9.99"). 
                            STR = STR + STRING("", "x(44)") 
                                    + STRING(get-bemerk(gl-jourhis.bemerk), "x(62)"). 
                        END.
                    END. 
                END.
            END.
    
            DO:                
              RUN calcRevCost(t-bal, INPUT-OUTPUT p-bal, INPUT-OUTPUT y-bal).
              IF gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 THEN
              DO:
                  prev-bal = prev-bal + p-bal.

                  /* Don't Use
                  /*FD 25 May, 2022 => For discrapancy ending balance to begin balance next month*/
                  curr-tbal = t-bal.                                       
                  t-bal = p-bal + curr-tbal.
                  curr-totbal = tot-bal.
                  tot-bal = p-bal + curr-totbal.       
                  */           
              END.                                 

              IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 THEN 
              DO: 
                CREATE output-list. 
                ASSIGN counter = counter + 1
                       output-list.nr = counter.
                STR = "        " + "T O T A L       " . 
                RUN convert-balance(p-bal, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                 /* FD Comment
                STR = STR + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
                  + STRING(t-credit, "->>,>>>,>>>,>>9.99").
                */ 
                /*FD July 12, 2021*/
                IF t-debit GE 0 THEN
                    STR = STR + STRING(t-debit, ">>>,>>>,>>>,>>>,>>9.99").
                ELSE STR = STR + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99").
                IF t-credit GE 0 THEN
                    STR = STR + STRING(t-credit, ">>>,>>>,>>>,>>>,>>9.99").
                ELSE STR = STR + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                IF acc-type = 1 OR acc-type = 4 THEN 
                DO: 
                  diff = t-credit - t-debit. 
                  tot-diff = tot-diff + t-credit - t-debit. 
                END. 
                ELSE 
                DO: 
                  diff = t-debit - t-credit. 
                  tot-diff = tot-diff - t-credit + t-debit. 
                END. 
                RUN convert-balance(diff, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                RUN convert-balance(t-bal, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                CREATE output-list. 
                ASSIGN counter = counter + 1
                       output-list.nr = counter.
              END. 
              ELSE DELETE output-list. /* have NO journals ==> record DELETEd */ 
            END. 
          END.
        END.
    END.
    ELSE IF acct-type NE 0 THEN DO:
    /*Irfan 22 Desember 2017 add sorting by acct-type*/
        FOR EACH gl-acct WHERE gl-acct.acc-type EQ INT(acct-type)
          AND gl-acct.fibukonto GE from-fibu 
          AND gl-acct.fibukonto LE to-fibu NO-LOCK BY gl-acct.fibukonto: 
          
          ASSIGN
            konto = gl-acct.fibukonto
            do-it = YES
          . 
          IF from-dept GT 0 AND gl-acct.deptnr NE from-dept THEN do-it = NO. 
          IF do-it THEN 
          DO: 
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
            RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
            /*STR = "        " + STRING(c, "x(13)") + SUBSTR(gl-acct.bezeich, 1, 20). */
            STR = "        " + STRING(c, "x(16)") + SUBSTR(gl-acct.bezeich, 1, 20).
            IF LENGTH(gl-acct.bezeich) GT 20 THEN 
              STR = STR + SUBSTR(gl-acct.bezeich, 21, 18). 
            ASSIGN
              t-debit       = 0 
              t-credit      = 0 
              p-bal         = 0 
              t-bal         = 0
              curr-tbal     = 0 
              curr-totbal   = 0 
              curr-ttbal    = 0 
            . 
            IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN 
            DO: 
              RUN calc-prevBalance(konto, OUTPUT p-bal, OUTPUT to-bal).
              ASSIGN
                  prev-bal = prev-bal + p-bal  
                  t-bal    = p-bal    + to-bal
                  tot-bal  = tot-bal  + t-bal + to-bal
              . 
            END. 
            
            FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
                USE-INDEX fibu_ix BY g-list.fibu BY g-list.datum:
                RELEASE gl-journal.
                t-date = g-list.datum.
                IF g-list.grecid NE 0 THEN DO:
                    IF t-date >= from-date AND t-date <= to-date THEN DO:
                        FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
                        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                        DELETE g-list.
                        
                        IF AVAILABLE gl-journal THEN
                        DO:
                            IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                gop-credit = gop-credit + gl-journal.credit. 
                                gop-debit = gop-debit + gl-journal.debit. 
                            END. 
                            
                            IF gl-acct.acc-type = 1 THEN 
                                sales = sales + gl-journal.credit - gl-journal.debit. 
                            ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                cost = cost + gl-journal.debit - gl-journal.credit. 
                            
                            t-debit = t-debit + gl-journal.debit. 
                            t-credit = t-credit + gl-journal.credit. 
                            
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
                            ELSE t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
                            
                            tot-debit = tot-debit + gl-journal.debit. 
                            tot-credit = tot-credit + gl-journal.credit. 
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
                            ELSE 
                                tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
                            
                            CREATE output-list. 
                            ASSIGN counter = counter + 1
                                   output-list.nr = counter.
                            STR = STRING(gl-jouhdr.datum) + STRING(gl-jouhdr.refno, "x(16)"). 
                            DO i = 1 TO 22: 
                                STR = STR + " ". 
                            END. 
                            /* FD Comment
                            STR = STR + STRING(gl-journal.debit, "->>,>>>,>>>,>>9.99") 
                                    + STRING(gl-journal.credit, "->>,>>>,>>>,>>9.99").
                            */
                            /*FD July 12, 2021*/
                            IF gl-journal.debit GE 0 THEN
                                STR = STR + STRING(gl-journal.debit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-journal.debit, "->>,>>>,>>>,>>>,>>9.99").
                            IF gl-journal.credit GE 0 THEN
                                STR = STR + STRING(gl-journal.credit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-journal.credit, "->>,>>>,>>>,>>>,>>9.99"). 
                            STR = STR + STRING("", "x(44) ") 
                                    + STRING(get-bemerk(gl-journal.bemerk), "x(62)"). 
                        END.
                    END. 
                    IF t-date >= from-datehis AND t-date <= to-datehis THEN DO:
                        FIND FIRST gl-jourhis WHERE RECID(gl-jourhis) = g-list.grecid NO-LOCK.
                        FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr NO-LOCK NO-ERROR.
                        DELETE g-list.
                        
                        IF AVAILABLE gl-jourhis THEN
                        DO:
                            IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                gop-credit = gop-credit + gl-jourhis.credit. 
                                gop-debit = gop-debit + gl-jourhis.debit. 
                            END. 
                            
                            IF gl-acct.acc-type = 1 THEN 
                                sales = sales + gl-jourhis.credit - gl-jourhis.debit. 
                            ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                cost = cost + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            t-debit = t-debit + gl-jourhis.debit. 
                            t-credit = t-credit + gl-jourhis.credit. 
                            
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                t-bal = t-bal - gl-jourhis.debit + gl-jourhis.credit. 
                            ELSE t-bal = t-bal + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            tot-debit = tot-debit + gl-jourhis.debit. 
                            tot-credit = tot-credit + gl-jourhis.credit. 
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                                tot-bal = tot-bal - gl-jourhis.debit + gl-jourhis.credit. 
                            ELSE 
                                tot-bal = tot-bal + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            CREATE output-list. 
                            ASSIGN counter = counter + 1
                                   output-list.nr = counter.
                            STR = STRING(gl-jhdrhis.datum) + STRING(gl-jhdrhis.refno, "x(13)"). 
                            DO i = 1 TO 22: 
                                STR = STR + " ". 
                            END. 
                            /* FD Comment
                            STR = STR + STRING(gl-jourhis.debit, "->>,>>>,>>>,>>9.99") 
                                    + STRING(gl-jourhis.credit, "->>,>>>,>>>,>>9.99").
                            */
                            /*FD July 12, 2021*/
                            IF gl-jourhis.debit GE 0 THEN
                                STR = STR + STRING(gl-jourhis.debit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-jourhis.debit, "->>,>>>,>>>,>>>,>>9.99").
                            IF gl-jourhis.credit GE 0 THEN
                                STR = STR + STRING(gl-jourhis.credit, ">>>,>>>,>>>,>>>,>>9.99").
                            ELSE STR = STR + STRING(gl-jourhis.credit, "->>,>>>,>>>,>>>,>>9.99").
                            STR = STR + STRING("", "x(44)") 
                                    + STRING(get-bemerk(gl-jourhis.bemerk), "x(62)"). 
                        END.
                    END. 
                END.
            END.
    
            DO: 
              RUN calcRevCost(t-bal, INPUT-OUTPUT p-bal, INPUT-OUTPUT y-bal).
              IF gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 THEN
              DO:
                  prev-bal = prev-bal + p-bal.

                  /* Don't Use
                  /*FD 25 May, 2022 => For discrapancy ending balance to begin balance next month*/
                  curr-tbal = t-bal.                                       
                  t-bal = p-bal + curr-tbal.
                  curr-totbal = tot-bal.
                  tot-bal = p-bal + curr-totbal.  
                  */                
              END.                  

              IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 THEN 
              DO: 
                CREATE output-list. 
                ASSIGN counter = counter + 1
                       output-list.nr = counter.
                STR = "        " + "T O T A L       " . 
                RUN convert-balance(p-bal, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                /* FD Comment
                STR = STR + STRING(t-debit, "->>,>>>,>>>,>>9.99") 
                  + STRING(t-credit, "->>,>>>,>>>,>>9.99"). 
                */
                /*FD July 12, 2021*/
                IF t-debit GE 0 THEN
                    STR = STR + STRING(t-debit, ">>>,>>>,>>>,>>>,>>9.99").
                ELSE STR = STR + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99").
                IF t-credit GE 0 THEN
                    STR = STR + STRING(t-credit, ">>>,>>>,>>>,>>>,>>9.99").
                ELSE STR = STR + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99").

                IF acc-type = 1 OR acc-type = 4 THEN 
                DO: 
                  diff = t-credit - t-debit. 
                  tot-diff = tot-diff + t-credit - t-debit. 
                END. 
                ELSE 
                DO: 
                  diff = t-debit - t-credit. 
                  tot-diff = tot-diff - t-credit + t-debit. 
                END. 
                RUN convert-balance(diff, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                RUN convert-balance(t-bal, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                CREATE output-list. 
                ASSIGN counter = counter + 1
                       output-list.nr = counter.
              END. 
              ELSE DELETE output-list. /* have NO journals ==> record DELETEd */ 
            END. 
          END. 
        END.
    END.
     
 
    IF prev-bal NE 0 OR tot-debit NE 0 OR tot-credit NE 0 THEN 
    DO: 
/*      CREATE output-list. */ 
        CREATE output-list. 
        ASSIGN counter = counter + 1
               output-list.nr = counter.
        STR = "        " + "Grand TOTAL     ". 
        RUN convert-balance(prev-bal, OUTPUT c). 
        STR = STR + STRING(c, "x(22)"). 
 
        /* FD Comment
        STR = STR + STRING(tot-debit, "->>,>>>,>>>,>>9.99") 
          + STRING(tot-credit, "->>,>>>,>>>,>>9.99"). 
        */
        /*FD July 12, 2021*/
        IF tot-debit GE 0 THEN
            STR = STR + STRING(tot-debit, ">>>,>>>,>>>,>>>,>>9.99").
        ELSE STR = STR + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99").
        IF tot-credit GE 0 THEN
            STR = STR + STRING(tot-credit, ">>>,>>>,>>>,>>>,>>9.99").
        ELSE STR = STR + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
        RUN convert-balance(tot-diff, OUTPUT c). 
        STR = STR + STRING(c, "x(22)"). 
        RUN convert-balance(tot-bal, OUTPUT c). 
        STR = STR + STRING(c, "x(22)"). 
    END. 
    IF to-date EQ close-date THEN RUN prof-loss-acct11. 
  END. 
END PROCEDURE. 

PROCEDURE create-list2:   
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-month AS INTEGER. 
 
DEFINE VARIABLE t-debit AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
DEFINE VARIABLE t-credit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE p-bal AS DECIMAL. 
DEFINE VARIABLE t-bal AS DECIMAL. 
DEFINE VARIABLE y-bal AS DECIMAL. 
 
DEFINE VARIABLE tot-debit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-credit LIKE t-credit INITIAL 0. 
DEFINE VARIABLE t-ybal AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
DEFINE VARIABLE tt-ybal AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
 
DEFINE VARIABLE prev-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-budget AS DECIMAL INITIAL 0. 
DEFINE VARIABLE diff AS DECIMAL. 
 
DEFINE VARIABLE tt-debit    LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-credit   LIKE t-credit INITIAL 0. 
DEFINE VARIABLE tt-pbal     LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-bal      LIKE t-debit INITIAL 0. 

DEFINE VARIABLE tt-diff AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE act-flag    AS INTEGER INITIAL 0. 
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE to-bal      AS DECIMAL.
DEFINE VARIABLE curr-tbal   AS DECIMAL.
DEFINE VARIABLE curr-totbal AS DECIMAL.
DEFINE VARIABLE curr-ttbal AS DECIMAL.

DEFINE BUFFER gl-account FOR gl-acct. 
 
ASSIGN
    in-procedure = YES
    sales         = 0 
    cost          = 0 
    gop-credit    = 0 
    gop-debit     = 0 
    tot-diff      = 0 
    act-flag      = 0
    . 

IF to-date LE DATE(month(close-date), 1, year(close-date)) - 1 THEN 
    act-flag = 1. 

FOR EACH output-list: 
    DELETE output-list. 
END. 

curr-month = close-month. 
IF sorttype = 2 THEN 
DO:
    IF acct-type = 0 THEN
    DO:
        FOR EACH gl-main NO-LOCK, 
            FIRST gl-account WHERE gl-account.main-nr = gl-main.nr 
            AND gl-account.fibukonto GE from-fibu 
            AND gl-account.fibukonto LE to-fibu BY gl-main.code: 
            
            ASSIGN
            prev-bal    = 0 
            tot-debit   = 0 
            tot-credit  = 0 
            t-ybal      = 0 
            tot-bal     = 0 
            tot-budget  = 0 
            diff        = 0 
            tot-diff    = 0
            curr-tbal   = 0
            curr-totbal = 0
            curr-ttbal  = 0
            . 
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
            STR = STRING(STRING(gl-main.code), "x(16)") 
                + SUBSTR(gl-main.bezeich, 1, 38). 
            
            FOR EACH gl-acct WHERE gl-acct.main-nr = gl-main.nr 
                AND gl-acct.fibukonto GE from-fibu AND gl-acct.fibukonto 
                LE to-fibu NO-LOCK BY gl-acct.fibukonto: 
                ASSIGN
                    konto    = gl-acct.fibukonto
                    t-debit  = 0 
                    t-credit = 0 
                    p-bal    = 0 
                    t-bal    = 0 
                    y-bal    = 0
                    . 
                
                IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN DO: 
                    RUN calc-prevBalance(konto, OUTPUT p-bal, OUTPUT to-bal).
                    ASSIGN
                        prev-bal = prev-bal + p-bal  
                        t-bal    = p-bal    + to-bal
                        /*MTtot-bal  = tot-bal  + t-bal + to-bal.*/
                        tot-bal  = tot-bal  + p-bal + to-bal.
                        
                        ASSIGN
                        tt-pbal  = tt-pbal  + p-bal  
                        tt-bal   = tt-bal   + p-bal + to-bal. 
                END. 
                
                FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto USE-INDEX fibu_ix:
                    t-date = g-list.datum.
                    RELEASE gl-journal.
                    IF g-list.grecid NE 0 THEN DO:
                        IF t-date >= from-datehis AND t-date <= to-datehis THEN DO:
                            FIND FIRST gl-jourhis WHERE RECID(gl-jourhis) = g-list.grecid NO-LOCK.
                            FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr NO-LOCK NO-ERROR.
                            DELETE g-list.
                            
                            IF AVAILABLE gl-jourhis THEN DO:
                                IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                    gop-credit = gop-credit + gl-jourhis.credit. 
                                    gop-debit = gop-debit + gl-jourhis.debit. 
                                END. 
                            
                                IF gl-acct.acc-type = 1 THEN 
                                    sales = sales + gl-jourhis.credit - gl-jourhis.debit. 
                                ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                    cost = cost + gl-jourhis.debit - gl-jourhis.credit. 
                                
                                t-debit = t-debit + gl-jourhis.debit. 
                                t-credit = t-credit + gl-jourhis.credit. 
                                
                                tot-debit = tot-debit + gl-jourhis.debit. 
                                tot-credit = tot-credit + gl-jourhis.credit. 
                                
                                tt-debit = tt-debit + gl-jourhis.debit. 
                                tt-credit = tt-credit + gl-jourhis.credit. 
                                
                                IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                                    t-bal = t-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                    tot-bal = tot-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                    tt-bal = tt-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                END. 
                                ELSE DO: 
                                    t-bal = t-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                    tot-bal = tot-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                    tt-bal = tt-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                END. 
                            END.
                        END.
                        ELSE IF t-date >= from-date AND t-date <= to-date THEN DO:
                            FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
                            FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                            DELETE g-list.
                            
                            IF AVAILABLE gl-journal THEN DO:
                                IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                    gop-credit = gop-credit + gl-journal.credit. 
                                    gop-debit = gop-debit + gl-journal.debit. 
                                END. 
                            
                                IF gl-acct.acc-type = 1 THEN 
                                    sales = sales + gl-journal.credit - gl-journal.debit. 
                                ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                    cost = cost + gl-journal.debit - gl-journal.credit. 
                                
                                t-debit = t-debit + gl-journal.debit. 
                                t-credit = t-credit + gl-journal.credit. 
                                
                                tot-debit = tot-debit + gl-journal.debit. 
                                tot-credit = tot-credit + gl-journal.credit. 
                                
                                tt-debit = tt-debit + gl-journal.debit. 
                                tt-credit = tt-credit + gl-journal.credit. 
                                
                                IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                                    t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
                                    tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
                                    tt-bal = tt-bal - gl-journal.debit + gl-journal.credit. 
                                END. 
                                ELSE DO: 
                                    t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
                                    tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
                                    tt-bal = tt-bal + gl-journal.debit - gl-journal.credit. 
                                END. 
                            END.
                        END.
                    END.
                END.               

                RUN calcRevCost(t-bal, INPUT-OUTPUT p-bal, INPUT-OUTPUT y-bal).
                IF gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 THEN
                DO:
                    prev-bal = prev-bal + p-bal.
                    
                    /* Don't Use
                    /*FD 25 May, 2022 => For discrapancy ending balance to begin balance next month*/
                    curr-tbal = t-bal.                                       
                    t-bal = p-bal + curr-tbal.
                    curr-totbal = tot-bal.
                    tot-bal = p-bal + curr-totbal.
                    curr-ttbal = tt-bal.
                    tt-bal = p-bal + curr-ttbal.
                    */
                END.

                IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 
                    OR y-bal NE 0 THEN DO: 
                    CREATE output-list. 
                    ASSIGN counter = counter + 1
                           output-list.nr = counter.
                    RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                    /*STR = STRING(c, "x(13)") + STRING(gl-acct.bezeich, "x(38)"). */
                    STR = STRING(c, "x(16)") + STRING(gl-acct.bezeich, "x(38)").
                    RUN convert-balance(p-bal, OUTPUT c). 
                    IF t-debit GE 0 THEN
                        str = str + STRING(c, "x(22)") 
                            + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99").
                    ELSE str = str + STRING(c, "x(22)") 
                            + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99"). 
                    IF t-credit GE 0 THEN
                        str = str + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                    ELSE str = str + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                    IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                        diff = - t-debit + t-credit. 
                        tot-diff = tot-diff + t-credit - t-debit. 
                        tt-diff = tt-diff + t-credit - t-debit. 
                    END. 
                    ELSE DO: 
                        diff = t-debit - t-credit. 
                        tot-diff = tot-diff - t-credit + t-debit. 
                        tt-diff = tt-diff - t-credit + t-debit. 
                    END. 
                    
                    RUN convert-balance(diff, OUTPUT c). 
                    STR = STR + STRING(c, "x(22)"). 
                    RUN convert-balance(t-bal, OUTPUT c). 
                    STR = STR + STRING(c, "x(22)"). 
                    RUN convert-balance(y-bal, OUTPUT c). 
                    STR = STR + STRING(c, "x(22)"). 

                    t-ybal = t-ybal + y-bal. 
                    tt-ybal = tt-ybal + y-bal. 
                    IF year(close-year) = year(to-date) THEN DO: 
                        IF gl-acct.acc-type = 1 THEN 
                            output-list.budget = - gl-acct.budget[month(to-date)]. 
                        ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                            output-list.budget = gl-acct.budget[month(to-date)]. 
                    END. 
                    ELSE IF year(close-year) = year(to-date) + 1 THEN DO: 
                        IF gl-acct.acc-type = 1 THEN 
                            output-list.budget = - gl-acct.ly-budget[month(to-date)]. 
                        ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                            output-list.budget = gl-acct.ly-budget[month(to-date)]. 
                    END. 
                    tot-budget = tot-budget + output-list.budget. 
                    IF output-list.budget NE 0 THEN 
                        output-list.proz = t-bal / output-list.budget * 100.                     
                END. 
            END. 
            
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
            STR = "                " + STRING("S U B T O T A L", "x(38)"). 
            RUN convert-balance(prev-bal, OUTPUT c). 
            tt-pbal2 = tt-pbal2 + prev-bal. /*debug*/

            IF tot-debit GE 0 THEN
            str = str + STRING(c, "x(22)") 
            + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99").
            ELSE str = str + STRING(c, "x(22)") 
            + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99"). 
            IF tot-credit GE 0 THEN
            str = str + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
            ELSE str = str + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
            
            RUN convert-balance(tot-diff, OUTPUT c). 
            STR = STR + STRING(c, "x(22)"). 
            RUN convert-balance(tot-bal, OUTPUT c). 
            STR = STR + STRING(c, "x(22)"). 
            RUN convert-balance(t-ybal, OUTPUT c). 
            STR = STR + STRING(c, "x(22)"). 
            output-list.budget = tot-budget. 
            IF output-list.budget NE 0 THEN 
            output-list.proz = tot-bal / output-list.budget * 100. 
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
        END.
    END.
    ELSE 
    DO:
        /*IRFAN add sorttype by account type 26/12/17*/
        FOR EACH gl-main NO-LOCK, 
            FIRST gl-account WHERE gl-account.acc-type = acct-type
            AND gl-account.main-nr = gl-main.nr 
            AND gl-account.fibukonto GE from-fibu 
            AND gl-account.fibukonto LE to-fibu BY gl-main.code: 
            
            ASSIGN
            prev-bal    = 0 
            tot-debit   = 0 
            tot-credit  = 0 
            t-ybal      = 0 
            tot-bal     = 0 
            tot-budget  = 0 
            diff        = 0 
            tot-diff    = 0
            curr-tbal   = 0
            curr-totbal = 0
            curr-ttbal  = 0
            . 
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
            STR = STRING(STRING(gl-main.code), "x(16)") + SUBSTR(gl-main.bezeich, 1, 38). 
            
            FOR EACH gl-acct WHERE  gl-acct.acc-type = acct-type 
                AND gl-acct.main-nr = gl-main.nr 
                AND gl-acct.fibukonto GE from-fibu AND gl-acct.fibukonto 
                LE to-fibu NO-LOCK BY gl-acct.fibukonto: 
                ASSIGN
                    konto    = gl-acct.fibukonto
                    t-debit  = 0 
                    t-credit = 0 
                    p-bal    = 0 
                    t-bal    = 0 
                    y-bal    = 0
                    

                    . 
                
                IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN DO: 
                    RUN calc-prevBalance(konto, OUTPUT p-bal, OUTPUT to-bal).
                    ASSIGN
                        prev-bal = prev-bal + p-bal  
                        t-bal    = p-bal    + to-bal
                        /*MTtot-bal  = tot-bal  + t-bal + to-bal.*/
                        tot-bal  = tot-bal  + p-bal + to-bal.
                        
                        ASSIGN
                        tt-pbal  = tt-pbal  + p-bal
                        tt-bal   = tt-bal   + p-bal + to-bal. 
                END. 
                
                FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
                    USE-INDEX fibu_ix:
                    t-date = g-list.datum.
                    RELEASE gl-journal.
                    IF g-list.grecid NE 0 THEN DO:
                        IF t-date >= from-datehis AND t-date <= to-datehis THEN DO:
                            FIND FIRST gl-jourhis WHERE RECID(gl-jourhis) = g-list.grecid NO-LOCK.
                            FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr NO-LOCK NO-ERROR.
                            DELETE g-list.
                            
                            IF AVAILABLE gl-jourhis THEN DO:
                                IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                    gop-credit = gop-credit + gl-jourhis.credit. 
                                    gop-debit = gop-debit + gl-jourhis.debit. 
                                END. 
                            
                                IF gl-acct.acc-type = 1 THEN 
                                    sales = sales + gl-jourhis.credit - gl-jourhis.debit. 
                                ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                    cost = cost + gl-jourhis.debit - gl-jourhis.credit. 
                                
                                t-debit = t-debit + gl-jourhis.debit. 
                                t-credit = t-credit + gl-jourhis.credit. 
                                
                                tot-debit = tot-debit + gl-jourhis.debit. 
                                tot-credit = tot-credit + gl-jourhis.credit. 
                                
                                tt-debit = tt-debit + gl-jourhis.debit. 
                                tt-credit = tt-credit + gl-jourhis.credit. 
                                
                                IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                                    t-bal = t-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                    tot-bal = tot-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                    tt-bal = tt-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                END. 
                                ELSE DO: 
                                    t-bal = t-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                    tot-bal = tot-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                    tt-bal = tt-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                END. 
                            END.
                        END.
                        ELSE IF t-date >= from-date AND t-date <= to-date THEN DO:
                            FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
                            FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                            DELETE g-list.
                            
                            IF AVAILABLE gl-journal THEN DO:
                                IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                    gop-credit = gop-credit + gl-journal.credit. 
                                    gop-debit = gop-debit + gl-journal.debit. 
                                END. 
                            
                                IF gl-acct.acc-type = 1 THEN 
                                    sales = sales + gl-journal.credit - gl-journal.debit. 
                                ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                    cost = cost + gl-journal.debit - gl-journal.credit. 
                                
                                t-debit = t-debit + gl-journal.debit. 
                                t-credit = t-credit + gl-journal.credit. 
                                
                                tot-debit = tot-debit + gl-journal.debit. 
                                tot-credit = tot-credit + gl-journal.credit. 
                                
                                tt-debit = tt-debit + gl-journal.debit. 
                                tt-credit = tt-credit + gl-journal.credit. 
                                
                                IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                                    t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
                                    tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
                                    tt-bal = tt-bal - gl-journal.debit + gl-journal.credit. 
                                END. 
                                ELSE DO: 
                                    t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
                                    tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
                                    tt-bal = tt-bal + gl-journal.debit - gl-journal.credit. 
                                END.                                 
                            END.
                        END.
                    END.
                END. 
                    
                RUN calcRevCost(t-bal, INPUT-OUTPUT p-bal, INPUT-OUTPUT y-bal).
                IF gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 THEN
                DO:
                    prev-bal = prev-bal + p-bal.

                    /* Don't Use
                    /*FD 25 May, 2022 => For discrapancy ending balance to begin balance next month*/
                    curr-tbal = t-bal.                                       
                    t-bal = p-bal + curr-tbal.
                    curr-totbal = tot-bal.
                    tot-bal = p-bal + curr-totbal.
                    curr-ttbal = tt-bal.
                    tt-bal = p-bal + curr-ttbal.    
                    */                
                END.                    
                
                IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 
                    OR y-bal NE 0 THEN DO: 
                    CREATE output-list. 
                    ASSIGN counter = counter + 1
                           output-list.nr = counter.
                    RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                    /*STR = STRING(c, "x(13)") + STRING(gl-acct.bezeich, "x(38)"). */
                    STR = STRING(c, "x(16)") + STRING(gl-acct.bezeich, "x(38)"). 
                    RUN convert-balance(p-bal, OUTPUT c). 
                    IF t-debit GE 0 THEN
                        str = str + STRING(c, "x(22)") 
                            + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99").
                    ELSE str = str + STRING(c, "x(22)") 
                            + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99"). 
                    IF t-credit GE 0 THEN
                        str = str + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                    ELSE str = str + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                    IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                        diff = - t-debit + t-credit. 
                        tot-diff = tot-diff + t-credit - t-debit. 
                        tt-diff = tt-diff + t-credit - t-debit. 
                    END. 
                    ELSE DO: 
                        diff = t-debit - t-credit. 
                        tot-diff = tot-diff - t-credit + t-debit. 
                        tt-diff = tt-diff - t-credit + t-debit. 
                    END. 

                    RUN convert-balance(diff, OUTPUT c). 
                    STR = STR + STRING(c, "x(22)"). 
                    RUN convert-balance(t-bal, OUTPUT c). 
                    STR = STR + STRING(c, "x(22)"). 
                    RUN convert-balance(y-bal, OUTPUT c). 
                    STR = STR + STRING(c, "x(22)"). 
                    t-ybal = t-ybal + y-bal. 
                    tt-ybal = tt-ybal + y-bal. 
                    IF year(close-year) = year(to-date) THEN DO: 
                        IF gl-acct.acc-type = 1 THEN 
                            output-list.budget = - gl-acct.budget[month(to-date)]. 
                        ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                            output-list.budget = gl-acct.budget[month(to-date)]. 
                    END. 
                    ELSE IF year(close-year) = year(to-date) + 1 THEN DO: 
                        IF gl-acct.acc-type = 1 THEN 
                            output-list.budget = - gl-acct.ly-budget[month(to-date)]. 
                        ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                            output-list.budget = gl-acct.ly-budget[month(to-date)]. 
                    END. 
                    tot-budget = tot-budget + output-list.budget. 
                    IF output-list.budget NE 0 THEN 
                        output-list.proz = t-bal / output-list.budget * 100. 
                END. 
            END. 

            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
            STR = "                " + STRING("S U B T O T A L", "x(38)"). 
            RUN convert-balance(prev-bal, OUTPUT c). 
            tt-pbal2 = tt-pbal2 + prev-bal. /*debug*/
            IF tot-debit GE 0 THEN
            str = str + STRING(c, "x(22)") 
            + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99").
            ELSE str = str + STRING(c, "x(22)") 
            + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99"). 
            IF tot-credit GE 0 THEN
            str = str + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
            ELSE str = str + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
            
            RUN convert-balance(tot-diff, OUTPUT c). 
            STR = STR + STRING(c, "x(22)"). 
            RUN convert-balance(tot-bal, OUTPUT c). 
            STR = STR + STRING(c, "x(22)"). 
            RUN convert-balance(t-ybal, OUTPUT c). 
            STR = STR + STRING(c, "x(22)"). 
            output-list.budget = tot-budget. 
            IF output-list.budget NE 0 THEN 
            output-list.proz = tot-bal / output-list.budget * 100. 
            CREATE output-list. 
            ASSIGN counter = counter + 1
                   output-list.nr = counter.
        END.
    END.
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    STR = "                " + STRING("T O T A L", "x(38)"). 
    RUN convert-balance(tt-pbal2, OUTPUT c).

    IF tt-debit GE 0 THEN
    str = str + STRING(c, "x(22)") 
    + STRING(tt-debit, "->>,>>>,>>>,>>>,>>9.99").
    ELSE str = str + STRING(c, "x(22)") 
    + STRING(tt-debit, "->>,>>>,>>>,>>>,>>9.99"). 
    IF tt-credit GE 0 THEN
    str = str + STRING(tt-credit, "->>,>>>,>>>,>>>,>>9.99"). 
    ELSE str = str + STRING(tt-credit, "->>,>>>,>>>,>>>,>>9.99"). 
    
    RUN convert-balance(tt-diff, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    RUN convert-balance(tt-bal, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    /* 
    RUN convert-balance(tt-ybal, OUTPUT c). 
    STR = STR + STRING(c, "x(20)"). 
    */ 
END. 
/* 
IF to-date EQ close-date THEN 
*/ 
IF from-dept = 0 THEN RUN prof-loss-acct21. 
END PROCEDURE.

PROCEDURE create-list2d:   
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-month AS INTEGER. 
 
DEFINE VARIABLE t-debit AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
DEFINE VARIABLE t-credit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE p-bal AS DECIMAL. 
DEFINE VARIABLE t-bal AS DECIMAL. 
DEFINE VARIABLE y-bal AS DECIMAL. 
 
DEFINE VARIABLE tot-debit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-credit LIKE t-credit INITIAL 0. 
DEFINE VARIABLE t-ybal AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
DEFINE VARIABLE tt-ybal AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"  INITIAL 0. 
 
DEFINE VARIABLE prev-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-budget AS DECIMAL INITIAL 0. 
DEFINE VARIABLE diff AS DECIMAL. 
 
DEFINE VARIABLE tt-debit    LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-credit   LIKE t-credit INITIAL 0. 
DEFINE VARIABLE tt-pbal     LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-bal      LIKE t-debit INITIAL 0. 

DEFINE VARIABLE tt-diff AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE act-flag    AS INTEGER INITIAL 0. 
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE to-bal      AS DECIMAL.

DEFINE VARIABLE curr-tbal   AS DECIMAL.
DEFINE VARIABLE curr-totbal AS DECIMAL.
DEFINE VARIABLE curr-ttbal AS DECIMAL.

DEFINE BUFFER gl-account FOR gl-acct. 
 
ASSIGN
    in-procedure = YES
    sales         = 0 
    cost          = 0 
    gop-credit    = 0 
    gop-debit     = 0 
    tot-diff      = 0 
    act-flag      = 0
    . 

IF to-date LE DATE(month(close-date), 1, year(close-date)) - 1 THEN 
    act-flag = 1. 

FOR EACH output-list: 
    DELETE output-list. 
END. 

curr-month = close-month. 
IF sorttype = 2 THEN DO: 
    FOR EACH gl-main NO-LOCK, 
        FIRST gl-account WHERE gl-account.main-nr = gl-main.nr 
        AND gl-account.fibukonto GE from-fibu 
        AND gl-account.fibukonto LE to-fibu 
        AND gl-account.deptnr = from-dept
        BY gl-main.code: 
        
        ASSIGN
        prev-bal    = 0 
        tot-debit   = 0 
        tot-credit  = 0 
        t-ybal      = 0 
        tot-bal     = 0 
        tot-budget  = 0 
        diff        = 0 
        tot-diff    = 0
        curr-tbal   = 0 
        curr-totbal = 0 
        curr-ttbal  = 0 
        . 
        CREATE output-list. 
        ASSIGN counter = counter + 1
               output-list.nr = counter.
        STR = STRING(STRING(gl-main.code), "x(16)") 
            + SUBSTR(gl-main.bezeich, 1, 38). 
        
        FOR EACH gl-acct WHERE gl-acct.main-nr = gl-main.nr 
            AND gl-acct.fibukonto GE from-fibu AND gl-acct.fibukonto 
            LE to-fibu AND gl-acct.deptnr = from-dept NO-LOCK BY gl-acct.fibukonto: 
            ASSIGN
                konto    = gl-acct.fibukonto
                t-debit  = 0 
                t-credit = 0 
                p-bal    = 0 
                t-bal    = 0 
                y-bal    = 0
                . 
            
            IF gl-acct.acc-type = 3 OR gl-acct.acc-type = 4 THEN DO: 
                RUN calc-prevBalance(konto, OUTPUT p-bal, OUTPUT to-bal).
                ASSIGN
                    prev-bal = prev-bal + p-bal  
                    t-bal    = p-bal    + to-bal
                    /*MTtot-bal  = tot-bal  + t-bal + to-bal.*/
                    tot-bal  = tot-bal  + p-bal + to-bal.
                    
                    ASSIGN
                    tt-pbal  = tt-pbal  + p-bal  
                    tt-bal   = tt-bal   + p-bal + to-bal. 
            END. 
            
            FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
                USE-INDEX fibu_ix:
                t-date = g-list.datum.
                RELEASE gl-journal.
                IF g-list.grecid NE 0 THEN DO:
                    IF t-date >= from-datehis AND t-date <= to-datehis THEN DO:
                        FIND FIRST gl-jourhis WHERE RECID(gl-jourhis) = g-list.grecid NO-LOCK.
                        FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.jnr = gl-jourhis.jnr NO-LOCK NO-ERROR.
                        DELETE g-list.
                        
                        IF AVAILABLE gl-jourhis THEN DO:
                            IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                gop-credit = gop-credit + gl-jourhis.credit. 
                                gop-debit = gop-debit + gl-jourhis.debit. 
                            END. 
                        
                            IF gl-acct.acc-type = 1 THEN 
                                sales = sales + gl-jourhis.credit - gl-jourhis.debit. 
                            ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                cost = cost + gl-jourhis.debit - gl-jourhis.credit. 
                            
                            t-debit = t-debit + gl-jourhis.debit. 
                            t-credit = t-credit + gl-jourhis.credit. 
                            
                            tot-debit = tot-debit + gl-jourhis.debit. 
                            tot-credit = tot-credit + gl-jourhis.credit. 
                            
                            tt-debit = tt-debit + gl-jourhis.debit. 
                            tt-credit = tt-credit + gl-jourhis.credit. 
                            
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                                t-bal = t-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                tot-bal = tot-bal - gl-jourhis.debit + gl-jourhis.credit. 
                                tt-bal = tt-bal - gl-jourhis.debit + gl-jourhis.credit. 
                            END. 
                            ELSE DO: 
                                t-bal = t-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                tot-bal = tot-bal + gl-jourhis.debit - gl-jourhis.credit. 
                                tt-bal = tt-bal + gl-jourhis.debit - gl-jourhis.credit. 
                            END. 
                        END.
                    END.
                    ELSE IF t-date >= from-date AND t-date <= to-date THEN DO:
                        FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
                        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
                        DELETE g-list.
                        
                        IF AVAILABLE gl-journal THEN DO:
                            IF gl-acct.fibukonto = pnl-acct THEN DO: 
                                gop-credit = gop-credit + gl-journal.credit. 
                                gop-debit = gop-debit + gl-journal.debit. 
                            END. 
                        
                            IF gl-acct.acc-type = 1 THEN 
                                sales = sales + gl-journal.credit - gl-journal.debit. 
                            ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                                cost = cost + gl-journal.debit - gl-journal.credit. 
                            
                            t-debit = t-debit + gl-journal.debit. 
                            t-credit = t-credit + gl-journal.credit. 
                            
                            tot-debit = tot-debit + gl-journal.debit. 
                            tot-credit = tot-credit + gl-journal.credit. 
                            
                            tt-debit = tt-debit + gl-journal.debit. 
                            tt-credit = tt-credit + gl-journal.credit. 
                            
                            IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                                t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
                                tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
                                tt-bal = tt-bal - gl-journal.debit + gl-journal.credit. 
                            END. 
                            ELSE DO: 
                                t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
                                tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
                                tt-bal = tt-bal + gl-journal.debit - gl-journal.credit. 
                            END. 
                        END.
                    END.
                END.
            END. 
                
            RUN calcRevCost(t-bal, INPUT-OUTPUT p-bal, INPUT-OUTPUT y-bal).
            IF gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 THEN
            DO:
                prev-bal = prev-bal + p-bal.
                
                /* Don't Use
                /*FD 25 May, 2022 => For discrapancy ending balance to begin balance next month*/
                curr-tbal = t-bal.                                       
                t-bal = p-bal + curr-tbal.
                curr-totbal = tot-bal.
                tot-bal = p-bal + curr-totbal.
                curr-ttbal = tt-bal.
                tt-bal = p-bal + curr-ttbal.
                */
            END.                
            
            IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 
                OR y-bal NE 0 THEN DO: 
                CREATE output-list. 
                ASSIGN counter = counter + 1
                       output-list.nr = counter.
                RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                /*STR = STRING(c, "x(13)") + STRING(gl-acct.bezeich, "x(38)"). */
                STR = STRING(c, "x(16)") + STRING(gl-acct.bezeich, "x(38)").
                RUN convert-balance(p-bal, OUTPUT c). 
                IF t-debit GE 0 THEN
                    str = str + STRING(c, "x(22)") 
                        + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99").
                ELSE str = str + STRING(c, "x(22)") 
                        + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99"). 
                IF t-credit GE 0 THEN
                    str = str + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                ELSE str = str + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN DO: 
                    diff = - t-debit + t-credit. 
                    tot-diff = tot-diff + t-credit - t-debit. 
                    tt-diff = tt-diff + t-credit - t-debit. 
                END. 
                ELSE DO: 
                    diff = t-debit - t-credit. 
                    tot-diff = tot-diff - t-credit + t-debit. 
                    tt-diff = tt-diff - t-credit + t-debit. 
                END. 
                
                RUN convert-balance(diff, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                RUN convert-balance(t-bal, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                RUN convert-balance(y-bal, OUTPUT c). 
                STR = STR + STRING(c, "x(22)"). 
                t-ybal = t-ybal + y-bal. 
                tt-ybal = tt-ybal + y-bal. 
                IF year(close-year) = year(to-date) THEN DO: 
                    IF gl-acct.acc-type = 1 THEN 
                        output-list.budget = - gl-acct.budget[month(to-date)]. 
                    ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                        output-list.budget = gl-acct.budget[month(to-date)]. 
                END. 
                ELSE IF year(close-year) = year(to-date) + 1 THEN DO: 
                    IF gl-acct.acc-type = 1 THEN 
                        output-list.budget = - gl-acct.ly-budget[month(to-date)]. 
                    ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
                        output-list.budget = gl-acct.ly-budget[month(to-date)]. 
                END. 
                tot-budget = tot-budget + output-list.budget. 
                IF output-list.budget NE 0 THEN 
                    output-list.proz = t-bal / output-list.budget * 100. 
            END. 
        END. 
        
        CREATE output-list.
        ASSIGN counter = counter + 1
               output-list.nr = counter.
        STR = "                " + STRING("S U B T O T A L", "x(38)"). 
        RUN convert-balance(prev-bal, OUTPUT c). 
        
        IF tot-debit GE 0 THEN
        str = str + STRING(c, "x(22)") 
        + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99").
        ELSE str = str + STRING(c, "x(22)") 
        + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99"). 
        IF tot-credit GE 0 THEN
        str = str + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
        ELSE str = str + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
        
        RUN convert-balance(tot-diff, OUTPUT c). 
        STR = STR + STRING(c, "x(22)"). 
        RUN convert-balance(tot-bal, OUTPUT c). 
        STR = STR + STRING(c, "x(22)"). 
        RUN convert-balance(t-ybal, OUTPUT c). 
        STR = STR + STRING(c, "x(22)"). 
        output-list.budget = tot-budget. 
        IF output-list.budget NE 0 THEN 
        output-list.proz = tot-bal / output-list.budget * 100. 
        CREATE output-list. 
        ASSIGN counter = counter + 1
               output-list.nr = counter.
    END. 
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    STR = "                " + STRING("T O T A L", "x(38)"). 
    RUN convert-balance(tt-pbal, OUTPUT c). 
    
    IF tt-debit GE 0 THEN
    str = str + STRING(c, "x(22)") 
    + STRING(tt-debit, "->>,>>>,>>>,>>>,>>9.99").
    ELSE str = str + STRING(c, "x(22)") 
    + STRING(tt-debit, "->>,>>>,>>>,>>>,>>9.99"). 
    IF tt-credit GE 0 THEN
    str = str + STRING(tt-credit, "->>,>>>,>>>,>>>,>>9.99"). 
    ELSE str = str + STRING(tt-credit, "->>,>>>,>>>,>>>,>>9.99"). 
    
    RUN convert-balance(tt-diff, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    RUN convert-balance(tt-bal, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    /* 
    RUN convert-balance(tt-ybal, OUTPUT c). 
    STR = STR + STRING(c, "x(20)"). 
    */ 
END. 
/* 
IF to-date EQ close-date THEN 
*/ 
/*IF from-dept = 0 THEN RUN prof-loss-acct21. */
END PROCEDURE.

PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO LENGTH(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 

PROCEDURE calc-prevBalance:
DEF INPUT PARAMETER  fibu   AS CHAR              NO-UNDO.
DEF OUTPUT PARAMETER p-bal  AS DECIMAL INITIAL 0 NO-UNDO.
DEF OUTPUT PARAMETER to-bal AS DECIMAL INITIAL 0 NO-UNDO.
DEF BUFFER gbuff FOR gl-acct.
    
    FIND FIRST gbuff WHERE gbuff.fibukonto = fibu NO-LOCK NO-ERROR.

    IF gbuff.acc-type NE 3 AND gbuff.acc-type NE 4 THEN RETURN.

    IF YEAR(close-year) = YEAR(t-from-date) AND MONTH(t-from-date) GE 2 THEN
      ASSIGN p-bal = gbuff.actual[prev-month].
    ELSE 
    DO:
      IF MONTH(t-from-date) GE 2 THEN
      FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
        AND gl-accthis.YEAR = YEAR(t-from-date) NO-LOCK NO-ERROR.
      ELSE FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
        AND gl-accthis.YEAR = YEAR(t-from-date) - 1 NO-LOCK NO-ERROR.
      IF AVAILABLE gl-accthis THEN ASSIGN p-bal = gl-accthis.actual[prev-month].
    END.
    IF gbuff.acc-type = 4 THEN p-bal = -1 * p-bal.
    
    IF p-bal NE 0 THEN RETURN.
    IF DAY(t-to-date + 1) NE 1 THEN RETURN. /* to-date must be end of month */
    FIND FIRST g-list WHERE g-list.fibu = fibu NO-ERROR.
    IF AVAILABLE g-list THEN RETURN.

    IF YEAR(t-to-date) = YEAR(close-date) THEN 
        to-bal = gbuff.actual[MONTH(t-to-date)].
    ELSE
    DO:
      FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
        AND gl-accthis.YEAR = YEAR(t-to-date) NO-LOCK NO-ERROR.
      IF AVAILABLE gl-accthis THEN to-bal = gl-accthis.actual[MONTH(t-to-date)].
    END.
    IF gbuff.acc-type = 4 THEN to-bal = -1 * to-bal.
END.
/*
PROCEDURE calc-prevBalance2:
DEF INPUT PARAMETER  fibu   AS CHAR              NO-UNDO.
DEF OUTPUT PARAMETER p-bal  AS DECIMAL INITIAL 0 NO-UNDO.
DEF OUTPUT PARAMETER to-bal AS DECIMAL INITIAL 0 NO-UNDO.
DEF BUFFER gbuff FOR gl-acct.
    
    FIND FIRST gbuff WHERE gbuff.fibukonto = fibu AND gbuff.acc-type EQ acct-type NO-LOCK NO-ERROR.

    /*IF gbuff.acc-type NE 3 AND gbuff.acc-type NE 4 THEN RETURN.*/

    IF YEAR(close-year) = YEAR(t-from-date) AND MONTH(t-from-date) GE 2 THEN
      ASSIGN p-bal = gbuff.actual[prev-month].
    ELSE 
    DO:
      IF MONTH(t-from-date) GE 2 THEN
      FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
        AND gl-accthis.YEAR = YEAR(t-from-date) NO-LOCK NO-ERROR.
      ELSE FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
        AND gl-accthis.YEAR = YEAR(t-from-date) - 1 NO-LOCK NO-ERROR.
      IF AVAILABLE gl-accthis THEN ASSIGN p-bal = gl-accthis.actual[prev-month].
    END.
    /*IF gbuff.acc-type = 4 THEN*/ p-bal = -1 * p-bal.
    
    IF p-bal NE 0 THEN RETURN.
    IF DAY(t-to-date + 1) NE 1 THEN RETURN. /* to-date must be end of month */
    FIND FIRST g-list WHERE g-list.fibu = fibu NO-ERROR.
    IF AVAILABLE g-list THEN RETURN.

    IF YEAR(t-to-date) = YEAR(close-date) THEN 
        to-bal = gbuff.actual[MONTH(t-to-date)].
    ELSE
    DO:
      FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
        AND gl-accthis.YEAR = YEAR(t-to-date) NO-LOCK NO-ERROR.
      IF AVAILABLE gl-accthis THEN to-bal = gl-accthis.actual[MONTH(t-to-date)].
    END.
    /*IF gbuff.acc-type = 4 THEN*/ to-bal = -1 * to-bal.
END.
*/
PROCEDURE convert-balance: 
DEFINE INPUT PARAMETER balance AS DECIMAL. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  IF balance GE 0 THEN  
  DO:
      IF NOT show-longbal THEN
        S  = STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
      ELSE S  = STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
  END.
  ELSE 
  DO: 
    balance = - balance. 
    IF balance GE 0 THEN
    DO:
      IF NOT show-longbal THEN
        ch = TRIM(STRING(balance, "->>,>>>,>>>,>>>,>>9.99")). 
      ELSE ch = TRIM(STRING(balance, "->>,>>>,>>>,>>>,>>9.99")). 
    END.
    ELSE
    DO:
      IF NOT show-longbal THEN
        ch = TRIM(STRING(balance, "->>,>>>,>>>,>>>,>>9.99")). 
      ELSE ch = TRIM(STRING(balance, "->>,>>>,>>>,>>>,>>9.99")). 
    END.
    s = "(" + ch + ")". 
    DO i = 1 TO 20 - LENGTH(ch): 
     s = " " + s. 
   END. 
  END. 
END. 

PROCEDURE prof-loss-acct11: 
/****** special handling: retained earning Acct-No **/ 
DEFINE VARIABLE m       AS INTEGER. 
DEFINE VARIABLE p-bal   AS DECIMAL. 
DEFINE VARIABLE t-bal   AS DECIMAL. 
DEFINE VARIABLE diff    AS DECIMAL. 
DEFINE VARIABLE c       AS CHAR. 

  FIND FIRST gl-acct WHERE gl-acct.fibukonto = pnl-acct NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN 
  DO: 
/* %%% */ 
    IF year(close-year) = year(t-to-date) THEN 
    DO: 
      m = close-month - 1. 
      IF m GE 1 THEN p-bal = - gl-acct.actual[m]. 
      ELSE p-bal = - gl-acct.last-yr[12]. 
    END. 
    ELSE 
    IF year(close-year) = (year(t-to-date) + 1) THEN 
    DO: 
      m = close-month - 1. 
      IF m GE 1 THEN p-bal = - gl-acct.last-yr[m]. 
    END. 
/* %%% */ 
/* 
    t-bal = - gl-acct.actual[close-month]. 
    IF t-bal = 0 THEN 
*/ 
    t-bal = p-bal + sales - cost + gop-credit - gop-debit. 
    diff = gop-credit + sales - gop-debit - cost. 
 
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    STR = "        " +  "Expected GOP ". 
    RUN convert-balance(p-bal, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    IF (gop-credit + sales) GE 0 THEN 
    STR = STR + STRING((gop-debit + cost), "->>,>>>,>>>,>>>,>>9.99") 
      + STRING((gop-credit + sales), "->>,>>>,>>>,>>>,>>9.99"). 
    ELSE STR = STR + STRING((gop-debit + cost), "->>,>>>,>>>,>>>,>>9.99") 
      + STRING((gop-credit + sales), "->>,>>>,>>>,>>>,>>9.99"). 
    RUN convert-balance(diff, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    RUN convert-balance(t-bal, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
  END. 
END PROCEDURE. 

PROCEDURE calcRevCost:
  DEF INPUT        PARAMETER t-bal AS DECIMAL.
  DEF INPUT-OUTPUT PARAMETER p-bal AS DECIMAL.
  DEF INPUT-OUTPUT PARAMETER y-bal AS DECIMAL.
  DEF VAR p-sign                   AS INTEGER INITIAL 1 NO-UNDO.
  DEF VAR n                        AS INTEGER           NO-UNDO.

  IF gl-acct.acc-typ = 3 OR gl-acct.acc-type = 4 THEN 
  DO: 
      y-bal = t-bal.
      RETURN.
  END.
  IF gl-acct.acc-type = 1 THEN p-sign = -1.
  IF pbal-flag AND MONTH(from-date) GT 1 THEN
  DO:
    IF YEAR(close-year) = YEAR(from-date) THEN
    DO n = 1 TO MONTH(from-date) - 1:
      p-bal = p-bal + p-sign * gl-acct.actual[n]. 
    END.
    ELSE
    DO:
      FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = gl-acct.fibukonto
          AND gl-accthis.YEAR = YEAR(from-date) NO-LOCK NO-ERROR.
      IF AVAILABLE gl-accthis THEN
      DO n = 1 TO MONTH(from-date) - 1:
        p-bal = p-bal + p-sign * gl-accthis.actual[n]. 
      END.
    END.
  END.
  IF YEAR(close-year) = YEAR(from-date) THEN
  DO n = 1 TO MONTH(to-date):
    y-bal = y-bal + p-sign * gl-acct.actual[n]. 
  END.
  ELSE
  DO:
    FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = gl-acct.fibukonto
        AND gl-accthis.YEAR = YEAR(from-date) NO-LOCK NO-ERROR.
    IF AVAILABLE gl-accthis THEN
    DO n = 1 TO MONTH(to-date):
      y-bal = y-bal + p-sign * gl-accthis.actual[n]. 
    END.
  END.
END.

PROCEDURE prof-loss-acct21: 
/****** special handling: retained earning Acct-No **/ 
DEFINE VARIABLE m AS INTEGER. 
DEFINE VARIABLE p-bal AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INIT 0. 
DEFINE VARIABLE t-bal AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99" INIT 0. 
DEFINE VARIABLE diff  AS DECIMAL INIT 0. 
DEFINE VARIABLE c     AS CHAR. 
DEFINE BUFFER hbuff   FOR gl-accthis.


  FIND FIRST gl-acct WHERE gl-acct.fibukonto = pnl-acct NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN 
  DO:
    FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = pnl-acct
      AND gl-accthis.YEAR = (YEAR(t-to-date) - 1) NO-LOCK NO-ERROR.
    IF year(close-year) = year(t-to-date) THEN 
    DO: 
      m = close-month - 1. 
      IF m GE 1 THEN p-bal = - gl-acct.actual[m]. 
      ELSE 
      DO:
        IF AVAILABLE gl-accthis THEN 
          p-bal = - gl-accthis.actual[12].
        ELSE p-bal = - gl-acct.last-yr[12]. 
      END.
    END.
    ELSE
    DO:
      FIND FIRST hbuff WHERE hbuff.fibukonto = pnl-acct
        AND hbuff.YEAR = YEAR(t-to-date) NO-LOCK NO-ERROR.
      IF AVAILABLE hbuff THEN
      DO:
        m = close-month - 1. 
        IF m GE 1 THEN p-bal = - hbuff.actual[m]. 
        ELSE 
        DO:
          IF AVAILABLE gl-accthis THEN 
            p-bal = - gl-accthis.actual[12].
          ELSE p-bal = - hbuff.last-yr[12]. 
        END.
      END.
    END.
/* 
    IF year(close-year) = (year(to-date) + 1) THEN 
    DO: 
      m = close-month - 1. 
      IF m GE 1 THEN p-bal = - gl-acct.last-yr[m]. 
    END. 
    ELSE IF year(close-year) = year(to-date) - 1 THEN 
    p-bal = - gl-acct.last-yr[close-month - 1]. 
*/

    t-bal = p-bal + sales - cost + gop-credit - gop-debit. 
    diff = gop-credit + sales - gop-debit - cost. 
 
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
    STR = "                " + STRING("Balance - " + gl-acct.bezeich, "x(38)"). 
    RUN convert-balance(p-bal, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 

    IF (gop-debit + cost) GE 0 THEN 
    str = str + STRING((gop-debit + cost), "->>,>>>,>>>,>>>,>>9.99"). 
    ELSE
    str = str + STRING((gop-debit + cost), "->>,>>>,>>>,>>>,>>9.99"). 
    
    IF (gop-credit + sales) GE 0 THEN 
    str = str + STRING((gop-credit + sales), "->>,>>>,>>>,>>>,>>9.99"). 
    ELSE  
    str = str + STRING((gop-credit + sales), "->>,>>>,>>>,>>>,>>9.99"). 
    
    RUN convert-balance(diff, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    RUN convert-balance(t-bal, OUTPUT c). 
    STR = STR + STRING(c, "x(22)"). 
    CREATE output-list. 
    ASSIGN counter = counter + 1
           output-list.nr = counter.
  END. 
END. 

PROCEDURE sendNextRecords:
DEF OUTPUT PARAMETER TABLE FOR result-list.
  EMPTY TEMP-TABLE result-list.
  ASSIGN curr-i = 1.
  FIND NEXT output-list NO-ERROR.
  DO WHILE AVAILABLE output-list AND curr-i LE numSend:
    CREATE result-list.
    BUFFER-COPY output-list TO result-list.
    curr-i = curr-i + 1.
    IF curr-i LE numSend THEN
      FIND NEXT output-list NO-ERROR.
  END.
END.

PROCEDURE delete-procedure:
    DELETE PROCEDURE hHandle NO-ERROR.
END.

