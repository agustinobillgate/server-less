
DEFINE TEMP-TABLE bline-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD userinit LIKE bediener.userinit 
  FIELD selected AS LOGICAL INITIAL NO 
  FIELD name LIKE bediener.username 
  FIELD bl-recid AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE summary1
    FIELD usrinit       LIKE bediener.userinit
    FIELD username      LIKE bediener.username
    FIELD artnr         AS INTEGER
    FIELD amount        AS DECIMAL FORMAT "->>,>>>,>>9.99".

DEFINE TEMP-TABLE cash-art
    FIELD pos-nr        AS INTEGER
    FIELD artnr         LIKE artikel.artnr
    FIELD bezeich       LIKE artikel.bezeich
    FIELD amount        AS DECIMAL FORMAT "->>,>>>,>>9.99"
    FIELD tamount       AS DECIMAL FORMAT "->>,>>>,>>9.99".

DEFINE TEMP-TABLE turnover 
  FIELD departement     LIKE h-bill.departement 
  FIELD usr-nr          LIKE bediener.nr 
  FIELD name            AS CHAR FORMAT "x(16)" COLUMN-LABEL "Username"
  FIELD rechnr          AS CHAR FORMAT "x(7)" COLUMN-LABEL "Bill-No" 
  FIELD zinr            LIKE zimmer.zinr INITIAL ""
  FIELD info            AS CHAR    FORMAT "x(48)"        LABEL "Info" 
  FIELD curr            AS CHAR    FORMAT "x(4)"         LABEL "Curr"
  FIELD p-cash          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Cash(Local)"
  FIELD f-cash          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Cash(Foreign)"
  FIELD c-ledger        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "City Ledger"
  FIELD creditcard      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Credit Card"            
  FIELD flag            AS INTEGER INITIAL 0
  FIELD gname           AS CHAR FORMAT "x(16)" COLUMN-LABEL "Guest Name".

DEF INPUT  PARAMETER TABLE FOR bline-list.
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER shift AS INT.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER curr-shift as char format "x(48)".
DEF OUTPUT PARAMETER nt-cash     as DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-fcash    as DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-ledger   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER nt-credit   as DECIMAL FORMAT "->>>,>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER TABLE FOR turnover.
DEF OUTPUT PARAMETER TABLE FOR summary1.
DEF OUTPUT PARAMETER TABLE FOR cash-art.

DEFINE BUFFER cbuff  FOR cash-art.

DEFINE VARIABLE tot-cash     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-fcash    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-ledger   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-credit   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-amount   AS DECIMAL EXTENT 6 FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE nt-amount   AS DECIMAL EXTENT 6 FORMAT "->>>,>>>,>>>,>>9.99".

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "FO-daysale".

RUN daysale-list1.

