
DEFINE TEMP-TABLE bk-list LIKE bk-rset
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE t-bk-raum LIKE bk-raum.
DEFINE TEMP-TABLE t-bk-setup LIKE bk-setup.

DEF INPUT PARAMETER raum AS CHAR. 
DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER setup-id AS INT.
DEF INPUT PARAMETER record-id AS INT.
DEF OUTPUT PARAMETER raum-bez AS CHAR.
DEF OUTPUT PARAMETER setup-bez AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR bk-list.
DEF OUTPUT PARAMETER TABLE FOR t-bk-raum.
DEF OUTPUT PARAMETER TABLE FOR t-bk-setup.

CREATE bk-list.
IF curr-select = "chg" THEN RUN fill-bk-list.

FOR EACH bk-raum NO-LOCK:
    CREATE t-bk-raum.
    BUFFER-COPY bk-raum TO t-bk-raum.
END.
FOR EACH bk-setup NO-LOCK:
    CREATE t-bk-setup.
    BUFFER-COPY bk-setup TO t-bk-setup.
END.

PROCEDURE fill-bk-list: 
  /* FD Comment
  FIND FIRST bk-rset WHERE bk-rset.raum = raum 
    AND bk-rset.setup-id = setup-id NO-LOCK.
  */
  FIND FIRST bk-rset WHERE RECID(bk-rset) EQ record-id NO-LOCK. /*FD Nov 4, 2022 => For Web*/

  FIND FIRST bk-raum WHERE bk-raum.raum = raum NO-LOCK NO-ERROR. /* Malik Serverless 777 add if available */
  IF AVAILABLE bk-raum THEN
  DO:
    FIND FIRST bk-setup WHERE bk-setup.setup-id = setup-id NO-LOCK. 
    raum-bez = bk-raum.bezeich. 
    setup-bez = bk-setup.bezeich. 
    bk-list.raum = bk-rset.raum. 
    bk-list.bezeich = bk-rset.bezeich. 
    bk-list.groesse = bk-rset.groesse. 
    bk-list.nebenstelle = bk-rset.nebenstelle. 
    bk-list.personen = bk-rset.personen. 
    bk-list.preis = bk-rset.preis. 
    bk-list.vorbereit = bk-rset.vorbereit. 
    bk-list.vname = bk-rset.vname. 
    bk-list.rec-id = RECID(bk-rset).
  END.
END. 
