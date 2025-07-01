DEFINE TEMP-TABLE s-list 
  FIELD pos         AS INTEGER
  FIELD artnr       AS INTEGER 
  FIELD new-created AS LOGICAL INITIAL NO
  FIELD bemerk      AS CHAR FORMAT "x(24)"
. 
DEFINE TEMP-TABLE ins-list
    FIELD t-recid       AS INT
    FIELD artnr         LIKE l-order.artnr 
    FIELD bezeich       LIKE l-artikel.bezeich 
    FIELD anzahl        LIKE l-order.anzahl 
    FIELD traubensort   LIKE l-artikel.traubensort 
    FIELD txtnr         LIKE l-order.txtnr 
    FIELD lieferdatum   LIKE l-order.lieferdatum 
    FIELD stornogrund   LIKE l-order.stornogrund 
    FIELD bemerk        AS CHAR FORMAT "x(24)"
    FIELD quality       LIKE l-order.quality
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD new-created   AS LOGICAL INIT NO
    FIELD lief-nr       LIKE l-order.lief-nr
    FIELD op-art        LIKE l-order.op-art
    FIELD docu-nr       LIKE l-order.docu-nr
    FIELD bestelldatum  LIKE l-order.bestelldatum
    .
    
DEFINE BUFFER l-art FOR l-artikel. 


DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER pos          AS INT  NO-UNDO.
DEFINE INPUT PARAMETER s-artnr      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER bemerkung    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER docu-nr      AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER qty          AS DEC  NO-UNDO.
DEFINE INPUT PARAMETER delivery     AS DATE NO-UNDO.
DEFINE INPUT PARAMETER bestelldatum AS DATE NO-UNDO.
DEFINE INPUT PARAMETER traubensort  AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER cost-acct    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER lief-einheit AS DECIMAL  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR ins-list.

DEFINE VARIABLE price0 AS DECIMAL. 
DEFINE VARIABLE int-costacct AS INTEGER NO-UNDO INIT ?.

RUN create-list.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
pos = pos + 1. 
DO: 
    CREATE s-list. 
    ASSIGN 
      s-list.artnr          = s-artnr 
      s-list.new-created    = YES
      s-list.pos            = pos
      s-list.bemerk         = bemerkung
    .
    CREATE l-order. 
    ASSIGN 
      l-order.docu-nr       = docu-nr 
      l-order.artnr         = s-artnr 
      l-order.anzahl        = qty 
      l-order.lieferdatum   = delivery 
      /*l-order.stornogrund   = cost-acct */
      l-order.pos           = pos 
      l-order.bestelldatum  = bestelldatum 
      l-order.op-art        = 1 
      l-order.lief-fax[1]   = bediener.username 
      l-order.lief-fax[3]   = traubensort /* delivery Unit */ 
      l-order.flag          = YES
      l-order.besteller     = bemerkung.

    ASSIGN int-costacct = INTEGER(cost-acct) NO-ERROR.
    IF int-costacct NE 0 THEN l-order.stornogrund = cost-acct. 
    IF lief-einheit NE 0 THEN l-order.txtnr = lief-einheit. 
    RELEASE l-order. 
END. 
    

FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.lief-nr = 0 
    AND l-order.loeschflag LE 1 NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK, 
    FIRST s-list WHERE s-list.artnr = l-order.artnr BY s-list.pos DESCENDING. 
    CREATE ins-list.
    ASSIGN  ins-list.t-recid       = RECID(l-order)
            ins-list.artnr         = l-order.artnr 
            ins-list.bezeich       = l-art.bezeich 
            ins-list.anzahl        = l-order.anzahl 
            ins-list.traubensort   = l-art.traubensort 
            ins-list.txtnr         = l-order.txtnr 
            ins-list.lieferdatum   = l-order.lieferdatum 
            ins-list.stornogrund   = l-order.stornogrund 
            ins-list.bemerk        = s-list.bemerk 
            ins-list.quality       = l-order.quality
            ins-list.jahrgang      = l-art.jahrgang
            ins-list.new-created   = s-list.new-created
            ins-list.lief-nr       = l-order.lief-nr
            ins-list.op-art        = l-order.op-art
            ins-list.docu-nr       = l-order.docu-nr
            ins-list.bestelldatum  = l-order.bestelldatum
            .
END.
                                                        
/******************************* PROCEDURES ***********************************/  
PROCEDURE create-list: 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND l-order.pos GT 0 
    AND l-order.lief-nr = 0 AND l-order.loeschflag LE 1 NO-LOCK
    BY l-order.pos: 
    CREATE s-list.
    ASSIGN
      s-list.artnr  = l-order.artnr
      s-list.pos    = l-order.pos
      s-list.bemerk = l-order.besteller
      pos           = l-order.pos
    .
  END. 
END. 

