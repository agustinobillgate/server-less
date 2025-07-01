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
  FIELD app-rej             AS CHAR FORMAT "x(60)" LABEL "Approve/Reject" 
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
  FIELD del-reason          AS CHAR LABEL "Delete Reason" FORMAT "x(32)"
  FIELD desc-coa            AS CHARACTER FORMAT "x(20)"
  FIELD lief-fax3           LIKE l-orderhdr.lief-fax[3]
  FIELD masseinheit         LIKE l-artikel.masseinheit
  FIELD lief-fax-2          LIKE l-order.lief-fax[2]
  FIELD ek-letzter          AS DECIMAL
  FIELD supplier            AS CHARACTER
  FIELD vk-preis            LIKE l-artikel.vk-preis      /* Average Price Gerald 210220 */
  FIELD a-firma             LIKE l-lieferant.firma      /*gerald last-supplier*/
  /* FIELD avg-pprice       LIKE l-artikel.vk-preis             Add by Michael @ 09/05/2019 for Luxton Cirebon request - ticket no C071EE */
  FIELD last-pbook    AS DECIMAL FORMAT "->>,>>>,>>9.99" /*gerald last-purchase based pbook*/
  .

DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER docu-nr AS CHAR.

RUN update-list.

PROCEDURE update-list:
DEFINE VARIABLE nr AS INTEGER. 
  FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK. 
  nr = RECID(l-orderhdr). 
  FIND FIRST s-list WHERE s-list.s-recid = nr. 
  s-list.lieferdatum = STRING(l-orderhdr.lieferdatum). 
  s-list.instruct = l-orderhdr.lief-fax[3]. 
  FOR EACH s-list WHERE s-list.docu-nr = docu-nr AND s-list.artnr GT 0: 
    FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid NO-LOCK. 
    s-list.qty  = l-order.anzahl.
    s-list.zeit = l-order.zeit. 
    IF l-order.anzahl NE 0 THEN s-list.str3 
      = STRING(l-order.anzahl,">>>,>>9.99"). 
    s-list.konto = l-order.stornogrund.
    s-list.approved = l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") = 0 
        AND ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " "
        AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " " . 
    s-list.rejected = l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") > 0. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto  = l-order.stornogrund NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
        s-list.konto       = l-order.stornogrund /*+ ";" + gl-acct.bezeich*/.
        s-list.stornogrund = l-order.stornogrund /*+ ";" + gl-acct.bezeich*/.
    END.
  END. 
  IF l-orderhdr.lief-fax[2] NE "" THEN 
  DO: 
      FIND FIRST s-list WHERE s-list.docu-nr = docu-nr AND s-list.artnr = 0. 
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

  IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
    DO:
        IF ENTRY(1, l-orderhdr.lief-fax[2], ";") EQ " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") EQ " "
            AND ENTRY(3, l-orderhdr.lief-fax[2], ";") EQ " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") EQ " " THEN
            ASSIGN s-list.app-rej   = "".
        /*ELSE s-list.app-rej         = ENTRY(1, ENTRY(1, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                      ENTRY(1, ENTRY(2, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                      ENTRY(1, ENTRY(3, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                      ENTRY(1, ENTRY(4, l-orderhdr.lief-fax[2], ";"), " ")  .*/

        ELSE s-list.app-rej         = ENTRY(1, l-orderhdr.lief-fax[2], ";") + ";" +
                                      ENTRY(2, l-orderhdr.lief-fax[2], ";") + ";" +
                                      ENTRY(3, l-orderhdr.lief-fax[2], ";") + ";" +
                                      ENTRY(4, l-orderhdr.lief-fax[2], ";")  .
        /*MESSAGE SUBSTRING(ENTRY(1, l-orderhdr.lief-fax[2], ";"),1,2)
            VIEW-AS ALERT-BOX INFO BUTTONS OK.*/

    END.
    IF INDEX(l-orderhdr.lief-fax[2],"|") > 0 THEN
    ASSIGN  s-list.rej-reason = TRIM(ENTRY(3, l-orderhdr.lief-fax[2], "|"))
            s-list.app-rej    = TRIM(ENTRY (4, ENTRY(1, l-orderhdr.lief-fax[2], "|"), ";"))
            .
END. 

/*MT
PROCEDURE update-list: 
DEFINE VARIABLE nr AS INTEGER. 
  /*MTCLOSE QUERY q2.*/
  FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK. 
  nr = RECID(l-orderhdr). 
  FIND FIRST s-list WHERE s-list.s-recid = nr. 
  s-list.lieferdatum = STRING(l-orderhdr.lieferdatum). 
  s-list.instruct = l-orderhdr.lief-fax[3]. 
  FOR EACH s-list WHERE s-list.docu-nr = docu-nr AND s-list.artnr GT 0: 
    FIND FIRST l-order WHERE RECID(l-order) = s-list.s-recid NO-LOCK. 
    s-list.qty = l-order.anzahl. 
    IF l-order.anzahl NE 0 THEN s-list.str3 
      = STRING(l-order.anzahl,">>>,>>9.99"). 
    s-list.konto = l-order.stornogrund. 
    s-list.approved = l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") = 0 
        AND ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " "
        AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " " . 
    s-list.rejected = l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") > 0. 
  END. 
  IF l-orderhdr.lief-fax[2] NE "" THEN 
  DO: 
      FIND FIRST s-list WHERE s-list.docu-nr = docu-nr AND s-list.artnr = 0. 
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
  /*MTRUN disp-it.*/
END. 
*/
