/*ITA 020514 --> penambahan validasi ketika menghapus pr*/

DEFINE TEMP-TABLE s-list 
  FIELD selected            AS LOGICAL INITIAL NO 
  FIELD flag                AS LOGICAL INITIAL NO
  FIELD loeschflag          AS INTEGER INITIAL 0 
  FIELD approved            AS LOGICAL INITIAL NO 
  FIELD rejected            AS LOGICAL INITIAL NO
  FIELD s-recid             AS INTEGER 
  FIELD docu-nr             AS CHAR 
  FIELD po-nr               AS CHAR 
  FIELD deptnr              AS INTEGER 
  FIELD str0                AS CHAR FORMAT "x(10)" LABEL "PR-Number" 
  FIELD bestelldatum        AS CHAR FORMAT "x(8)"  LABEL "IssuDate" 
  FIELD lieferdatum         AS CHAR FORMAT "x(8)"  LABEL "Required" 
  FIELD pos                 AS INTEGER INITIAL 999999
  FIELD artnr               AS INTEGER FORMAT ">>>>>>>" LABEL "ArtNo" 
  FIELD bezeich             AS CHAR FORMAT "x(33)" LABEL "Description" 
  FIELD qty                 AS DECIMAL FORMAT ">>>,>>9.99" 
  FIELD str3                AS CHAR FORMAT "x(10)" LABEL "  Quantity" 
  FIELD dunit               AS CHAR FORMAT "x(6)"  LABEL "D-Unit" 
  FIELD lief-einheit        AS DECIMAL 
  FIELD str4                AS CHAR FORMAT "x(6)"  LABEL " Cont." 
  FIELD userinit            AS CHAR FORMAT "x(3)"  LABEL "ID " 
  FIELD pchase-nr           AS CHAR FORMAT "x(10)" LABEL "PO-Number" 
  FIELD pchase-date         AS DATE LABEL "Date" 
  FIELD app-rej             AS CHAR FORMAT "x(14)" LABEL "Approve/Reject" 
  FIELD rej-reason          AS CHAR FORMAT "x(36)" LABEL "Reject Reason"
  FIELD cid                 AS CHAR FORMAT "x(3)"  LABEL "CID"
  FIELD cdate               AS DATE                LABEL "CancDate"
  FIELD instruct            AS CHAR FORMAT "x(36)" LABEL "Remark"
  FIELD konto               LIKE gl-acct.fibukonto 
  /*M 04/06/12 -> show item based on selected supplier */
  FIELD supNo               AS INT 
  FIELD currNo              AS INT
  FIELD duprice             AS DEC
  FIELD du-price1           AS DEC
  FIELD du-price2           AS DEC
  FIELD du-price3           AS DEC
  FIELD anzahl              AS INT
  FIELD txtnr               LIKE l-order.txtnr
  FIELD suppn1              AS CHAR FORMAT "x(30)"
  FIELD supp1               AS INT
  FIELD suppn2              AS CHAR FORMAT "x(30)"
  FIELD supp2               AS INT
  FIELD suppn3              AS CHAR FORMAT "x(30)"
  FIELD supp3               AS INT
  FIELD supps               AS CHAR
  FIELD einzelpreis         AS DECIMAL
  FIELD amount              LIKE l-order.warenwert
  FIELD stornogrund         LIKE l-order.stornogrund
  FIELD besteller           LIKE l-order.besteller
  FIELD lief-fax2           LIKE l-orderhdr.lief-fax[2]
  FIELD last-pdate          AS DATE
  FIELD last-pprice         AS DECIMAL FORMAT "->>,>>>,>>9.99"
  /*wen 160318*/            
  FIELD zeit                LIKE l-order.zeit  
  FIELD min-bestand         LIKE l-artikel.min-bestand 
  FIELD max-bestand         LIKE l-artikel.anzverbrauch
  FIELD del-reason          AS CHAR
  FIELD desc-coa            AS CHARACTER FORMAT "x(20)"
  FIELD lief-fax3           LIKE l-orderhdr.lief-fax[3]
  FIELD masseinheit         LIKE l-artikel.masseinheit
  FIELD lief-fax-2          LIKE l-order.lief-fax[2]
  FIELD ek-letzter          AS DECIMAL                
  FIELD supplier            AS CHARACTER
  FIELD vk-preis            LIKE l-artikel.vk-preis      /* Average Price Gerald 210220 */
  FIELD a-firma             LIKE l-lieferant.firma      /*gerald last-supplier*/
  FIELD last-pbook    AS DECIMAL FORMAT "->>,>>>,>>9.99" /*gerald last-purchase based pbook*/
  .

