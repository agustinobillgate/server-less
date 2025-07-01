DEFINE TEMP-TABLE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)"
  FIELD sorting AS CHAR FORMAT "x(1)" . 

DEFINE TEMP-TABLE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE TEMP-TABLE username
    FIELD order-nr      AS CHAR FORMAT "x(30)"
    FIELD create-by     AS CHAR FORMAT "x(30)"
    FIELD modify-by     AS CHAR FORMAT "x(30)"
    FIELD close-by      AS CHAR FORMAT "x(30)"
    FIELD close-date    AS DATE  
    FIELD close-time    AS CHAR FORMAT "x(10)"
    FIELD last-arrival  AS DATE
    FIELD total-amount  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" .

DEFINE TEMP-TABLE temp
    FIELD sorting           AS CHAR /* LIKE cost-list.sorting */
    FIELD Order-Date        AS DATE /* LIKE fa-ordheader.Order-Date */
    FIELD Order-Nr          AS CHAR /* LIKE fa-ordheader.Order-Nr */
    FIELD Order-Type        AS CHAR /* LIKE fa-ordheader.Order-Type */   
    FIELD bezeich           AS CHAR 
    FIELD firma             AS CHAR /* LIKE l-lieferant.firma */
    FIELD wabkurz           AS CHAR /* LIKE w-list.wabkurz */  
    FIELD Released-Date     AS DATE /* LIKE fa-ordheader.Released-Date */
    FIELD create-by         AS CHAR /* LIKE username.create-by */
    FIELD Created-Date      AS DATE /* LIKE fa-ordheader.Created-Date */ 
    FIELD printed           AS DATE /* LIKE fa-ordheader.printed */        
    FIELD Expected-Delivery AS DATE /* LIKE  fa-ordheader.Expected-Delivery */
    FIELD modify-by         AS CHAR /* LIKE username.modify-by */
    FIELD modified-date     AS DATE /* LIKE fa-ordheader.modified-date */
    FIELD close-by          AS CHAR /* LIKE username.close-by */              
    FIELD close-date        AS DATE /* LIKE username.close-date */           
    FIELD close-time        AS CHAR /* LIKE username.close-time */           
    FIELD last-arrival      AS DATE /* LIKE username.last-arrival */
    FIELD Released-Flag     AS LOGICAL /* LIKE fa-ordheader.Released-Flag */
    FIELD Supplier-Nr       AS INTEGER /* LIKE fa-ordheader.Supplier-Nr */
    FIELD ActiveFlag        AS INTEGER /* LIKE fa-ordheader.ActiveFlag */
    FIELD Order-Desc        AS CHAR /* LIKE fa-ordheader.Order-Desc */
    FIELD Order-Name        AS CHAR /* LIKE fa-ordheader.Order-Name */
    FIELD total-amount      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" /* LIKE username.total-amount */
    FIELD devnote-no        AS CHAR /* LIKE fa-op.lscheinnr */
    FIELD arive-amount      AS DECIMAL /* LIKE fa-op.warenwert */
    FIELD order-amount      AS DECIMAL. /* LIKE fa-order.order-amount */

DEFINE TEMP-TABLE temp-detail
  FIELD COA    AS CHAR /* LIKE fa-artikel.fibukonto /* fa-grup.fibukonto */*/
  FIELD desc1  AS CHAR /* LIKE mathis.name */
  FIELD qty    AS INTEGER /* LIKE fa-order.order-qty */ 
  FIELD price  AS DECIMAL  /* LIKE fa-order.order-price */
  FIELD amount AS DECIMAL /* LIKE fa-order.order-amount */
  FIELD order-number AS CHAR. /* LIKE fa-order.order-nr. */

DEFINE TEMP-TABLE payload-list
  FIELD from-date   AS DATE
  FIELD to-date     AS DATE
  FIELD billdate    AS DATE
  FIELD stat-order  AS INT
  FIELD lnumber     AS INT
  FIELD all-supp    AS LOGICAL
  FIELD po-number   AS CHAR.


DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE INPUT PARAMETER TABLE FOR cost-list.
DEFINE INPUT PARAMETER TABLE FOR w-list.
DEFINE INPUT PARAMETER TABLE FOR username.
DEFINE OUTPUT PARAMETER TABLE FOR temp.
DEFINE OUTPUT PARAMETER TABLE FOR temp-detail.


DEFINE VARIABLE min-statorder AS INTEGER.
DEFINE VARIABLE temp-amount AS DECIMAL.
DEFINE VARIABLE tot-qty AS INTEGER.
DEFINE VARIABLE tot-price AS DECIMAL.
DEFINE VARIABLE tot-amount AS DECIMAL.

FIND FIRST payload-list.
IF payload-list.stat-order = 0 AND payload-list.all-supp THEN
DO:
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
    AND fa-ordheader.order-date LE payload-list.to-date AND fa-ordheader.activeflag EQ 0 
    AND fa-ordheader.Expected-Delivery GE payload-list.billdate NO-LOCK USE-INDEX datumactive ,
    FIRST w-list WHERE w-list.nr EQ fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr EQ fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr EQ fa-ordheader.order-nr NO-LOCK:
    tot-qty = 0.
    tot-price = 0.
    tot-amount = 0.  
    IF (payload-list.po-number = "" OR fa-ordheader.order-nr = payload-list.po-number) THEN
    DO:
      CREATE temp.
      ASSIGN
        temp.sorting           = cost-list.sorting
        temp.Order-Date        = fa-ordheader.Order-Date
        temp.Order-Nr          = fa-ordheader.Order-Nr
        temp.Order-Type        = fa-ordheader.Order-Type   
        temp.bezeich           = cost-list.bezeich 
        temp.firma             = l-lieferant.firma
        temp.wabkurz           = w-list.wabkurz  
        temp.Released-Date     = fa-ordheader.Released-Date
        temp.create-by         = username.create-by
        temp.Created-Date      = fa-ordheader.Created-Date 
        temp.printed           = fa-ordheader.printed        
        temp.Expected-Delivery = fa-ordheader.Expected-Delivery
        temp.modify-by         = username.modify-by 
        temp.modified-date     = fa-ordheader.modified-date 
        temp.close-by          = username.close-by              
        temp.close-date        = username.close-date           
        temp.close-time        = username.close-time           
        temp.last-arrival      = username.last-arrival
        temp.Released-Flag     = fa-ordheader.Released-Flag
        temp.Supplier-Nr       = fa-ordheader.Supplier-Nr
        temp.ActiveFlag        = fa-ordheader.ActiveFlag
        temp.Order-Desc        = fa-ordheader.Order-Desc
        temp.Order-Name        = fa-ordheader.Order-Name
        temp.total-amount      = username.total-amount.
      FIND FIRST fa-op WHERE fa-op.docu-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
      IF AVAILABLE fa-op THEN temp.devnote-no = fa-op.lscheinnr.

      FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:

          CREATE temp-detail.
          ASSIGN
            temp-detail.COA    = fa-artikel.fibukonto
            temp-detail.desc1  = mathis.name
            temp-detail.qty    = fa-order.order-qty
            temp-detail.price  = fa-order.order-price
            temp-detail.amount = fa-order.order-amount
            temp-detail.order-number = fa-order.order-nr
          tot-qty = tot-qty + fa-order.order-qty.
          tot-price = tot-price + fa-order.order-price.
          tot-amount = tot-amount + fa-order.order-amount.
      END.
      CREATE temp-detail.
        ASSIGN
          temp-detail.COA    = ""
          temp-detail.desc1  = "T O T A L"
          temp-detail.qty    = tot-qty
          temp-detail.price  = tot-price
          temp-detail.amount = tot-amount
          temp-detail.order-number = fa-ordheader.order-nr.
    END.
  END.

