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
  FIELD userinit            AS CHAR FORMAT "x(2)"  LABEL "ID " 
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

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR s-list.
DEFINE INPUT PARAMETER lief-nr      AS INTEGER. 
DEFINE INPUT PARAMETER po-nr        AS CHAR. 
DEFINE INPUT PARAMETER billdate     AS DATE.
DEFINE INPUT PARAMETER user-init    AS CHAR.

FIND FIRST bediener WHERE bediener.userinit = user-init.
RUN update-slist.


PROCEDURE update-slist: 
DEFINE VARIABLE curr-pr AS CHAR INITIAL "". 
DEFINE buffer s-list1 FOR s-list. 
  
  curr-pr = "". 

  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = po-nr 
        NO-LOCK NO-ERROR. 
    FIND FIRST l-order WHERE l-order.artnr = s-list.artnr 
      AND l-order.lief-nr = lief-nr AND l-order.op-art = 2 
      AND l-order.docu-nr = po-nr NO-LOCK NO-ERROR. 

    IF AVAILABLE l-order THEN 
    DO: 
      s-list.po-nr = l-order.docu-nr. 
      FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid 
        EXCLUSIVE-LOCK. 
      IF AVAILABLE l-order THEN
      DO:
          l-order.lief-fax[2] = po-nr. 
          l-order.loeschflag = 1. 
          l-order.bestelldatum = billdate. 
          FIND CURRENT l-order NO-LOCK. 
          s-list.pchase-nr = l-order.lief-fax[2]. 
          s-list.pchase-date = billdate. 
          s-list.loeschflag = 1. 
      END.
      
      IF AVAILABLE l-orderhdr AND l-orderhdr.lief-fax[2] NE "" THEN 
      DO:
          
          IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
          DO:
              /*ITA 02/06/13 */
              IF NUM-ENTRIES(l-orderhdr.lief-fax[2], ";") GE 3 THEN
                  ASSIGN s-list.approved = YES. 
              ELSE ASSIGN s-list.approved = NO. 
              /*IF ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " " THEN
                  ASSIGN s-list.approved = YES. 
              ELSE ASSIGN s-list.approved = NO. */
          END.
          ELSE s-list.rejected = YES.
      END.

      IF curr-pr NE s-list.docu-nr THEN 
      DO: 
        curr-pr = s-list.docu-nr. 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        l-order.loeschflag = 1. 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.artnr = 0 AND s-list1.docu-nr 
          = s-list.docu-nr. 
        s-list1.loeschflag = 1. 
      END. 
    END. 
  END. 
  curr-pr = "". 

  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    IF curr-pr NE s-list.docu-nr THEN 
    DO: 
      curr-pr = s-list.docu-nr. 
      FIND FIRST l-order WHERE l-order.docu-nr = curr-pr AND l-order.artnr GT 0 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0 AND l-order.op-art = 1 
      AND l-order.lief-nr = 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-order THEN 
      DO: 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        ASSIGN
          l-order.loeschflag      = 1
          l-order.lieferdatum-eff = billdate 
          l-order.angebot-lief[3] = bediener.nr
        . 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.docu-nr = curr-pr 
          AND s-list1.artnr = 0. 
        ASSIGN
          s-list1.loeschflag  = 1
          s-list1.cdate       = billdate 
          s-list1.cid         = bediener.userinit
        . 
      END. 
    END. 
    s-list.selected = NO. 
    s-list.loeschflag = 1. 
  END. 
END. 

