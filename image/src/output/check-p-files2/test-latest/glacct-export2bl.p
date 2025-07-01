

DEF WORKFILE note-list 
  FIELD s-recid AS INTEGER 
  FIELD bemerk AS CHAR. 

DEFINE TEMP-TABLE g-list
    FIELD fibukonto         LIKE gl-acct.fibukonto
    FIELD debit             LIKE gl-journal.debit
    FIELD credit            LIKE gl-journal.credit
    FIELD bemerk            AS CHAR
    FIELD userinit          LIKE gl-journal.userinit
    FIELD sysdate           LIKE gl-journal.sysdate
    FIELD zeit              LIKE gl-journal.zeit
    FIELD chginit           LIKE gl-journal.chginit
    FIELD chgdate           LIKE gl-journal.chgdate
    FIELD jnr               LIKE gl-journal.jnr
    FIELD bezeich           LIKE gl-acct.bezeich
    FIELD doc-date          AS DATE
    FIELD curr              AS CHARACTER FORMAT "x(4)"
    FIELD post-date         AS DATE
    FIELD ref               AS CHARACTER
    FIELD doc-header        AS CHARACTER
    FIELD comp              AS CHARACTER
    FIELD code1             AS CHARACTER FORMAT "x(1)" 
    FIELD amount            AS DECIMAL   FORMAT ">,>>>,>>>,>>9.99"
    FIELD costc             AS CHARACTER FORMAT "x(5)"
    FIELD profc             AS CHARACTER FORMAT "x(5)"
    FIELD acc-type          AS CHARACTER
    FIELD deptnr            AS INTEGER   FORMAT ">>9"
    FIELD revtype           AS CHARACTER FORMAT "x(8)"
    FIELD datum             LIKE gl-jouhdr.datum
    FIELD refno             LIKE gl-jouhdr.refno.

DEFINE TEMP-TABLE t-gl-journal  LIKE gl-journal.
DEFINE TEMP-TABLE t-gl-jouhdr   LIKE gl-jouhdr
        FIELD b-recid           AS INTEGER
        FIELD code1             AS CHARACTER FORMAT "x(1)".

DEFINE VARIABLE fromdate            AS DATE .
DEFINE VARIABLE todate              AS DATE .
DEFINE VARIABLE mm                  AS INTEGER.


DEFINE INPUT PARAMETER fdate       AS DATE                NO-UNDO.
DEFINE INPUT PARAMETER tdate       AS DATE                NO-UNDO.
DEFINE OUTPUT PARAMETER loc-curr    AS CHAR               NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR  t-gl-jouhdr.
DEFINE OUTPUT PARAMETER TABLE FOR g-list.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

RUN htpchar.p(152, OUTPUT loc-curr).
ASSIGN 
    fromdate = fdate
    todate   = tdate.

                      
RUN display-it.
FIND FIRST t-gl-jouhdr NO-ERROR.
IF AVAILABLE t-gl-jouhdr THEN RUN disp-it2.

PROCEDURE display-it:
    FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE fromdate
        AND gl-jouhdr.datum LE todate NO-LOCK
        BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
        CREATE t-gl-jouhdr.
        BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
    END.
END.

PROCEDURE disp-it2:
    FOR EACH note-list: 
    DELETE note-list. 
    END.
    FOR EACH g-list:
      DELETE g-list.
    END.
    
    FOR EACH t-gl-jouhdr NO-LOCK:        
        FOR EACH gl-journal WHERE gl-journal.jnr = t-gl-jouhdr.jnr NO-LOCK BY gl-journal.sysdate BY gl-journal.zeit:

            FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK NO-ERROR. 
            /*FIND FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal)) NO-LOCK NO-ERROR.*/
            FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
            FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK NO-ERROR.

                CREATE g-list.
                ASSIGN 
                g-list.fibukonto = gl-acct.fibukonto
                g-list.bemerk    = get-bemerk(gl-journal.bemerk)
                g-list.userinit  = gl-journal.userinit
                g-list.sysdate   = gl-journal.sysdate
                g-list.zeit      = gl-journal.zeit
                g-list.chginit   = gl-journal.chginit
                g-list.chgdate   = gl-journal.chgdate
                g-list.jnr       = gl-journal.jnr
                g-list.bezeich   = gl-acct.bemerk
                g-list.post-date = t-gl-jouhdr.datum
                g-list.acc-type  = STRING(gl-acct.acc-type)
                g-list.deptnr    = gl-acct.deptnr.
                
                IF AVAILABLE gl-jouhdr THEN
                    ASSIGN
                    g-list.datum     = gl-jouhdr.datum.
                    g-list.refno     = gl-jouhdr.refno.

                IF gl-journal.debit NE 0 AND gl-journal.credit NE 0 THEN DO:
                    ASSIGN g-list.debit     = gl-journal.debit.
                    
                    CREATE g-list.
                    ASSIGN 
                        g-list.fibukonto = gl-acct.fibukonto
                        g-list.bemerk    = get-bemerk(gl-journal.bemerk)
                        g-list.userinit  = gl-journal.userinit
                        g-list.sysdate   = gl-journal.sysdate
                        g-list.zeit      = gl-journal.zeit
                        g-list.chginit   = gl-journal.chginit
                        g-list.chgdate   = gl-journal.chgdate
                        g-list.jnr       = gl-journal.jnr
                        g-list.bezeich   = gl-acct.bemerk
                        g-list.post-date = t-gl-jouhdr.datum
                        g-list.acc-type  = STRING(gl-acct.acc-type)
                        g-list.deptnr    = gl-acct.deptnr
                        g-list.credit    = gl-journal.credit
                    .
                    
                    IF AVAILABLE gl-jouhdr THEN
                        ASSIGN
                        g-list.datum     = gl-jouhdr.datum.
                        g-list.refno     = gl-jouhdr.refno.   
                END.
                ELSE 
                    ASSIGN
                        g-list.debit     = gl-journal.debit
                        g-list.credit    = gl-journal.credit
                     .
        END.
    END.
END.



