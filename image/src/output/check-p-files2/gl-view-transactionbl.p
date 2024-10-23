
DEFINE TEMP-TABLE joulist LIKE vhp.gl-journal
    FIELD selFlag AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE b3-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD debit     LIKE joulist.debit
    FIELD credit    LIKE joulist.credit
    FIELD bemerk    LIKE joulist.bemerk
    FIELD userinit  LIKE joulist.userinit
    FIELD sysdate   LIKE joulist.sysdate
    FIELD chginit   LIKE joulist.chginit
    FIELD chgdate   LIKE joulist.chgdate
    FIELD selFlag   LIKE joulist.selFlag
    FIELD bezeich   LIKE gl-acct.bezeich.

DEFINE INPUT PARAMETER srecid   AS INTEGER.
DEFINE INPUT PARAMETER jnr      AS INTEGER. 
DEFINE INPUT PARAMETER refno    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR b3-list.

DEFINE BUFFER gl-acct1  FOR gl-acct. 

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

/* New Methode for discrepency data years 2015, Verdana Property and Global => fadly 02/07/19 */
FIND FIRST vhp.gl-journal WHERE vhp.gl-journal.jnr = jnr AND INTEGER(RECID(vhp.gl-journal)) = srecid NO-LOCK NO-ERROR.
IF AVAILABLE vhp.gl-journal THEN
DO:        
    FOR EACH vhp.gl-journal WHERE vhp.gl-journal.jnr = jnr NO-LOCK:
      CREATE joulist.
      BUFFER-COPY vhp.gl-journal TO joulist.
      joulist.bemerk = STRING(get-bemerk(joulist.bemerk), "x(50)").  
      IF INTEGER(RECID(vhp.gl-journal)) = srecid THEN
        ASSIGN joulist.selFlag = YES.
    END.
END.
ELSE
DO:
    FOR EACH vhp.gl-jourhis WHERE vhp.gl-jourhis.jnr = jnr NO-LOCK:
      CREATE joulist.
      BUFFER-COPY vhp.gl-jourhis TO joulist.
      joulist.bemerk = STRING(get-bemerk(joulist.bemerk), "x(50)").  
      IF INTEGER(RECID(gl-jourhis)) = srecid THEN
        ASSIGN joulist.selFlag = YES.
    END.
END.
/*END New Method fadly*/
/* Old Method
FOR EACH vhp.gl-journal WHERE vhp.gl-journal.jnr = jnr NO-LOCK:
  CREATE joulist.
  BUFFER-COPY vhp.gl-journal TO joulist.
  joulist.bemerk = STRING(get-bemerk(joulist.bemerk), "x(50)").
  IF INTEGER(RECID(vhp.gl-journal)) = srecid THEN
    ASSIGN joulist.selFlag = YES.
END.
*/
FOR EACH joulist WHERE joulist.jnr = jnr NO-LOCK, 
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = joulist.fibukonto NO-LOCK 
    BY joulist.selFlag DESCENDING BY gl-acct1.fibukonto:
    CREATE b3-list.
    ASSIGN
        b3-list.fibukonto = gl-acct1.fibukonto
        b3-list.debit     = joulist.debit
        b3-list.credit    = joulist.credit
        b3-list.bemerk    = joulist.bemerk
        b3-list.userinit  = joulist.userinit
        b3-list.sysdate   = joulist.sysdate
        b3-list.chginit   = joulist.chginit
        b3-list.chgdate   = joulist.chgdate
        b3-list.selFlag   = joulist.selFlag
        b3-list.bezeich   = gl-acct1.bezeich.
END.