END.  
ELSE IF payload-list.stat-order = 0 AND NOT payload-list.all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
    AND fa-ordheader.order-date LE payload-list.to-date AND fa-ordheader.activeflag = 0 
    AND fa-ordheader.supplier-nr EQ payload-list.lnumber AND fa-ordheader.Expected-Delivery GE payload-list.billdate  NO-LOCK 
    USE-INDEX datumactivesupp ,
    FIRST w-list WHERE w-list.nr EQ fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr EQ fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr EQ fa-ordheader.order-nr NO-LOCK:
    IF (payload-list.po-number = "" OR fa-ordheader.order-nr = payload-list.po-number)  THEN
    DO:
      CREATE temp.
      ASSIGN
        temp.sorting           = cost-list.sorting
        temp.Order-Date        = fa-ordheader.Order-Date
        temp.Order-Nr          = fa-ordheader.Order-Nr
        temp.Order-Type        = fa-ordheader.Order-Type   
        temp.bezeich           = cost-list.bezeich 
        temp.firma             = l-lieferant.firma
        temp.wabkurz           = w-list.wabkurz  
        temp.Released-Date     = fa-ordheader.Released-Date
        temp.create-by         = username.create-by
        temp.Created-Date      = fa-ordheader.Created-Date 
        temp.printed           = fa-ordheader.printed        
        temp.Expected-Delivery = fa-ordheader.Expected-Delivery
        temp.modify-by         = username.modify-by 
        temp.modified-date     = fa-ordheader.modified-date 
        temp.close-by          = username.close-by              
        temp.close-date        = username.close-date           
        temp.close-time        = username.close-time           
        temp.last-arrival      = username.last-arrival
        temp.Released-Flag     = fa-ordheader.Released-Flag
        temp.Supplier-Nr       = fa-ordheader.Supplier-Nr
        temp.ActiveFlag        = fa-ordheader.ActiveFlag
        temp.Order-Desc        = fa-ordheader.Order-Desc
        temp.Order-Name        = fa-ordheader.Order-Name
        temp.total-amount      = username.total-amount.
      FIND FIRST fa-op WHERE fa-op.docu-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
      IF AVAILABLE fa-op THEN temp.devnote-no = fa-op.lscheinnr.

      FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:

          CREATE temp-detail.
          ASSIGN
            temp-detail.COA    = fa-artikel.fibukonto
            temp-detail.desc1  = mathis.name
            temp-detail.qty    = fa-order.order-qty
            temp-detail.price  = fa-order.order-price
            temp-detail.amount = fa-order.order-amount
            temp-detail.order-number = fa-order.order-nr
          tot-qty = tot-qty + fa-order.order-qty.
          tot-price = tot-price + fa-order.order-price.
          tot-amount = tot-amount + fa-order.order-amount.
      END.
      CREATE temp-detail.
        ASSIGN
          temp-detail.COA    = ""
          temp-detail.desc1  = "T O T A L"
          temp-detail.qty    = tot-qty
          temp-detail.price  = tot-price
          temp-detail.amount = tot-amount
          temp-detail.order-number = fa-ordheader.order-nr.
    END.
  END.