DEF INPUT  PARAMETER TABLE FOR s-list.
DEF INPUT  PARAMETER s-list-artnr AS INT.
DEF INPUT  PARAMETER billdate  AS DATE.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER del-cur-row AS LOGICAL INIT NO.

DEFINE VARIABLE docu-nr AS CHAR. 
DEFINE buffer s1-list FOR s-list.


/*ITA 270318*/
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
FIND FIRST s-list WHERE s-list.artnr = s-list-artnr NO-LOCK NO-ERROR. /*ITA 020514*/
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = s-list.docu-nr NO-LOCK NO-ERROR.
IF AVAILABLE l-orderhdr THEN DO:
    FIND CURRENT l-orderhdr EXCLUSIVE-LOCK.
    ASSIGN l-orderhdr.lief-fax[3] = l-orderhdr.lief-fax[3] + "-" +  user-init + ";" + s-list.del-reason.
    FIND CURRENT l-orderhdr NO-LOCK.
    RELEASE l-orderhdr.
END.

IF s-list-artnr = 0 THEN 
DO: 
    docu-nr = s-list.docu-nr. 
    FIND FIRST l-order WHERE l-order.lief-nr = 0 
      AND l-order.pos = 0 AND l-order.artnr = 0 
      AND l-order.docu-nr = docu-nr EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE l-order THEN
    DO:
      CREATE l-order.
      ASSIGN l-order.docu-nr = docu-nr.
    END.
    ASSIGN
        l-order.loeschflag      = 2
        l-order.lieferdatum-eff = billdate 
        l-order.angebot-lief[3] = bediener.nr
    .
    FIND CURRENT l-order NO-LOCK. 
    
    
    FOR EACH s1-list WHERE s1-list.docu-nr = docu-nr:
      IF s1-list.artnr GT 0 THEN 
      DO: 
        FIND FIRST l-order WHERE RECID(l-order) = s1-list.s-recid 
          EXCLUSIVE-LOCK. 
        ASSIGN
          l-order.loeschflag      = 2
          l-order.lieferdatum-eff = billdate 
          l-order.angebot-lief[3] = bediener.nr
        . 
        FIND CURRENT l-order NO-LOCK.
      END. 
      ASSIGN
        s1-list.loeschflag = 2
        s1-list.cid        = bediener.username
        s1-list.cdate      = billdate
      .
    END.
    RETURN NO-APPLY. 
END. 
ELSE 
DO: 
    docu-nr = s-list.docu-nr. 
    s-list.loeschflag = 2.
    
    FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid EXCLUSIVE-LOCK. 
    ASSIGN
      l-order.loeschflag      = 2
      l-order.lieferdatum-eff = billdate 
      l-order.angebot-lief[3] = bediener.nr
    . 
    FIND CURRENT l-order NO-LOCK.
    FIND FIRST s1-list WHERE s1-list.docu-nr = docu-nr 
      AND s1-list.artnr GT 0 AND s1-list.loeschflag LE 1 NO-ERROR. 
    IF NOT AVAILABLE s1-list THEN 
    DO: 
      FIND FIRST l-order WHERE l-order.lief-nr = 0 
        AND l-order.pos = 0 AND l-order.artnr = 0 
        AND l-order.docu-nr = docu-nr EXCLUSIVE-LOCK. 
      ASSIGN
        l-order.loeschflag      = 2
        l-order.lieferdatum-eff = billdate 
        l-order.angebot-lief[3] = bediener.nr
      . 
      FIND CURRENT l-order NO-LOCK.
      RETURN NO-APPLY. 
    END.
    ELSE del-cur-row = YES.
    
END. 