/*MT
PROCEDURE update-slist: 
DEFINE VARIABLE curr-pr AS CHAR INITIAL "". 
DEFINE buffer s-list1 FOR s-list. 
  
  curr-pr = "". 

  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = po-nr 
        NO-LOCK NO-ERROR. 
    FIND FIRST l-order WHERE l-order.artnr = s-list.artnr 
      AND l-order.lief-nr = lief-nr AND l-order.op-art = 2 
      AND l-order.docu-nr = po-nr NO-LOCK NO-ERROR. 

    IF AVAILABLE l-order THEN 
    DO: 
      s-list.po-nr = l-order.docu-nr. 
      FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid 
        EXCLUSIVE-LOCK. 
      IF AVAILABLE l-order THEN
      DO:
          l-order.lief-fax[2] = po-nr. 
          l-order.loeschflag = 1. 
          l-order.bestelldatum = billdate. 
          FIND CURRENT l-order NO-LOCK. 
          s-list.pchase-nr = l-order.lief-fax[2]. 
          s-list.pchase-date = billdate. 
          s-list.loeschflag = 1. 
      END.
      
      IF AVAILABLE l-orderhdr AND l-orderhdr.lief-fax[2] NE "" THEN 
      DO:
          
          IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
          DO:
              /*ITA 02/06/13 */
              IF NUM-ENTRIES(l-orderhdr.lief-fax[2], ";") GE 3 THEN
                  ASSIGN s-list.approved = YES. 
              ELSE ASSIGN s-list.approved = NO. 
              /*IF ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " " THEN
                  ASSIGN s-list.approved = YES. 
              ELSE ASSIGN s-list.approved = NO. */
          END.
          ELSE s-list.rejected = YES.
      END.

      IF curr-pr NE s-list.docu-nr THEN 
      DO: 
        curr-pr = s-list.docu-nr. 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        l-order.loeschflag = 1. 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.artnr = 0 AND s-list1.docu-nr 
          = s-list.docu-nr. 
        s-list1.loeschflag = 1. 
      END. 
    END. 
  END. 
  curr-pr = "". 

  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    IF curr-pr NE s-list.docu-nr THEN 
    DO: 
      curr-pr = s-list.docu-nr. 
      FIND FIRST l-order WHERE l-order.docu-nr = curr-pr AND l-order.artnr GT 0 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0 AND l-order.op-art = 1 
      AND l-order.lief-nr = 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-order THEN 
      DO: 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        ASSIGN
          l-order.loeschflag      = 1
          l-order.lieferdatum-eff = billdate 
          l-order.angebot-lief[3] = bediener.nr
        . 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.docu-nr = curr-pr 
          AND s-list1.artnr = 0. 
        ASSIGN
          s-list1.loeschflag  = 1
          s-list1.cdate       = billdate 
          s-list1.cid         = bediener.userinit
        . 
      END. 
    END. 
    s-list.selected = NO. 
    s-list.loeschflag = 1. 
  END. 
  
END. 

PROCEDURE update-slist: 
DEFINE INPUT PARAMETER lief-nr AS INTEGER. 
DEFINE INPUT PARAMETER po-nr AS CHAR. 
DEFINE VARIABLE curr-pr AS CHAR INITIAL "". 
DEFINE buffer s-list1 FOR s-list. 
  
  curr-pr = "". 
  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = po-nr 
        NO-LOCK NO-ERROR. 
    FIND FIRST l-order WHERE l-order.artnr = s-list.artnr 
      AND l-order.lief-nr = lief-nr AND l-order.op-art = 2 
      AND l-order.docu-nr = po-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-order THEN 
    DO: 
      s-list.po-nr = l-order.docu-nr. 
      FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid 
        EXCLUSIVE-LOCK. 
      IF AVAILABLE l-order THEN
      DO:
          l-order.lief-fax[2] = po-nr. 
          l-order.loeschflag = 1. 
          l-order.bestelldatum = billdate. 
          FIND CURRENT l-order NO-LOCK. 
          s-list.pchase-nr = l-order.lief-fax[2]. 
          s-list.pchase-date = billdate. 
          s-list.loeschflag = 1. 
      END.
 
      IF AVAILABLE l-orderhdr AND l-orderhdr.lief-fax[2] NE "" THEN 
      DO:
          IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
          DO:
              IF ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " " THEN
                  ASSIGN s-list.approved = YES. 
              ELSE ASSIGN s-list.approved = NO. 
          END.
          ELSE s-list.rejected = YES.
      END.

      IF curr-pr NE s-list.docu-nr THEN 
      DO: 
        curr-pr = s-list.docu-nr. 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        l-order.loeschflag = 1. 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.artnr = 0 AND s-list1.docu-nr 
          = s-list.docu-nr. 
        s-list1.loeschflag = 1. 
      END. 
    END. 
  END. 
  curr-pr = "". 
  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    IF curr-pr NE s-list.docu-nr THEN 
    DO: 
      curr-pr = s-list.docu-nr. 
      FIND FIRST l-order WHERE l-order.docu-nr = curr-pr AND l-order.artnr GT 0 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0 AND l-order.op-art = 1 
      AND l-order.lief-nr = 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-order THEN 
      DO: 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        ASSIGN
          l-order.loeschflag      = 1
          l-order.lieferdatum-eff = billdate 
          l-order.angebot-lief[3] = bediener.nr
        . 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.docu-nr = curr-pr 
          AND s-list1.artnr = 0. 
        ASSIGN
          s-list1.loeschflag  = 1
          s-list1.cdate       = billdate 
          s-list1.cid         = bediener.userinit
        . 
      END. 
    END. 
    s-list.selected = NO. 
    s-list.loeschflag = 1. 
  END.
