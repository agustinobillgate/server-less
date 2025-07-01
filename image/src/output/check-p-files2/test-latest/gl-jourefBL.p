DEFINE TEMP-TABLE output-list 
    FIELD STR AS CHAR
    FIELD refno AS CHAR. 

DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER from-refno AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR output-list.

RUN create-list.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
    n = INDEX(bemerk, ";&&"). 
    IF n > 0 THEN RETURN SUBSTR(bemerk, 1, n - 1). 
    ELSE RETURN bemerk. 
END. 

PROCEDURE create-list:
DEFINE VARIABLE debit AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE credit AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE balance AS DECIMAL FORMAT "->>>,>>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE refno AS CHAR. 
DEFINE VARIABLE h-bezeich AS CHAR. 
DEFINE VARIABLE id AS CHAR FORMAT "x(2)". 
 
DEFINE VARIABLE t-debit LIKE debit INITIAL 0. 
DEFINE VARIABLE t-credit LIKE credit INITIAL 0. 
DEFINE VARIABLE tot-debit LIKE debit INITIAL 0. 
DEFINE VARIABLE tot-credit LIKE credit INITIAL 0. 
DEFINE VARIABLE chgdate AS CHAR FORMAT "x(8)". 

    FOR EACH output-list: 
        delete output-list. 
    END. 
    DO: 
        IF sorttype = 2 THEN 
        DO:
            FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date 
                NO-LOCK NO-ERROR.
            
            /* Frans: #BAF72A */
            IF NOT AVAILABLE gl-jouhdr THEN DO:
            FOR EACH gl-jhdrhis WHERE gl-jhdrhis.datum GE from-date AND gl-jhdrhis.datum LE to-date 
                    NO-LOCK BY gl-jhdrhis.datum BY gl-jhdrhis.refno: 

                      balance = 0. 
                      t-debit = 0. 
                      t-credit = 0. 
                      create output-list. 
                      output-list.refno = gl-jhdrhis.refno.
                      STR = "        " + STRING(gl-jhdrhis.refno, "x(30)") + STRING(gl-jhdrhis.bezeich, "x(30)").   /*"x(13)", gerald*/ /*william change refno 16 to 30 304D61*/
                          FOR EACH gl-jourhis WHERE  gl-jourhis.jnr = gl-jhdrhis.jnr NO-LOCK, 
                              FIRST gl-acct WHERE gl-acct.fibukonto = gl-jourhis.fibukonto NO-LOCK 
                              BY gl-jourhis.fibukonto: 
                              IF gl-jourhis.chgdate = ? THEN 
                                  chgdate = "". 
                              ELSE 
                                  chgdate = STRING(gl-jourhis.chgdate). 
                              
                              RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                              create output-list. 
                              STR = STRING(gl-jhdrhis.datum) 
                                  + STRING(c, "x(30)") /*"x(13)", gerald*/ /*william change 16 to 30 304D61*/
                                  + STRING(gl-acct.bezeich, "x(30)") 
                                  + STRING(gl-jourhis.debit, "->>>,>>>,>>>,>>>,>>9.99") 
                                  + STRING(gl-jourhis.credit, "->>>,>>>,>>>,>>>,>>9.99") 
                                  + STRING(gl-jourhis.userinit, "x(2)") 
                                  + STRING(gl-jourhis.sysdate) 
                                  + STRING(gl-jourhis.chginit, "x(2)") 
                                  + STRING(chgdate, "x(8)") 
                                  + STRING(get-bemerk(gl-jourhis.bemerk), "x(100)")
                                  + STRING(gl-jourhis.jnr, ">>>,>>>,>>9"). 
                              t-debit = t-debit + gl-jourhis.debit. 
                              t-credit = t-credit + gl-jourhis.credit. 
                              tot-debit = tot-debit + gl-jourhis.debit. 
                              tot-credit = tot-credit + gl-jourhis.credit. 
                          END. 
                      create output-list. 
                      DO i = 1 TO 54: /*william change 40 to 54 304D61*/
                          STR = STR + " ". 
                      END. 
                      STR = STR + "T O T A L     " + STRING(t-debit, "->>>,>>>,>>>,>>>,>>9.99") 
                          + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9.99"). 
                      create output-list.
                    END.
            END.
            ELSE DO:
            FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date 
                NO-LOCK BY gl-jouhdr.datum BY gl-jouhdr.refno:
                IF AVAILABLE gl-jouhdr THEN DO: 
                      balance = 0. 
                      t-debit = 0. 
                      t-credit = 0. 
                      create output-list. 
                      output-list.refno = gl-jouhdr.refno.
                      STR = "        " + STRING(gl-jouhdr.refno, "x(30)") + STRING(gl-jouhdr.bezeich, "x(30)").   /*"x(13)", gerald*/ /*william change refno 16 to 30 304D61*/
                          FOR EACH gl-journal WHERE  gl-journal.jnr = gl-jouhdr.jnr NO-LOCK, 
                              FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK 
                              BY gl-journal.fibukonto: 
                              IF gl-journal.chgdate = ? THEN 
                                  chgdate = "". 
                              ELSE 
                                  chgdate = STRING(gl-journal.chgdate). 
                              
                              RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                              create output-list. 
                              STR = STRING(gl-jouhdr.datum) 
                                  + STRING(c, "x(30)") /*"x(13)", gerald*/ /*william change 16 to 30 304D61*/
                                  + STRING(gl-acct.bezeich, "x(30)") 
                                  + STRING(gl-journal.debit, "->>>,>>>,>>>,>>>,>>9.99") 
                                  + STRING(gl-journal.credit, "->>>,>>>,>>>,>>>,>>9.99") 
                                  + STRING(gl-journal.userinit, "x(2)") 
                                  + STRING(gl-journal.sysdate) 
                                  + STRING(gl-journal.chginit, "x(2)") 
                                  + STRING(chgdate, "x(8)") 
                                  + STRING(get-bemerk(gl-journal.bemerk), "x(100)")
                                  + STRING(gl-journal.jnr, ">>>,>>>,>>9"). 
                              t-debit = t-debit + gl-journal.debit. 
                              t-credit = t-credit + gl-journal.credit. 
                              tot-debit = tot-debit + gl-journal.debit. 
                              tot-credit = tot-credit + gl-journal.credit. 
                          END. 
                      create output-list. 
                      DO i = 1 TO 54: /*william change 40 to 54 304D61*/
                          STR = STR + " ". 
                      END. 
                      STR = STR + "T O T A L     " + STRING(t-debit, "->>>,>>>,>>>,>>>,>>9.99") 
                          + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9.99"). 
                      create output-list. 
                END.
                        
            END.
            END.
            

            create output-list. 
            DO i = 1 TO 48: /*william change 34 to 48 304D61*/
                STR = STR + " ". 
            END. 
            STR = STR + "GRAND T O T A L     " + STRING(tot-debit, "->>>,>>>,>>>,>>>,>>9.99") 
                      + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9.99"). 
        END. 
        ELSE 
        DO: 
            FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date AND gl-jouhdr.datum LE to-date 
                AND gl-jouhdr.refno = from-refno 
                NO-LOCK BY gl-jouhdr.datum BY gl-jouhdr.refno: 
                balance = 0. 
                t-debit = 0. 
                t-credit = 0. 
                create output-list. 
                output-list.refno = gl-jouhdr.refno.
                STR = "        " + STRING(gl-jouhdr.refno, "x(30)") + STRING(gl-jouhdr.bezeich, "x(30)").   /*"x(13)", gerald*/ /*william change refno 16 to 30 304D61*/
                FOR EACH gl-journal WHERE  gl-journal.jnr = gl-jouhdr.jnr NO-LOCK, 
                    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK 
                    BY gl-journal.fibukonto: 
                    IF gl-journal.chgdate = ? THEN 
                        chgdate = "". 
                    ELSE 
                        chgdate = STRING(gl-journal.chgdate). 
                    RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                    create output-list. 
                    STR = STRING(gl-jouhdr.datum) 
                        + STRING(c, "x(30)")    /*"x(13)", gerald*/ /*william change 16 to 30 304D61*/
                        + STRING(gl-acct.bezeich, "x(30)") 
                        + STRING(gl-journal.debit, "->>>,>>>,>>>,>>>,>>9.99") 
                        + STRING(gl-journal.credit, "->>>,>>>,>>>,>>>,>>9.99") 
                        + STRING(gl-journal.userinit, "x(2)") 
                        + STRING(gl-journal.sysdate) 
                        + STRING(gl-journal.chginit, "x(2)") 
                        + STRING(chgdate, "x(8)") 
                        + STRING(get-bemerk(gl-journal.bemerk), "x(100)")
                        + STRING(gl-journal.jnr, ">>>,>>>,>>9"). 
                    t-debit = t-debit + gl-journal.debit. 
                    t-credit = t-credit + gl-journal.credit. 
                    tot-debit = t-debit + gl-journal.debit. 
                    tot-credit = t-credit + gl-journal.credit. 
                END. 
                create output-list. 
                DO i = 1 TO 54: /*william change 40 to 54 304D61*/
                    STR = STR + " ". 
                END. 
                STR = STR + "T O T A L     " + STRING(t-debit, "->>>,>>>,>>>,>>>,>>9.99") 
                          + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9.99"). 
                create output-list. 
            END. 
            create output-list. 
            DO i = 1 TO 54: /*william change 40 to 54 304D61*/
                STR = STR + " ". 
            END. 
            STR = STR + "T O T A L     " + STRING(tot-debit, "->>>,>>>,>>>,>>>,>>9.99") 
                      + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9.99"). 
        END. 
    END. 
END. 

PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
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

