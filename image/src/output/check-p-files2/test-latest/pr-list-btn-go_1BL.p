
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
  FIELD currNo              AS INT /*Alder - Serverless - Issue 824*/
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
  FIELD einzelpreis         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
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
  /* FIELD avg-pprice          LIKE l-artikel.vk-preis Add by Michael @ 08/05/2019 for Luxton Cirebon request - ticket no C071EE */
  FIELD desc-coa            AS CHARACTER FORMAT "x(20)"
  FIELD lief-fax3           LIKE l-orderhdr.lief-fax[3]
  FIELD masseinheit         LIKE l-artikel.masseinheit
  FIELD lief-fax-2          LIKE l-order.lief-fax[2]  
  FIELD ek-letzter          AS DECIMAL
  FIELD supplier            AS CHARACTER
  FIELD vk-preis            LIKE l-artikel.vk-preis      /* Average Price Gerald 210220 */
  FIELD a-firma             LIKE l-lieferant.firma   /*gerald last-supplier*/
  FIELD last-pbook    AS DECIMAL FORMAT "->>,>>>,>>9.99" /*gerald last-purchase based pbook*/
  .

DEF INPUT-OUTPUT PARAMETER po-nr AS CHAR.
DEF INPUT-OUTPUT PARAMETER pr-nr AS CHAR.
DEF INPUT-OUTPUT PARAMETER curr-dept AS INT.
DEF INPUT-OUTPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER po-type AS INT.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.

DEFINE BUFFER s-list1 FOR s-list.
DEFINE BUFFER l-od1   FOR l-order.
DEFINE BUFFER l-odhdr FOR l-orderhdr.
DEFINE BUFFER bod     FOR l-order.