END. 
*/
/*MT
PROCEDURE update-slist:
DEFINE VARIABLE curr-pr AS CHAR INITIAL "". 
DEFINE buffer s-list1 FOR s-list. 
  curr-pr = "". 
  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = po-nr 
        NO-LOCK NO-ERROR. 
    FIND FIRST l-order WHERE l-order.artnr = s-list.artnr 
      AND l-order.lief-nr = lief-nr AND l-order.op-art = 2 
      AND l-order.docu-nr = po-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-order THEN 
    DO: 
      s-list.po-nr = l-order.docu-nr. 
      FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid 
        EXCLUSIVE-LOCK. 
      IF AVAILABLE l-order THEN
      DO:
          l-order.lief-fax[2] = po-nr. 
          l-order.loeschflag = 1. 
          l-order.bestelldatum = billdate. 
          FIND CURRENT l-order NO-LOCK. 
          s-list.pchase-nr = l-order.lief-fax[2]. 
          s-list.pchase-date = billdate. 
          s-list.loeschflag = 1. 
      END.
 
      IF AVAILABLE l-orderhdr AND l-orderhdr.lief-fax[2] NE "" THEN 
      DO:
          IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
          DO:
              IF ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " 
                  AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " " THEN
                  ASSIGN s-list.approved = YES. 
              ELSE ASSIGN s-list.approved = NO. 
          END.
          ELSE s-list.rejected = YES.
      END.

      IF curr-pr NE s-list.docu-nr THEN 
      DO: 
        curr-pr = s-list.docu-nr. 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        l-order.loeschflag = 1. 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.artnr = 0 AND s-list1.docu-nr 
          = s-list.docu-nr. 
        s-list1.loeschflag = 1. 
      END. 
    END. 
  END. 
  curr-pr = "". 
  FOR EACH s-list WHERE s-list.selected AND s-list.artnr GT 0 
    BY s-list.docu-nr: 
    IF curr-pr NE s-list.docu-nr THEN 
    DO: 
      curr-pr = s-list.docu-nr. 
      FIND FIRST l-order WHERE l-order.docu-nr = curr-pr AND l-order.artnr GT 0 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0 AND l-order.op-art = 1 
      AND l-order.lief-nr = 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-order THEN 
      DO: 
        FIND FIRST l-order WHERE l-order.docu-nr = curr-pr 
          AND l-order.pos = 0 EXCLUSIVE-LOCK. 
        ASSIGN
          l-order.loeschflag      = 1
          l-order.lieferdatum-eff = billdate 
          l-order.angebot-lief[3] = bediener.nr
        . 
        FIND CURRENT l-order NO-LOCK. 
        FIND FIRST s-list1 WHERE s-list1.docu-nr = curr-pr 
          AND s-list1.artnr = 0. 
        ASSIGN
          s-list1.loeschflag  = 1
          s-list1.cdate       = billdate 
          s-list1.cid         = bediener.userinit
        . 
      END. 
    END. 
    s-list.selected = NO. 
    s-list.loeschflag = 1. 
  END.
END. 
*/
