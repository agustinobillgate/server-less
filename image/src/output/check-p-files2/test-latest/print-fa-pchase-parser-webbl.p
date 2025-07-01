DEFINE TEMP-TABLE op-list 
  FIELD artnr       AS INTEGER 
  FIELD anzahl      AS DECIMAL 
  FIELD bezeich     AS CHAR 
  FIELD bez-aend    AS LOGICAL INITIAL NO 
  FIELD disc        AS DECIMAL 
  FIELD disc2       AS DECIMAL 
  FIELD vat         AS DECIMAL 
  FIELD epreis      AS DECIMAL 
  FIELD epreis0     AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD konto       AS CHAR 
  FIELD warenwert0  AS DECIMAL
  FIELD remark      AS CHAR
. 

DEF INPUT  PARAMETER docu-nr        AS CHAR. 
DEF OUTPUT PARAMETER err            AS INT INIT 0.
DEF OUTPUT PARAMETER supplier-name  AS CHAR.
DEF OUTPUT PARAMETER bill-recv      AS CHAR.
DEF OUTPUT PARAMETER address1       AS CHAR.
DEF OUTPUT PARAMETER address2       AS CHAR.
DEF OUTPUT PARAMETER order-date     AS DATE.
DEF OUTPUT PARAMETER deliv-date     AS DATE.
DEF OUTPUT PARAMETER telefon        AS CHAR.
DEF OUTPUT PARAMETER fax            AS CHAR.
DEF OUTPUT PARAMETER pr-nr          AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR op-list.

RUN create-list.

PROCEDURE create-list:
  DEFINE VARIABLE create-it AS LOGICAL. 
  DEFINE VARIABLE curr-bez  AS CHAR. 
  DEFINE VARIABLE bez-aend  AS LOGICAL. 
  DEFINE VARIABLE disc      AS DECIMAL. 
  DEFINE VARIABLE disc2     AS DECIMAL. 
  DEFINE VARIABLE vat       AS DECIMAL. 
  DEFINE VARIABLE tot-qty   AS DECIMAL FORMAT "->>,>>9.99" INITIAL 0.

  DEFINE BUFFER l-art FOR l-artikel. 
  
  FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = docu-nr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE fa-ordheader THEN
  DO:
    err = 2.
    /*MT
    HIDE MESSAGE NO-PAUSE.
    MESSAGE "fa-order record not found. Printing process stopped."
      VIEW-AS ALERT-BOX INFORMATION.
    */
    RETURN.
  END.
  
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr 
    = fa-ordheader.supplier-nr NO-LOCK NO-ERROR. 
  IF AVAILABLE l-lieferant THEN
  DO:
    ASSIGN 
        supplier-name = l-lieferant.namekontakt + ", " + l-lieferant.vorname1 
                        + " " + l-lieferant.anrede1
        bill-recv     = l-lieferant.firma
        address1      = l-lieferant.adresse1
        address2      = l-lieferant.adresse2
        order-date    = DATE(fa-ordheader.order-date)
        deliv-date    = DATE(fa-ordheader.expected-delivery)
        telefon       = l-lieferant.telefon
        fax           = l-lieferant.fax
        pr-nr         = fa-ordheader.pr-nr
        .
  END.

  FOR EACH fa-order WHERE fa-order.order-nr = docu-nr AND 
    fa-order.activeflag = 0 NO-LOCK BY fa-order.fa-pos :

    create-it = NO. 

    bez-aend = NO. 
    
    FIND FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK.
    curr-bez = mathis.NAME.

    disc = 0. 
    disc2 = 0. 

    FIND FIRST op-list WHERE op-list.artnr = fa-order.fa-nr 
    AND op-list.epreis = fa-order.order-price 
    AND op-list.bezeich = mathis.NAME
    AND op-list.disc = fa-order.discount1 AND op-list.disc2 = discount2 
    NO-ERROR. 

    IF NOT AVAILABLE op-list OR create-it THEN 
    DO: 
      vat = 0. 
      CREATE op-list.
      ASSIGN
        op-list.artnr = fa-order.fa-nr
        op-list.bezeich = curr-bez
        op-list.bez-aend = bez-aend 
        op-list.epreis = fa-order.order-price 
        op-list.epreis0 = fa-order.order-price 
        /*op-list.konto = l-order.stornogrund*/
        op-list.remark = fa-order.fa-remarks
        op-list.disc = fa-order.discount1
        op-list.disc2 = fa-order.discount2
        op-list.vat = fa-order.vat
        disc = fa-order.discount1 / 100
        disc2 = fa-order.discount2 / 100
        vat = fa-order.vat / 100.
    END. 
    op-list.epreis0 = fa-order.order-price / (1 - disc) / (1 - disc2) / (1 + vat). 
    op-list.anzahl = op-list.anzahl + fa-order.order-qty. 
    op-list.warenwert = op-list.warenwert + fa-order.order-amount. 
    op-list.warenwert0 = op-list.warenwert0 
        + fa-order.order-amount / (1 - disc) / (1 - disc2) / (1 + vat). 
    tot-qty = tot-qty + fa-order.order-qty. 
  END. 
END.
