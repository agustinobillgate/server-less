DEF TEMP-TABLE s-list LIKE l-order
    FIELD curr          AS CHAR
    FIELD exrate        AS DEC
    FIELD s-recid       AS INTEGER
    FIELD amount        AS DEC  /*IT 270612 -> add local amount and total*/
    FIELD supp1         AS INT
    FIELD supp2         AS INT /*FT 210912*/
    FIELD supp3         AS INT  
    FIELD suppn1        AS CHAR FORMAT "x(30)"
    FIELD suppn2        AS CHAR FORMAT "x(30)"
    FIELD suppn3        AS CHAR FORMAT "x(30)"
    FIELD supps         AS CHAR FORMAT "x(30)"
    FIELD du-price1     AS DEC
    FIELD du-price2     AS DEC  
    FIELD du-price3     AS DEC
    FIELD curr1         AS CHAR
    FIELD curr2         AS CHAR
    FIELD curr3         AS CHAR
    FIELD fdate1        AS DATE
    FIELD fdate2        AS DATE
    FIELD fdate3        AS DATE
    FIELD tdate1        AS DATE
    FIELD tdate2        AS DATE
    FIELD tdate3        AS DATE
    FIELD desc-coa      AS CHARACTER FORMAT "x(20)"
    FIELD last-pprice   AS DECIMAL FORMAT "->>,>>>,>>9.99"  /* Add by Michael @ 09/05/2019 for Luxton Cirebon request - ticket no C071EE */
    FIELD avg-pprice    LIKE l-artikel.vk-preis     
    FIELD lprice        LIKE l-artikel.ek-letzter        /*last-purchase based artikel*/
    FIELD lief-fax2     LIKE l-orderhdr.lief-fax[2]
    FIELD ek-letzter    AS DECIMAL
    FIELD lief-einheit  AS INTEGER
    FIELD supplier      AS CHARACTER
    FIELD lief-fax-2    LIKE l-order.lief-fax[2]
    FIELD vk-preis      LIKE l-artikel.vk-preis 
    FIELD soh           AS DECIMAL
    FIELD last-pdate    AS DATE /*gerald add last purchase date*/
    FIELD a-firma       LIKE l-lieferant.firma   /*gerald last-supplier*/
    FIELD last-pbook    AS DECIMAL FORMAT "->>,>>>,>>9.99" /*gerald last-purchase based pbook*/
    .

DEF TEMP-TABLE t-parameters
    FIELD varname LIKE parameters.varname
    FIELD vstring LIKE parameters.vstring.

DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-waehrung LIKE waehrung.

DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         LIKE l-artikel.artnr
    FIELD traubensort   LIKE l-artikel.traubensort
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD soh           AS DECIMAL /*545FBD gerald*/
    .

DEFINE BUFFER usr       FOR bediener. 
DEFINE BUFFER b-list    FOR s-list.

DEF INPUT PARAMETER docu-nr AS CHAR.

DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER comments AS CHAR.
DEF OUTPUT PARAMETER deptnr AS INT.
DEF OUTPUT PARAMETER lieferdatum AS DATE.
DEF OUTPUT PARAMETER deptname AS CHAR.
DEF OUTPUT PARAMETER hierarchie AS LOGICAL.
DEF OUTPUT PARAMETER tot AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99".
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.

DEFINE VARIABLE local-curr  AS INTEGER   NO-UNDO.
DEFINE VARIABLE amt         AS DECIMAL   NO-UNDO.
DEFINE VARIABLE def-curr    AS CHARACTER NO-UNDO.

FIND FIRST htparam WHERE paramnr = 386 NO-LOCK. 
hierarchie = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate.
/*NAUFAL 090621 - find htparam 152 for default currency*/
FIND FIRST htparam WHERE paramnr EQ 152 NO-LOCK.
def-curr = htparam.fchar.
 
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK. 
comments = l-orderhdr.lief-fax[3]. 
deptnr = l-orderhdr.angebot-lief[1]. 
lieferdatum = l-orderhdr.lieferdatum. 
CREATE t-l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
 
FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
  AND parameters.section = "Name" 
  AND INTEGER(parameters.varname) = deptnr NO-LOCK NO-ERROR. 
IF AVAILABLE parameters THEN deptname = parameters.vstring. 

RUN reload-s-list.
FOR EACH l-artikel USE-INDEX artnr_ix NO-LOCK:
    CREATE t-l-artikel.
    ASSIGN
    t-l-artikel.rec-id        = RECID(l-artikel)
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.traubensort   = l-artikel.traubensort
    t-l-artikel.lief-einheit  = l-artikel.lief-einheit
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.jahrgang      = l-artikel.jahrgang.
END.

FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" NO-LOCK:
    CREATE t-parameters.
    ASSIGN
    t-parameters.varname = parameters.varname
    t-parameters.vstring = parameters.vstring.
END.

FOR EACH waehrung NO-LOCK:
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
END.

DEFINE VARIABLE tot-anz         AS DECIMAL.
DEFINE VARIABLE anz-anf-best    AS DECIMAL.
DEFINE VARIABLE anz-eingang     AS DECIMAL.
DEFINE VARIABLE anz-ausgang     AS DECIMAL.

/*FOR EACH s-list:
    /*NA - Ganti validasi karena muncul popup l-bestand not available*/
    FIND FIRST l-artikel WHERE l-artikel.artnr EQ s-list.artnr NO-LOCK NO-ERROR.
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND l-bestand.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN
    DO:
        IF l-bestand.anz-anf-best EQ ? THEN
            anz-anf-best = 0.
        ELSE
            anz-anf-best = l-bestand.anz-anf-best.
        IF l-bestand.anz-eingang EQ ? THEN
            anz-eingang = 0.
        ELSE
            anz-eingang = l-bestand.anz-eingang.
        IF l-bestand.anz-ausgang EQ ? THEN
            anz-ausgang = 0.
        ELSE
            anz-ausgang = l-bestand.anz-ausgang.
        
        tot-anz = anz-anf-best + anz-eingang - anz-ausgang.
    END.
    ELSE
    DO:
        tot-anz = 0.
    END.
    ASSIGN 
       s-list.soh    = tot-anz
       /*s-list.lprice = l-artikel.ek-letzter*/
       tot-anz       = 0
       .
END.*/