procedure daysale-list1: 
define variable curr-s  as integer. 
define variable billnr  as integer. 
define variable dept    as integer format ">>9" initial 1. 
define variable d-name  as character format "x(24)". 
define variable usr-nr as integer. 
define variable d-found as logical initial "no". 
define variable c-found as logical initial "no". 
define variable vat     as decimal. 
define variable service as decimal. 
define variable netto   as decimal. 
define variable i       as integer. 
DEFINE VARIABLE pos     AS INTEGER.
DEFINE VARIABLE bill-no AS INTEGER.
DEFINE VARIABLE guestname AS CHAR.
define variable found   as logical initial NO. /* Malik Serverless 579 no -> NO */
DEFINE VARIABLE do-it   AS LOGICAL INITIAL NO.
DEFINE VARIABLE t-resnr AS CHAR.
DEF BUFFER tlist FOR turnover.

  for each turnover: 
    delete turnover. 
  end. 

  FOR EACH cash-art:
      DELETE cash-art.
  END.

  FOR EACH summary1:
      DELETE summary1.
  END.
  
  ASSIGN
      tot-cash      = 0
      tot-ledger    = 0
      tot-credit    = 0
      tot-fcash     = 0
      nt-cash       = 0
      nt-ledger     = 0
      nt-credit     = 0
      nt-fcash      = 0.
 
  IF shift = 0 THEN
      curr-shift = translateExtended("SHIFT : ALL", lvCAREA, "").
  ELSE IF shift = 1 THEN
      curr-shift = translateExtended("SHIFT : MORNING", lvCAREA, "").
  ELSE IF shift = 2 THEN
      curr-shift = translateExtended("SHIFT : NOON", lvCAREA, "").
  ELSE IF shift = 1 THEN
      curr-shift = translateExtended("SHIFT : DINNER", lvCAREA, "").
  ELSE IF shift = 1 THEN
      curr-shift = translateExtended("SHIFT : SUPPER", lvCAREA, "").

  FOR EACH bline-list WHERE bline-list.SELECTED = YES BY bline-list.NAME:
      FIND FIRST bediener WHERE RECID(bediener) = bline-list.bl-recid NO-LOCK NO-ERROR. /* Malik Serverless 579 add NO-ERROR and if availlable */
      IF AVAILABLE bediener THEN
      DO:
        ASSIGN
            tot-cash      = 0
            tot-ledger    = 0
            tot-credit    = 0
            tot-fcash     = 0
            found         = NO.
        FOR EACH billjournal WHERE billjournal.bill-datum = from-date AND 
            billjournal.departement = 0 AND billjournal.anzahl NE 0 AND 
            billjournal.userinit = bediener.userinit NO-LOCK,
            FIRST artikel WHERE artikel.artnr = billjournal.artnr AND
            artikel.departement = 0 AND (artikel.artart = 2 OR artikel.artart = 6
                                        OR artikel.artart = 7) NO-LOCK
            BY billjournal.rechnr:
            IF shift = 0 THEN do-it = YES.
            ELSE do-it = billjournal.betriebsnr = shift.
            IF do-it THEN
            DO:
                found = YES.
                FIND FIRST bill WHERE bill.rechnr = billjournal.rechnr 
                    AND bill.rechnr NE 0 NO-LOCK NO-ERROR.

                FIND FIRST turnover WHERE turnover.rechnr = STRING(billjournal.rechnr)
                    AND turnover.usr-nr = bediener.nr NO-ERROR.
                IF NOT AVAILABLE turnover THEN
                DO:
                    CREATE turnover.
                    ASSIGN
                        turnover.rechnr   = STRING(billjournal.rechnr)
                        turnover.usr-nr   = bediener.nr
                        turnover.name     = bediener.username.
                    IF AVAILABLE bill THEN
                    DO:
                        FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND 
                            res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN
                            turnover.gname = res-line.NAME.
                        ASSIGN
                        turnover.zinr     = bill.zinr .
                    END.
                    ELSE
                    DO:
                        /*ITA 231014*/
                        IF billjournal.bezeich MATCHES "*#*" THEN 
                            ASSIGN t-resnr = ENTRY(2,billjournal.bezeich,"#").
                        ELSE ASSIGN t-resnr = billjournal.bezeich.

                        t-resnr = ENTRY(1,t-resnr,"]").
                        FIND FIRST res-line WHERE res-line.resnr = INT(t-resnr) NO-LOCK NO-ERROR.
                        IF AVAILABLE res-line THEN
                            turnover.gname = res-line.NAME.
                    END.
                END.

                IF artikel.artart = 2 THEN
                DO:
                    ASSIGN
                        turnover.c-ledger     = turnover.c-ledger - billjournal.betrag
                        tot-ledger            = tot-ledger - billjournal.betrag.
                END.
                ELSE IF artikel.artart = 6 THEN
                DO:
                    IF artikel.pricetab THEN
                    DO:
                        FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr NO-LOCK NO-ERROR.
                        IF AVAILABLE waehrung THEN
                            turnover.curr = waehrung.wabkurz.
                        ASSIGN
                            turnover.f-cash       = turnover.f-cash - billjournal.fremdwaehrng
                            tot-fcash             = tot-fcash - billjournal.fremdwaehrng.
                    END.
                    ELSE 
                    ASSIGN
                        turnover.p-cash       = turnover.p-cash - billjournal.betrag
                        tot-cash              = tot-cash - billjournal.betrag.
                    FIND FIRST cash-art WHERE cash-art.artnr = artikel.artnr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE cash-art THEN
                    DO:
                        CREATE cash-art.
                        ASSIGN
                            cash-art.artnr = artikel.artnr
                            cash-art.bezeich = artikel.bezeich.
                        FIND LAST cbuff NO-LOCK.
                        IF AVAILABLE cbuff THEN
                            ASSIGN cash-art.pos-nr = cbuff.pos-nr + 1.
                        ELSE ASSIGN cash-art.pos-nr = 1.
                    END.
                    FIND FIRST summary1 WHERE summary1.usrinit = billjournal.userinit 
                        AND summary1.artnr = artikel.artnr NO-ERROR.
                    IF NOT AVAILABLE summary1 THEN
                    DO:
                        CREATE summary1.
                        ASSIGN
                            summary1.artnr        = artikel.artnr
                            summary1.usrinit     = bediener.userinit.
                    END.
                    summary1.amount = summary1.amount - billjournal.betrag.
                END.
                ELSE IF artikel.artart = 7 THEN
                DO:
                    ASSIGN
                        turnover.creditcard   = turnover.creditcard - billjournal.betrag
                        tot-credit            = tot-credit - billjournal.betrag
                        turnover.INFO         = ENTRY(2, billjournal.bezeich, "/") NO-ERROR.
                END.
            END.
        END.
        IF found THEN
        DO:
            CREATE turnover.
            ASSIGN
                turnover.rechnr       = "TOTAL"
                turnover.flag         = 1
                turnover.p-cash       = tot-cash
                turnover.c-ledger     = tot-ledger
                turnover.creditcard   = tot-credit
                turnover.f-cash       = tot-fcash.
        END.
      END.
  END.
  
  
  create turnover. 
  turnover.rechnr = "G-TOTAL".
  turnover.flag = 3.
  
  FOR EACH tlist WHERE tlist.flag = 0:
      turnover.p-cash = turnover.p-cash + tlist.p-cash.  
      turnover.c-ledger = turnover.c-ledger + tlist.c-ledger.  
      turnover.creditcard = turnover.creditcard + tlist.creditcard.
      turnover.f-cash = turnover.f-cash + tlist.f-cash.
  END.                                           

  ASSIGN
  nt-cash = turnover.p-cash
  nt-ledger = turnover.c-ledger
  nt-credit = turnover.creditcard /* Malik Serverless 579 turnover.credit -> turnover.creditcard */
  nt-fcash = turnover.f-cash.

end.  