DEFINE VARIABLE curr-pos  AS INTEGER INITIAL 0.
DEFINE VARIABLE temp-nr AS CHAR.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FOR EACH s-list1 WHERE s-list1.selected = YES AND s-list1.artnr GT 0 
    BY s-list1.docu-nr:
    
    IF pr-nr = "" THEN 
    DO: 
      pr-nr = s-list1.docu-nr.
      temp-nr =  s-list1.docu-nr. /* Add By Gerald TIKET D37393 231219*/

      IF po-type = 1 THEN 
      DO:
        RUN get-ponum(lief-nr, pr-nr, OUTPUT po-nr). 
        CREATE l-orderhdr.
        ASSIGN
            l-orderhdr.lief-nr  = lief-nr
            l-orderhdr.docu-nr  = po-nr
            l-orderhdr.angebot-lief[3] = s-list1.currno /*M 060612 -> using currency from pr */ /*Alder - Serverless - Issue 824*/
         .
        FIND CURRENT l-orderhdr NO-LOCK.
      END.
    END. 
    /* Add By Gerald TIKET D37393 231219*/
    ELSE 
    DO:
      IF temp-nr NE s-list1.docu-nr THEN DO:
          pr-nr = pr-nr + " | " + s-list1.docu-nr. 
          temp-nr = s-list1.docu-nr.
    
          IF po-type = 1 THEN 
          DO:
             
            FIND FIRST bod WHERE bod.docu-nr = po-nr
                AND bod.pos = 0 
                AND bod.bestelldatum = billdate 
                AND bod.lief-nr = lief-nr
                AND bod.op-art = 2      
                AND bod.betriebsnr = 2 NO-LOCK NO-ERROR.
            IF AVAILABLE bod THEN DO:
                FIND CURRENT bod EXCLUSIVE-LOCK.
                ASSIGN bod.lief-fax[1] = pr-nr.
                FIND CURRENT bod NO-LOCK.
                RELEASE bod.
            END.

            /*RUN get-ponum(lief-nr, pr-nr, OUTPUT po-nr). 
          
            CREATE l-orderhdr.
            ASSIGN
                l-orderhdr.lief-nr  = lief-nr
                l-orderhdr.docu-nr  = po-nr
                l-orderhdr.angebot-lief[3] = s-list1.currNo /*M 060612 -> using currency from pr */            
             .
            FIND CURRENT l-orderhdr NO-LOCK.*/
          END.
      END.      
    END.

    /*end additional*/
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-list1.artnr NO-LOCK. 
    FIND FIRST l-od1 WHERE RECID(l-od1) = s-list1.s-recid 
      NO-LOCK. 
    IF curr-dept = 0 THEN 
    DO:    
      FIND FIRST l-odhdr WHERE l-odhdr.docu-nr 
        = l-od1.docu-nr AND l-odhdr.betriebsnr GE 9 
        AND l-odhdr.lief-nr = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE l-odhdr THEN curr-dept = l-odhdr.angebot-lief[1]. 
    END.
    FIND FIRST l-order WHERE l-order.artnr = s-list1.artnr 
      AND l-order.op-art = 2 AND l-order.bestelldatum = billdate 
      AND l-order.docu-nr = po-nr 
      AND l-order.stornogrund = s-list1.konto NO-LOCK NO-ERROR. 
        
    IF AVAILABLE l-order THEN 
    DO: 
      FIND CURRENT l-order EXCLUSIVE-LOCK.
      l-order.anzahl = l-order.anzahl + s-list1.qty. 
      l-order.warenwert = l-order.anzahl * l-order.einzelpreis. 
      FIND CURRENT l-order NO-LOCK. 
    END.
    ELSE 
    DO: 
      curr-pos = curr-pos + 1. 
      CREATE l-order. 
      /*M 060612 -> using price from pr if not 0 */
      IF s-list1.duprice EQ 0 THEN
          l-order.einzelpreis  = l-artikel.ek-aktuell * l-artikel.lief-einheit.
      ELSE l-order.einzelpreis  = s-list1.duprice.
      ASSIGN 
          l-order.artnr        = s-list1.artnr 
          l-order.anzahl       = s-list1.qty 
          l-order.txtnr        = l-artikel.lief-einheit 
          l-order.pos          = curr-pos 
          l-order.bestelldatum = billdate 
          l-order.op-art       = 2 
          l-order.docu-nr      = po-nr 
          l-order.lief-nr      = lief-nr 
          l-order.lief-fax[1]  = bediener.username 
          l-order.flag         = YES 
          l-order.betriebsnr   = 2 
          l-order.stornogrund  = s-list1.konto 
          l-order.angebot-lief[3] = s-list1.currno /*M 060612 -> using currency from pr */ /*Alder - Serverless - Issue 824*/
          l-order.warenwert    = l-order.anzahl * l-order.einzelpreis
          l-order.besteller    = s-list1.instruct
          l-order.zeit         = s-list1.zeit
          l-order.lief-fax[3] = l-artikel.traubensorte. /*Alder - Serverless - Issue 824*/
      
      FIND FIRST gl-acct WHERE gl-acct.fibukonto  = l-order.stornogrund NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 824*/
      IF AVAILABLE gl-acct THEN
      DO:
          ASSIGN
            /*s-list.konto       = l-order.stornogrund + ";" + gl-acct.bezeich
            s-list.stornogrund = l-order.stornogrund + ";" + gl-acct.bezeich*/
            s-list1.desc-coa    = gl-acct.bezeich. /*Alder - Serverless - Issue 824*/
      END.
      /* Add by Michael @ 08/05/2019 for Luxton Cirebon request - ticket no C071EE */
      /*MESSAGE l-artikel.vk-preis VIEW-AS ALERT-BOX INFO.
      ASSIGN s-list.avg-pprice = l-artikel.vk-preis.*/
      /* End of add */
      FIND CURRENT l-order NO-LOCK. 
    END. 
END. 

PROCEDURE get-ponum: 
DEFINE INPUT PARAMETER lief-nr AS INTEGER. 
DEFINE INPUT PARAMETER pr AS CHAR. 
DEFINE OUTPUT PARAMETER docu-nr AS CHAR FORMAT "x(11)". 
DEFINE buffer l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
  s = "P" + SUBSTR(STRING(year(billdate)),3,2) + STRING(month(billdate), "99") 
     + STRING(day(billdate), "99"). 
  FOR EACH l-orderhdr1 WHERE l-orderhdr1.bestelldatum = billdate 
    AND l-orderhdr1.betriebsnr LE 1 
    AND l-orderhdr1.docu-nr MATCHES "P*" NO-LOCK BY l-orderhdr1.docu-nr descending: 
    i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,8,3)). 
    i = i + 1. 
    docu-nr = s + STRING(i, "999"). 
    create l-order. 
    ASSIGN 
      l-order.docu-nr = docu-nr 
      l-order.pos = 0 
      l-order.bestelldatum = billdate 
      l-order.lief-nr = lief-nr 
      l-order.op-art = 2 
      l-order.lief-fax[1] = pr 
      l-order.betriebsnr = 2. 
    RETURN. 
  END. 
  docu-nr = s + STRING(i, "999"). 
  create l-order. 
  ASSIGN 
      l-order.docu-nr = docu-nr 
      l-order.pos = 0 
      l-order.bestelldatum = billdate 
      l-order.lief-nr = lief-nr 
      l-order.op-art = 2 
      l-order.lief-fax[1] = pr 
      l-order.betriebsnr = 2. 
  RETURN. 
END. 

