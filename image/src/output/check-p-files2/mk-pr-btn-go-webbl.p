

DEF TEMP-TABLE s-list LIKE l-order
    FIELD s-recid AS INTEGER.

DEF INPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER docu-nr                     AS CHAR.
DEF INPUT PARAMETER rec-id                      AS INT.
DEF INPUT PARAMETER dml-created                 AS LOGICAL.
DEF INPUT PARAMETER t-l-orderhdr-lieferdatum    AS DATE.
DEF INPUT PARAMETER t-l-orderhdr-angebot-lief   AS INT.
DEF INPUT PARAMETER comments-screen-value       AS CHAR.
DEF INPUT PARAMETER dml-grp                     AS INT.
DEF INPUT PARAMETER dml-datum                   AS DATE.

DEF OUTPUT PARAMETER created                    AS LOGICAL.
DEF OUTPUT PARAMETER pr-nr                      AS CHAR.

FOR EACH s-list:
    CREATE l-order.
    l-order.zeit    = s-list.zeit.
    BUFFER-COPY s-list TO l-order.
    ASSIGN l-order.zeit = TIME.
    FIND CURRENT l-order NO-LOCK.
    
END.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id.
ASSIGN 
    l-orderhdr.lieferdatum = t-l-orderhdr-lieferdatum
    l-orderhdr.lief-fax[3] = comments-screen-value
    l-orderhdr.lief-fax[2] = " ; ; ; "
    l-orderhdr.angebot-lief[1] = t-l-orderhdr-angebot-lief
    created                = YES 
    pr-nr                  = docu-nr
.

IF dml-created THEN RUN del-dml-art.

PROCEDURE del-dml-art: 
DEFINE BUFFER dml-art1 FOR dml-art. 
  IF dml-grp = 0 THEN 
  FOR EACH dml-art WHERE dml-art.datum = dml-datum 
    AND dml-art.anzahl NE 0 EXCLUSIVE-LOCK: 
    DELETE dml-art. 
  END. 
  ELSE 
  FOR EACH dml-art WHERE dml-art.datum = dml-datum 
    AND dml-art.anzahl NE 0 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr 
    AND l-artikel.zwkum = dml-grp NO-LOCK: 
    FIND FIRST dml-art1 WHERE RECID(dml-art1) = RECID(dml-art) EXCLUSIVE-LOCK. 
    DELETE dml-art1. 
  END. 
END. 

