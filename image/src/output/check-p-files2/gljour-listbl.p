DEF WORKFILE note-list 
  FIELD s-recid AS INTEGER 
  FIELD bemerk AS CHAR. 

DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr.
    /*FIELD b-recid AS INTEGER.*/

DEFINE TEMP-TABLE b2-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD debit     LIKE gl-journal.debit
    FIELD credit    LIKE gl-journal.credit
    FIELD bemerk    AS CHAR
    FIELD userinit  LIKE gl-journal.userinit
    FIELD sysdate   LIKE gl-journal.sysdate
    FIELD zeit      LIKE gl-journal.zeit
    FIELD chginit   LIKE gl-journal.chginit
    FIELD chgdate   LIKE gl-journal.chgdate
    FIELD jnr       LIKE gl-journal.jnr
    FIELD bezeich   LIKE gl-acct.bezeich
    /*NA 191020 - tambah field untuk mapping acct
    FIELD map-acct  AS CHAR*/.

DEF INPUT  PARAMETER sorttype  AS INT.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-jouhdr.
DEF OUTPUT PARAMETER TABLE FOR b2-list.
/*MTDEF VAR sorttype AS INT INIT 1.
DEF VAR from-date AS DATE INIT 01/01/09.
DEF VAR to-date AS DATE INIT 12/30/09.*/

RUN display-it.
FIND FIRST t-gl-jouhdr NO-ERROR.
IF AVAILABLE t-gl-jouhdr THEN RUN disp-it2.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

PROCEDURE display-it:
    FOR EACH gl-jouhdr
        WHERE gl-jouhdr.activeflag = sorttype
        AND gl-jouhdr.batch = NO
        AND gl-jouhdr.datum GE from-date
        AND gl-jouhdr.datum LE to-date NO-LOCK
        BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
        /*DISP gl-jouhdr.datum.*/
        CREATE t-gl-jouhdr.
        BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
    END.
END.

PROCEDURE disp-it2:
  FOR EACH note-list: 
    DELETE note-list. 
  END. 
  FOR EACH gl-journal WHERE gl-journal.jnr = t-gl-jouhdr.jnr NO-LOCK: 
    CREATE note-list. 
    note-list.s-recid = RECID(gl-journal). 
    note-list.bemerk = get-bemerk(gl-journal.bemerk). 
  END. 
  FOR EACH gl-journal WHERE gl-journal.jnr = t-gl-jouhdr.jnr NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK, 
    FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal)) 
    NO-LOCK BY gl-journal.sysdate BY gl-journal.zeit:
      CREATE b2-list.
      ASSIGN 
          b2-list.fibukonto = gl-acct.fibukonto
          b2-list.debit     = gl-journal.debit
          b2-list.credit    = gl-journal.credit
          b2-list.bemerk    = note-list.bemerk
          b2-list.userinit  = gl-journal.userinit
          b2-list.sysdate   = gl-journal.sysdate
          b2-list.zeit      = gl-journal.zeit
          b2-list.chginit   = gl-journal.chginit
          b2-list.chgdate   = gl-journal.chgdate
          b2-list.jnr       = gl-journal.jnr
          b2-list.bezeich   = gl-acct.bezeich
          /*NA 191020 - tambah field untuk mapping acct
          b2-list.map-acct  = ENTRY(2, gl-acct.userinit, ";")*/.
  END.
END.
