
DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT PARAMETER bediener-username AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER currdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.

FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
currdate = htparam.fdate. 

RUN new-pr-number.

FIND CURRENT l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).

PROCEDURE new-pr-number: 
DEFINE buffer l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
DEFINE VARIABLE docu-nr AS CHAR. 

    DO TRANSACTION:
        CREATE l-orderhdr. 
        CREATE t-l-orderhdr.
        s = "R" + SUBSTR(STRING(year(currdate)),3,2) + STRING(month(currdate), "99") 
           + STRING(day(currdate), "99"). 
        FOR EACH l-orderhdr1 WHERE l-orderhdr1.bestelldatum = currdate 
          NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
          i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,8,3)). 
          i = i + 1. 
          ASSIGN docu-nr = s + STRING(i, "999") 
                  l-orderhdr.docu-nr        = docu-nr
                  l-orderhdr.besteller      = bediener.username
                  l-orderhdr.bestelldatum   = currdate
                  l-orderhdr.lieferdatum    = currdate + 1 
                      .
          RETURN. 
        END. 
        ASSIGN docu-nr = s + STRING(i, "999") 
                l-orderhdr.docu-nr        = docu-nr
                l-orderhdr.besteller      = bediener-username
                l-orderhdr.bestelldatum   = currdate
                l-orderhdr.lieferdatum    = currdate + 1 
                    .
        
    END.
    /*
    FIND CURRENT l-orderhdr.
    CREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.
    ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
    */
END PROCEDURE. 