ELSE IF payload-list.stat-order = 2 AND payload-list.all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
    AND fa-ordheader.order-date LE payload-list.to-date AND fa-ordheader.activeflag EQ 0 
    AND fa-ordheader.Expected-Delivery LT payload-list.billdate NO-LOCK USE-INDEX datumactive,
    FIRST w-list WHERE w-list.nr EQ fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr EQ fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr EQ fa-ordheader.order-nr NO-LOCK:
    IF (payload-list.po-number = "" OR fa-ordheader.order-nr = payload-list.po-number)  THEN
    DO:
      CREATE temp.
      ASSIGN
        temp.sorting           = cost-list.sorting
        temp.Order-Date        = fa-ordheader.Order-Date
        temp.Order-Nr          = fa-ordheader.Order-Nr
        temp.Order-Type        = fa-ordheader.Order-Type   
        temp.bezeich           = cost-list.bezeich 
        temp.firma             = l-lieferant.firma
        temp.wabkurz           = w-list.wabkurz  
        temp.Released-Date     = fa-ordheader.Released-Date
        temp.create-by         = username.create-by
        temp.Created-Date      = fa-ordheader.Created-Date 
        temp.printed           = fa-ordheader.printed        
        temp.Expected-Delivery = fa-ordheader.Expected-Delivery
        temp.modify-by         = username.modify-by 
        temp.modified-date     = fa-ordheader.modified-date 
        temp.close-by          = username.close-by              
        temp.close-date        = username.close-date           
        temp.close-time        = username.close-time           
        temp.last-arrival      = username.last-arrival
        temp.Released-Flag     = fa-ordheader.Released-Flag
        temp.Supplier-Nr       = fa-ordheader.Supplier-Nr
        temp.ActiveFlag        = fa-ordheader.ActiveFlag
        temp.Order-Desc        = fa-ordheader.Order-Desc
        temp.Order-Name        = fa-ordheader.Order-Name
        temp.total-amount      = username.total-amount.
      FIND FIRST fa-op WHERE fa-op.docu-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
      IF AVAILABLE fa-op THEN temp.devnote-no = fa-op.lscheinnr.

      FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:

        CREATE temp-detail.
        ASSIGN
          temp-detail.COA    = fa-artikel.fibukonto
          temp-detail.desc1  = mathis.name
          temp-detail.qty    = fa-order.order-qty
          temp-detail.price  = fa-order.order-price
          temp-detail.amount = fa-order.order-amount
          temp-detail.order-number = fa-order.order-nr
        tot-qty = tot-qty + fa-order.order-qty.
        tot-price = tot-price + fa-order.order-price.
        tot-amount = tot-amount + fa-order.order-amount.
      END.
      CREATE temp-detail.
        ASSIGN
          temp-detail.COA    = ""
          temp-detail.desc1  = "T O T A L"
          temp-detail.qty    = tot-qty
          temp-detail.price  = tot-price
          temp-detail.amount = tot-amount
          temp-detail.order-number = fa-ordheader.order-nr.
    END.
  END.
ELSE IF payload-list.stat-order = 2 AND NOT payload-list.all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
    AND fa-ordheader.order-date LE payload-list.to-date AND fa-ordheader.activeflag = 0 
    AND fa-ordheader.supplier-nr EQ payload-list.lnumber AND fa-ordheader.Expected-Delivery LT payload-list.billdate  NO-LOCK 
    USE-INDEX datumactivesupp ,
    FIRST w-list WHERE w-list.nr EQ fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr EQ fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr EQ fa-ordheader.order-nr NO-LOCK:
    IF (payload-list.po-number = "" OR fa-ordheader.order-nr = payload-list.po-number)  THEN
    DO:
      CREATE temp.
      ASSIGN
        temp.sorting           = cost-list.sorting
        temp.Order-Date        = fa-ordheader.Order-Date
        temp.Order-Nr          = fa-ordheader.Order-Nr
        temp.Order-Type        = fa-ordheader.Order-Type   
        temp.bezeich           = cost-list.bezeich 
        temp.firma             = l-lieferant.firma
        temp.wabkurz           = w-list.wabkurz  
        temp.Released-Date     = fa-ordheader.Released-Date
        temp.create-by         = username.create-by
        temp.Created-Date      = fa-ordheader.Created-Date 
        temp.printed           = fa-ordheader.printed        
        temp.Expected-Delivery = fa-ordheader.Expected-Delivery
        temp.modify-by         = username.modify-by 
        temp.modified-date     = fa-ordheader.modified-date 
        temp.close-by          = username.close-by              
        temp.close-date        = username.close-date           
        temp.close-time        = username.close-time           
        temp.last-arrival      = username.last-arrival
        temp.Released-Flag     = fa-ordheader.Released-Flag
        temp.Supplier-Nr       = fa-ordheader.Supplier-Nr
        temp.ActiveFlag        = fa-ordheader.ActiveFlag
        temp.Order-Desc        = fa-ordheader.Order-Desc
        temp.Order-Name        = fa-ordheader.Order-Name
        temp.total-amount      = username.total-amount.
      FIND FIRST fa-op WHERE fa-op.docu-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
      IF AVAILABLE fa-op THEN temp.devnote-no = fa-op.lscheinnr.

      FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK,
        FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
        FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:

        CREATE temp-detail.
        ASSIGN
          temp-detail.COA    = fa-artikel.fibukonto
          temp-detail.desc1  = mathis.name
          temp-detail.qty    = fa-order.order-qty
          temp-detail.price  = fa-order.order-price
          temp-detail.amount = fa-order.order-amount
          temp-detail.order-number = fa-order.order-nr
        tot-qty = tot-qty + fa-order.order-qty.
        tot-price = tot-price + fa-order.order-price.
        tot-amount = tot-amount + fa-order.order-amount.
      END.
      CREATE temp-detail.
        ASSIGN
          temp-detail.COA    = ""
          temp-detail.desc1  = "T O T A L"
          temp-detail.qty    = tot-qty
          temp-detail.price  = tot-price
          temp-detail.amount = tot-amount
          temp-detail.order-number = fa-ordheader.order-nr.
    END.
  END.
