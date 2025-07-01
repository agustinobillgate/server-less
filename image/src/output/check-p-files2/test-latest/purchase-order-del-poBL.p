
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER q2-list-docu-nr AS CHAR.
DEF INPUT PARAMETER bediener-username AS CHAR.

RUN del-po.

PROCEDURE del-po:
DEFINE buffer l-od  FOR l-order. 
DEFINE buffer l-od1 FOR l-order. 
  FIND FIRST l-od WHERE l-od.docu-nr = q2-list-docu-nr AND l-od.pos EQ 0 
      EXCLUSIVE-LOCK. 
  ASSIGN
    l-od.loeschflag = 2 
    l-od.lieferdatum-eff = billdate
    l-od.lief-fax[3] = bediener-username
  . 
  FIND CURRENT l-od NO-LOCK. 
 
  FOR EACH l-od1 WHERE l-od1.docu-nr = q2-list-docu-nr AND 
    l-od1.pos GT 0 AND l-od1.loeschflag = 0 NO-LOCK: 
    FIND FIRST l-od WHERE RECID(l-od) = RECID(l-od1) EXCLUSIVE-LOCK.
    ASSIGN
      l-od.loeschflag = 2
      l-od.lieferdatum = billdate 
      l-od.lief-fax[2] = bediener-username
    . 
    FIND CURRENT l-od NO-LOCK. 
  END. 
END. 
