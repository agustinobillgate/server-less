DEFINE TEMP-TABLE ins-list
    FIELD t-recid       AS INTEGER
    FIELD artnr         AS INTEGER
    FIELD bezeich       AS CHARACTER
    FIELD anzahl        AS DECIMAL
    FIELD traubensort   AS CHARACTER 
    FIELD txtnr         AS INTEGER
    FIELD lieferdatum   AS DATE
    FIELD stornogrund   AS CHARACTER
    FIELD bemerk        AS CHAR FORMAT "x(24)"
    FIELD quality       AS CHARACTER
    FIELD jahrgang      AS INTEGER
    FIELD new-created   AS LOGICAL INIT NO
    FIELD lief-nr       AS INTEGER
    FIELD op-art        AS INTEGER
    FIELD docu-nr       AS CHARACTER
    FIELD bestelldatum  AS DATE
    FIELD soh           AS DECIMAL /*545FBD gerald*/
.

DEFINE INPUT PARAMETER pos AS INTEGER.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE INPUT PARAMETER TABLE FOR ins-list.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 

FOR EACH ins-list WHERE ins-list.new-created NO-LOCK,
  FIRST l-artikel WHERE l-artikel.artnr = ins-list.artnr NO-LOCK:
  pos = pos + 1.
  CREATE l-order. 
  ASSIGN 
    l-order.docu-nr       = ins-list.docu-nr 
    l-order.artnr         = ins-list.artnr 
    l-order.anzahl        = ins-list.anzahl 
    l-order.lieferdatum   = ins-list.lieferdatum 
    l-order.pos           = pos 
    l-order.bestelldatum  = ins-list.bestelldatum 
    l-order.op-art        = 1 
    l-order.lief-fax[1]   = bediener.username 
    l-order.lief-fax[3]   = l-artikel.traubensort /* delivery Unit */ 
    l-order.flag          = YES
    l-order.besteller     = ins-list.bemerk
    l-order.stornogrund   = ins-list.stornogrund
    l-order.txtnr         = l-artikel.lief-einheit.
END.
