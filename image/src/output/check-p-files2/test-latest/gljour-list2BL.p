DEF WORKFILE note-list 
  FIELD s-recid AS INTEGER 
  FIELD bemerk AS CHAR. 

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
    FIELD map-acct  AS CHAR.

DEF INPUT  PARAMETER jnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR b2-list.

RUN disp-it2.

FIND FIRST b2-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE b2-list THEN RUN disp-it3.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

PROCEDURE disp-it2:
  FOR EACH note-list: 
    DELETE note-list. 
  END. 
  FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK: 
    CREATE note-list. 
    note-list.s-recid = RECID(gl-journal). 
    note-list.bemerk = get-bemerk(gl-journal.bemerk). 
  END. 
  FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK, 
    FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal)) 
    NO-LOCK BY gl-acct.fibukonto BY gl-journal.sysdate BY gl-journal.zeit:
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
        b2-list.bezeich   = gl-acct.bezeich.
  END.
END.

/* add by bernatd DA71D9*/
PROCEDURE disp-it3:
  FOR EACH note-list: 
      DELETE note-list. 
  END. 
  FOR EACH gl-jourhis WHERE gl-jourhis.jnr = jnr NO-LOCK: 
      CREATE note-list. 
      note-list.s-recid = RECID(gl-jourhis). 
      note-list.bemerk = get-bemerk(gl-jourhis.bemerk). 
  END. 
  FOR EACH gl-jourhis WHERE gl-jourhis.jnr = jnr NO-LOCK, 
      FIRST gl-acct WHERE gl-acct.fibukonto = gl-jourhis.fibukonto NO-LOCK, 
      FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-jourhis)) 
      NO-LOCK BY gl-jourhis.sysdate BY gl-jourhis.zeit:
      CREATE b2-list.
      ASSIGN 
          b2-list.fibukonto = gl-acct.fibukonto
          b2-list.debit     = gl-jourhis.debit
          b2-list.credit    = gl-jourhis.credit
          b2-list.bemerk    = note-list.bemerk
          b2-list.userinit  = gl-jourhis.userinit
          b2-list.sysdate   = gl-jourhis.sysdate
          b2-list.zeit      = gl-jourhis.zeit
          b2-list.chginit   = gl-jourhis.chginit
          b2-list.chgdate   = gl-jourhis.chgdate
          b2-list.jnr       = gl-jourhis.jnr
          b2-list.bezeich   = gl-acct.bezeich.
 
      IF NUM-ENTRIES(gl-acct.userinit, ";") GT 1 THEN
      DO:
          b2-list.map-acct  = ENTRY(2, gl-acct.userinit, ";"). 
      END.
      ELSE
      DO:
          b2-list.map-acct  = " ". 
      END.     
  END.
END.
/* end bernatd DA71D9*/
