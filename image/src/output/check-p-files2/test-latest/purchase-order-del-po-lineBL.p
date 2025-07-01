
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER l-orderhdr-rec-id AS INT.
DEF INPUT PARAMETER bediener-username AS CHAR.
DEF OUTPUT PARAMETER del-mainpo AS LOGICAL INITIAL NO.


FIND FIRST l-order WHERE RECID(l-order) = rec-id.
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = l-orderhdr-rec-id.
RUN del-po-line.

PROCEDURE del-po-line: 
DEFINE buffer l-od FOR l-order. 
 
  FIND CURRENT l-order EXCLUSIVE-LOCK. 
  ASSIGN
    l-order.loeschflag = 2
    l-order.lieferdatum = billdate 
    l-order.lief-fax[2] = bediener-username
  .
  FIND CURRENT l-order NO-LOCK. 
 
  FIND FIRST l-od WHERE l-od.docu-nr = l-orderhdr.docu-nr AND 
    l-od.pos GT 0 AND l-od.loeschflag = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-od THEN 
  DO: 
    FIND FIRST l-od WHERE l-od.docu-nr = l-orderhdr.docu-nr AND 
    l-od.pos EQ 0 EXCLUSIVE-LOCK NO-ERROR. 
    ASSIGN
      l-od.loeschflag = 2
      l-od.lieferdatum-eff = billdate 
      l-od.lief-fax[3] = bediener-username
    . 
    FIND CURRENT l-od NO-LOCK. 
  END. 
  del-mainpo = YES. 
END. 
