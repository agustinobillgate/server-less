DEFINE TEMP-TABLE t-bill-line       LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-blinebuff   LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-bill        LIKE bill
    FIELD bl-recid          AS INTEGER.

DEFINE INPUT PARAMETER pvILanguage              AS INTEGER. 
DEFINE INPUT PARAMETER bil-flag                 AS INTEGER. 
DEFINE INPUT PARAMETER b-recid                  AS INTEGER. 
DEFINE INPUT PARAMETER t-bill-rechnr            AS INTEGER.
DEFINE INPUT PARAMETER bill-line-departement    AS INTEGER.
DEFINE INPUT PARAMETER transdate                AS DATE.
DEFINE INPUT PARAMETER billart                  AS INTEGER.
DEFINE INPUT PARAMETER qty                      AS INTEGER.
DEFINE INPUT PARAMETER price                    AS DECIMAL.
DEFINE INPUT PARAMETER amount                   AS DECIMAL.
DEFINE INPUT PARAMETER amount-foreign           AS DECIMAL.
DEFINE INPUT PARAMETER DESCRIPTION              AS CHAR.
DEFINE INPUT PARAMETER voucher-nr               AS CHAR.
DEFINE INPUT PARAMETER cancel-str               AS CHAR.
DEFINE INPUT PARAMETER user-init                AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER rechnr            AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER balance           AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER balance-foreign   AS DECIMAL.
DEFINE OUTPUT PARAMETER error-desc              AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag            AS LOGICAL  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.

{SupertransBL.i}
DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "mbns-inv-paywith-deposit-webBL".

DEFINE VARIABLE master-str      AS CHAR       NO-UNDO.
DEFINE VARIABLE master-rechnr   AS CHAR       NO-UNDO.
DEFINE VARIABLE master-flag     AS LOGICAL    NO-UNDO.
DEFINE VARIABLE str1            AS CHARACTER  NO-UNDO INIT "NS".
DEFINE VARIABLE bline-dept      AS INTEGER    NO-UNDO.
DEFINE VARIABLE gname           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bil-recid       AS INTEGER    NO-UNDO.
DEFINE VARIABLE telbill-flag    AS LOGICAL NO-UNDO.
DEFINE VARIABLE babill-flag     AS LOGICAL NO-UNDO.

DEFINE VARIABLE depoart         AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez         AS CHARACTER NO-UNDO.
DEFINE VARIABLE p-253           AS LOGICAL.

DEFINE VARIABLE gastnrmember    AS INTEGER          NO-UNDO.
DEFINE VARIABLE price-decimal   AS INTEGER          NO-UNDO.
DEFINE VARIABLE double-currency AS LOGICAL          NO-UNDO.
DEFINE VARIABLE foreign-rate    AS LOGICAL          NO-UNDO.
DEFINE VARIABLE exchg-rate      AS DECIMAL INIT 1   NO-UNDO.
DEFINE VARIABLE currZeit        AS INTEGER          NO-UNDO.
DEFINE VARIABLE bill-date       AS DATE             NO-UNDO. 
DEFINE VARIABLE curr-room       AS CHAR             NO-UNDO.
DEFINE VARIABLE skip-it         AS LOGICAL.

DEFINE BUFFER resline FOR res-line.
DEFINE BUFFER buf-artikel FOR artikel.
DEFINE BUFFER buf-bill-line FOR bill-line.

FIND FIRST htparam WHERE htparam.paramnr EQ 1068 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel OR artikel.artart NE 5 THEN
    DO:           
        error-desc = translateExtended ("Deposit article not defined.",lvCAREA,"").  
        success-flag = NO.
        RETURN. 
    END.
    ASSIGN 
        depoart = artikel.artnr
        depobez = artikel.bezeich
        .
END.

RUN htplogic.p(253, OUTPUT p-253).
IF p-253 THEN
DO: 
    error-desc = translateExtended ("Night Audit is running, posting not possible",lvCAREA,""). 
    success-flag = NO.
    RETURN.
END.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
IF foreign-rate OR double-currency THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 

ASSIGN
  currZeit    = TIME
  master-flag = NO
.

RUN update-to-bill.

RUN read-bill2bl.p (5, b-recid, ?, ?, ?, ?, ?, ?, ?, ?,             
    OUTPUT telbill-flag, OUTPUT babill-flag, OUTPUT TABLE t-bill).

