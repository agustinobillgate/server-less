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

DEFINE INPUT PARAMETER TABLE FOR ins-list.    
        
FOR EACH ins-list WHERE ins-list.new-created: 
    FIND FIRST l-order WHERE l-order.artnr = ins-list.artnr 
        EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-order THEN DELETE l-order. 
END. 
