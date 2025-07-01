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
    FIELD sorting    LIKE cost-list.sorting
    FIELD Order-Date LIKE fa-ordheader.Order-Date
    FIELD Order-Nr   LIKE fa-ordheader.Order-Nr
    FIELD Order-Type LIKE fa-ordheader.Order-Type   
    FIELD bezeich    LIKE cost-list.bezeich 
    FIELD firma      LIKE l-lieferant.firma
    FIELD wabkurz    LIKE w-list.wabkurz  
    FIELD Released-Date LIKE fa-ordheader.Released-Date
    FIELD create-by  LIKE username.create-by
    FIELD Created-Date LIKE fa-ordheader.Created-Date 
    FIELD printed   LIKE fa-ordheader.printed        
    FIELD Expected-Delivery LIKE  fa-ordheader.Expected-Delivery
    FIELD modify-by LIKE username.modify-by 
    FIELD modified-date LIKE fa-ordheader.modified-date 
    FIELD close-by  LIKE username.close-by              
    FIELD close-date LIKE username.close-date           
    FIELD close-time LIKE username.close-time           
    FIELD last-arrival LIKE username.last-arrival
    FIELD Released-Flag LIKE fa-ordheader.Released-Flag
    FIELD Supplier-Nr LIKE fa-ordheader.Supplier-Nr
    FIELD ActiveFlag LIKE fa-ordheader.ActiveFlag
    FIELD Order-Desc LIKE fa-ordheader.Order-Desc
    FIELD Order-Name LIKE fa-ordheader.Order-Name
    FIELD total-amount LIKE username.total-amount.

DEFINE INPUT PARAMETER from-date  AS DATE. 
DEFINE INPUT PARAMETER to-date    AS DATE.
DEFINE INPUT PARAMETER billdate   AS DATE. 
DEFINE INPUT PARAMETER stat-order AS INT.
DEFINE INPUT PARAMETER lnumber    AS INT.
DEFINE INPUT PARAMETER all-supp   AS LOGICAL.
DEFINE INPUT PARAMETER po-number  AS CHAR. 
DEFINE INPUT PARAMETER TABLE FOR cost-list.
DEFINE INPUT PARAMETER TABLE FOR w-list.
DEFINE INPUT PARAMETER TABLE FOR username.
DEFINE OUTPUT PARAMETER TABLE FOR temp.

DEFINE VARIABLE min-statorder AS INTEGER.

IF stat-order = 0 AND all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date >= from-date 
    AND fa-ordheader.order-date <= to-date AND fa-ordheader.activeflag = 0 
    AND fa-ordheader.Expected-Delivery >= billdate NO-LOCK USE-INDEX datumactive ,
    FIRST w-list WHERE w-list.nr = fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr = fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr = fa-ordheader.order-nr NO-LOCK:

    IF (po-number = "" OR fa-ordheader.order-nr = po-number) THEN
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
    END.
  END.
ELSE IF stat-order = 0 AND NOT all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date >= from-date 
    AND fa-ordheader.order-date <= to-date AND fa-ordheader.activeflag = 0 
    AND fa-ordheader.supplier-nr = lnumber AND fa-ordheader.Expected-Delivery >= billdate  NO-LOCK 
    USE-INDEX datumactivesupp ,
    FIRST w-list WHERE w-list.nr = fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr = fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr = fa-ordheader.order-nr NO-LOCK:
    IF (po-number = "" OR fa-ordheader.order-nr = po-number)  THEN
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
    END.
  END.
ELSE IF stat-order = 2 AND all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date >= from-date 
    AND fa-ordheader.order-date <= to-date AND fa-ordheader.activeflag = 0 
    AND fa-ordheader.Expected-Delivery < billdate NO-LOCK USE-INDEX datumactive,
    FIRST w-list WHERE w-list.nr = fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr = fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr = fa-ordheader.order-nr NO-LOCK:
    IF (po-number = "" OR fa-ordheader.order-nr = po-number)  THEN
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
    END.
  END.
ELSE IF stat-order = 2 AND NOT all-supp THEN
  FOR EACH fa-ordheader WHERE fa-ordheader.order-date >= from-date 
    AND fa-ordheader.order-date <= to-date AND fa-ordheader.activeflag = 0 
    AND fa-ordheader.supplier-nr = lnumber AND fa-ordheader.Expected-Delivery < billdate  NO-LOCK 
    USE-INDEX datumactivesupp ,
    FIRST w-list WHERE w-list.nr = fa-ordheader.currency NO-LOCK,
    FIRST cost-list WHERE cost-list.nr = fa-ordheader.dept-nr NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr NO-LOCK ,
    FIRST username WHERE username.order-nr = fa-ordheader.order-nr NO-LOCK:
    IF (po-number = "" OR fa-ordheader.order-nr = po-number)  THEN
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
    END.
  END.
ELSE
DO:
  IF stat-order = 1 THEN min-statorder = 1.
  IF stat-order = 3 THEN min-statorder = 2.
  IF all-supp THEN
    FOR EACH fa-ordheader WHERE fa-ordheader.order-date >= from-date 
      AND fa-ordheader.order-date <= to-date AND fa-ordheader.activeflag = min-statorder NO-LOCK 
      USE-INDEX datumactive,
      FIRST w-list WHERE w-list.nr = fa-ordheader.currency NO-LOCK,
      FIRST cost-list WHERE cost-list.nr = fa-ordheader.dept-nr NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr NO-LOCK ,
      FIRST username WHERE username.order-nr = fa-ordheader.order-nr NO-LOCK:
      IF (po-number = "" OR fa-ordheader.order-nr = po-number)  THEN
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
      END.
    END.
  ELSE
    FOR EACH fa-ordheader WHERE fa-ordheader.order-date >= from-date 
      AND fa-ordheader.order-date <= to-date AND fa-ordheader.activeflag = min-statorder
      AND fa-ordheader.supplier-nr = lnumber NO-LOCK USE-INDEX datumactivesupp ,
      FIRST w-list WHERE w-list.nr = fa-ordheader.currency NO-LOCK,
      FIRST cost-list WHERE cost-list.nr = fa-ordheader.dept-nr NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr NO-LOCK ,
      FIRST username WHERE username.order-nr = fa-ordheader.order-nr NO-LOCK:
      IF (po-number = "" OR fa-ordheader.order-nr = po-number)  THEN
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
      END.
    END.
END.