/*******************************************************************************************
                                        PROCEDURE
*******************************************************************************************/
PROCEDURE update-to-bill:
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr EQ 110 NO-LOCK. 
    bill-date = vhp.htparam.fdate. 
    IF transdate NE ? THEN bill-date = transdate. 
    ELSE
    DO:
        FIND FIRST htparam WHERE paramnr EQ 253 NO-LOCK. 
        IF htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
    END.
    IF amount-foreign = ? THEN amount-foreign = 0.

    FIND FIRST bill WHERE RECID(bill) EQ b-recid NO-LOCK. 
    IF bill.flag EQ 1 AND bil-flag EQ 0 THEN 
    DO: 
        error-desc = translateExtended ("The Bill was closed / guest checked out",lvCAREA,"") + CHR(10)
                + translateExtended ("Bill entry is no longer possible!",lvCAREA,""). 
        success-flag = NO.
        RETURN. 
    END. 

    DO TRANSACTION:
        FIND CURRENT bill EXCLUSIVE-LOCK. 
        ASSIGN 
            curr-room    = bill.zinr
            gastnrmember = bill.gastnr
            .

        IF NOT artikel.autosaldo THEN bill.rgdruck = 0.

        IF bill.datum LT bill-date OR bill.datum EQ ? THEN bill.datum = bill-date. 
        
        bill.saldo = bill.saldo + amount. 
        IF double-currency OR foreign-rate THEN bill.mwst[99] = bill.mwst[99] + amount-foreign. 
        IF bill.rechnr EQ 0 THEN 
        DO: 
            FIND FIRST counters WHERE counters.counter-no EQ 3 EXCLUSIVE-LOCK. 
            counters.counter = counters.counter + 1. 
            bill.rechnr = counters.counter. 
            IF transdate NE ? THEN bill.datum = transdate. 
            FIND CURRENT counter NO-LOCK. 
        END. 
        ASSIGN rechnr = bill.rechnr. 

        CREATE bill-line. 
        ASSIGN
            bill-line.rechnr       = bill.rechnr
            bill-line.massnr       = bill.resnr
            bill-line.billin-nr    = bill.reslinnr
            bill-line.zinr         = curr-room
            bill-line.artnr        = depoart
            bill-line.anzahl       = 1
            bill-line.betrag       = amount 
            bill-line.fremdwbetrag = amount-foreign
            bill-line.bezeich      = depobez
            bill-line.departement  = artikel.departement 
            bill-line.zeit         = TIME
            bill-line.userinit     = user-init 
            bill-line.bill-datum   = bill-date
        . 
        IF voucher-nr NE "" THEN bill-line.bezeich = bill-line.bezeich + "/" + voucher-nr.
        FIND CURRENT bill-line NO-LOCK. 

        CREATE t-bill-line.
        BUFFER-COPY bill-line TO t-bill-line.
        ASSIGN 
            t-bill-line.artart   = artikel.artart
            t-bill-line.bl-recid = INTEGER(RECID(bill-line))
            .

        FIND FIRST umsatz WHERE umsatz.artnr EQ depoart 
            AND umsatz.departement EQ artikel.departement 
            AND umsatz.datum EQ bill-date EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE umsatz THEN 
        DO: 
            CREATE umsatz.
            ASSIGN
              umsatz.artnr       = depoart 
              umsatz.datum       = bill-date 
              umsatz.departement = artikel.departement
              . 
        END.
        ASSIGN
            umsatz.betrag = umsatz.betrag + amount
            umsatz.anzahl = umsatz.anzahl + 1
            . 
        FIND CURRENT umsatz NO-LOCK.

        CREATE billjournal. 
        ASSIGN
            billjournal.rechnr       = bill.rechnr
            billjournal.zinr         = curr-room
            billjournal.artnr        = depoart
            billjournal.anzahl       = 1
            billjournal.fremdwaehrng = amount-foreign 
            billjournal.betrag       = amount
            billjournal.bezeich      = depobez
            billjournal.departement  = artikel.departement 
            billjournal.epreis       = price
            billjournal.zeit         = TIME
            billjournal.stornogrund  = cancel-str 
            billjournal.userinit     = user-init 
            billjournal.bill-datum   = bill-date
            . 
        IF voucher-nr NE "" THEN billjournal.bezeich = billjournal.bezeich + "/" + voucher-nr. 
        FIND CURRENT billjournal NO-LOCK. 

        balance = bill.saldo. 
        IF double-currency OR foreign-rate THEN balance-foreign = bill.mwst[99]. 
    
        FIND CURRENT bill NO-LOCK. 
    END.
END PROCEDURE.
