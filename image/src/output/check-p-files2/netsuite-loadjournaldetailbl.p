DEFINE TEMP-TABLE gldetail-list
    FIELD jnr       LIKE gl-jouhdr.jnr
    FIELD datum     LIKE gl-jouhdr.datum
    FIELD refno     LIKE gl-jouhdr.refno
    FIELD bezeich   LIKE gl-jouhdr.bezeich
    FIELD debit     AS DECIMAL FORMAT "->>>>>>>>>>>>>9"
    FIELD credit    AS DECIMAL FORMAT "->>>>>>>>>>>>>9"
    FIELD userinit  LIKE gl-journal.userinit
    FIELD bemerk    AS CHAR FORMAT "x(60)"
    FIELD jtype     LIKE gl-jouhdr.jtype
    FIELD fibukonto LIKE gl-journal.fibukonto
    FIELD mappingcoa AS CHAR
    FIELD coadept    AS INT
    FIELD dept-id    AS INT
    FIELD class-id   AS INT
    FIELD entity-id  AS INT
    .

/**/
DEF INPUT  PARAMETER from-date AS DATE. 
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR gldetail-list.
/**/
/*
DEFINE VARIABLE from-date AS DATE INIT 05/19/23. 
DEFINE VARIABLE to-date   AS DATE INIT 05/25/23.
*/

DEFINE VARIABLE t-from-date     AS DATE NO-UNDO.
DEFINE VARIABLE t-to-date       AS DATE NO-UNDO.
DEFINE VARIABLE from-datehis    AS DATE NO-UNDO.
DEFINE VARIABLE to-datehis      AS DATE NO-UNDO.
DEFINE VARIABLE t-date          AS DATE NO-UNDO.

DEFINE VARIABLE bemerkgl AS CHAR.

FUNCTION lastDay RETURNS DATE ( INPUT d AS DATE ):
    RETURN ADD-INTERVAL( DATE( MONTH( d ), 1, YEAR( d )), 1, "month" ) - 1.
END FUNCTION.

ASSIGN
    t-from-date = from-date
    t-to-date = to-date
    from-date = ?
    t-date = ?. 

FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum LE lastDay(t-from-date) NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN DO: /*Data only available on present datastore*/
    ASSIGN
        from-date = t-from-date
        to-date = t-to-date.
    RUN disp-it.
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
                RUN disp-it-his.
                ASSIGN
                    from-date = t-date
                    to-date   = t-to-date.
                    RUN disp-it.
                LEAVE.
             END.
        END.
    END.
    ELSE DO: /*Data only available on archive datastore*/
        ASSIGN
            from-datehis = t-from-date
            to-datehis = t-to-date.
        RUN disp-it-his.
    END.
END.

/*CURRENT-WINDOW:WIDTH = 250.*/
FOR EACH gldetail-list.
    gldetail-list.bemerk = REPLACE(gldetail-list.bemerk, "&","").
    gldetail-list.bemerk = REPLACE(gldetail-list.bemerk, "/","-").
    /*DISP gldetail-list EXCEPT bezeich bemerk refno WITH WIDTH 210.*/ 
END.

PROCEDURE disp-it: 
  FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date 
      AND gl-jouhdr.datum LE to-date NO-LOCK, 
      EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr 
      AND gl-journal.fibukonto = fibu NO-LOCK 
      BY gl-jouhdr.datum:
      
      IF NUM-ENTRIES(gl-journal.bemerk,";") GE 2 THEN bemerkgl = ENTRY(1, gl-journal.bemerk,";").
      ELSE bemerkgl = gl-journal.bemerk.

      CREATE gldetail-list.
      ASSIGN
        gldetail-list.jnr       = gl-jouhdr.jnr
        gldetail-list.datum     = gl-jouhdr.datum
        gldetail-list.refno     = gl-jouhdr.refno
        gldetail-list.bezeich   = gl-jouhdr.bezeich
        gldetail-list.debit     = gl-journal.debit
        gldetail-list.credit    = gl-journal.credit
        gldetail-list.userinit  = gl-journal.userinit
        gldetail-list.bemerk    = gl-jouhdr.refno + "|" + bemerkgl
        gldetail-list.jtype     = gl-jouhdr.jtype
        gldetail-list.fibukonto = gl-journal.fibukonto.

        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ gl-journal.fibukonto NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            gldetail-list.coadept = gl-acct.deptnr.
            IF NUM-ENTRIES(gl-acct.userinit,";") GE 2 THEN gldetail-list.mappingcoa = ENTRY(2,gl-acct.userinit,";").
            ELSE gldetail-list.mappingcoa = "".

            IF NUM-ENTRIES(gl-acct.bemerk,"|") GE 2 THEN
            DO:
                gldetail-list.dept-id   = INT(ENTRY(1,gl-acct.bemerk,"|")). 
                gldetail-list.class-id  = INT(ENTRY(2,gl-acct.bemerk,"|")).  
                gldetail-list.entity-id = INT(REPLACE(ENTRY(3,gl-acct.bemerk,"|"),";","")).  
            END.
        END. 
  END.
END. 

PROCEDURE disp-it-his: 
  FOR EACH gl-jhdrhis WHERE gl-jhdrhis.datum GE from-datehis 
      AND gl-jhdrhis.datum LE to-datehis NO-LOCK, 
      EACH gl-jourhis WHERE gl-jourhis.jnr = gl-jhdrhis.jnr 
      AND gl-jourhis.fibukonto = fibu NO-LOCK 
      BY gl-jhdrhis.datum:

      IF NUM-ENTRIES(gl-journal.bemerk,";") GE 2 THEN bemerkgl = ENTRY(1, gl-journal.bemerk,";").
      ELSE bemerkgl = gl-journal.bemerk.

      CREATE gldetail-list.
      ASSIGN
        gldetail-list.jnr       = gl-jhdrhis.jnr
        gldetail-list.datum     = gl-jhdrhis.datum
        gldetail-list.refno     = gl-jhdrhis.refno
        gldetail-list.bezeich   = gl-jhdrhis.bezeich
        gldetail-list.debit     = gl-jourhis.debit
        gldetail-list.credit    = gl-jourhis.credit
        gldetail-list.userinit  = gl-jourhis.userinit
        gldetail-list.bemerk    = gl-jhdrhis.bezeich + "|" + bemerkgl
        gldetail-list.jtype     = gl-jhdrhis.jtype
        gldetail-list.fibukonto = gl-jourhis.fibukonto.

        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ gl-jourhis.fibukonto NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            gldetail-list.coadept = gl-acct.deptnr.
            IF NUM-ENTRIES(gl-acct.userinit,";") GE 2 THEN gldetail-list.mappingcoa = ENTRY(2,gl-acct.userinit,";").
            ELSE gldetail-list.mappingcoa = "".

            IF NUM-ENTRIES(gl-acct.bemerk,"|") GE 2 THEN
            DO:
                gldetail-list.dept-id   = INT(ENTRY(1,gl-acct.bemerk,"|")). 
                gldetail-list.class-id  = INT(ENTRY(2,gl-acct.bemerk,"|")).  
                gldetail-list.entity-id = INT(REPLACE(ENTRY(3,gl-acct.bemerk,"|"),";","")).  
            END.
        END. 
  END.
END. 

