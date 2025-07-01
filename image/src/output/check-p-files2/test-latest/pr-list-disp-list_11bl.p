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

DEFINE BUFFER   usrbuff    FOR bediener.
DEFINE BUFFER t-lieferant FOR l-lieferant.

DEF INPUT  PARAMETER char1          AS CHAR.
DEF INPUT  PARAMETER billdate       AS DATE.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER outstand-flag  AS LOGICAL.
DEF INPUT  PARAMETER expired-flag   AS LOGICAL.
DEF INPUT  PARAMETER approve-flag   AS LOGICAL.
DEF INPUT  PARAMETER reject-flag    AS LOGICAL.
DEF INPUT  PARAMETER artnumber      AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR s-list.

RUN disp-list(char1).

FOR EACH s-list:
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = s-list.docu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-orderhdr THEN
    DO:
        ASSIGN 
            s-list.lief-fax2 = l-orderhdr.lief-fax[2]
            s-list.lief-fax3 = l-orderhdr.lief-fax[3].
    END.
END.

PROCEDURE disp-list: 
DEFINE INPUT PARAMETER pr-nr AS CHAR. 
DEFINE VARIABLE app-flag     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE rej-flag     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE rej-reason   AS CHAR INITIAL "".
DEFINE VARIABLE do-it        AS LOGICAL NO-UNDO.
DEFINE BUFFER usr   FOR bediener. 
DEFINE BUFFER sbuff FOR s-list.
DEFINE BUFFER tbuff FOR s-list.
    
  IF pr-nr NE "" THEN 
  DO: 
    FIND FIRST l-orderhdr WHERE l-orderhdr.betriebsnr GE 9 
      AND l-orderhdr.docu-nr = pr-nr AND l-orderhdr.bestelldatum = billdate 
      AND l-orderhdr.lief-nr = 0 NO-LOCK. 
    app-flag = (l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") = 0) 
        AND ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " " 
        AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " ". 
    rej-flag = (l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") > 0). 
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
      AND parameters.section = "Name" 
      AND INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] 
        NO-LOCK NO-ERROR. 
    FIND FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
      AND l-order.pos = 0 AND l-order.lief-nr = 0 NO-LOCK NO-ERROR. 
    /*FIND LAST l-op WHERE l-op.op-art = 1 NO-LOCK NO-ERROR.
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR.*/
    CREATE s-list. 
    IF AVAILABLE parameters THEN s-list.bezeich = parameters.vstring. 
    ASSIGN 
        s-list.pos              = 0
        s-list.s-recid          = RECID(l-orderhdr) 
        s-list.docu-nr          = l-orderhdr.docu-nr 
        s-list.str0             = l-orderhdr.docu-nr 
        s-list.deptnr           = l-orderhdr.angebot-lief[1] 
        s-list.bestelldatum     = STRING(l-orderhdr.bestelldatum) 
        s-list.lieferdatum      = STRING(l-orderhdr.lieferdatum) 
        s-list.approved         = app-flag 
        s-list.rejected         = rej-flag
        /*s-list.last-pdate       = l-op.datum
        s-list.last-pprice      = l-artikel.ek-letzter*/.

    IF NUM-ENTRIES(l-orderhdr.lief-fax[3], "-") GT 1 THEN DO:
        ASSIGN s-list.del-reason = ENTRY(2, l-orderhdr.lief-fax[3], "-")
               s-list.instruct   = ENTRY(1, l-orderhdr.lief-fax[3], "-").
    END.
    ELSE s-list.instruct   = l-orderhdr.lief-fax[3].

    IF l-orderhdr.betriebsnr EQ 10 THEN s-list.flag = YES.
    IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
    DO:
        IF ENTRY(1, l-orderhdr.lief-fax[2], ";") EQ " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") EQ " "
            AND ENTRY(3, l-orderhdr.lief-fax[2], ";") EQ " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") EQ " " THEN
            ASSIGN s-list.app-rej   = "".
        ELSE s-list.app-rej         = ENTRY(1, ENTRY(1, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                      ENTRY(1, ENTRY(2, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                      ENTRY(1, ENTRY(3, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                      ENTRY(1, ENTRY(4, l-orderhdr.lief-fax[2], ";"), " ")  .
    END.
    IF INDEX(l-orderhdr.lief-fax[2],"|") > 0 THEN
    ASSIGN  
        s-list.rej-reason = TRIM(ENTRY(3, l-orderhdr.lief-fax[2], "|"))
        s-list.app-rej    = TRIM(ENTRY(4, ENTRY(1, l-orderhdr.lief-fax[2], "|"), ";")).

    IF AVAILABLE l-order THEN s-list.loeschflag = l-order.loeschflag. 
 
    /*FOR EACH l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
      AND l-order.loeschflag LE 1 AND l-order.pos GT 0 
      AND l-order.lief-nr = 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK BY l-artikel.bezeich: */

    FIND FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
      AND l-order.loeschflag LE 1 AND l-order.pos GT 0 
      AND l-order.lief-nr = 0 USE-INDEX order_ix NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-order:
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE l-artikel THEN 
      DO:  
        FIND FIRST usr WHERE usr.username = l-order.lief-fax[1] NO-LOCK.           
        CREATE s-list. 
        ASSIGN 
            s-list.s-recid        = RECID(l-order) 
            s-list.deptnr         = l-orderhdr.angebot-lief[1] 
            s-list.docu-nr        = l-order.docu-nr 
            s-list.po-nr          = l-order.lief-fax[2] 
            s-list.pos            = l-order.pos
            s-list.artnr          = l-artikel.artnr 
            s-list.bezeich        = l-artikel.bezeich 
            s-list.qty            = l-order.anzahl 
            s-list.dunit          = l-artikel.traubensort 
            s-list.lief-einheit   = l-artikel.lief-einheit 
            s-list.approved       = app-flag 
            s-list.rejected       = rej-flag
            s-list.loeschflag     = l-order.loeschflag 
            s-list.userinit       = usr.userinit 
            s-list.pchase-nr      = l-order.lief-fax[2] 
            s-list.konto          = l-order.stornogrund 
            s-list.pchase-date    = l-order.bestelldatum
            s-list.cdate          = l-order.lieferdatum-eff
            s-list.instruct       = l-order.besteller 
            /*M 04/06/12 -> show item based on selected supplier */
            s-list.supNo          = l-order.angebot-lief[2] 
            s-list.currNo         = l-order.angebot-lief[3]
            s-list.duprice        = l-order.einzelpreis
            s-list.amount         = l-order.warenwert /*sis 2801115*/
            s-list.anzahl         = l-order.anzahl
            s-list.txtnr          = l-order.txtnr
            s-list.einzelpreis    = l-order.einzelpreis
            /*wen*/
            s-list.zeit           = l-order.zeit
            s-list.min-bestand    = l-artikel.min-bestand 
            s-list.max-bestand    = l-artikel.anzverbrauch
            s-list.masseinheit    = l-artikel.masseinheit
            s-list.lief-fax2      = l-order.lief-fax[2]
            s-list.last-pprice    = l-artikel.ek-letzter.
        
        /*FIND LAST l-op WHERE l-op.op-art = 1 AND l-op.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-op THEN 
              ASSIGN s-list.last-pdate     = l-op.datum*/
                     
    
        /*gerald last purchase and last date purchase*/            
        /*FIND LAST l-pprice WHERE l-pprice.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-pprice THEN 
        DO:
            FIND FIRST t-lieferant WHERE t-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK NO-ERROR.
            ASSIGN s-list.last-pdate  = l-pprice.bestelldatum
                   s-list.last-pbook  = l-pprice.einzelpreis
                   s-list.a-firma     = t-lieferant.firma.
        END.*/
    
        FOR EACH l-pprice WHERE l-pprice.artnr = l-artikel.artnr NO-LOCK,
            FIRST t-lieferant WHERE t-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
            BY l-pprice.bestelldatum DESC:
              ASSIGN s-list.last-pdate  = l-pprice.bestelldatum
                     s-list.last-pbook  = l-pprice.einzelpreis
                     s-list.a-firma     = t-lieferant.firma.
              LEAVE.
        END.                                                                                         
        
        FIND FIRST gl-acct WHERE gl-acct.fibukonto  = l-order.stornogrund NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            ASSIGN s-list.konto       = l-order.stornogrund + ";" + gl-acct.bezeich
                   s-list.desc-coa    = gl-acct.bezeich.
        END. 
    
        IF l-order.bestellart NE "" THEN
        DO:
            ASSIGN
                s-list.du-price1        = DEC(ENTRY(2,ENTRY(1, l-order.bestellart , "-"),";"))/ 100
                s-list.du-price2        = DEC(ENTRY(2,ENTRY(2, l-order.bestellart , "-"),";")) / 100
                s-list.du-price3        = DEC(ENTRY(2,ENTRY(3, l-order.bestellart , "-"),";")) / 100
                s-list.supp1            = INT(ENTRY(1,ENTRY(1, l-order.bestellart , "-"),";"))
                s-list.supp2            = INT(ENTRY(1,ENTRY(2, l-order.bestellart , "-"),";"))
                s-list.supp3            = INT(ENTRY(1,ENTRY(3, l-order.bestellart , "-"),";"))
                .
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
        
        IF l-order.angebot-lief[3] NE 0 THEN
        DO:
          FIND FIRST usrbuff WHERE usrbuff.nr = l-order.angebot-lief[3] 
              NO-LOCK NO-ERROR.
          IF AVAILABLE usrbuff THEN s-list.cid = usrbuff.userinit.
        END.
        
        IF l-order.anzahl NE 0 THEN s-list.str3 
            = STRING(l-order.anzahl,">>>,>>9.99"). 
        IF l-artikel.lief-einheit NE 0 THEN s-list.str4 
            = STRING(l-artikel.lief-einheit,">>,>>9"). 
        IF l-order.lieferdatum NE ? THEN 
            s-list.lieferdatum = STRING(l-order.lieferdatum).
      END.
      FIND NEXT l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
         AND l-order.loeschflag LE 1 AND l-order.pos GT 0 
         AND l-order.lief-nr = 0 USE-INDEX order_ix NO-LOCK NO-ERROR.
    END. 
    RETURN. 
  END.

  FOR EACH s-list:
      DELETE s-list.
  END. 

  DO: 
    FOR EACH l-orderhdr WHERE l-orderhdr.bestelldatum GE from-date 
      AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr GE 9 
      NO-LOCK BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr: 
      app-flag = (l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") = 0)
          AND ENTRY(1, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") NE " " 
          AND ENTRY(3, l-orderhdr.lief-fax[2], ";") NE " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") NE " ". 
      rej-flag = (l-orderhdr.lief-fax[2] NE "" AND INDEX(l-orderhdr.lief-fax[2],"|") > 0). 
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
      AND parameters.section = "Name" 
      AND INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] NO-LOCK NO-ERROR. 
      FIND FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
        AND l-order.pos = 0 AND l-order.lief-nr = 0 
        AND l-order.artnr EQ artnumber NO-LOCK NO-ERROR. /*DODY*/ 

      do-it = YES.
      IF outstand-flag AND NOT app-flag AND NOT rej-flag 
        AND l-orderhdr.lieferdatum GE billdate THEN do-it = NO.
      IF do-it AND expired-flag AND NOT app-flag AND NOT rej-flag 
        AND l-orderhdr.lieferdatum LT billdate THEN do-it = NO.
      IF do-it AND approve-flag AND app-flag THEN do-it = NO.
      IF do-it AND reject-flag  AND rej-flag THEN do-it = NO.

      IF do-it THEN
      DO:
        /*FIND LAST l-op WHERE l-op.op-art = 1 NO-LOCK NO-ERROR.
        FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR.*/
        CREATE s-list. 
        IF AVAILABLE parameters THEN s-list.bezeich = parameters.vstring. 
        ASSIGN 
          s-list.pos              = 0
          s-list.s-recid          = RECID(l-orderhdr) 
          s-list.docu-nr          = l-orderhdr.docu-nr 
          s-list.str0             = l-orderhdr.docu-nr 
          s-list.deptnr           = l-orderhdr.angebot-lief[1] 
          s-list.bestelldatum     = STRING(l-orderhdr.bestelldatum) 
          s-list.lieferdatum      = STRING(l-orderhdr.lieferdatum) 
          s-list.approved         = app-flag 
          s-list.rejected         = rej-flag 
          /*s-list.last-pdate       = l-op.datum
          s-list.last-pprice      = l-artikel.ek-letzter*/.
        IF l-orderhdr.betriebsnr EQ 10 THEN s-list.flag = YES.

        IF NUM-ENTRIES(l-orderhdr.lief-fax[3], "-") GT 1 THEN DO:
            ASSIGN s-list.del-reason = ENTRY(2, l-orderhdr.lief-fax[3], "-")
                   s-list.instruct   = ENTRY(1, l-orderhdr.lief-fax[3], "-").
        END.
        ELSE s-list.instruct   = l-orderhdr.lief-fax[3].

        IF INDEX(l-orderhdr.lief-fax[2],"|") = 0 THEN
        DO:
            IF ENTRY(1, l-orderhdr.lief-fax[2], ";") EQ " " AND ENTRY(2, l-orderhdr.lief-fax[2], ";") EQ " "
                AND ENTRY(3, l-orderhdr.lief-fax[2], ";") EQ " " AND ENTRY(4, l-orderhdr.lief-fax[2], ";") EQ " " THEN
                ASSIGN s-list.app-rej          = "".
            ELSE s-list.app-rej         = ENTRY(1, ENTRY(1, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                          ENTRY(1, ENTRY(2, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                          ENTRY(1, ENTRY(3, l-orderhdr.lief-fax[2], ";"), " ") + ";" +
                                          ENTRY(1, ENTRY(4, l-orderhdr.lief-fax[2], ";"), " ")  .
        END.
        IF INDEX(l-orderhdr.lief-fax[2],"|") > 0 THEN
        ASSIGN  s-list.rej-reason = TRIM(ENTRY(3, l-orderhdr.lief-fax[2], "|"))
                s-list.app-rej          = TRIM(ENTRY (4, ENTRY(1, l-orderhdr.lief-fax[2], "|"), ";"))
                .
        IF AVAILABLE l-order THEN s-list.loeschflag = l-order.loeschflag. 
 
        FIND FIRST sbuff WHERE RECID(sbuff) = RECID(s-list) NO-LOCK.

        /*FOR EACH l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
          AND l-order.pos GT 0 AND l-order.lief-nr = 0 
            AND l-order.artnr EQ artnumber NO-LOCK, /*DODY*/
          FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK
             BY l-order.docu-nr BY l-artikel.bezeich: */

        FIND FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
          AND l-order.pos GT 0 AND l-order.lief-nr = 0
          AND l-order.artnr EQ artnumber USE-INDEX order_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE l-order:
          FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-artikel THEN 
          DO:

            FIND FIRST usr WHERE usr.username = l-order.lief-fax[1] NO-LOCK. 
            FIND FIRST tbuff WHERE tbuff.docu-nr = l-order.docu-nr
                AND tbuff.pos = 0
                AND tbuff.loeschflag = l-order.loeschflag NO-ERROR.
            IF NOT AVAILABLE tbuff THEN
            DO:
              CREATE tbuff.
              BUFFER-COPY sbuff TO tbuff.
              ASSIGN tbuff.loeschflag = l-order.loeschflag.
            END.              
            CREATE s-list. 
            ASSIGN 
              s-list.s-recid        = RECID(l-order) 
              s-list.deptnr         = l-orderhdr.angebot-lief[1] 
              s-list.docu-nr        = l-order.docu-nr 
              s-list.po-nr          = l-order.lief-fax[2] 
              s-list.pos            = l-order.pos
              s-list.artnr          = l-artikel.artnr 
              s-list.bezeich        = l-artikel.bezeich 
              s-list.qty            = l-order.anzahl 
              s-list.dunit          = l-artikel.traubensort 
              s-list.lief-einheit   = l-artikel.lief-einheit 
              s-list.approved       = app-flag 
              s-list.rejected       = rej-flag
              s-list.pchase-date    = l-order.bestelldatum 
              s-list.loeschflag     = l-order.loeschflag 
              s-list.konto          = l-order.stornogrund 
              s-list.userinit       = usr.userinit 
              s-list.pchase-nr      = l-order.lief-fax[2]
              s-list.cdate          = l-order.lieferdatum-eff
              s-list.instruct       = l-order.besteller 
              /*M 04/06/12 -> show item based on selected supplier */
              s-list.supNo          = l-order.angebot-lief[2]           
              s-list.currNo         = l-order.angebot-lief[3]           
              s-list.duprice        = l-order.einzelpreis               
              s-list.amount         = l-order.warenwert /*eko*/ 
              s-list.anzahl         = l-order.anzahl                  
              s-list.txtnr          = l-order.txtnr                   
              s-list.einzelpreis    = l-order.einzelpreis
              /*wen*/
              s-list.zeit           = l-order.zeit
              s-list.min-bestand    = l-artikel.min-bestand 
              s-list.max-bestand    = l-artikel.anzverbrauch
              s-list.masseinheit    = l-artikel.masseinheit
              s-list.last-pprice    = l-artikel.ek-letzter.
              
            /*FIND LAST l-op WHERE l-op.op-art = 1 AND l-op.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-op THEN 
                ASSIGN s-list.last-pdate     = l-op.datum*/
                       
            
            /*gerald last purchase and last date purchase*/            
            /*FIND LAST l-pprice WHERE l-pprice.artnr = l-artikel.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-pprice THEN 
            DO:
                FIND FIRST t-lieferant WHERE t-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK NO-ERROR.
                ASSIGN s-list.last-pdate  = l-pprice.bestelldatum
                       s-list.last-pbook  = l-pprice.einzelpreis
                       s-list.a-firma     = t-lieferant.firma.
            END.*/
            
            FOR EACH l-pprice WHERE l-pprice.artnr = l-artikel.artnr NO-LOCK,
                FIRST t-lieferant WHERE t-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
                BY l-pprice.bestelldatum DESC:
                  ASSIGN s-list.last-pdate  = l-pprice.bestelldatum
                         s-list.last-pbook  = l-pprice.einzelpreis
                         s-list.a-firma     = t-lieferant.firma.
                  LEAVE.
            END.                                                                                                
            
            FIND FIRST gl-acct WHERE gl-acct.fibukonto  = l-order.stornogrund NO-LOCK NO-ERROR.
            IF AVAILABLE gl-acct THEN
            DO:
              ASSIGN s-list.konto = l-order.stornogrund + ";" + gl-acct.bezeich
                     s-list.desc-coa = gl-acct.bezeich.
            END. 
            
            IF l-order.bestellart NE "" THEN
            DO:
                ASSIGN
                    s-list.du-price1        = DEC(ENTRY(2,ENTRY(1, l-order.bestellart , "-"),";"))/ 100
                    s-list.du-price2        = DEC(ENTRY(2,ENTRY(2, l-order.bestellart , "-"),";")) / 100
                    s-list.du-price3        = DEC(ENTRY(2,ENTRY(3, l-order.bestellart , "-"),";")) / 100
                    s-list.supp1            = INT(ENTRY(1,ENTRY(1, l-order.bestellart , "-"),";"))
                    s-list.supp2            = INT(ENTRY(1,ENTRY(2, l-order.bestellart , "-"),";"))
                    s-list.supp3            = INT(ENTRY(1,ENTRY(3, l-order.bestellart , "-"),";"))
                    .
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
            
            IF NOT AVAILABLE sbuff THEN
            ASSIGN
                s-list.str0             = l-order.docu-nr 
                s-list.bestelldatum     = STRING(l-orderhdr.bestelldatum) 
                s-list.lieferdatum      = STRING(l-orderhdr.lieferdatum) 
            .
            
            IF l-order.angebot-lief[3] NE 0 THEN
            DO:
              FIND FIRST usrbuff WHERE usrbuff.nr = l-order.angebot-lief[3] 
                  NO-LOCK NO-ERROR.
              IF AVAILABLE usrbuff THEN s-list.cid = usrbuff.userinit.
            END.
            
            IF l-order.lieferdatum NE ? THEN 
              s-list.lieferdatum = STRING(l-order.lieferdatum). 
            IF l-order.anzahl NE 0 THEN s-list.str3 
              = STRING(l-order.anzahl,">>>,>>9.99"). 
            IF l-artikel.lief-einheit NE 0 THEN s-list.str4 
              = STRING(l-artikel.lief-einheit,">>,>>9"). 
          END.
          FIND NEXT l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
              AND l-order.pos GT 0 AND l-order.lief-nr = 0
              AND l-order.artnr EQ artnumber USE-INDEX order_ix NO-LOCK NO-ERROR.
        END. 
      END. 
    END.
  END.
END. 