PROCEDURE reload-s-list:
    FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND l-order.pos GT 0 
        AND l-order.lief-nr = 0 AND l-order.loeschflag LE 1 NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK BY l-artikel.bezeich: 
        FIND FIRST usr WHERE usr.username = l-order.lief-fax[1] NO-LOCK.
        CREATE s-list.
        BUFFER-COPY l-order TO s-list.
        amt = s-list.anzahl * s-list.einzelpreis.
        ASSIGN 
            s-list.amount           = l-order.warenwert
            s-list.s-recid          = RECID(l-order)
            s-list.angebot-lief[2]  = l-order.angebot-lief[2]
            s-list.einzelpreis      = l-order.einzelpreis
            s-list.lief-fax-2       = l-order.lief-fax[2]
            /*add by gerald 140420*/
            s-list.ek-letzter     = l-artikel.ek-letzter
            s-list.lief-einheit   = l-artikel.lief-einheit
            s-list.vk-preis       = l-artikel.vk-preis
            s-list.lprice         = l-artikel.ek-letzter.

        IF l-order.bestellart NE "" THEN
        ASSIGN 
          s-list.supp1     = INT(ENTRY(1,ENTRY(1, l-order.bestellart , "-"),";"))
          s-list.du-price1 = DEC(ENTRY(2,ENTRY(1, l-order.bestellart , "-"),";"))/ 100    /*SIS 281013*/
          s-list.curr1     = ENTRY(3,ENTRY(1, l-order.bestellart , "-"), ";")
          s-list.fdate1    = DATE(ENTRY(4,ENTRY(1, l-order.bestellart , "-"), ";"))
          s-list.tdate1    = DATE(ENTRY(5,ENTRY(1, l-order.bestellart , "-"), ";"))
          s-list.supp2     = INT(ENTRY(1,ENTRY(2, l-order.bestellart , "-"),";"))
          s-list.du-price2 = DEC(ENTRY(2,ENTRY(2, l-order.bestellart , "-"),";")) / 100   /*sis 281013*/
          s-list.curr2     = ENTRY(3,ENTRY(2, l-order.bestellart , "-"), ";")
          s-list.fdate2    = DATE(ENTRY(4,ENTRY(2, l-order.bestellart , "-"), ";"))
          s-list.tdate2    = DATE(ENTRY(5,ENTRY(2, l-order.bestellart , "-"), ";"))
          s-list.supp3     = INT(ENTRY(1,ENTRY(3, l-order.bestellart , "-"),";"))
          s-list.du-price3 = DEC(ENTRY(2,ENTRY(3, l-order.bestellart , "-"),";")) / 100   /*sis 281013*/
          s-list.curr1     = ENTRY(3,ENTRY(3, l-order.bestellart , "-"), ";")
          s-list.fdate1    = DATE(ENTRY(4,ENTRY(3, l-order.bestellart , "-"), ";"))
          s-list.tdate1    = DATE(ENTRY(5,ENTRY(3, l-order.bestellart , "-"), ";")).

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp1 NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
          s-list.suppn1 = l-lieferant.firma.
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp2 NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
          s-list.suppn2 = l-lieferant.firma.
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp3 NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
          s-list.suppn3 = l-lieferant.firma.
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.angebot-lief[2] NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
          s-list.supps = l-lieferant.firma.

        FIND FIRST gl-acct WHERE gl-acct.fibukonto  = l-order.stornogrund NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            ASSIGN
                s-list.desc-coa       = gl-acct.bezeich.
        END.

        /*gerald last purchase and last date purchase*/  
        FOR EACH l-pprice WHERE l-pprice.artnr = l-artikel.artnr NO-LOCK,
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-pprice.lief-nr NO-LOCK 
          BY l-pprice.bestelldatum DESC:
            ASSIGN s-list.last-pdate  = l-pprice.bestelldatum
                   s-list.last-pbook  = l-pprice.einzelpreis
                   s-list.a-firma     = l-lieferant.firma.
            LEAVE.
        END.  

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-order.lief-nr NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
            ASSIGN
                s-list.supplier     = l-lieferant.firma.
        END.

        /*geral soh pindah sini dari atas*/
        FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
            AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
          ASSIGN 
              s-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                          - l-bestand.anz-ausgang.
        END.
        
        /*wen
        FOR EACH l-op WHERE l-op.artnr = l-op.artnr AND l-op.lscheinnr MATCHES "*I*"
            BY l-op.datum DESC:
            IF AVAILABLE l-op THEN
            FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr         NO-LOCK NO-ERROR.
            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK NO-ERROR.
                ASSIGN
                    s-list.po-number    = l-op.lscheinnr
                    s-list.ek-letzter   = l-artikel.ek-letzter
                    s-list.lief-einheit = l-artikel.lief-einheit
                    s-list.supplier     = l-lieferant.firma.
        END. 
        /*wen*/*/

        /*M 010612 -> add supplier and currency */
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = l-order.angebot-lief[3]
          NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN 
        ASSIGN s-list.curr = waehrung.wabkurz
               s-list.exrate = waehrung.ankauf / waehrung.einheit.

        IF AVAILABLE waehrung THEN 
        DO:
          local-curr = INT(s-list.angebot-lief[3]).
          IF local-curr NE 1 THEN 
          DO:
             ASSIGN s-list.exrate = waehrung.ankauf / waehrung.einheit.
             /*s-list.amount = amt * s-list.exrate.  */
          END.
        END.

        /*IT 270612 -> add local amount and total*/
        tot = 0.
        FIND FIRST s-list NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE s-list:
            /*NAUFAL 090621 - add validation to set curr value to htparam 152*/
            IF s-list.curr EQ "" OR s-list.curr EQ " " THEN s-list.curr = def-curr.
            tot = tot + s-list.amount.
            FIND NEXT s-list NO-LOCK NO-ERROR.
            FIND CURRENT s-list NO-LOCK NO-ERROR.
        END.
    END.
END.
