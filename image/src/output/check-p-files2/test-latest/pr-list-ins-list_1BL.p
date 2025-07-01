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
  FIELD a-firma             LIKE l-lieferant.firma    /*gerald last-supplier*/
  FIELD last-pbook    AS DECIMAL FORMAT "->>,>>>,>>9.99" /*gerald last-purchase based pbook*/
  .

DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.
DEFINE INPUT PARAMETER docu-nr AS CHAR. 

RUN ins-list.

FOR EACH s-list:
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = s-list.docu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-orderhdr THEN
    DO:
        ASSIGN 
            s-list.lief-fax2 = l-orderhdr.lief-fax[2]
            s-list.lief-fax3 = l-orderhdr.lief-fax[3].
    END.
END.

PROCEDURE ins-list: 
DEFINE VARIABLE nr AS INTEGER. 
DEFINE buffer usr FOR bediener. 
  
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.lief-nr = 0 AND l-order.pos GT 0 NO-LOCK: 
    nr = RECID(l-order). 
    FIND FIRST s-list WHERE s-list.s-recid = nr NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO:
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK. 
      FIND FIRST usr WHERE usr.username = l-order.lief-fax[1] NO-LOCK. 
      create s-list. 
      ASSIGN 
        s-list.s-recid          = RECID(l-order) 
        s-list.docu-nr          = l-order.docu-nr 
        s-list.pos              = l-order.pos
        s-list.artnr            = l-artikel.artnr 
        s-list.bezeich          = l-artikel.bezeich 
        s-list.qty              = l-order.anzahl 
        s-list.dunit            = l-artikel.traubensort 
        s-list.lief-einheit     = l-artikel.lief-einheit 
        s-list.pchase-date      = l-order.bestelldatum 
        s-list.konto            = l-order.stornogrund 
        s-list.userinit         = usr.userinit
        s-list.instruct         = l-order.besteller 
        /*M 04/06/12 -> show item based on selected supplier */
        s-list.supNo            = l-order.angebot-lief[2] 
        s-list.currNo           = l-order.angebot-lief[3]
        s-list.duprice          = l-order.einzelpreis

        s-list.anzahl           = l-order.anzahl
        s-list.txtnr            = l-order.txtnr
        s-list.einzelpreis      = l-order.einzelpreis
        s-list.zeit             = l-order.zeit
        s-list.masseinheit      = l-artikel.masseinheit
        s-list.lief-fax-2       = l-order.lief-fax[2]
        s-list.vk-preis         = l-artikel.vk-preis.

      IF l-order.bestellart NE "" THEN
      DO:
          ASSIGN
              s-list.du-price1        = INT(ENTRY(2,ENTRY(1, l-order.bestellart , "-"),";"))/ 100
              s-list.du-price2        = INT(ENTRY(2,ENTRY(2, l-order.bestellart , "-"),";")) / 100
              s-list.du-price3        = INT(ENTRY(2,ENTRY(3, l-order.bestellart , "-"),";")) / 100
              s-list.supp1            = INT(ENTRY(1,ENTRY(1, l-order.bestellart , "-"),";"))
              s-list.supp2            = INT(ENTRY(1,ENTRY(2, l-order.bestellart , "-"),";"))
              s-list.supp3            = INT(ENTRY(1,ENTRY(3, l-order.bestellart , "-"),";")).
      END.

      
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp1 NO-LOCK NO-ERROR.
      IF AVAILABLE l-lieferant THEN
        s-list.suppn1 = l-lieferant.firma.
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp2 NO-LOCK NO-ERROR.
      IF AVAILABLE l-lieferant THEN
        s-list.suppn2 = l-lieferant.firma.
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp3 NO-LOCK NO-ERROR.
      IF AVAILABLE l-lieferant THEN
        s-list.suppn3 = l-lieferant.firma.
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supNo NO-LOCK NO-ERROR.
      IF AVAILABLE l-lieferant THEN
        s-list.supps = l-lieferant.firma.

      IF l-order.anzahl NE 0 THEN s-list.str3 
        = STRING(l-order.anzahl,">>>,>>9.99"). 
      IF l-artikel.lief-einheit NE 0 THEN s-list.str4 
        = STRING(l-artikel.lief-einheit,">>,>>9"). 
      IF l-order.lieferdatum NE ? THEN 
        s-list.lieferdatum = STRING(l-order.lieferdatum). 
    END. 
  END.
END. 

/*MT
PROCEDURE ins-list:
DEFINE VARIABLE nr AS INTEGER. 
DEFINE buffer usr FOR bediener. 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.lief-nr = 0 AND l-order.pos GT 0 NO-LOCK: 
    nr = RECID(l-order). 
    FIND FIRST s-list WHERE s-list.s-recid = nr NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK. 
      FIND FIRST usr WHERE usr.username = l-order.lief-fax[1] NO-LOCK. 
      create s-list. 
      ASSIGN 
        s-list.s-recid          = RECID(l-order) 
        s-list.docu-nr          = l-order.docu-nr 
        s-list.pos              = l-order.pos
        s-list.artnr            = l-artikel.artnr 
        s-list.bezeich          = l-artikel.bezeich 
        s-list.qty              = l-order.anzahl 
        s-list.dunit            = l-artikel.traubensort 
        s-list.lief-einheit     = l-artikel.lief-einheit 
        s-list.pchase-date      = l-order.bestelldatum 
        s-list.konto            = l-order.stornogrund 
        s-list.userinit         = usr.userinit
      . 
      IF l-order.anzahl NE 0 THEN s-list.str3 
        = STRING(l-order.anzahl,">>>,>>9.99"). 
      IF l-artikel.lief-einheit NE 0 THEN s-list.str4 
        = STRING(l-artikel.lief-einheit,">>,>>9"). 
      IF l-order.lieferdatum NE ? THEN 
        s-list.lieferdatum = STRING(l-order.lieferdatum). 
    END. 
  END.
END. 
*/