ELSE
DO:
  IF payload-list.stat-order = 1 THEN min-statorder = 1.
  IF payload-list.stat-order = 3 THEN min-statorder = 2.
  IF payload-list.all-supp THEN
    FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
      AND fa-ordheader.order-date LE payload-list.to-date AND fa-ordheader.activeflag EQ min-statorder NO-LOCK 
      USE-INDEX datumactive,
      FIRST w-list WHERE w-list.nr EQ fa-ordheader.currency NO-LOCK,
      FIRST cost-list WHERE cost-list.nr EQ fa-ordheader.dept-nr NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-ordheader.supplier-nr NO-LOCK ,
      FIRST username WHERE username.order-nr EQ fa-ordheader.order-nr NO-LOCK:
      IF (payload-list.po-number = "" OR fa-ordheader.order-nr = payload-list.po-number)  THEN
      DO:
        CREATE temp.
        ASSIGN
          temp.sorting           = cost-list.sorting
          temp.Order-Date        = fa-ordheader.Order-Date
          temp.Order-Nr          = fa-ordheader.Order-Nr
          temp.Order-Type        = fa-ordheader.Order-Type   
          temp.bezeich           = cost-list.bezeich 
          temp.firma             = l-lieferant.firma
          temp.wabkurz           = w-list.wabkurz  
          temp.Released-Date     = fa-ordheader.Released-Date
          temp.create-by         = username.create-by
          temp.Created-Date      = fa-ordheader.Created-Date 
          temp.printed           = fa-ordheader.printed        
          temp.Expected-Delivery = fa-ordheader.Expected-Delivery
          temp.modify-by         = username.modify-by 
          temp.modified-date     = fa-ordheader.modified-date 
          temp.close-by          = username.close-by              
          temp.close-date        = username.close-date           
          temp.close-time        = username.close-time           
          temp.last-arrival      = username.last-arrival
          temp.Released-Flag     = fa-ordheader.Released-Flag
          temp.Supplier-Nr       = fa-ordheader.Supplier-Nr
          temp.ActiveFlag        = fa-ordheader.ActiveFlag
          temp.Order-Desc        = fa-ordheader.Order-Desc
          temp.Order-Name        = fa-ordheader.Order-Name
          temp.total-amount      = username.total-amount.
        FIND FIRST fa-op WHERE fa-op.docu-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-op THEN temp.devnote-no = fa-op.lscheinnr.

        FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK,
          FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
          FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:

          CREATE temp-detail.
          ASSIGN
            temp-detail.COA    = fa-artikel.fibukonto
            temp-detail.desc1  = mathis.name
            temp-detail.qty    = fa-order.order-qty
            temp-detail.price  = fa-order.order-price
            temp-detail.amount = fa-order.order-amount
            temp-detail.order-number = fa-order.order-nr
          tot-qty = tot-qty + fa-order.order-qty.
          tot-price = tot-price + fa-order.order-price.
          tot-amount = tot-amount + fa-order.order-amount.
        END.
        CREATE temp-detail.
          ASSIGN
            temp-detail.COA    = ""
            temp-detail.desc1  = "T O T A L"
            temp-detail.qty    = tot-qty
            temp-detail.price  = tot-price
            temp-detail.amount = tot-amount
            temp-detail.order-number = fa-ordheader.order-nr.
      END.
    END.
  ELSE
    FOR EACH fa-ordheader WHERE fa-ordheader.order-date GE payload-list.from-date 
      AND fa-ordheader.order-date LE payload-list.to-date AND fa-ordheader.activeflag EQ min-statorder
      AND fa-ordheader.supplier-nr EQ payload-list.lnumber NO-LOCK USE-INDEX datumactivesupp ,
      FIRST w-list WHERE w-list.nr EQ fa-ordheader.currency NO-LOCK,
      FIRST cost-list WHERE cost-list.nr EQ fa-ordheader.dept-nr NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ fa-ordheader.supplier-nr NO-LOCK ,
      FIRST username WHERE username.order-nr EQ fa-ordheader.order-nr NO-LOCK:
      IF (payload-list.po-number = "" OR fa-ordheader.order-nr = payload-list.po-number)  THEN
      DO:
        CREATE temp.
        ASSIGN
          temp.sorting           = cost-list.sorting
          temp.Order-Date        = fa-ordheader.Order-Date
          temp.Order-Nr          = fa-ordheader.Order-Nr
          temp.Order-Type        = fa-ordheader.Order-Type   
          temp.bezeich           = cost-list.bezeich 
          temp.firma             = l-lieferant.firma
          temp.wabkurz           = w-list.wabkurz  
          temp.Released-Date     = fa-ordheader.Released-Date
          temp.create-by         = username.create-by
          temp.Created-Date      = fa-ordheader.Created-Date 
          temp.printed           = fa-ordheader.printed        
          temp.Expected-Delivery = fa-ordheader.Expected-Delivery
          temp.modify-by         = username.modify-by 
          temp.modified-date     = fa-ordheader.modified-date 
          temp.close-by          = username.close-by              
          temp.close-date        = username.close-date           
          temp.close-time        = username.close-time           
          temp.last-arrival      = username.last-arrival
          temp.Released-Flag     = fa-ordheader.Released-Flag
          temp.Supplier-Nr       = fa-ordheader.Supplier-Nr
          temp.ActiveFlag        = fa-ordheader.ActiveFlag
          temp.Order-Desc        = fa-ordheader.Order-Desc
          temp.Order-Name        = fa-ordheader.Order-Name
          temp.total-amount      = username.total-amount.
        FIND FIRST fa-op WHERE fa-op.docu-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-op THEN temp.devnote-no = fa-op.lscheinnr.

        FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK,
          FIRST mathis WHERE mathis.nr EQ fa-order.fa-nr NO-LOCK,
          FIRST fa-artikel WHERE fa-artikel.nr EQ mathis.nr NO-LOCK:

          CREATE temp-detail.
          ASSIGN
            temp-detail.COA    = fa-artikel.fibukonto
            temp-detail.desc1  = mathis.name
            temp-detail.qty    = fa-order.order-qty
            temp-detail.price  = fa-order.order-price
            temp-detail.amount = fa-order.order-amount
            temp-detail.order-number = fa-order.order-nr
          tot-qty = tot-qty + fa-order.order-qty.
          tot-price = tot-price + fa-order.order-price.
          tot-amount = tot-amount + fa-order.order-amount.
        END.
        CREATE temp-detail.
          ASSIGN
            temp-detail.COA    = ""
            temp-detail.desc1  = "T O T A L"
            temp-detail.qty    = tot-qty
            temp-detail.price  = tot-price
            temp-detail.amount = tot-amount
            temp-detail.order-number = fa-ordheader.order-nr.
      END.
    END.
END.

FOR EACH temp:
    FOR EACH fa-op WHERE fa-op.docu-nr = temp.order-nr AND fa-op.lscheinnr = temp.devnote-no NO-LOCK:
        temp-amount = temp-amount + fa-op.warenwert.
    END.
    ASSIGN
      temp.arive-amount = temp-amount
      temp-amount = 0.

    FOR EACH fa-order WHERE fa-order.order-nr = temp.order-nr NO-LOCK:
        temp-amount = temp-amount + fa-order.order-amount.
    END.
    ASSIGN
      temp.order-amount = temp-amount
      temp-amount = 0.
END.
