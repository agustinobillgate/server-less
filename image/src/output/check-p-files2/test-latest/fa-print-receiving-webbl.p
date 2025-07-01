
DEFINE TEMP-TABLE str-list 
  FIELD artnr AS INTEGER
  FIELD qty AS DECIMAL 
  FIELD warenwert AS DECIMAL 
  FIELD munit AS CHAR 
  FIELD bezeich AS CHAR
  FIELD nr AS INTEGER
  FIELD price AS DECIMAL
  FIELD lscheinnr AS CHAR.
  

DEFINE INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init   AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER lief-nr     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER po-nr       AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER store       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER to-date     AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER deliv-nr    AS CHAR    NO-UNDO. 
DEFINE OUTPUT PARAMETER printer-nr AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER show-price AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER crterm     AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER d-purchase AS LOGICAL NO-UNDO. 
DEFINE OUTPUT PARAMETER unit-price AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER firma      AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-amount AS DECIMAL.

{Supertransbl.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fa-print-receiving". 

FIND FIRST htparam WHERE paramnr = 111 NO-LOCK. 
printer-nr = finteger. 
  
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
 
FIND FIRST fa-ordheader WHERE fa-ordheader.supplier-nr = lief-nr 
  AND fa-ordheader.order-nr = po-nr NO-LOCK NO-ERROR. 
IF AVAILABLE fa-ordheader THEN crterm = fa-ordheader.credit-term. 
 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
IF AVAILABLE l-lieferant THEN firma = l-lieferant.firma.
IF store = 0 THEN RUN create-list. 
ELSE RUN create-list1. 

FIND CURRENT fa-ordheader NO-LOCK. 

PROCEDURE create-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE create-it AS LOGICAL. 
 
FOR EACH str-list: 
  delete str-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  i = 0. 
  d-purchase = NO. 

  FOR EACH fa-op WHERE fa-op.datum EQ to-date 
  AND fa-op.lief-nr = lief-nr 
  AND fa-op.loeschflag = 0 
  /*AND fa-op.loeschflag LE 1 */ 
  AND fa-op.anzahl NE 0 
  AND fa-op.lscheinnr = deliv-nr  
  AND fa-op.docu-nr = po-nr NO-LOCK, 
  FIRST mathis WHERE mathis.nr = fa-op.nr 
  NO-LOCK /*BY l-op.pos*/ BY fa-op.zeit BY mathis.NAME: 

    i = i + 1. 
    IF fa-op.docu-nr = fa-op.lscheinnr THEN d-purchase = YES. 
    
    tot-anz = tot-anz + fa-op.anzahl. 
    IF show-price THEN tot-amount = tot-amount + fa-op.warenwert. 
    IF show-price THEN unit-price = fa-op.einzelpreis. 
    
    /* comment this code by Oscar (18 Oktober 2024) - C11EAE */
    /* FIND FIRST str-list WHERE str-list.artnr = fa-op.nr NO-ERROR. 
    create-it = NOT AVAILABLE str-list.  */

    CREATE str-list.
    ASSIGN
        str-list.artnr = fa-op.nr
        str-list.qty = fa-op.anzahl
        str-list.munit = "unit " /*l-artikel.masseinheit*/
        str-list.nr = mathis.nr
        str-list.bezeich = mathis.NAME
        str-list.price = unit-price
        str-list.warenwert = fa-op.warenwert
        str-list.lscheinnr = fa-op.lscheinnr
      .
  END. 
  CREATE str-list. 
  ASSIGN
      str-list.bezeich = "T O T A L"
      str-list.qty = tot-anz
      str-list.warenwert = tot-amount.
END. 
 
PROCEDURE create-list1: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE create-it AS LOGICAL. 
 
FOR EACH str-list: 
  delete str-list. 
END. 
 
  tot-anz = 0. 
  tot-amount = 0. 
  i = 0. 
  d-purchase = NO. 

  FOR EACH fa-op WHERE fa-op.datum EQ to-date 
  AND fa-op.lief-nr = lief-nr 
  AND fa-op.loeschflag  = 0 
  /*AND l-op.loeschflag LE 1*/ 
  AND fa-op.anzahl NE 0 
  /*AND l-op.lager-nr = store */
  AND fa-op.lscheinnr = deliv-nr 
  AND fa-op.docu-nr = po-nr NO-LOCK, 
  FIRST mathis WHERE mathis.nr = fa-op.nr 
  NO-LOCK /*BY l-op.pos*/ BY fa-op.zeit BY mathis.NAME: 

    i = i + 1. 
    IF fa-op.docu-nr = fa-op.lscheinnr THEN d-purchase = YES. 

    tot-anz = tot-anz + fa-op.anzahl. 
    IF show-price THEN tot-amount = tot-amount + fa-op.warenwert. 
    IF show-price THEN unit-price = fa-op.einzelpreis. 
    
    /* comment this code by Oscar (18 Oktober 2024) - C11EAE */
    /* FIND FIRST str-list WHERE str-list.artnr = fa-op.nr NO-ERROR. 
    create-it = NOT AVAILABLE str-list.  */

    CREATE str-list. 
    ASSIGN
        str-list.artnr = fa-op.nr
        str-list.qty = fa-op.anzahl
        str-list.munit = "unit" /*l-artikel.masseinheit*/
        str-list.nr = mathis.nr
        str-list.bezeich = mathis.NAME
        str-list.price = unit-price
        str-list.warenwert = fa-op.warenwert
        str-list.lscheinnr = fa-op.lscheinnr
      .
  END. 
  CREATE str-list. 
  ASSIGN
      str-list.bezeich = "T O T A L"
      str-list.qty = tot-anz
      str-list.warenwert = tot-anz.
END. 
