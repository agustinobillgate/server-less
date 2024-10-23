DEFINE TEMP-TABLE bk-list LIKE bk-rset
    FIELD rec-id AS INT.

DEF INPUT PARAMETER TABLE FOR bk-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER t-bk-raum-raum AS CHAR.
DEF INPUT PARAMETER t-bk-setup-setup-id AS INT.
DEF OUTPUT PARAMETER recid-rset AS INT.

FIND FIRST bk-list.
IF case-type = 1 THEN RUN fill-bk-rset. 
ELSE RUN update-bk-rset. 

PROCEDURE fill-bk-rset:
  FIND FIRST bk-list.
  CREATE bk-rset.
    bk-rset.raum = t-bk-raum-raum. 
    bk-rset.setup-id = t-bk-setup-setup-id. 
    bk-rset.bezeich = bk-list.bezeich. 
    bk-rset.groesse = bk-list.groesse. 
    bk-rset.nebenstelle = bk-list.nebenstelle. 
    bk-rset.personen = bk-list.personen. 
    bk-rset.preis = bk-list.preis. 
    bk-rset.vorbereit = bk-list.vorbereit. 
    bk-rset.vname = bk-list.vname. 

  FOR EACH bk-rset NO-LOCK BY RECID(bk-rset) DESC:
    recid-rset = RECID(bk-rset).
    LEAVE.
  END.  
END. 

PROCEDURE update-bk-rset: 
  FIND FIRST bk-rset WHERE RECID(bk-rset) = bk-list.rec-id NO-LOCK NO-ERROR.
  IF AVAILABLE bk-rset THEN
  DO:
    FIND CURRENT bk-rset EXCLUSIVE-LOCK.
      bk-rset.raum = t-bk-raum-raum. 
      bk-rset.setup-id = t-bk-setup-setup-id. 
      bk-rset.bezeich = bk-list.bezeich. 
      bk-rset.groesse = bk-list.groesse. 
      bk-rset.nebenstelle = bk-list.nebenstelle. 
      bk-rset.personen = bk-list.personen. 
      bk-rset.preis = bk-list.preis. 
      bk-rset.vorbereit = bk-list.vorbereit. 
      bk-rset.vname = bk-list.vname. 
    FIND CURRENT bk-rset NO-LOCK.
  END.     
END. 
