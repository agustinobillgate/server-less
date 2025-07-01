DEFINE TEMP-TABLE t-order
  FIELD fa-nr LIKE fa-order.fa-nr  
  FIELD NAME LIKE mathis.NAME
  FIELD asset LIKE  mathis.asset  
  FIELD order-qty LIKE fa-order.order-qty
  FIELD order-price LIKE fa-order.order-price
  FIELD order-amount LIKE fa-order.order-amount 
  FIELD order-nr     LIKE fa-order.order-nr     /*MG Kebutuhan CLOUD 53B264*/
  FIELD model        LIKE mathis.model.         /*MG Kebutuhan CLOUD 53B264*/

DEFINE INPUT PARAMETER t-table AS CHAR.
DEFINE INPUT PARAMETER supplier-nr LIKE fa-ordheader.supplier-nr.
DEFINE INPUT PARAMETER order-nr LIKE fa-ordheader.order-nr.
DEFINE OUTPUT PARAMETER flag-avail AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-order.

FOR EACH t-order:
    DELETE t-order.
END.

IF t-table = "l-kredit" THEN
DO:
  FIND FIRST l-kredit WHERE l-kredit.lief-nr = supplier-nr 
    AND l-kredit.name = order-nr AND l-kredit.zahlkonto GT 0 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN flag-avail = YES.
  ELSE flag-avail = NO.
END.
ELSE IF t-table = "fa-order" THEN
DO:
  FIND FIRST fa-order WHERE fa-order.order-nr = order-nr NO-LOCK NO-ERROR.
  IF AVAILABLE fa-order THEN flag-avail = YES.
  ELSE flag-avail = NO.
END.
ELSE IF t-table = "fa-order2" THEN
DO:
  FOR EACH fa-order WHERE fa-order.order-nr = order-nr 
    AND fa-order.activeflag = 0  NO-LOCK, 
    FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK 
    BY fa-order.fa-pos: 
    CREATE t-order.
    ASSIGN
      t-order.fa-nr = fa-order.fa-nr  
      t-order.NAME = mathis.NAME
      t-order.asset = mathis.asset  
      t-order.order-qty = fa-order.order-qty
      t-order.order-price = fa-order.order-price
      t-order.order-amount = fa-order.order-amount
      t-order.order-nr     = fa-order.order-nr
      t-order.model        = mathis.model.
  END.
END.

