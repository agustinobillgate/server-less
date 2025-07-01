
DEFINE TEMP-TABLE bline-list 
  FIELD bl-recid    AS INTEGER 
  FIELD artnr       AS INTEGER 
  FIELD dept        AS INTEGER 
  FIELD anzahl      AS INTEGER 
  FIELD massnr      AS INTEGER    
  FIELD billin-nr   AS INTEGER 
  FIELD zeit        AS INTEGER
  FIELD mwst-code   AS INTEGER INITIAL 0
  FIELD vatProz     AS DECIMAL INITIAL 0
  FIELD epreis      AS DECIMAL 
  FIELD netto       AS DECIMAL INITIAL 0 
  FIELD fsaldo      AS DECIMAL 
  FIELD saldo       AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD orts-tax    AS DECIMAL INITIAL 0 
  FIELD voucher     AS CHAR 
  FIELD bezeich     AS CHAR 
  FIELD zinr        LIKE zimmer.zinr        /*MT 20/07/12 change zinr format */
  FIELD gname       AS CHAR 
  FIELD origin-id   AS CHAR INITIAL ""
  FIELD userinit    AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD ankunft     AS DATE 
  FIELD abreise     AS DATE 
  FIELD datum       AS DATE 
. 

DEFINE TEMP-TABLE sum-tbl
    FIELD mwst-code     LIKE artikel.mwst-code
    FIELD sum-date      AS CHAR INITIAL ""
    FIELD sum-roomnr    AS CHAR INITIAL ""
    FIELD sum-desc      AS CHAR INITIAL ""
    FIELD sum-amount    AS DEC  INITIAL 0
    FIELD sum-id        AS CHAR INITIAL ""
    FIELD sum-amount-bef-tax    AS DEC  INITIAL 0.

DEFINE TEMP-TABLE t-str3
    FIELD str3 AS CHAR.

DEFINE TEMP-TABLE t-spbill-list 
  FIELD selected AS LOGICAL INITIAL YES 
  FIELD bl-recid AS INTEGER.

DEFINE TEMP-TABLE bl-guest
    FIELD zinr       AS CHAR
    FIELD curr-guest AS CHAR.

DEF TEMP-TABLE bline-vatlist
    FIELD seqnr   AS INTEGER
    FIELD vatnr   AS INTEGER INIT 0
    FIELD bezeich AS CHAR    FORMAT "x(24)"
    FIELD betrag  AS DECIMAL FORMAT "->>>,>>>,>>9.99"
.

DEFINE INPUT PARAMETER TABLE FOR t-spbill-list.
DEFINE INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER curr-status      AS CHAR         NO-UNDO.
DEFINE INPUT PARAMETER briefnr          AS INTEGER      NO-UNDO. 
DEFINE INPUT PARAMETER resnr            AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER reslinnr         AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER inv-type         AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER rechnr           AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER curr-program     AS CHAR         NO-UNDO.
DEFINE INPUT PARAMETER gastnr           AS INTEGER      NO-UNDO. 
DEFINE INPUT PARAMETER spbill-flag      AS LOGICAL.
DEFINE INPUT PARAMETER user-init        AS CHAR.
DEFINE INPUT PARAMETER LnLDelimeter     AS CHAR.

DEF OUTPUT  PARAMETER str1              AS CHARACTER  NO-UNDO.
DEF OUTPUT  PARAMETER str2              AS CHARACTER  NO-UNDO.
DEF OUTPUT  PARAMETER str3              AS CHARACTER  NO-UNDO.
DEF OUTPUT  PARAMETER TABLE FOR t-str3.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "print-bill-lnl".

DEFINE VARIABLE briefnr2        AS INTEGER  NO-UNDO.
DEFINE VARIABLE briefnr21       AS INTEGER  NO-UNDO.
DEFINE VARIABLE htl-name        AS CHARACTER.
DEFINE VARIABLE htl-adr1        AS CHARACTER.
DEFINE VARIABLE htl-adr2        AS CHARACTER.
DEFINE VARIABLE htl-adr3        AS CHARACTER.
DEFINE VARIABLE htl-tel         AS CHARACTER.
DEFINE VARIABLE htl-fax         AS CHARACTER.
DEFINE VARIABLE htl-email       AS CHARACTER.

DEFINE VARIABLE bill-recv       AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bill-no         AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bl-descript     AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bl-descript0    AS CHARACTER  NO-UNDO INITIAL "".
DEFINE VARIABLE bl-voucher      AS CHARACTER  NO-UNDO INITIAL "".
DEFINE VARIABLE bl0-balance     AS DECIMAL INITIAL 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE bl0-balance1    AS DECIMAL INITIAL 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE bl-balance      AS DECIMAL INITIAL 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE bl-balance1     AS DECIMAL INITIAL 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99".
DEFINE VARIABLE sum-anz         AS DECIMAL INITIAL 0 FORMAT "->>>".

DEFINE VARIABLE address1        AS CHARACTER  NO-UNDO.
DEFINE VARIABLE address2        AS CHARACTER  NO-UNDO.
DEFINE VARIABLE address3        AS CHARACTER  NO-UNDO.
DEFINE VARIABLE email           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE hp-no           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE acc             AS CHARACTER  NO-UNDO.
DEFINE VARIABLE adult           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE child1          AS CHARACTER  NO-UNDO.
DEFINE VARIABLE child2          AS CHARACTER  NO-UNDO.
DEFINE VARIABLE complGst        AS CHARACTER  NO-UNDO.
DEFINE VARIABLE room-no         AS CHARACTER  NO-UNDO.
DEFINE VARIABLE room-price      AS CHARACTER  NO-UNDO.
DEFINE VARIABLE arrival         AS CHARACTER  NO-UNDO.
DEFINE VARIABLE departure       AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bl-guest        AS CHARACTER  NO-UNDO.
DEFINE VARIABLE l-guest         AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bl-instruct     AS CHARACTER  NO-UNDO.
DEFINE VARIABLE resno           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE in-word         AS CHARACTER  NO-UNDO.
DEFINE VARIABLE room-cat        AS CHARACTER  NO-UNDO.
DEFINE VARIABLE city            AS CHARACTER NO-UNDO. /*020317*/
DEFINE VARIABLE country         AS CHARACTER NO-UNDO.
DEFINE VARIABLE zip             AS CHARACTER NO-UNDO.
DEFINE VARIABLE hp-guest        AS CHARACTER NO-UNDO.
DEFINE VARIABLE phone           AS CHARACTER NO-UNDO.

DEFINE VARIABLE sstr1           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE sstr2           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE sstr3           AS CHARACTER  NO-UNDO.
DEFINE VARIABLE w-length        AS INTEGER INITIAL 40.  /* bill.saldo WordLen */ 
DEFINE VARIABLE progname        AS CHARACTER  NO-UNDO. 
DEFINE VARIABLE temp-amt        AS DECIMAL INITIAL 0.
DEFINE VARIABLE WI-gastnr       AS INTEGER  NO-UNDO.
DEFINE VARIABLE IND-gastnr      AS INTEGER  NO-UNDO.


DEFINE VARIABLE ma-gst-amount             AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE ma-gst-tot-sales-artikel  AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE ma-gst-tot-non-taxable    AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE ma-gst-tot-taxable        AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE ma-gst-gtot-tax           AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE curr-guest                AS CHAR           NO-UNDO.


/*ITA 251017 --> add for Cambodia*/
DEFINE VARIABLE tot-inclvat  AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE net-amount   AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE serv-code    AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE acc-tax      AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE vat-cam      AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE do-it        AS LOGICAL NO-UNDO.

DEFINE VARIABLE membernumber            AS CHAR           NO-UNDO.

DEFINE VARIABLE mgst         AS DECIMAL NO-UNDO.
DEFINE VARIABLE artnr-1001   AS DECIMAL NO-UNDO.

/*Ragung add tax-code variable*/

DEFINE VARIABLE guest-taxcode AS CHAR NO-UNDO.
DEFINE VARIABLE nopd          AS CHAR NO-UNDO. /*ragung for pure hospitalyty*/

DEFINE VARIABLE tot-service-code          AS DECIMAL INIT 0 NO-UNDO.
DEFINE VARIABLE serv1                     AS DECIMAL        NO-UNDO.
DEFINE VARIABLE vat1                      AS DECIMAL        NO-UNDO.
DEFINE VARIABLE vat3                      AS DECIMAL        NO-UNDO.
DEFINE VARIABLE fact1                     AS DECIMAL        NO-UNDO.
DEFINE VARIABLE netto                     AS DECIMAL        NO-UNDO.

DEFINE BUFFER guest1 FOR guest.

DEFINE VARIABLE selected-room   AS CHAR.
IF inv-type = 9 AND NUM-ENTRIES(curr-program,";") GT 1 THEN
    ASSIGN
        selected-room = ENTRY(2,curr-program,";")
        curr-program  = ENTRY(1,curr-program,";").

FIND FIRST htparam WHERE htparam.paramnr = 415 NO-LOCK. 
briefnr2 = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 495 NO-LOCK. 
briefnr21 = htparam.finteger. 

/*sis 240913*/
FIND FIRST paramtext WHERE txtnr = 200 NO-LOCK. 
htl-name = paramtext.ptext. 
FIND FIRST paramtext WHERE txtnr = 201 NO-LOCK. 
htl-adr1 = paramtext.ptext. 
FIND FIRST paramtext WHERE txtnr = 202 NO-LOCK. 
htl-adr2 = paramtext.ptext. 
FIND FIRST paramtext WHERE txtnr = 203 NO-LOCK. 
htl-adr3 = paramtext.ptext. 
FIND FIRST paramtext WHERE txtnr = 204 NO-LOCK. 
htl-tel = paramtext.ptext. 
FIND FIRST paramtext WHERE txtnr = 205 NO-LOCK. 
htl-fax = paramtext.ptext. 
FIND FIRST paramtext WHERE txtnr = 206 NO-LOCK. 
htl-email = paramtext.ptext. 
/*end sis*/

FIND FIRST bill WHERE bill.rechnr = rechnr NO-LOCK NO-ERROR.

IF curr-program = "ns-invoice" THEN
DO:
    /**/
    DEFINE VARIABLE service-ns           AS DECIMAL.
    DEFINE VARIABLE vat-ns               AS DECIMAL.
    DEFINE VARIABLE amount-bef-tax-ns    AS DECIMAL INIT 0 NO-UNDO.
    DEFINE VARIABLE vat2-ns              AS DECIMAL.
    DEFINE VARIABLE fact-ns              AS DECIMAL INIT 1 NO-UNDO.

    FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
    IF AVAILABLE guest THEN
    DO:
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN membernumber = mc-guest.cardnum.

        /** paramnr 664 */
        bill-recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.NAME + " " + guest.anredefirma. /*Modified By Gerald 070120*/
       

        /** paramnr 643 - 645 */
        address1 = TRIM(guest.adresse1).
        address2 = TRIM(guest.adresse2).
        address3 = TRIM(guest.adresse3).
        city     = TRIM(guest.wohnort).
        country  = TRIM(guest.land).
        zip      = TRIM(guest.plz).
        /** paramnr 413 */
        hp-no = STRING(guest.mobil-telefon, "x(16)").
        phone = STRING(guest.telefon, "x(16)").
        guest-taxcode = STRING(guest.firmen-nr).
    END.

    /*Request ITA 140219*/
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.resnr = bill.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        FIND FIRST guest1 WHERE guest1.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN DO:
            ASSIGN hp-guest = STRING(guest.mobil-telefon, "x(16)").
        END.
    END.

    /** paramnr 673 */
    IF bill.flag = 0 THEN 
        bill-no = STRING(bill.rechnr) + " / " + STRING(bill.printnr). 
    ELSE IF bill.flag = 1 THEN 
        bill-no = STRING(bill.rechnr) + translateExtended ("(DUPLICATE)",lvCAREA,"").  
    
    /** paramnr 1096 */
    ASSIGN 
        ma-gst-amount            = 0
        ma-gst-tot-sales-artikel = 0
        ma-gst-tot-non-taxable   = 0
        ma-gst-tot-taxable       = 0.

    IF NOT spbill-flag THEN
    FOR EACH bill-line WHERE bill-line.rechnr = rechnr ,
        FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = bill-line.departement NO-LOCK 
        BY vhp.bill-line.bill-datum BY vhp.bill-line.zeit:
        IF artikel.artart = 0 OR artikel.artart = 1 
            OR artikel.artart = 8 OR artikel.artart = 9 THEN
            ASSIGN  bl0-balance     = bl0-balance + bill-line.betrag
                    bl0-balance1    = bl0-balance1 + bill-line.fremdwbetrag
                    bl-balance      = bl-balance + bill-line.betrag 
                    bl-balance1     = bl-balance1 + bill-line.fremdwbetrag. 

        IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
        DO:
            DO:
              ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
              IF bill-line.bill-datum LE 08/31/18 THEN DO:
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + (bill-line.betrag / 1.06).
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.
              ELSE DO:
                  IF artikel.artnr = 1001 OR artikel.artnr = 1002 THEN DO:
                       IF bill-line.betrag GT 0 THEN 
                            ASSIGN artnr-1001 = artnr-1001 + bill-line.betrag.
                        mgst   = mgst + bill-line.betrag.
                  END.
                  ELSE DO:
                      IF artikel.artnr NE 1001 THEN DO:
                          IF artikel.mwst-code NE 0 THEN
                              ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                          IF artikel.mwst-code EQ 0 THEN
                              ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                      END.                 
                  END.
              END.             
            END.

            /* Malik 7B6276 */
            IF artikel.service-code NE 0 THEN DO:
                RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                                        bill-line.bill-datum, OUTPUT serv1, OUTPUT vat1, OUTPUT vat3,
                                        OUTPUT fact1).
                ASSIGN netto = bill-line.betrag / fact1
                       tot-service-code = tot-service-code + (netto * serv1).                                           
            END.            
            /* END Malik */
              /*
              IF bill-line.bill-datum LE 05/31/18 THEN DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.artart = 1 THEN DO:
                         ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                  END.
                  ELSE DO:
                      IF artikel.mwst-code NE 0 THEN
                          ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                      IF artikel.mwst-code EQ 0 THEN
                          ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                  END.
              END.    
              ELSE DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + bill-line.betrag.
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.*/
        END.
    END.
    ELSE
    FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
        FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
        AND vhp.bill-line.rechnr = rechnr,
        FIRST artikel WHERE artikel.artnr = bill-line.artnr
            AND artikel.departement = bill-line.departement NO-LOCK 
        BY vhp.bill-line.bill-datum BY vhp.bill-line.zeit :
        ASSIGN  bl0-balance     = bl0-balance + bill-line.betrag
                bl0-balance1    = bl0-balance1 + bill-line.fremdwbetrag
                bl-balance      = bl-balance + bill-line.betrag 
                bl-balance1     = bl-balance1 + bill-line.fremdwbetrag. 
        
        IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
        DO:
            DO:
              ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
              IF bill-line.bill-datum LE 08/31/18 THEN DO:
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + (bill-line.betrag / 1.06).
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.
              ELSE DO:
                  IF artikel.artnr = 1001 OR artikel.artnr = 1002 THEN DO:
                       IF bill-line.betrag GT 0 THEN 
                            ASSIGN artnr-1001 = artnr-1001 + bill-line.betrag.
                        mgst   = mgst + bill-line.betrag.
                  END.
                  ELSE DO:
                      IF artikel.artnr NE 1001 THEN DO:
                          IF artikel.mwst-code NE 0 THEN
                              ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                          IF artikel.mwst-code EQ 0 THEN
                              ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                      END.                 
                  END.
              END.             
            END.
              /*
              IF bill-line.bill-datum LE 05/31/18 THEN DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.artart = 1 THEN DO:
                         ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                  END.
                  ELSE DO:
                      IF artikel.mwst-code NE 0 THEN
                          ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                      IF artikel.mwst-code EQ 0 THEN
                          ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                  END.
              END.    
              ELSE DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + bill-line.betrag.
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.*/
        END.
    END.

    IF ma-gst-amount NE 0 THEN DO:
          ASSIGN
              ma-gst-amount       = (ma-gst-amount * 6 / 100) + mgst.
              ma-gst-tot-taxable  = /*ma-gst-tot-taxable +*/ (ma-gst-tot-sales-artikel - ma-gst-amount - ma-gst-tot-non-taxable).
              ma-gst-gtot-tax     = ma-gst-amount + ma-gst-tot-taxable + ma-gst-tot-non-taxable.
             
    END.
    ELSE DO:
          IF artnr-1001 NE 0 THEN 
              ASSIGN ma-gst-amount       = artnr-1001
                     ma-gst-tot-taxable  = /*ma-gst-tot-taxable +*/ (ma-gst-tot-sales-artikel - artnr-1001 - ma-gst-tot-non-taxable).
          ma-gst-gtot-tax     = artnr-1001 + ma-gst-tot-taxable + ma-gst-tot-non-taxable.        
          
    END.

    IF briefnr = briefnr2 OR briefnr = briefnr21 THEN
        FIND FIRST htparam WHERE htparam.paramnr = 416 NO-LOCK. 
    ELSE FIND FIRST htparam WHERE htparam.paramnr = 410 NO-LOCK. 
    progname = htparam.fchar. 
                 
    IF (progname NE "") THEN 
    DO: 
        IF progname = "word_chinese.p" THEN 
        DO: 
            IF briefnr = briefnr2 THEN /* Revenue Amount IN Foreign Currency */ 
                RUN VALUE(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2, 
                    OUTPUT sstr3). 
            ELSE 
            DO: 
                IF bl0-balance NE 0 THEN RUN VALUE(progname) (bl0-balance, w-length, 
                    OUTPUT sstr1, OUTPUT sstr2, OUTPUT sstr3). 
                ELSE IF inv-type = 2  /** single line option **/ THEN 
                    RUN VALUE(progname) (bl-balance, w-length, OUTPUT sstr1, 
                OUTPUT sstr2, OUTPUT sstr3). 
                ELSE RUN VALUE(progname) (bill.saldo, w-length, OUTPUT sstr1, 
                    OUTPUT sstr2, OUTPUT sstr3). 
            END. 
            in-word = TRIM(sstr3).
        END. 
        ELSE
        DO: 
            IF briefnr = briefnr2 OR briefnr = briefnr21 
            THEN /* Revenue Amount IN Foreign Currency */ 
                RUN value(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2). 
            ELSE 
            DO: 
                IF bl0-balance NE 0 THEN 
                    RUN value(progname) (bl0-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
                ELSE IF inv-type = 2  /** single line option **/ THEN 
                    RUN value(progname) (bl-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
                ELSE RUN value(progname) (bill.saldo, w-length, OUTPUT sstr1, OUTPUT sstr2). 
            END. 
            in-word = TRIM(sstr1) + " " + TRIM(sstr2).
        END.               
    END.                   

    /*ITA 251017 --> for cambodia*/
    ASSIGN do-it = NO.
    FIND FIRST htparam WHERE htparam.paramnr = 271 NO-LOCK NO-ERROR.
    IF htparam.flogical THEN DO:
          RUN fobill-vatlistbl.p (pvILanguage, rechnr, OUTPUT TABLE bline-vatlist).
          FIND FIRST bline-vatlist NO-ERROR.
          IF AVAILABLE bline-vatlist THEN ASSIGN do-it = YES.
    END.
    
    FIND FIRST bill-line WHERE bill-line.rechnr = rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN DO:
        IF bill-line.departement = 0 THEN DO:
          nopd = "01.00171.400".
        END.
        ELSE IF bill-line.departement = 11 THEN DO:
          nopd = "01.00171.403".
        END.
        ELSE nopd = "01.00171.401".
    END.


    bl-balance = 0.
    IF curr-status = "design" THEN
    DO:
        IF htl-adr1     EQ ? THEN htl-adr1      = "".  
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF bill-recv    EQ ? THEN bill-recv     = "".
        IF bill-no      EQ ? THEN bill-no       = "".
        IF address1     EQ ? THEN address1      = "".
        IF address2     EQ ? THEN address2      = "".
        IF address3     EQ ? THEN address3      = "".
        IF hp-no        EQ ? THEN hp-no         = "".
        IF room-no      EQ ? THEN room-no       = "".
        IF arrival      EQ ? THEN arrival       = "".
        IF departure    EQ ? THEN departure     = "".
        IF bl-guest     EQ ? THEN bl-guest      = "".
        IF resno        EQ ? THEN resno         = "".
        IF user-init    EQ ? THEN user-init     = "".
        IF hp-guest     EQ ? THEN hp-guest      = "".
        IF phone        EQ ? THEN phone         = "".
        IF membernumber EQ ? THEN membernumber  = "".
        IF htl-name     EQ ? THEN htl-name      = "".
        IF htl-adr1     EQ ? THEN htl-adr1      = "".
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF htl-tel      EQ ? THEN htl-tel       = "".
        IF htl-fax      EQ ? THEN htl-fax       = "".
        IF htl-email    EQ ? THEN htl-email     = "".


        str1 =  "$bill-recv" + bill-recv + LnLDelimeter + 
                "$bill-no" + bill-no + LnLDelimeter + 
                "$bl-id" + user-init + LnLDelimeter + 
                "$Date" + STRING(TODAY, "99/99/9999") + LnLDelimeter + 
                "$bl-time" + STRING(TIME, "HH:MM").

        /*sis 250913*/
        str1 = str1 + LnLDelimeter +
                "$htl-name" + htl-name + LnLDelimeter +
                "$htl-adr1" + htl-adr1 + LnLDelimeter +
                "$htl-adr2" + htl-adr2 + LnLDelimeter +
                "$htl-adr3" + htl-adr3 + LnLDelimeter +
                "$htl-tel" + htl-tel + LnLDelimeter +
                "$htl-fax" + htl-fax + LnLDelimeter +
                "$htl-email" + htl-email + LnLDelimeter +
                "$gst-amount" + STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$tot-taxable" + STRING(ma-gst-tot-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$non-taxable" + STRING(ma-gst-tot-non-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$grand-total" + STRING(ma-gst-gtot-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$address1"    + address1      + LnLDelimeter + 
                "$address2"    + address2      + LnLDelimeter + 
                "$address3"    + address3      + LnLDelimeter + 
                "$city"        + city          + LnLDelimeter +
                "$country"     + country       + LnLDelimeter +
                "$zip"         + zip           + LnLDelimeter +
                "$hp-guest"    + hp-guest      + LnLDelimeter +
                "$phone"       + phone         + LnLDelimeter +
                "$memberno"    + membernumber  + LnLDelimeter + 
                "$guest-taxcode"  + guest-taxcode + LnLDelimeter + 
                "$nopd"           + nopd + LnLDelimeter +
                "$service-code" + STRING(tot-service-code, "->>>,>>>,>>>,>>>,>>9.99").

        /*end sis 250913*/

        str2 =  translateExtended("Date",lvCAREA, "") + LnLDelimeter +
                translateExtended("Description",lvCAREA, "") + LnLDelimeter +
                translateExtended("Qty",lvCAREA, "") + LnLDelimeter +
                translateExtended("Amount",lvCAREA, "") + LnLDelimeter +  
                translateExtended("Balance",lvCAREA, "") + LnLDelimeter +
                translateExtended("Voucher",lvCAREA, "") + LnLDelimeter +
                translateExtended("RoomNo",lvCAREA, "")  + LnLDelimeter +
                translateExtended("GST 6%",lvCAREA, "").
    
        IF inv-type = 2 THEN
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr = rechnr
                 NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
                /* paramnr 2306 */
                bl-voucher = "".
                /**
                RUN enter-single-line.p(OUTPUT bl-descript).
                **/
                bl-descript0 = ENTRY(1, bl-descript, "/").
                IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                DO:
                    /*MT 01/03/13 */
                    IF bl-descript MATCHES "*c/i*" 
                        OR bl-descript MATCHES "*c/o*"
                        THEN
                    DO:
                        IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                            bl-voucher   = ENTRY(3, bl-descript, "/").
                    END.
                    ELSE
                        bl-voucher   = ENTRY(2, bl-descript, "/").
                END.

                FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                    AND res-line.reslinnr = bill-line.billin-nr
                    AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                END.
                ELSE ASSIGN curr-guest = " ".

                bl-balance = bl-balance + bill-line.betrag.
                str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                        bl-descript + LnLDelimeter + 
                        STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                        STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        in-word + LnLDelimeter +
                        bl-guest + LnLDelimeter +
                        bl-descript0 + LnLDelimeter +
                        bl-voucher + LnLDelimeter +
                        bill-line.zinr + LnLDelimeter +
                        STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        curr-guest + LnLDelimeter +
                        STRING(" ")+ LnLDelimeter + 
                        STRING(" ") + LnLDelimeter +
                        STRING(bill-line.epreis, "->>>,>>>,>>>,>>>,>>9.99").
            END.

            IF do-it THEN DO:
                FIND FIRST bline-vatlist NO-LOCK NO-ERROR.
                IF AVAILABLE bline-vatlist THEN DO:
                    str3 = str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                           + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
                    FIND FIRST t-str3 NO-ERROR.
                    IF AVAILABLE t-str3 THEN
                        t-str3.str3 = t-str3.str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                                      + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").              
                END.
            END.    
        END.
        ELSE
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr = rechnr
                 NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
                bl-voucher = "".
                bl-descript = bill-line.bezeich.
                bl-descript0 = ENTRY(1, bl-descript, "/").
                IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                DO:
                    /*MT 01/03/13 */
                    IF bl-descript MATCHES "*c/i*" 
                        OR bl-descript MATCHES "*c/o*"
                        THEN
                    DO:
                        IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                            bl-voucher   = ENTRY(3, bl-descript, "/").
                    END.
                    ELSE
                        bl-voucher   = ENTRY(2, bl-descript, "/").
                END.

                FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                    AND res-line.reslinnr = bill-line.billin-nr
                    AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                END.
                ELSE ASSIGN curr-guest = " ".
                /* Malik 7B6276 */
                ASSIGN fact-ns = 1.
                FIND FIRST artikel WHERE artikel.artnr = 
                    bill-line.artnr AND artikel.departement = 
                    bill-line.departement NO-LOCK.
                IF artikel.mwst-code NE 0 OR artikel.service-code NE 0
                    OR artikel.prov-code NE 0 THEN
                RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement, 
                    bill-line.bill-datum, OUTPUT service-ns, OUTPUT vat-ns, 
                    OUTPUT vat2-ns, OUTPUT fact-ns).
                ASSIGN vat-ns = vat-ns + vat2-ns.
                
                amount-bef-tax-ns = bill-line.betrag.
                amount-bef-tax-ns = amount-bef-tax-ns / fact-ns.
                /* END Malik */
                           
                bl-balance = bl-balance + bill-line.betrag.
                str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                        bl-descript + LnLDelimeter + 
                        STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                        STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        in-word + LnLDelimeter +
                        bl-guest + LnLDelimeter +
                        bl-descript0 + LnLDelimeter +
                        bl-voucher + LnLDelimeter +
                        bill-line.zinr + LnLDelimeter +
                        STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        curr-guest + LnLDelimeter +
                        STRING(" ")+ LnLDelimeter + 
                        STRING(" ") + LnLDelimeter +
                        STRING(bill-line.epreis, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        STRING(amount-bef-tax-ns, "->>>,>>>,>>>,>>>,>>9.99") 
                        .
                        
            END.

            IF do-it THEN DO:
                FIND FIRST bline-vatlist NO-LOCK NO-ERROR.
                IF AVAILABLE bline-vatlist THEN DO:
                    str3 = str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                           + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
                    FIND FIRST t-str3 NO-ERROR.
                    IF AVAILABLE t-str3 THEN
                        t-str3.str3 = t-str3.str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                                      + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").              
                END.
            END.    
        END.
    END.
    ELSE IF curr-status = "print" THEN
    DO:
        IF htl-adr1     EQ ? THEN htl-adr1      = "".  
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF bill-recv    EQ ? THEN bill-recv     = "".
        IF bill-no      EQ ? THEN bill-no       = "".
        IF address1     EQ ? THEN address1      = "".
        IF address2     EQ ? THEN address2      = "".
        IF address3     EQ ? THEN address3      = "".
        IF hp-no        EQ ? THEN hp-no         = "".
        IF room-no      EQ ? THEN room-no       = "".
        IF arrival      EQ ? THEN arrival       = "".
        IF departure    EQ ? THEN departure     = "".
        IF bl-guest     EQ ? THEN bl-guest      = "".
        IF resno        EQ ? THEN resno         = "".
        IF user-init    EQ ? THEN user-init     = "".
        IF hp-guest     EQ ? THEN hp-guest      = "".
        IF phone        EQ ? THEN phone         = "".
        IF membernumber EQ ? THEN membernumber  = "".
        IF htl-name     EQ ? THEN htl-name      = "".
        IF htl-adr1     EQ ? THEN htl-adr1      = "".
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF htl-tel      EQ ? THEN htl-tel       = "".
        IF htl-fax      EQ ? THEN htl-fax       = "".
        IF htl-email    EQ ? THEN htl-email     = "".

       str1 =  "$bill-recv" + bill-recv + LnLDelimeter + 
                "$bill-no" + bill-no + LnLDelimeter + 
                "$bl-id" + user-init + LnLDelimeter + 
                "$Date" + STRING(TODAY, "99/99/9999") + LnLDelimeter + 
                "$bl-time" + STRING(TIME, "HH:MM"). 

        /*sis 250913*/
        str1 = str1 + LnLDelimeter +
                "$htl-name" + htl-name + LnLDelimeter +
                "$htl-adr1" + htl-adr1 + LnLDelimeter +
                "$htl-adr2" + htl-adr2 + LnLDelimeter +
                "$htl-adr3" + htl-adr3 + LnLDelimeter +
                "$htl-tel" + htl-tel + LnLDelimeter +
                "$htl-fax" + htl-fax + LnLDelimeter +
                "$htl-email" + htl-email + LnLDelimeter +
                "$gst-amount" + STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$tot-taxable" + STRING(ma-gst-tot-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$non-taxable" + STRING(ma-gst-tot-non-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$grand-total" + STRING(ma-gst-gtot-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$address1"    + address1      + LnLDelimeter + 
                "$address2"    + address2      + LnLDelimeter + 
                "$address3"    + address3      + LnLDelimeter + 
                "$city"        + city          + LnLDelimeter +
                "$country"     + country       + LnLDelimeter +
                "$zip"         + zip           + LnLDelimeter +
                "$hp-guest"    + hp-guest      + LnLDelimeter +
                "$phone"       + phone         + LnLDelimeter + 
                "$guest-taxcode"  + guest-taxcode + LnLDelimeter + 
                "$nopd"           + nopd + LnLDelimeter +
                "$service-code" + STRING(tot-service-code, "->>>,>>>,>>>,>>>,>>9.99")
                .
        /*end sis 250913*/

        str2 =  translateExtended("Date",lvCAREA, "") + LnLDelimeter +
                translateExtended("Description",lvCAREA, "") + LnLDelimeter +
                translateExtended("Qty",lvCAREA, "") + LnLDelimeter +
                translateExtended("Amount",lvCAREA, "") + LnLDelimeter + 
                translateExtended("Balance",lvCAREA, "") + LnLDelimeter +
                translateExtended("Voucher",lvCAREA, "") + LnLDelimeter +
                translateExtended("RoomNo",lvCAREA, "") + LnLDelimeter +
                translateExtended("GST 6%",lvCAREA, "").
    
        IF NOT spbill-flag THEN
        DO:
            IF inv-type = 2 THEN
            DO:
                temp-amt = 0.

                FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr AND
                    artikel.departement = bill-line.departement AND
                    (artikel.artart = 0 OR artikel.artart = 1 OR 
                     artikel.artart = 8 OR artikel.artart = 9) NO-LOCK :
                
                    FIND FIRST sum-tbl WHERE sum-tbl.mwst-code = artikel.mwst-code NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE sum-tbl THEN
                    DO:     
                        /**
                        RUN enter-single-line.p(OUTPUT bl-descript).
                        **/
                        
                        CREATE sum-tbl.
                        ASSIGN  sum-tbl.mwst-code   = artikel.mwst-code
                                sum-tbl.sum-desc    = bl-descript
                                sum-tbl.sum-amount  = bill-line.betrag
                                .
                        RELEASE sum-tbl.
                    END.
                    ELSE
                    DO:
                        temp-amt = sum-tbl.sum-amount.
                        temp-amt = temp-amt + bill-line.betrag.

                        ASSIGN sum-tbl.sum-amount = temp-amt.
                        RELEASE sum-tbl.
                    END.
                END.

                FOR EACH sum-tbl NO-LOCK :
                    sum-anz = 0.
                    FOR EACH bill-line WHERE bill-line.rechnr = rechnr
                        AND bill-line.artnr = sum-tbl.mwst-code NO-LOCK:
                        sum-anz = sum-anz + bill-line.anzahl.
                    END.
                    bl-voucher = "".
                    bl-descript = sum-tbl.sum-desc.
                    bl-descript0 = ENTRY(1, bl-descript, "/").
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                    DO:
                        /*MT 01/03/13 */
                        IF bl-descript MATCHES "*c/i*" 
                            OR bl-descript MATCHES "*c/o*"
                            THEN
                        DO:
                            IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                                bl-voucher   = ENTRY(3, bl-descript, "/").
                        END.
                        ELSE
                            bl-voucher   = ENTRY(2, bl-descript, "/").
                    END.
                    bl-balance = bl-balance + sum-tbl.sum-amount.

                    FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                        AND res-line.reslinnr = bill-line.billin-nr
                        AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                    END.
                    ELSE ASSIGN curr-guest = " ".

                    CREATE t-str3.
                    t-str3.str3 =  "" + LnLDelimeter + 
                              bl-descript + LnLDelimeter + 
                            /*MTSTRING(bill-line.anzahl, "->>>") + LnLDelimeter +*/
                            STRING(sum-anz, "->>>") + LnLDelimeter +
                            STRING(sum-tbl.sum-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                            STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            in-word + LnLDelimeter +
                            bl-guest + LnLDelimeter +
                            bl-descript0 + LnLDelimeter +
                            bl-voucher + LnLDelimeter +
                            bill-line.zinr + LnLDelimeter +
                            STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            curr-guest.
                END.
            END.
            ELSE IF inv-type = 3 THEN
            DO:
                temp-amt = 0.

                FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                    AND artikel.departement = bill-line.departement 
                    AND (artikel.artart = 0 OR artikel.artart = 1 
                         OR artikel.artart = 8 OR artikel.artart = 9) NO-LOCK 
                    BY bill-line.zinr BY bill-line.bezeich BY bill-line.bill-datum DESC: 

                    FIND FIRST sum-tbl WHERE sum-tbl.sum-desc = bill-line.bezeich NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE sum-tbl THEN
                    DO:        
                        CREATE sum-tbl.
                        ASSIGN  sum-tbl.sum-date    = STRING(bill-line.bill-datum)
                                sum-tbl.sum-desc    = bill-line.bezeich
                                sum-tbl.sum-amount  = bill-line.betrag
                                .
                        RELEASE sum-tbl.
                    END.
                    ELSE
                    DO:
                        temp-amt = sum-tbl.sum-amount.
                        temp-amt = temp-amt + bill-line.betrag.

                        ASSIGN sum-tbl.sum-amount = temp-amt.
                        RELEASE sum-tbl.
                    END.
                END.

                FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                    AND artikel.departement = bill-line.departement 
                    AND (artikel.artart = 2 OR artikel.artart = 5 
                         OR artikel.artart = 6 OR artikel.artart = 7) NO-LOCK 
                    BY bill-line.zinr BY bill-line.bezeich BY bill-line.bill-datum DESC: 

                    FIND FIRST sum-tbl WHERE sum-tbl.sum-desc = bill-line.bezeich NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE sum-tbl THEN
                    DO:        
                        CREATE sum-tbl.
                        ASSIGN  sum-tbl.sum-desc    = bill-line.bezeich
                                sum-tbl.sum-amount  = bill-line.betrag
                                .
                        RELEASE sum-tbl.
                    END.
                    ELSE
                    DO:
                        temp-amt = sum-tbl.sum-amount.
                        temp-amt = temp-amt + bill-line.betrag.

                        ASSIGN sum-tbl.sum-amount = temp-amt.
                        RELEASE sum-tbl.
                    END.
                END.

                FOR EACH sum-tbl NO-LOCK :
                    sum-anz = 0.
                    FOR EACH bill-line WHERE bill-line.rechnr = rechnr
                        AND bill-line.bezeich = sum-tbl.sum-desc NO-LOCK:
                        sum-anz = sum-anz + bill-line.anzahl.
                    END.
                    bl-voucher = "".
                    bl-descript = sum-tbl.sum-desc.
                    bl-descript0 = ENTRY(1, bl-descript, "/").
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                    DO:
                        /*MT 01/03/13 */
                        IF bl-descript MATCHES "*c/i*" 
                            OR bl-descript MATCHES "*c/o*"
                            THEN
                        DO:
                            IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                                bl-voucher   = ENTRY(3, bl-descript, "/").
                        END.
                        ELSE
                            bl-voucher   = ENTRY(2, bl-descript, "/").
                    END.
                    bl-balance = bl-balance + sum-tbl.sum-amount.

                    FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                        AND res-line.reslinnr = bill-line.billin-nr
                        AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                    END.
                    ELSE ASSIGN curr-guest = " ".

                    CREATE t-str3.
                    t-str3.str3 =   sum-tbl.sum-date + LnLDelimeter + 
                                    bl-descript + LnLDelimeter + 
                                    /*MTSTRING(bill-line.anzahl, "->>>") + LnLDelimeter +*/
                                    STRING(sum-anz, "->>>") + LnLDelimeter +
                                    STRING(sum-tbl.sum-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                                    STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                    in-word + LnLDelimeter +
                                    bl-guest + LnLDelimeter +
                                    bl-descript0 + LnLDelimeter +
                                    bl-voucher + LnLDelimeter +
                                    bill-line.zinr + LnLDelimeter +
                                    STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                    curr-guest + LnLDelimeter + 
                                    STRING(" ")+ LnLDelimeter + 
                                    STRING(" ").
                END.

                IF do-it THEN DO:
                    FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                        NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                        str3 =  STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter +
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter +  
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
        
                        CREATE t-str3.
                        ASSIGN t-str3.str3 = str3.              
                    END.
              END.   
            END.
            ELSE
            DO: 
                FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK :
                    bl-voucher = "".
                    bl-descript = bill-line.bezeich.
                    bl-descript0 = ENTRY(1, bl-descript, "/").
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                    DO:
                        /*MT 01/03/13 */
                        IF bl-descript MATCHES "*c/i*" 
                            OR bl-descript MATCHES "*c/o*"
                            THEN
                        DO:
                            IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                                bl-voucher   = ENTRY(3, bl-descript, "/").
                        END.
                        ELSE
                            bl-voucher   = ENTRY(2, bl-descript, "/").
                    END.

                    bl-balance = bl-balance + bill-line.betrag.

                    FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                        AND res-line.reslinnr = bill-line.billin-nr
                        AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                    END.
                    ELSE ASSIGN curr-guest = " ".

                    /* Malik 7B6276 */
                    ASSIGN fact-ns = 1.
                    FIND FIRST artikel WHERE artikel.artnr = 
                        bill-line.artnr AND artikel.departement = 
                        bill-line.departement NO-LOCK.
                    IF artikel.mwst-code NE 0 OR artikel.service-code NE 0
                        OR artikel.prov-code NE 0 THEN
                    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement, 
                        bill-line.bill-datum, OUTPUT service-ns, OUTPUT vat-ns, 
                        OUTPUT vat2-ns, OUTPUT fact-ns).
                    ASSIGN vat-ns = vat-ns + vat2-ns.
                    
                    amount-bef-tax-ns = bill-line.betrag.
                    amount-bef-tax-ns = amount-bef-tax-ns / fact-ns.
                    /* END Malik */

                    CREATE t-str3.
                    t-str3.str3 =   STRING(bill-line.bill-datum) + LnLDelimeter + 
                                    bl-descript + LnLDelimeter + 
                                    STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                                    STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                                    STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                    in-word + LnLDelimeter +
                                    bl-guest + LnLDelimeter +
                                    bl-descript0 + LnLDelimeter +
                                    bl-voucher + LnLDelimeter +
                                    bill-line.zinr + LnLDelimeter +
                                    STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                    curr-guest + LnLDelimeter +
                                    STRING(" ")+ LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bill-line.epreis, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                    STRING(amount-bef-tax-ns, "->>>,>>>,>>>,>>>,>>9.99") 
                                    .
                END.
                IF do-it THEN DO:
                    FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                        NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                        str3 =  STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter +
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter +  
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
        
                        CREATE t-str3.
                        ASSIGN t-str3.str3 = str3.              
                    END.
              END.   

            END.
        END.
        ELSE /** spbill-flag */
        DO:
            IF inv-type = 2 THEN
            DO:
                FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
                    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
                    AND vhp.bill-line.rechnr = rechnr,
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK
                    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit:

                    /**
                    RUN enter-single-line.p(OUTPUT bl-descript).
                    **/
                    bl-descript0 = ENTRY(1, bl-descript, "/").
                    bl-voucher = "".
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                    DO:
                        /*MT 01/03/13 */
                        IF bl-descript MATCHES "*c/i*" 
                            OR bl-descript MATCHES "*c/o*"
                            THEN
                        DO:
                            IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                                bl-voucher   = ENTRY(3, bl-descript, "/").
                        END.
                        ELSE
                            bl-voucher   = ENTRY(2, bl-descript, "/").
                    END.
                    
                    bl-balance = bl-balance + bill-line.betrag.
                    FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                        AND res-line.reslinnr = bill-line.billin-nr
                        AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                    END.
                    ELSE ASSIGN curr-guest = " ".

                    CREATE t-str3.
                    t-str3.str3 =  "" + LnLDelimeter + 
                            bl-descript + LnLDelimeter + 
                            STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                            STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                            STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            in-word + LnLDelimeter +
                            bl-guest + LnLDelimeter +
                            bl-descript0 + LnLDelimeter +
                            bl-voucher + LnLDelimeter +
                            bill-line.zinr + LnLDelimeter +
                            STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            curr-guest + LnLDelimeter +
                            STRING(" ")+ LnLDelimeter + 
                            STRING(" ") + LnLDelimeter +
                            STRING(bill-line.epreis, "->>>,>>>,>>>,>>>,>>9.99").
                END.
                IF do-it THEN DO:
                    FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                        NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                        str3 =  STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter +
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter +  
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
        
                        CREATE t-str3.
                        ASSIGN t-str3.str3 = str3.              
                    END.
                 END.   
            END.
            ELSE IF inv-type = 3 THEN
            DO:
                temp-amt = 0.

                FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
                    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
                    AND vhp.bill-line.rechnr = rechnr,
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                    AND artikel.departement = bill-line.departement NO-LOCK 
                    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit
                    BY bill-line.zinr BY bill-line.bezeich BY bill-line.bill-datum DESC: 
                      
                    FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                        AND res-line.reslinnr = bill-line.billin-nr
                        AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                    END.
                    ELSE ASSIGN curr-guest = " ".

                    bl-balance = bl-balance + bill-line.betrag.
                    str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                            bill-line.bezeich + LnLDelimeter + 
                            STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                            STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                            STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            in-word + LnLDelimeter +
                            bl-guest + LnLDelimeter +
                            bill-line.zinr + LnLDelimeter +
                            STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            curr-guest + LnLDelimeter +
                            STRING(" ")+ LnLDelimeter + 
                            STRING(" ") + LnLDelimeter +
                            STRING(bill-line.epreis, "->>>,>>>,>>>,>>>,>>9.99").
                END.

                IF do-it THEN DO:
                    FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                        NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                        str3 =  STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter +
                                " "         + LnLDelimeter + 
                                STRING(" ") + LnLDelimeter + 
                                " "         + LnLDelimeter +  
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter + 
                                " "         + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(" ") + LnLDelimeter +
                                STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
        
                        CREATE t-str3.
                        ASSIGN t-str3.str3 = str3.              
                    END.
                 END.   
            END.
            ELSE
            FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
                FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
                AND vhp.bill-line.rechnr = rechnr NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit:
                bl-voucher = "".
                bl-descript = bill-line.bezeich.
                bl-descript0 = ENTRY(1, bl-descript, "/").
                IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                DO:
                    /*MT 01/03/13 */
                    IF bl-descript MATCHES "*c/i*" 
                        OR bl-descript MATCHES "*c/o*"
                        THEN
                    DO:
                        IF NUM-ENTRIES(bl-descript, "/") GT 2 THEN
                            bl-voucher   = ENTRY(3, bl-descript, "/").
                    END.
                    ELSE
                        bl-voucher   = ENTRY(2, bl-descript, "/").
                END.
                bl-balance = bl-balance + bill-line.betrag.
                FIND FIRST res-line WHERE res-line.resnr = bill-line.massnr
                    AND res-line.reslinnr = bill-line.billin-nr
                    AND res-line.zinr     =  bill-line.zinr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN ASSIGN curr-guest = guest.NAME.
                END.
                ELSE ASSIGN curr-guest = " ".

                CREATE t-str3.
                t-str3.str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                        bl-descript + LnLDelimeter + 
                        STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                        STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        in-word + LnLDelimeter +
                        bl-guest + LnLDelimeter +
                        bl-descript0 + LnLDelimeter +
                        bl-voucher + LnLDelimeter +
                        bill-line.zinr + LnLDelimeter +
                        STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        curr-guest + LnLDelimeter +
                        STRING(" ")+ LnLDelimeter + 
                        STRING(" ") + LnLDelimeter +
                        STRING(bill-line.epreis, "->>>,>>>,>>>,>>>,>>9.99").
            END.
            IF do-it THEN DO:
                FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                    NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                    str3 =  STRING(" ") + LnLDelimeter + 
                            " "         + LnLDelimeter + 
                            STRING(" ") + LnLDelimeter +
                            " "         + LnLDelimeter + 
                            STRING(" ") + LnLDelimeter + 
                            " "         + LnLDelimeter +  
                            " "         + LnLDelimeter + 
                            " "         + LnLDelimeter + 
                            " "         + LnLDelimeter +
                            STRING(" ") + LnLDelimeter +
                            STRING(" ") + LnLDelimeter +
                            STRING(" ") + LnLDelimeter +
                            STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                            STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
    
                    CREATE t-str3.
                    ASSIGN t-str3.str3 = str3.              
                END.
             END.   
        END.
    END.
END.

ELSE IF curr-program = "fo-invoice" THEN
DO:
  DEFINE VARIABLE paidout           AS INTEGER INITIAL 0 NO-UNDO.
  DEFINE VARIABLE frate             AS DECIMAL INITIAL 1. 
  DEFINE VARIABLE rm-serv           AS LOGICAL. 
  DEFINE VARIABLE rm-vat            AS LOGICAL. 
  DEFINE VARIABLE service           AS DECIMAL.
  DEFINE VARIABLE vat               AS DECIMAL.
  DEFINE VARIABLE amount-bef-tax    AS DECIMAL INIT 0 NO-UNDO.
  DEFINE VARIABLE vat2              AS DECIMAL.
  DEFINE VARIABLE fact              AS DECIMAL INIT 1 NO-UNDO.

  FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE res-line THEN RETURN.

  FIND FIRST htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = htparam.finteger. 

  FOR EACH bline-list:
      DELETE bline-list. 
  END. 
 
  IF NOT spbill-flag THEN
  FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK 
      BY bill-line.sysdate BY bill-line.zeit: 
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
      AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE artikel THEN 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
          AND artikel.departement = 0 NO-LOCK.

      /*ITA
      FIND FIRST bline-list WHERE bline-list.artnr = bill-line.artnr 
          AND bline-list.dept = bill-line.departement 
          AND bline-list.bezeich = bill-line.bezeich 
          AND bline-list.datum = bill-line.bill-datum 
          AND bline-list.saldo = - bill-line.betrag NO-ERROR. 
      IF AVAILABLE bline-list THEN DELETE bline-list. 
      ELSE */
      DO: 
          CREATE bline-list. 
          BUFFER-COPY bill-line TO bline-list.
          ASSIGN 
            bline-list.bl-recid = RECID(bill-line)
            bline-list.dept     = bill-line.departement
            bline-list.datum    = bill-line.bill-datum
            bline-list.fsaldo   = 0
            bline-list.saldo    = bill-line.betrag
            bline-list.epreis   = bill-line.epreis
          . 
          RUN calc-bl-balance1(bill-line.bill-datum,
              bill-line.betrag, bill-line.fremdwbetrag,
              INPUT-OUTPUT bline-list.fsaldo).
      END.
  END. 
  ELSE
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES,
      FIRST bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
      AND bill-line.rechnr = rechnr NO-LOCK:
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
      AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE artikel THEN 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
          AND artikel.departement = 0 NO-LOCK.

      /*ITA
      FIND FIRST bline-list WHERE bline-list.artnr = bill-line.artnr 
          AND bline-list.dept = bill-line.departement 
          AND bline-list.bezeich = bill-line.bezeich 
          AND bline-list.datum = bill-line.bill-datum 
          AND bline-list.saldo = - bill-line.betrag NO-ERROR. 
      IF AVAILABLE bline-list THEN DELETE bline-list. 
      ELSE */
      DO:  
          CREATE bline-list. 
          BUFFER-COPY bill-line TO bline-list.
          ASSIGN 
            bline-list.bl-recid = RECID(bill-line)
            bline-list.dept     = bill-line.departement
            bline-list.datum    = bill-line.bill-datum
            bline-list.fsaldo   = 0
            bline-list.saldo    = bill-line.betrag
            bline-list.epreis   = bill-line.epreis
          . 
          RUN calc-bl-balance1(bill-line.bill-datum,
              bill-line.betrag, bill-line.fremdwbetrag,
              INPUT-OUTPUT bline-list.fsaldo).
      END.
  END.

  /************************************************/
  FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
  rm-vat = htparam.flogical. 
  FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
  rm-serv = htparam.flogical.
  FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK. 
  FIND FIRST artikel WHERE artikel.artnr = arrangement.artnr-logis 
      AND artikel.departement = 0 NO-LOCK. 
  IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
  ELSE 
  DO: 
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
  END.
  ASSIGN
      service = 0 
      vat = 0
    . 
  IF rm-serv THEN
  DO:
      FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
        service = htparam.fdecimal / 100. 
  END.
  IF rm-vat THEN
  DO:
      FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
        vat = htparam.fdecimal / 100. 
      FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
      IF htparam.flogical THEN vat = vat + vat * service. 
  END.
  

  FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK. 
  IF AVAILABLE guest THEN
  DO:
      ASSIGN  
              bill-recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.NAME + " " + guest.anredefirma     /* paramnr 664 */  /* Modified By Gerald 070120*/
              address1 = TRIM(guest.adresse1)     /** paramnr 643 */
              address2 = TRIM(guest.adresse2)     /** paramnr 644 */
              address3 = TRIM(guest.adresse3)     /** paramnr 645 */
              email    = TRIM(guest.email-adr)    /** paramnr 1087 */
              hp-no = STRING(guest.mobil-telefon, "x(16)")    /** paramnr 413 */
              phone = STRING(guest.telefon, "x(16)").
          .

      /** paramnr 658 */
      FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK NO-ERROR.
      WI-gastnr = htparam.finteger.
      FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK NO-ERROR.
      IND-gastnr = htparam.finteger.
      IF guest.karteityp = 0 OR guest.gastnr = WI-gastnr OR
          guest.gastnr = IND-gastnr THEN
          room-price = STRING(res-line.zipreis, ">>>,>>>,>>9.99").
      ELSE IF res-line.gastnrmember = res-line.gastnrpay THEN
          room-price = STRING(res-line.zipreis, ">>>,>>>,>>9.99").
  END.

  /*Request ITA 140219*/
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.resnr = bill.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN 
    DO:
        FIND FIRST guest1 WHERE guest1.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN 
        DO:
            ASSIGN hp-guest = STRING(guest1.mobil-telefon, "x(16)").
        END.
    END.

    /** paramnr 1096 */
  ma-gst-amount = 0.
  ma-gst-tot-sales-artikel = 0.
  ma-gst-tot-non-taxable = 0.
  ma-gst-tot-taxable = 0.
  mgst  = 0.
  FOR EACH bline-list NO-LOCK,
      FIRST bill-line WHERE RECID(bill-line) = bline-list.bl-recid NO-LOCK,
      FIRST artikel WHERE artikel.artnr = bill-line.artnr
        AND artikel.departement = bill-line.departement NO-LOCK
      BY vhp.bill-line.bill-datum BY vhp.bill-line.zeit :
      ASSIGN
          bl-balance      = bl-balance + bill-line.betrag
          bl0-balance1    = bl0-balance1 + bill-line.fremdwbetrag
          bl-balance1     = bl-balance1 + bill-line.fremdwbetrag.
      IF (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9) THEN
          bl0-balance = bl0-balance + bill-line.betrag. 
      ELSE IF artikel.artart = 6 AND artikel.zwkum = paidout THEN
          bl0-balance = bl0-balance + bill-line.betrag.

      IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
      DO:
            DO:
              ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
              IF bill-line.bill-datum LE 08/31/18 THEN DO:
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + (bill-line.betrag / 1.06).
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.
              ELSE DO:
                  IF artikel.artnr = 1001 OR artikel.artnr = 1002 THEN DO:
                       IF bill-line.betrag GT 0 THEN 
                            ASSIGN artnr-1001 = artnr-1001 + bill-line.betrag.
                        mgst   = mgst + bill-line.betrag.
                  END.
                  ELSE DO:
                      IF artikel.artnr NE 1001 THEN DO:
                          IF artikel.mwst-code NE 0 THEN
                              ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                          IF artikel.mwst-code EQ 0 THEN
                              ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                      END.                 
                  END.
              END.             
            END.
      END.
  END.
  IF ma-gst-amount NE 0 THEN DO:
      ASSIGN
          ma-gst-amount       = (ma-gst-amount * 6 / 100) + mgst.
          ma-gst-tot-taxable  = /*ma-gst-tot-taxable +*/ (ma-gst-tot-sales-artikel - ma-gst-amount - ma-gst-tot-non-taxable).
          ma-gst-gtot-tax     = ma-gst-amount + ma-gst-tot-taxable + ma-gst-tot-non-taxable.         
  END.
  ELSE DO:
      IF artnr-1001 NE 0 THEN 
          ASSIGN ma-gst-amount       = artnr-1001
                 ma-gst-tot-taxable  = /*ma-gst-tot-taxable +*/ (ma-gst-tot-sales-artikel - artnr-1001 - ma-gst-tot-non-taxable).
      ma-gst-gtot-tax     = artnr-1001 + ma-gst-tot-taxable + ma-gst-tot-non-taxable.        
  END.
  
  IF briefnr = briefnr2 OR briefnr = briefnr21 THEN
      FIND FIRST htparam WHERE htparam.paramnr = 416 NO-LOCK. 
  ELSE FIND FIRST htparam WHERE htparam.paramnr = 410 NO-LOCK. 
  progname = htparam.fchar. 

  IF (progname NE "") THEN 
  DO: 
      IF progname = "word_chinese.p" THEN 
      DO: 
          IF briefnr = briefnr2 THEN /* Revenue Amount IN Foreign Currency */ 
              RUN VALUE(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2, 
                  OUTPUT sstr3). 
          ELSE 
          DO: 
              IF bl0-balance NE 0 THEN RUN VALUE(progname) (bl0-balance, w-length, 
                  OUTPUT sstr1, OUTPUT sstr2, OUTPUT sstr3). 
              ELSE IF inv-type = 2  /** single line option **/ THEN 
                  RUN VALUE(progname) (bl-balance, w-length, OUTPUT sstr1, 
              OUTPUT sstr2, OUTPUT sstr3). 
              ELSE RUN VALUE(progname) (bill.saldo, w-length, OUTPUT sstr1, 
                  OUTPUT sstr2, OUTPUT sstr3). 
          END. 
          in-word = TRIM(sstr3).
      END. 
      ELSE
      DO: 
          IF briefnr = briefnr2 OR briefnr = briefnr21 
          THEN /* Revenue Amount IN Foreign Currency */ 
              RUN value(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2). 
          ELSE 
          DO: 
              IF bl0-balance NE 0 THEN 
                RUN value(progname) (bl0-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
              ELSE IF inv-type = 2  /** single line option **/ OR spbill-flag THEN 
                RUN value(progname) (bl-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
              ELSE RUN value(progname) (vhp.bill.saldo, w-length, OUTPUT sstr1, OUTPUT sstr2). 
          END. 
          in-word = TRIM(sstr1) + " " + TRIM(sstr2).
      END.               
  END.
  
  FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE res-line THEN 
  DO:
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN room-cat = zimmer.bezeich.  /*FT 6/8/12 room-cat*/
      
      /** paramnr 662 */
      room-no = TRIM(res-line.zinr).
      /** paramnr 655 - 656 */
      IF AVAILABLE bill AND bill.resnr GT 0 AND bill.reslinnr = 0 THEN
      DO:
          IF res-line.resstatus GE 6 AND res-line.resstatus LE 8 THEN
          DO:
              arrival = STRING(res-line.ankunft).
              departure = STRING(res-line.abreise).
          END.
      END.
      ELSE
      DO:
          arrival = STRING(res-line.ankunft).
          IF res-line.ankzeit NE 0 THEN
          DO:
              arrival   = STRING(res-line.ankunft) + " " + STRING(res-line.ankzeit,"HH:MM").
              departure = STRING(res-line.abreise) + " " + STRING(res-line.abreisezeit,"HH:MM").
          END.
      END.
    
      /** paramnr 2317 */
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
      DO:
         /* bl-guest = guest.name + ", " + guest.vorname1 + " " + guest.anrede1. */
          bl-guest = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.NAME . /* geral Request tiket FD55AD 29/11/2019 */
        
          FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE mc-guest THEN membernumber = mc-guest.cardnum.
      END.
    
      /** paramnr 607 */
      IF res-line.CODE NE "" THEN
      DO:
          FIND FIRST queasy WHERE queasy.KEY = 9 AND queasy.number1 = INTEGER(res-line.CODE) NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN bl-instruct = TRIM(queasy.char1).
      END.
    
    
      /** paramnr 663 */
      acc = STRING(res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis).
      
      /** paramnr 743 */
      adult = STRING(res-line.erwachs).
      
      /** paramnr 744 */
      child1 = STRING(res-line.kind1).
      
      /** paramnr 745 */
      child2 = STRING(res-line.kind2).
      
      /** paramnr 746 */
      complGst = STRING(res-line.gratis).
    
      /** paramnr 665 */
      resno = STRING(resnr).
  END.  
  /** paramnr 673 */
  IF bill.flag = 0 THEN 
      bill-no = STRING(bill.rechnr) + " / " + STRING(bill.printnr). 
  ELSE IF bill.flag = 1 THEN 
      bill-no = STRING(bill.rechnr) + translateExtended ("(DUPLICATE)",lvCAREA,""). 

  /*ITA 251017 --> for cambodia*/
  FIND FIRST htparam WHERE htparam.paramnr = 271 NO-LOCK NO-ERROR.
  IF htparam.flogical THEN DO:
      RUN fobill-vatlistbl.p (pvILanguage, rechnr, OUTPUT TABLE bline-vatlist).
      FIND FIRST bline-vatlist NO-ERROR.
      IF AVAILABLE bline-vatlist THEN ASSIGN do-it = YES.
  END.

  FIND FIRST bill-line WHERE bill-line.rechnr = rechnr NO-LOCK NO-ERROR.
  IF bill-line.departement = 0 THEN DO:
    nopd = "01.00171.400".
  END.
  ELSE IF bill-line.departement = 11 THEN DO:
    nopd = "01.00171.403".
  END.
  ELSE nopd = "01.00171.401".
  /************************************************/

  str1 =  "$bill-recv"      + bill-recv                         + LnLDelimeter + 
          "$bill-no"        + bill-no                           + LnLDelimeter + 
          "$address1"       + address1                          + LnLDelimeter + 
          "$address2"       + address2                          + LnLDelimeter + 
          "$address3"       + address3                          + LnLDelimeter + 
          "$email"          + email                             + LnLDelimeter +
          "$hp-no"          + hp-no                             + LnLDelimeter +
          "$acc"            + acc                               + LnLDelimeter + 
          "$adult"          + adult                             + LnLDelimeter + 
          "$child1"         + child1                            + LnLDelimeter + 
          "$child2"         + child2                            + LnLDelimeter + 
          "$complGst"       + complGst                          + LnLDelimeter + 
          "$room-no"        + room-no                           + LnLDelimeter + 
          "$room-price"     + room-price                        + LnLDelimeter + 
          "$arrival"        + arrival                           + LnLDelimeter + 
          "$arrival0"       + arrival                           + LnLDelimeter + 
          "$departure"      + departure                         + LnLDelimeter + 
          "$departure0"     + departure                         + LnLDelimeter + 
          "$bl-guest"       + TRIM(bl-guest)                    + LnLDelimeter + 
          "$bl-instruct"    + bl-instruct                       + LnLDelimeter + 
          "$resno"          + resno                             + LnLDelimeter + 
          "$bl-id"          + user-init                         + LnLDelimeter + 
          "$Date"           + STRING(TODAY, "99/99/9999")       + LnLDelimeter + 
          "$bl-time"        + STRING(TIME, "HH:MM")             + LnLDelimeter +
          "$room-cat"       + room-cat                          + LnLDelimeter +
          "$htl-name"       + htl-name                          + LnLDelimeter +
          "$htl-adr1"       + htl-adr1                          + LnLDelimeter +
          "$htl-adr2"       + htl-adr2                          + LnLDelimeter +
          "$htl-adr3"       + htl-adr3                          + LnLDelimeter +
          "$htl-tel"        + htl-tel                           + LnLDelimeter +
          "$htl-fax"        + htl-fax                           + LnLDelimeter +
          "$htl-email"      + htl-email                         + LnLDelimeter +
          "$gst-amount"     + STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
          "$tot-taxable"    + STRING(ma-gst-tot-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
          "$non-taxable"    + STRING(ma-gst-tot-non-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
          "$grand-total"    + STRING(ma-gst-gtot-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
          "$hp-guest"       + hp-guest      + LnLDelimeter +
          "$phone"          + phone         + LnLDelimeter +
          "$memberno"       + membernumber  + LnLDelimeter +
          "$nopd"           + nopd.

  
  str2 =  translateExtended("Date",lvCAREA, "")                 + LnLDelimeter +
          translateExtended("Description/Voucher",lvCAREA, "")  + LnLDelimeter +
          translateExtended("Qty",lvCAREA, "")                  + LnLDelimeter +
          translateExtended("RmNo",lvCAREA, "")                 + LnLDelimeter +
          translateExtended("Amount",lvCAREA, "")               + LnLDelimeter +  
          translateExtended("ID",lvCAREA, "")                   + LnLDelimeter +
          translateExtended("Guest Name",lvCAREA, "")           + LnLDelimeter +
          translateExtended("Description",lvCAREA, "")          + LnLDelimeter +
          translateExtended("Voucher",lvCAREA, "")              + LnLDelimeter +
          translateExtended("Amount Before Tax",lvCAREA, "")    + LnLDelimeter +
          translateExtended("Foreign Amount",lvCAREA, "")       + LnLDelimeter +
          translateExtended("Balance",lvCAREA, "")              + LnLDelimeter +
          translateExtended("In Word",lvCAREA, "")              + LnLDelimeter +
          translateExtended("GST 6%",lvCAREA, "").

  bl-balance = 0.
  IF curr-status = "design" THEN
  DO:
      FIND FIRST bline-list NO-LOCK NO-ERROR.
      IF NOT AVAILABLE bline-list THEN RETURN NO-APPLY.
      bl-descript = bline-list.bezeich.
      bl-descript0 = ENTRY(1, bl-descript, "/").
      IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
          bl-voucher   = ENTRY(2, bl-descript, "/").
      
      amount-bef-tax = bline-list.saldo.
      amount-bef-tax = amount-bef-tax / (1 + service + vat).

      bl-balance     = bl-balance + bline-list.saldo.
      ma-gst-amount     = 0.
      str3 = STRING(bline-list.datum) + LnLDelimeter + 
             bl-descript + LnLDelimeter + 
             STRING(bline-list.anzahl, "->>>") + LnLDelimeter +
             bline-list.zinr + LnLDelimeter + 
             STRING(bline-list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
             bline-list.userinit + LnLDelimeter +  
             bl-guest + LnLDelimeter + 
             bl-descript0 + LnLDelimeter + 
             bl-voucher + LnLDelimeter +
             STRING(amount-bef-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
             STRING(bline-list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
             STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
             in-word + LnLDelimeter +
             STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99").
      
      CREATE t-str3.
      ASSIGN t-str3.str3 = str3.

      IF do-it THEN DO:
        FIND FIRST bline-vatlist NO-LOCK NO-ERROR.
        IF AVAILABLE bline-vatlist THEN DO:
            str3 = str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                   + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            FIND FIRST t-str3 NO-ERROR.
            IF AVAILABLE t-str3 THEN
                t-str3.str3 = t-str3.str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                              + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").              
        END.
      END.    
  END.
  ELSE IF curr-status = "print" THEN
  DO:
      FOR EACH bline-list NO-LOCK:
          ASSIGN
              bl-voucher   = ""
              bl-descript  = bline-list.bezeich
              bl-descript0 = ENTRY(1, bl-descript, "/")
          .
          IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
              bl-voucher   = ENTRY(2, bl-descript, "/").

          /* SY AUG 13 2017 */
          ASSIGN fact = 1.
          FIND FIRST bill-line WHERE RECID(bill-line) = 
              bline-list.bl-recid NO-LOCK.
          FIND FIRST artikel WHERE artikel.artnr = 
              bill-line.artnr AND artikel.departement = 
              bill-line.departement NO-LOCK.
          IF artikel.mwst-code NE 0 OR artikel.service-code NE 0
              OR artikel.prov-code NE 0 THEN
          RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement, 
            bill-line.bill-datum, OUTPUT service, OUTPUT vat, 
            OUTPUT vat2, OUTPUT fact).
          ASSIGN vat = vat + vat2.
          
          amount-bef-tax = bline-list.saldo.
          amount-bef-tax = amount-bef-tax / fact.

          bl-balance     = bl-balance + bline-list.saldo.
          str3 =  STRING(bline-list.datum) + LnLDelimeter + 
                bl-descript + LnLDelimeter + 
                STRING(bline-list.anzahl, "->>>") + LnLDelimeter +
                bline-list.zinr + LnLDelimeter + 
                STRING(bline-list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                bline-list.userinit + LnLDelimeter +  
                bl-guest + LnLDelimeter + 
                bl-descript0 + LnLDelimeter + 
                bl-voucher + LnLDelimeter +
                STRING(amount-bef-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                STRING(bline-list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                in-word + LnLDelimeter +
                STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99")  + LnLDelimeter + 
                STRING(" ")+ LnLDelimeter + 
                STRING(" ").

          CREATE t-str3.
          ASSIGN t-str3.str3 = str3.
      END.


      IF do-it THEN DO:
            FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                str3 =  STRING(" ") + LnLDelimeter + 
                        " "         + LnLDelimeter + 
                        STRING(" ") + LnLDelimeter +
                        " "         + LnLDelimeter + 
                        STRING(" ") + LnLDelimeter + 
                        " "         + LnLDelimeter +  
                        " "         + LnLDelimeter + 
                        " "         + LnLDelimeter + 
                        " "         + LnLDelimeter +
                        STRING(" ") + LnLDelimeter +
                        STRING(" ") + LnLDelimeter +
                        STRING(" ") + LnLDelimeter +
                        " "         + LnLDelimeter +
                        STRING(" ") + LnLDelimeter + 
                        STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                        STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").

                CREATE t-str3.
                ASSIGN t-str3.str3 = str3.              
            END.
      END.   
  END.
END.
ELSE IF curr-program = "master-inv" THEN
DO:
    FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
    IF AVAILABLE guest THEN
    DO:
        FIND FIRST mc-guest WHERE mc-guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN membernumber = mc-guest.cardnum.

        /** paramnr 664 */
        bill-recv = guest.anrede1 + " . " + guest.vorname1 + " , " + guest.NAME 
                    + " " + guest.anredefirma. /*Modified by Gerald 070120*/

        /** paramnr 643 - 645 */
        address1 = TRIM(guest.adresse1).
        address2 = TRIM(guest.adresse2).
        address3 = TRIM(guest.adresse3).
    
        /** paramnr 413 */
        hp-no = STRING(guest.mobil-telefon, "x(16)").
        phone = STRING(guest.telefon, "x(16)").
        guest-taxcode = STRING(guest.firmen-nr).

    END.

    FIND FIRST res-line WHERE res-line.resnr = resnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        /** paramnr 662 */
        room-no = TRIM(res-line.zinr).

        /** paramnr 655 - 656 */
        IF AVAILABLE bill AND bill.resnr GT 0 AND bill.reslinnr = 0 THEN
        DO:
            IF res-line.resstatus GE 6 AND res-line.resstatus LE 8 THEN
            DO:
                arrival = STRING(res-line.ankunft).
                departure = STRING(res-line.abreise).
            END.
        END.
        ELSE
        DO:
            arrival = STRING(res-line.ankunft).
            IF res-line.ankzeit NE 0 THEN
            DO:
                arrival = STRING(res-line.ankunft) + " " 
                    + STRING(res-line.ankzeit,"HH:MM").
                departure = STRING(res-line.abreise) + " " 
                    + STRING(res-line.abreisezeit,"HH:MM").
            END.
        END.

        FIND FIRST guest1 WHERE guest1.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN DO:
            ASSIGN hp-guest = STRING(guest.mobil-telefon, "x(16)").
        END.

        /** paramnr 1094 */
        FOR EACH res-line WHERE res-line.resnr = resnr 
            AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 
            NO-LOCK BY res-line.name BY res-line.zinr: 
            IF res-line.NAME NE " " THEN
                bl-guest = bl-guest + res-line.NAME + "    # " + res-line.zinr + CHR(10).
        END.
    END.

    /** paramnr 673 */
    IF bill.flag = 0 THEN 
        bill-no = STRING(bill.rechnr) + " / " + STRING(bill.printnr). 
    ELSE IF bill.flag = 1 THEN 
        bill-no = STRING(bill.rechnr) + translateExtended ("(DUPLICATE)",lvCAREA,"").  

    /** paramnr 1096 */
    ma-gst-amount            = 0.
    ma-gst-tot-sales-artikel = 0.
    ma-gst-tot-non-taxable   = 0.
    ma-gst-tot-taxable       = 0.

    IF NOT spbill-flag THEN
    FOR EACH bill-line WHERE bill-line.rechnr = rechnr  ,
        FIRST artikel WHERE artikel.artnr = bill-line.artnr
            AND artikel.departement = bill-line.departement NO-LOCK
        BY vhp.bill-line.bill-datum BY vhp.bill-line.zeit :
        IF artikel.artart = 0 OR artikel.artart = 1 
            OR artikel.artart = 8 OR artikel.artart = 9 THEN
            ASSIGN  bl0-balance     = bl0-balance + bill-line.betrag
                    bl0-balance1    = bl0-balance1 + bill-line.fremdwbetrag
                    bl-balance      = bl-balance + bill-line.betrag 
                    bl-balance1     = bl-balance1 + bill-line.fremdwbetrag.

        /*IF (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9) THEN
              bl0-balance = bl0-balance + bill-line.betrag.*/ /*Eko, FOUND: Penyebab InWord menjadi Double*/
        ELSE IF artikel.artart = 6 AND artikel.zwkum = paidout THEN
              bl0-balance = bl0-balance + bill-line.betrag.

        IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
        DO:
            DO:
              ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
              IF bill-line.bill-datum LE 08/31/18 THEN DO:
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + (bill-line.betrag / 1.06).
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.
              ELSE DO:
                  IF artikel.artnr = 1001 OR artikel.artnr = 1002 THEN DO:
                       IF bill-line.betrag GT 0 THEN 
                            ASSIGN artnr-1001 = artnr-1001 + bill-line.betrag.
                        mgst   = mgst + bill-line.betrag.
                  END.
                  ELSE DO:
                      IF artikel.artnr NE 1001 THEN DO:
                          IF artikel.mwst-code NE 0 THEN
                              ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                          IF artikel.mwst-code EQ 0 THEN
                              ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                      END.                 
                  END.
              END.             
            END.


              /*
              IF bill-line.bill-datum LE 05/31/18 THEN DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.artart = 1 THEN DO:
                         ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                  END.
                  ELSE DO:
                      IF artikel.mwst-code NE 0 THEN
                          ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                      IF artikel.mwst-code EQ 0 THEN
                          ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                  END.
              END.    
              ELSE DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + bill-line.betrag.
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.*/
        END.
    END.
    ELSE
    FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
        FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
        AND vhp.bill-line.rechnr = rechnr,
        FIRST artikel WHERE artikel.artnr = bill-line.artnr
            AND artikel.departement = bill-line.departement NO-LOCK 
        BY vhp.bill-line.bill-datum BY vhp.bill-line.zeit :
        ASSIGN  bl0-balance     = bl0-balance + bill-line.betrag
                bl0-balance1    = bl0-balance1 + bill-line.fremdwbetrag
                bl-balance      = bl-balance + bill-line.betrag 
                bl-balance1     = bl-balance1 + bill-line.fremdwbetrag.           
        IF (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9) THEN
              bl0-balance = bl0-balance + bill-line.betrag. 
        ELSE IF artikel.artart = 6 AND artikel.zwkum = paidout THEN
              bl0-balance = bl0-balance + bill-line.betrag.

        IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
        DO:
            DO:
              ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
              IF bill-line.bill-datum LE 08/31/18 THEN DO:
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + (bill-line.betrag / 1.06).
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.
              ELSE DO:
                  IF artikel.artnr = 1001 OR artikel.artnr = 1002 THEN DO:
                       IF bill-line.betrag GT 0 THEN 
                            ASSIGN artnr-1001 = artnr-1001 + bill-line.betrag.
                        mgst   = mgst + bill-line.betrag.
                  END.
                  ELSE DO:
                      IF artikel.artnr NE 1001 THEN DO:
                          IF artikel.mwst-code NE 0 THEN
                              ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                          IF artikel.mwst-code EQ 0 THEN
                              ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                      END.                 
                  END.
              END.             
            END.

              /*
              IF bill-line.bill-datum LE 05/31/18 THEN DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.artart = 1 THEN DO:
                         ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                  END.
                  ELSE DO:
                      IF artikel.mwst-code NE 0 THEN
                          ma-gst-amount = ma-gst-amount + (bill-line.betrag / 1.06).
                      IF artikel.mwst-code EQ 0 THEN
                          ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
                  END.
              END.    
              ELSE DO:
                  ma-gst-tot-sales-artikel = ma-gst-tot-sales-artikel + bill-line.betrag.
                  IF artikel.mwst-code NE 0 THEN
                     ma-gst-tot-taxable = ma-gst-tot-taxable + bill-line.betrag.
                  IF artikel.mwst-code EQ 0 THEN
                     ma-gst-tot-non-taxable = ma-gst-tot-non-taxable + bill-line.betrag.
              END.*/
        END.
    END.

    IF ma-gst-amount NE 0 THEN DO:
      ASSIGN
          ma-gst-amount       = (ma-gst-amount * 6 / 100) + mgst.
          ma-gst-tot-taxable  = /*ma-gst-tot-taxable +*/ (ma-gst-tot-sales-artikel - ma-gst-amount - ma-gst-tot-non-taxable).
          ma-gst-gtot-tax     = ma-gst-amount + ma-gst-tot-taxable + ma-gst-tot-non-taxable.
         
    END.
    ELSE DO:
          IF artnr-1001 NE 0 THEN 
              ASSIGN ma-gst-amount       = artnr-1001
                     ma-gst-tot-taxable  = /*ma-gst-tot-taxable +*/ (ma-gst-tot-sales-artikel - artnr-1001 - ma-gst-tot-non-taxable).
          ma-gst-gtot-tax     = artnr-1001 + ma-gst-tot-taxable + ma-gst-tot-non-taxable.        
          
   END.

    IF briefnr = briefnr2 OR briefnr = briefnr21 THEN
        FIND FIRST htparam WHERE htparam.paramnr = 416 NO-LOCK. 
    ELSE FIND FIRST htparam WHERE htparam.paramnr = 410 NO-LOCK. 
    progname = htparam.fchar. 
                 
    IF (progname NE "") THEN 
    DO: 
        IF progname = "word_chinese.p" THEN 
        DO: 
            IF briefnr = briefnr2 THEN /* Revenue Amount IN Foreign Currency */ 
                RUN VALUE(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2, 
                    OUTPUT sstr3). 
            ELSE 
            DO: 
                IF bl0-balance NE 0 THEN RUN VALUE(progname) (bl0-balance, w-length, 
                    OUTPUT sstr1, OUTPUT sstr2, OUTPUT sstr3). 
                ELSE IF inv-type = 2  /** single line option **/ THEN 
                    RUN VALUE(progname) (bl-balance, w-length, OUTPUT sstr1, 
                OUTPUT sstr2, OUTPUT sstr3). 
                ELSE RUN VALUE(progname) (bill.saldo, w-length, OUTPUT sstr1, 
                    OUTPUT sstr2, OUTPUT sstr3). 
            END. 
            in-word = TRIM(sstr3).
        END. 
        ELSE
        DO: 
            IF briefnr = briefnr2 OR briefnr = briefnr21 
            THEN /* Revenue Amount IN Foreign Currency */ 
                RUN value(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2). 
            ELSE 
            DO: 
                IF bl0-balance NE 0 THEN 
                    RUN value(progname) (bl0-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
                ELSE IF inv-type = 2  /** single line option **/ THEN 
                    RUN value(progname) (bl-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
                ELSE RUN value(progname) (bill.saldo, w-length, OUTPUT sstr1, OUTPUT sstr2). 
            END. 
            in-word = TRIM(sstr1) + " " + TRIM(sstr2).
        END.               
    END.                   
    
    /*ITA 251017 --> for cambodia*/
    FIND FIRST htparam WHERE htparam.paramnr = 271 NO-LOCK NO-ERROR.
    IF htparam.flogical THEN DO:
          RUN fobill-vatlistbl.p (pvILanguage, rechnr, OUTPUT TABLE bline-vatlist).
          FIND FIRST bline-vatlist NO-ERROR.
          IF AVAILABLE bline-vatlist THEN ASSIGN do-it = YES.
    END.

    FIND FIRST bill-line WHERE bill-line.rechnr = rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN DO:
        IF bill-line.departement = 0 THEN DO:
          nopd = "01.00171.400".
        END.
        ELSE IF bill-line.departement = 11 THEN DO:
          nopd = "01.00171.403".
        END.
        ELSE nopd = "01.00171.401".
    END.

    bl-balance = 0.
    IF curr-status = "design" THEN
    DO:
        IF htl-adr1     EQ ? THEN htl-adr1      = "".  
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF bill-recv    EQ ? THEN bill-recv     = "".
        IF bill-no      EQ ? THEN bill-no       = "".
        IF address1     EQ ? THEN address1      = "".
        IF address2     EQ ? THEN address2      = "".
        IF address3     EQ ? THEN address3      = "".
        IF hp-no        EQ ? THEN hp-no         = "".
        IF room-no      EQ ? THEN room-no       = "".
        IF arrival      EQ ? THEN arrival       = "".
        IF departure    EQ ? THEN departure     = "".
        IF bl-guest     EQ ? THEN bl-guest      = "".
        IF resno        EQ ? THEN resno         = "".
        IF user-init    EQ ? THEN user-init     = "".
        IF hp-guest     EQ ? THEN hp-guest      = "".
        IF phone        EQ ? THEN phone         = "".
        IF membernumber EQ ? THEN membernumber  = "".
        IF htl-name     EQ ? THEN htl-name      = "".
        IF htl-adr1     EQ ? THEN htl-adr1      = "".
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF htl-tel      EQ ? THEN htl-tel       = "".
        IF htl-fax      EQ ? THEN htl-fax       = "".
        IF htl-email    EQ ? THEN htl-email     = "".
        

        str1 =  "$bill-recv" + bill-recv + LnLDelimeter + 
                "$bill-no" + bill-no + LnLDelimeter + 
                "$address1" + address1 + LnLDelimeter + 
                "$address2" + address2 + LnLDelimeter + 
                "$address3" + address3 + LnLDelimeter + 
                "$hp-no" + hp-no + LnLDelimeter +
                "$room-no" + room-no + LnLDelimeter + 
                "$arrival" + arrival + LnLDelimeter + 
                "$arrival0" + arrival + LnLDelimeter + 
                "$departure" + departure + LnLDelimeter + 
                "$departure0" + departure + LnLDelimeter + 
                "$bl-guest" + bl-guest + LnLDelimeter + 
                "$resno" + resno + LnLDelimeter + 
                "$bl-id" + user-init + LnLDelimeter + 
                "$Date" + STRING(TODAY, "99/99/9999") + LnLDelimeter + 
                "$bl-time" + STRING(TIME, "HH:MM") + LnLDelimeter +
                "$hp-guest"    + hp-guest      + LnLDelimeter +
                "$phone"       + phone          + LnLDelimeter +
                "$memberno"    + membernumber + LnLDelimeter +
                "$guest-taxcode"  + guest-taxcode + LnLDelimeter +
                "$nopd"           + nopd.  

        /*sis 250913*/
        str1 = str1 + LnLDelimeter +
                "$htl-name" + htl-name + LnLDelimeter +
                "$htl-adr1" + htl-adr1 + LnLDelimeter +
                "$htl-adr2" + htl-adr2 + LnLDelimeter +
                "$htl-adr3" + htl-adr3 + LnLDelimeter +
                "$htl-tel" + htl-tel + LnLDelimeter +
                "$htl-fax" + htl-fax + LnLDelimeter +
                "$htl-email" + htl-email + LnLDelimeter +
                "$gst-amount" + STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$tot-taxable" + STRING(ma-gst-tot-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$non-taxable" + STRING(ma-gst-tot-non-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$grand-total" + STRING(ma-gst-gtot-tax, "->>>,>>>,>>>,>>>,>>9.99").
        /*end sis 250913*/
            
        str2 =  translateExtended("Date",lvCAREA, "") + LnLDelimeter +
                translateExtended("RmNo",lvCAREA, "") + LnLDelimeter +
                translateExtended("Description",lvCAREA, "") + LnLDelimeter +
                translateExtended("Qty",lvCAREA, "") + LnLDelimeter +
                translateExtended("Amount",lvCAREA, "") + LnLDelimeter +  
                translateExtended("Balance",lvCAREA, "") + LnLDelimeter +
                translateExtended("ID",lvCAREA, "") + LnLDelimeter +
                translateExtended("Voucher",lvCAREA, "") + LnLDelimeter +
                translateExtended("GST 6%",lvCAREA, "").
    
        IF inv-type = 2 THEN 
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr = rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
                /*ITA*/
                FIND FIRST res-line WHERE res-line.resnr = resnr
                    AND res-line.zinr = bill-line.zinr
                    AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                    AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    ASSIGN l-guest = res-line.NAME.
                END.


                /**
                RUN enter-single-line.p(OUTPUT bl-descript).
                **/
                ASSIGN
                    bl-voucher   = ""
                    bl-descript0 = ENTRY(1, bl-descript, "/")
                .
                IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                           bl-voucher   = ENTRY(2, bl-descript, "/").
                
                bl-balance  = bl-balance + bill-line.betrag.
                str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                        bill-line.zinr + LnLDelimeter + 
                        bill-line.bezeich + LnLDelimeter + 
                        STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                        STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                        bill-line.userinit + LnLDelimeter +  
                        in-word + LnLDelimeter +
                        bl-guest + LnLDelimeter +
                        bl-descript0 + LnLDelimeter +
                        bl-voucher + LnLDelimeter +
                        STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        l-guest.
            END.


            IF do-it THEN DO:
                FIND FIRST bline-vatlist NO-LOCK NO-ERROR.
                IF AVAILABLE bline-vatlist THEN DO:
                    str3 = str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                           + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
                    FIND FIRST t-str3 NO-ERROR.
                    IF AVAILABLE t-str3 THEN
                        t-str3.str3 = t-str3.str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                                      + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").              
                END.
            END.           
        END.
        ELSE
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr = rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
                /*ITA*/
                FIND FIRST res-line WHERE res-line.resnr = resnr
                    AND res-line.zinr = bill-line.zinr
                    AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                    AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    ASSIGN l-guest = res-line.NAME.
                END.

                ASSIGN
                    bl-voucher   = ""
                    bl-descript  = bill-line.bezeich
                    bl-descript0 = ENTRY(1, bl-descript, "/").

                IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                           bl-voucher   = ENTRY(2, bl-descript, "/").
                bl-balance  = bl-balance + bill-line.betrag.
                str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                        bill-line.zinr + LnLDelimeter + 
                        bill-line.bezeich + LnLDelimeter + 
                        STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                        STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                        bill-line.userinit + LnLDelimeter +  
                        in-word + LnLDelimeter +
                        bl-guest + LnLDelimeter +
                        bl-descript0 + LnLDelimeter +
                        bl-voucher + LnLDelimeter +
                        STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        l-guest.
            END.

            IF do-it THEN DO:
                FIND FIRST bline-vatlist NO-LOCK NO-ERROR.
                IF AVAILABLE bline-vatlist THEN DO:
                    str3 = str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                           + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
                    FIND FIRST t-str3 NO-ERROR.
                    IF AVAILABLE t-str3 THEN
                        t-str3.str3 = t-str3.str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                                      + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").              
                END.
            END.     
        END.
    END.

    ELSE IF curr-status = "print" THEN
    DO:
        IF htl-adr1     EQ ? THEN htl-adr1      = "".  
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF bill-recv    EQ ? THEN bill-recv     = "".
        IF bill-no      EQ ? THEN bill-no       = "".
        IF address1     EQ ? THEN address1      = "".
        IF address2     EQ ? THEN address2      = "".
        IF address3     EQ ? THEN address3      = "".
        IF hp-no        EQ ? THEN hp-no         = "".
        IF room-no      EQ ? THEN room-no       = "".
        IF arrival      EQ ? THEN arrival       = "".
        IF departure    EQ ? THEN departure     = "".
        IF bl-guest     EQ ? THEN bl-guest      = "".
        IF resno        EQ ? THEN resno         = "".
        IF user-init    EQ ? THEN user-init     = "".
        IF hp-guest     EQ ? THEN hp-guest      = "".
        IF phone        EQ ? THEN phone         = "".
        IF membernumber EQ ? THEN membernumber  = "".
        IF htl-name     EQ ? THEN htl-name      = "".
        IF htl-adr1     EQ ? THEN htl-adr1      = "".
        IF htl-adr2     EQ ? THEN htl-adr2      = "".
        IF htl-adr3     EQ ? THEN htl-adr3      = "".
        IF htl-tel      EQ ? THEN htl-tel       = "".
        IF htl-fax      EQ ? THEN htl-fax       = "".
        IF htl-email    EQ ? THEN htl-email     = "".

        str1 =  "$bill-recv" + bill-recv + LnLDelimeter + 
                "$bill-no" + bill-no + LnLDelimeter + 
                "$address1" + address1 + LnLDelimeter + 
                "$address2" + address2 + LnLDelimeter + 
                "$address3" + address3 + LnLDelimeter + 
                "$hp-no" + hp-no + LnLDelimeter +
                "$room-no" + room-no + LnLDelimeter + 
                "$arrival" + arrival + LnLDelimeter + 
                "$arrival0" + arrival + LnLDelimeter + 
                "$departure" + departure + LnLDelimeter + 
                "$departure0" + departure + LnLDelimeter + 
                "$bl-guest" + bl-guest + LnLDelimeter + 
                "$resno" + resno + LnLDelimeter + 
                "$bl-id" + user-init + LnLDelimeter + 
                "$Date" + STRING(TODAY, "99/99/9999") + LnLDelimeter + 
                "$bl-time" + STRING(TIME, "HH:MM") + LnLDelimeter +
                "$hp-guest"    + hp-guest      + LnLDelimeter +
                "$phone"       + phone + LnLDelimeter +
                "$guest-taxcode"  + guest-taxcode + LnLDelimeter +
                "$nopd"           + nopd.  

        /*sis 250913*/
        str1 = str1 + LnLDelimeter +
                "$htl-name" + htl-name + LnLDelimeter +
                "$htl-adr1" + htl-adr1 + LnLDelimeter +
                "$htl-adr2" + htl-adr2 + LnLDelimeter +
                "$htl-adr3" + htl-adr3 + LnLDelimeter +
                "$htl-tel" + htl-tel + LnLDelimeter +
                "$htl-fax" + htl-fax + LnLDelimeter +
                "$htl-email" + htl-email + LnLDelimeter +
                "$gst-amount" + STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$tot-taxable" + STRING(ma-gst-tot-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$non-taxable" + STRING(ma-gst-tot-non-taxable, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                "$grand-total" + STRING(ma-gst-gtot-tax, "->>>,>>>,>>>,>>>,>>9.99").
        /*end sis 250913*/

        str2 =  translateExtended("Date",lvCAREA, "") + LnLDelimeter +
                translateExtended("RmNo",lvCAREA, "") + LnLDelimeter +
                translateExtended("Description",lvCAREA, "") + LnLDelimeter +
                translateExtended("Qty",lvCAREA, "") + LnLDelimeter +
                translateExtended("Amount",lvCAREA, "") + LnLDelimeter +  
                translateExtended("Balance",lvCAREA, "") + LnLDelimeter +
                translateExtended("ID",lvCAREA, "") + LnLDelimeter +
                translateExtended("Voucher",lvCAREA, "") + LnLDelimeter +
                translateExtended("GST 6%",lvCAREA, "").
    
        IF NOT spbill-flag THEN
        DO:
            IF inv-type = 2 THEN
            DO:
                /**
                RUN enter-single-line.p(OUTPUT bl-descript).
                **/

                FOR EACH bill-line WHERE bill-line.rechnr = rechnr,
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr AND
                    (artikel.artart = 0 OR artikel.artart = 1 OR 
                     artikel.artart = 8 OR artikel.artart = 9) NO-LOCK :

                    FIND FIRST sum-tbl WHERE sum-tbl.mwst-code = artikel.mwst-code NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE sum-tbl THEN
                    DO:     
                        /**
                        RUN enter-single-line.p(OUTPUT bl-descript).
                        **/

                        CREATE  sum-tbl.
                        ASSIGN  sum-tbl.mwst-code   = artikel.mwst-code
                                sum-tbl.sum-desc    = bl-descript
                                sum-tbl.sum-amount  = bill-line.betrag.

                        RELEASE sum-tbl.
                    END.
                    ELSE
                    DO:
                        temp-amt = sum-tbl.sum-amount.
                        temp-amt = temp-amt + bill-line.betrag.

                        ASSIGN sum-tbl.sum-amount = temp-amt.
                        RELEASE sum-tbl.
                    END.
                END.

                FOR EACH sum-tbl NO-LOCK :
                    ASSIGN
                        bl-voucher   = ""
                        bl-descript  = sum-tbl.sum-desc
                        bl-descript0 = ENTRY(1, bl-descript, "/")
                    .
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                               bl-voucher   = ENTRY(2, bl-descript, "/").
                    bl-balance = bl-balance + sum-tbl.sum-amount.

                    CREATE t-str3.
                    t-str3.str3 =   "" + LnLDelimeter + 
                                    "" + LnLDelimeter + 
                                    bl-descript + LnLDelimeter + 
                                    STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                                    STRING(sum-tbl.sum-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                                    STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                                    "" + LnLDelimeter +  
                                    in-word + LnLDelimeter +
                                    bl-guest + LnLDelimeter +
                                    bl-descript0 + LnLDelimeter +
                                    bl-voucher + LnLDelimeter +
                                    STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                    STRING(" ")+ LnLDelimeter + 
                                    STRING(" ").
                END.

                 IF do-it THEN DO:
                        FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                            NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                            str3 =  STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter +  
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                    STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            
                            CREATE t-str3.
                            ASSIGN t-str3.str3 = str3.              
                        END.
                 END.   
            END.
            ELSE IF inv-type = 4 THEN
            DO:
                temp-amt = 0.

                FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr 
                    AND artikel.departement = bill-line.departement NO-LOCK 
                    BY bill-line.zinr BY bill-line.bezeich BY bill-line.bill-datum DESC: 

                    FIND FIRST sum-tbl WHERE sum-tbl.sum-desc = bill-line.bezeich AND
                        sum-tbl.sum-roomnr = bill-line.zinr NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE sum-tbl THEN
                    DO:        
                        CREATE sum-tbl.
                        ASSIGN  sum-tbl.sum-date    = STRING(bill-line.bill-datum)
                                sum-tbl.sum-desc    = bill-line.bezeich
                                sum-tbl.sum-amount  = bill-line.betrag
                                sum-tbl.sum-roomnr  = bill-line.zinr
                                sum-tbl.sum-id      = bill-line.userinit
                                .
                        RELEASE sum-tbl.
                    END.
                    ELSE
                    DO:
                        temp-amt = sum-tbl.sum-amount.
                        temp-amt = temp-amt + bill-line.betrag.

                        ASSIGN sum-tbl.sum-amount = temp-amt.
                        RELEASE sum-tbl.
                    END.
                END.

                FOR EACH sum-tbl NO-LOCK :
                    sum-anz = 0.
                    FOR EACH bill-line WHERE bill-line.rechnr = rechnr
                        AND bill-line.bezeich = sum-tbl.sum-desc NO-LOCK:
                        sum-anz = sum-anz + bill-line.anzahl.
                    END.
                    
                    /*ITA*/
                    FIND FIRST res-line WHERE res-line.resnr = resnr
                        AND res-line.zinr = sum-tbl.sum-roomnr
                        AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                        AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        ASSIGN l-guest = res-line.NAME.
                    END.

                    ASSIGN
                        bl-voucher   = ""
                        bl-descript  = sum-tbl.sum-desc
                        bl-descript0 = ENTRY(1, bl-descript, "/")
                    .
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                               bl-voucher   = ENTRY(2, bl-descript, "/").
                    bl-balance = bl-balance + sum-tbl.sum-amount.

                    CREATE t-str3.
                    t-str3.str3 =  STRING(sum-tbl.sum-date) + LnLDelimeter + 
                                   sum-tbl.sum-roomnr + LnLDelimeter + 
                                   bl-descript + LnLDelimeter + 
                                   /*MTSTRING(bill-line.anzahl, "->>>") + LnLDelimeter +*/
                                   STRING(sum-anz, "->>>") + LnLDelimeter +
                                   STRING(sum-tbl.sum-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                                   STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                                   sum-tbl.sum-id + LnLDelimeter +  
                                   in-word + LnLDelimeter +
                                   bl-guest + LnLDelimeter +
                                   bl-descript0 + LnLDelimeter +
                                   bl-voucher + LnLDelimeter +
                                   STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                                   l-guest + LnLDelimeter +
                                   STRING(" ")+ LnLDelimeter + 
                                   STRING(" "). 
                END.
                  IF do-it THEN DO:
                        FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                            NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                            str3 =  STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter +  
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                    STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            
                            CREATE t-str3.
                            ASSIGN t-str3.str3 = str3.              
                        END.
                 END.   
            END.
            ELSE
                FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK :
                    ASSIGN
                        bl-voucher   = ""
                        bl-descript  = bill-line.bezeich
                        bl-descript0 = ENTRY(1, bl-descript, "/").

                    /*ITA*/
                    FIND FIRST res-line WHERE res-line.resnr = resnr
                        AND res-line.zinr = bill-line.zinr
                        AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                        AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        ASSIGN l-guest = res-line.NAME.
                    END.

                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                               bl-voucher   = ENTRY(2, bl-descript, "/").
                    bl-balance      = bl-balance + bill-line.betrag.
                    CREATE t-str3.
                    t-str3.str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                            bill-line.zinr + LnLDelimeter + 
                            bl-descript + LnLDelimeter + 
                            STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                            STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                            STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                            bill-line.userinit + LnLDelimeter +  
                            in-word + LnLDelimeter +
                            bl-guest + LnLDelimeter +
                            bl-descript0 + LnLDelimeter +
                            bl-voucher + LnLDelimeter +
                            STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            l-guest + LnLDelimeter +
                            STRING(" ")+ LnLDelimeter + 
                            STRING(" "). 
                END.
                  IF do-it THEN DO:
                        FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                            NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                            str3 =  STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter +  
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                    STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            
                            CREATE t-str3.
                            ASSIGN t-str3.str3 = str3.              
                        END.
                 END.   
        END.
        ELSE /** spbill */
        DO:
            IF inv-type = 2 THEN
            DO:
                FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
                FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
                AND vhp.bill-line.rechnr = rechnr,
                    FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK 
                    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit:

                    /**
                    RUN enter-single-line.p(OUTPUT bl-descript).
                    **/
                    ASSIGN
                        bl-voucher   = ""
                        bl-descript0 = ENTRY(1, bl-descript, "/")
                    .
                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
                               bl-voucher   = ENTRY(2, bl-descript, "/").
                    bl-balance = bl-balance + bill-line.betrag.

                    /*ITA*/
                    FIND FIRST res-line WHERE res-line.resnr = resnr
                        AND res-line.zinr = bill-line.zinr
                        AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                        AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        ASSIGN l-guest = res-line.NAME.
                    END.

                    CREATE t-str3.
                    t-str3.str3 =  "" + LnLDelimeter + 
                            "" + LnLDelimeter + 
                            bl-descript + LnLDelimeter + 
                            STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                            STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                            STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                            "" + LnLDelimeter +  
                            in-word + LnLDelimeter +
                            bl-guest + LnLDelimeter +
                            bl-descript0 + LnLDelimeter +
                            bl-voucher + LnLDelimeter +
                            STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            l-guest + LnLDelimeter +
                            STRING(" ")+ LnLDelimeter + 
                            STRING(" ").
                END.
                IF do-it THEN DO:
                        FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                            NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                            str3 =  STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter +  
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                    STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            
                            CREATE t-str3.
                            ASSIGN t-str3.str3 = str3.              
                        END.
                 END.   
            END.
            ELSE IF inv-type = 4 THEN
                FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
                FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
                AND vhp.bill-line.rechnr = rechnr NO-LOCK 
                BY vhp.bill-line.sysdate BY vhp.bill-line.zeit
                BY bill-line.zinr BY bill-line.bezeich BY bill-line.bill-datum DESC :
                    ASSIGN
                        bl-voucher   = ""
                        bl-descript  = bill-line.bezeich
                        bl-descript0 = ENTRY(1, bl-descript, "/").

                    IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN bl-voucher   = ENTRY(2, bl-descript, "/").
                    bl-balance      = bl-balance + bill-line.betrag.

                    /*ITA*/
                    FIND FIRST res-line WHERE res-line.resnr = resnr
                        AND res-line.zinr = bill-line.zinr
                        AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                        AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN DO:
                        ASSIGN l-guest = res-line.NAME.
                    END.

                    CREATE t-str3.
                    t-str3.str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                            bill-line.zinr + LnLDelimeter + 
                            bl-descript + LnLDelimeter + 
                            STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                            STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                            STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                            bill-line.userinit + LnLDelimeter +  
                            in-word + LnLDelimeter +
                            bl-guest + LnLDelimeter +
                            bl-descript0 + LnLDelimeter +
                            bl-voucher + LnLDelimeter +
                            STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                            l-guest + LnLDelimeter +
                            STRING(" ")+ LnLDelimeter + 
                            STRING(" "). 
                END.
                 IF do-it THEN DO:
                        FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                            NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                            str3 =  STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter +  
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                    STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            
                            CREATE t-str3.
                            ASSIGN t-str3.str3 = str3.              
                        END.
                 END.   
            ELSE
            FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
                FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
                AND vhp.bill-line.rechnr = rechnr NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit:
                ASSIGN
                    bl-voucher   = ""
                    bl-descript  = bill-line.bezeich
                    bl-descript0 = ENTRY(1, bl-descript, "/")
                .
                IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN bl-voucher   = ENTRY(2, bl-descript, "/").
                bl-balance      = bl-balance + bill-line.betrag.
                
                 /*ITA*/
                FIND FIRST res-line WHERE res-line.resnr = resnr
                    AND res-line.zinr = bill-line.zinr
                    AND res-line.resstatus NE 12 AND res-line.resstatus NE 9 
                    AND res-line.resstatus NE 10 AND res-line.resstatus NE 13 NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN DO:
                    ASSIGN l-guest = res-line.NAME.
                END.

                CREATE t-str3.
                t-str3.str3 =  STRING(bill-line.bill-datum) + LnLDelimeter + 
                        bill-line.zinr + LnLDelimeter + 
                        bl-descript + LnLDelimeter + 
                        STRING(bill-line.anzahl, "->>>") + LnLDelimeter +
                        STRING(bill-line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +  
                        bill-line.userinit + LnLDelimeter +  
                        in-word + LnLDelimeter +
                        bl-guest + LnLDelimeter +
                        bl-descript0 + LnLDelimeter +
                        bl-voucher + LnLDelimeter +
                        STRING(ma-gst-amount, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        l-guest + LnLDelimeter +
                        STRING(" ")+ LnLDelimeter + 
                        STRING(" "). 
            END.
                 IF do-it THEN DO:
                        FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                            NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                            str3 =  STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter +
                                    " "         + LnLDelimeter + 
                                    STRING(" ") + LnLDelimeter + 
                                    " "         + LnLDelimeter +  
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter + 
                                    " "         + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(" ") + LnLDelimeter +
                                    STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                                    STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
            
                            CREATE t-str3.
                            ASSIGN t-str3.str3 = str3.              
                        END.
                 END.   
        END.
    END.
END.
IF curr-program = "master-inv-room" THEN  /*FT*/
DO:
    FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
    IF AVAILABLE guest THEN
    DO:
        /** paramnr 664 */
        bill-recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.NAME 
                    + " " +  guest.anredefirma. /*Modified By Gerald 070120*/

        /** paramnr 643 - 645 */
        address1 = TRIM(guest.adresse1).
        address2 = TRIM(guest.adresse2).
        address3 = TRIM(guest.adresse3).
        city     = TRIM(guest.wohnort).
        country  = TRIM(guest.land).
        zip      = TRIM(guest.plz).

        /** paramnr 413 */
        hp-no = STRING(guest.mobil-telefon, "x(16)").
    END.

    EMPTY TEMP-TABLE bline-list.

    FOR EACH bill-line WHERE bill-line.rechnr = rechnr AND bill-line.zinr = selected-room:
        CREATE bline-list. 
        BUFFER-COPY bill-line TO bline-list.
        ASSIGN 
            bline-list.bl-recid = RECID(bill-line)
            bline-list.dept     = bill-line.departement
            bline-list.datum    = bill-line.bill-datum
            bline-list.fsaldo   = 0
            bline-list.saldo    = bill-line.betrag
            bline-list.epreis   = bill-line.epreis
          . 
        RUN calc-bl-balance1(bill-line.bill-datum,
            bill-line.betrag, bill-line.fremdwbetrag,
            INPUT-OUTPUT bline-list.fsaldo).
    END.

    FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.resstatus NE 12
        AND res-line.zinr = selected-room NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        reslinnr = res-line.reslinnr.
        /** paramnr 655 - 656 */
        IF AVAILABLE bill AND bill.resnr GT 0 AND bill.reslinnr = 0 THEN
        DO:
            IF res-line.resstatus GE 6 AND res-line.resstatus LE 8 THEN
            DO:
                arrival = STRING(res-line.ankunft).
                departure = STRING(res-line.abreise).
            END.
        END.
        ELSE
        DO:
            arrival = STRING(res-line.ankunft).
            IF res-line.ankzeit NE 0 THEN
            DO:
                arrival = STRING(res-line.ankunft) + " " + STRING(res-line.ankzeit,"HH:MM").
                departure = STRING(res-line.abreise) + " " + STRING(res-line.abreisezeit,"HH:MM").
            END.
        END.

            /** paramnr 2317 */
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
           /* bl-guest = guest.name + ", " + guest.vorname1 + " " + guest.anrede1. */
            bl-guest = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.NAME . /* geral Request tiket FD55AD 29/11/2019 */

        /** paramnr 663 */
        acc = STRING(res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis).
      
        /** paramnr 743 */
        adult = STRING(res-line.erwachs).
      
        /** paramnr 744 */
        child1 = STRING(res-line.kind1).
      
        /** paramnr 745 */
        child2 = STRING(res-line.kind2).
      
        /** paramnr 746 */
        complGst = STRING(res-line.gratis).
    
        /** paramnr 665 */
        resno = STRING(resnr).
    END.
    
    FIND FIRST zimmer WHERE zimmer.zinr = selected-room NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN room-cat = zimmer.bezeich.  /*FT 6/8/12 room-cat*/
    
    IF bill.flag = 0 THEN 
        bill-no = STRING(bill.rechnr) + " / " + STRING(bill.printnr). 
    ELSE IF bill.flag = 1 THEN 
        bill-no = STRING(bill.rechnr) + translateExtended ("(DUPLICATE)",lvCAREA,""). 

    /** paramnr 1096 */
    FOR EACH bline-list NO-LOCK,
        FIRST bill-line WHERE RECID(bill-line) = bline-list.bl-recid NO-LOCK,
        FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK :
        ASSIGN
            bl-balance      = bl-balance + bill-line.betrag
            bl0-balance1    = bl0-balance1 + bill-line.fremdwbetrag
            bl-balance1     = bl-balance1 + bill-line.fremdwbetrag.
        IF (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9) THEN
            bl0-balance = bl0-balance + bill-line.betrag. 
        ELSE IF artikel.artart = 6 AND artikel.zwkum = paidout THEN
            bl0-balance = bl0-balance + bill-line.betrag.
    END.
  
    IF briefnr = briefnr2 OR briefnr = briefnr21 THEN
        FIND FIRST htparam WHERE htparam.paramnr = 416 NO-LOCK. 
    ELSE FIND FIRST htparam WHERE htparam.paramnr = 410 NO-LOCK. 
    progname = htparam.fchar. 

    IF (progname NE "") THEN 
    DO: 
        IF progname = "word_chinese.p" THEN 
        DO: 
            IF briefnr = briefnr2 THEN /* Revenue Amount IN Foreign Currency */ 
                RUN VALUE(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2, OUTPUT sstr3). 
            ELSE 
            DO: 
                IF bl0-balance NE 0 THEN RUN VALUE(progname) (bl0-balance, w-length, 
                    OUTPUT sstr1, OUTPUT sstr2, OUTPUT sstr3). 
                ELSE IF inv-type = 2  /** single line option **/ THEN 
                    RUN VALUE(progname) (bl-balance, w-length, OUTPUT sstr1, OUTPUT sstr2, OUTPUT sstr3). 
                ELSE RUN VALUE(progname) (bill.saldo, w-length, OUTPUT sstr1, 
                  OUTPUT sstr2, OUTPUT sstr3). 
            END. 
            in-word = TRIM(sstr3).
        END. 
        ELSE
        DO: 
            IF briefnr = briefnr2 OR briefnr = briefnr21 
            THEN /* Revenue Amount IN Foreign Currency */ 
                RUN value(progname) (bl0-balance1, w-length, OUTPUT sstr1, OUTPUT sstr2). 
            ELSE 
            DO: 
                IF bl0-balance NE 0 THEN 
                    RUN value(progname) (bl0-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
                ELSE IF inv-type = 2  /** single line option **/ OR spbill-flag THEN 
                    RUN value(progname) (bl-balance, w-length, OUTPUT sstr1, OUTPUT sstr2). 
                ELSE RUN value(progname) (vhp.bill.saldo, w-length, OUTPUT sstr1, OUTPUT sstr2). 
            END. 
            in-word = TRIM(sstr1) + " " + TRIM(sstr2).
        END.               
    END.

    /*ITA 251017 --> for cambodia*/
      FIND FIRST htparam WHERE htparam.paramnr = 271 NO-LOCK NO-ERROR.
      IF htparam.flogical THEN DO:
          RUN fobill-vatlistbl.p (pvILanguage, rechnr, OUTPUT TABLE bline-vatlist).
          FIND FIRST bline-vatlist NO-ERROR.
          IF AVAILABLE bline-vatlist THEN ASSIGN do-it = YES.
      END.

    FIND FIRST bill-line WHERE bill-line.rechnr = rechnr NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN DO:
        IF bill-line.departement = 0 THEN DO:
          nopd = "01.00171.400".
        END.
        ELSE IF bill-line.departement = 11 THEN DO:
          nopd = "01.00171.403".
        END.
        ELSE nopd = "01.00171.401".
    END.

    /** paramnr 662 */
    room-no = selected-room.

    /** paramnr 673 */
    IF bill.flag = 0 THEN 
        bill-no = STRING(bill.rechnr) + " / " + STRING(bill.printnr). 
    ELSE IF bill.flag = 1 THEN 
        bill-no = STRING(bill.rechnr) + translateExtended ("(DUPLICATE)",lvCAREA,"").  
    /************************************************/

    ASSIGN
        str1 =  "$bill-recv"      + bill-recv                         + LnLDelimeter + 
            "$bill-no"        + bill-no                           + LnLDelimeter + 
            "$address1"       + address1                          + LnLDelimeter + 
            "$address2"       + address2                          + LnLDelimeter + 
            "$address3"       + address3                          + LnLDelimeter + 
            "$city"           + city                              + LnLDelimeter + 
            "$country"        + country                           + LnLDelimeter + 
            "$zip"            + zip                               + LnLDelimeter + 
            "$email"          + email                             + LnLDelimeter +
            "$hp-no"          + hp-no                             + LnLDelimeter +
            "$acc"            + acc                               + LnLDelimeter + 
            "$adult"          + adult                             + LnLDelimeter + 
            "$child1"         + child1                            + LnLDelimeter + 
            "$child2"         + child2                            + LnLDelimeter + 
            "$complGst"       + complGst                          + LnLDelimeter + 
            "$room-no"        + room-no                           + LnLDelimeter + 
            "$room-price"     + room-price                        + LnLDelimeter + 
            "$arrival"        + arrival                           + LnLDelimeter + 
            "$arrival0"       + arrival                           + LnLDelimeter + 
            "$departure"      + departure                         + LnLDelimeter + 
            "$departure0"     + departure                         + LnLDelimeter + 
            "$bl-guest"       + TRIM(bl-guest)                    + LnLDelimeter + 
            "$bl-instruct"    + bl-instruct                       + LnLDelimeter + 
            "$resno"          + resno                             + LnLDelimeter + 
            "$bl-id"          + user-init                         + LnLDelimeter + 
            "$Date"           + STRING(TODAY, "99/99/9999")       + LnLDelimeter + 
            "$bl-time"        + STRING(TIME, "HH:MM")             + LnLDelimeter +
            "$room-cat"       + room-cat                          + LnLDelimeter +
            "$htl-name"       + htl-name                          + LnLDelimeter +
            "$htl-adr1"       + htl-adr1                          + LnLDelimeter +
            "$htl-adr2"       + htl-adr2                          + LnLDelimeter +
            "$htl-adr3"       + htl-adr3                          + LnLDelimeter +
            "$htl-tel"        + htl-tel                           + LnLDelimeter +
            "$htl-fax"        + htl-fax                           + LnLDelimeter +
            "$htl-email"      + htl-email                         + LnLDelimeter +
            "$reslinnr"       + STRING(reslinnr)
        
        str2 =  translateExtended("Date",lvCAREA, "")                 + LnLDelimeter +
            translateExtended("Description/Voucher",lvCAREA, "")  + LnLDelimeter +
            translateExtended("Qty",lvCAREA, "")                  + LnLDelimeter +
            translateExtended("RmNo",lvCAREA, "")                 + LnLDelimeter +
            translateExtended("Amount",lvCAREA, "")               + LnLDelimeter +  
            translateExtended("ID",lvCAREA, "")                   + LnLDelimeter +
            translateExtended("Guest Name",lvCAREA, "")           + LnLDelimeter +
            translateExtended("Description",lvCAREA, "")          + LnLDelimeter +
            translateExtended("Voucher",lvCAREA, "")              + LnLDelimeter +
            translateExtended("Amount Before Tax",lvCAREA, "")    + LnLDelimeter +
            translateExtended("Foreign Amount",lvCAREA, "")       + LnLDelimeter +
            translateExtended("Balance",lvCAREA, "")              + LnLDelimeter +
            translateExtended("In Word",lvCAREA, "")
        bl-balance = 0.

    IF curr-status = "design" THEN
    DO:
        FIND FIRST bline-list NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bline-list THEN RETURN NO-APPLY.
        bl-descript = bline-list.bezeich.
        bl-descript0 = ENTRY(1, bl-descript, "/").
        IF NUM-ENTRIES(bl-descript, "/") GT 1 THEN
            bl-voucher   = ENTRY(2, bl-descript, "/").
        
        amount-bef-tax = bline-list.saldo.
        amount-bef-tax = amount-bef-tax / (1 + service + vat).
        
        bl-balance     = bl-balance + bline-list.saldo.
        str3 = STRING(bline-list.datum) + LnLDelimeter + 
               bl-descript + LnLDelimeter + 
               STRING(bline-list.anzahl, "->>>") + LnLDelimeter +
               bline-list.zinr + LnLDelimeter + 
               STRING(bline-list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
               bline-list.userinit + LnLDelimeter +  
               bl-guest + LnLDelimeter + 
               bl-descript0 + LnLDelimeter + 
               bl-voucher + LnLDelimeter +
               STRING(amount-bef-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
               STRING(bline-list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
               STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
               in-word
        .
        CREATE t-str3.
        ASSIGN t-str3.str3 = str3.

        IF do-it THEN DO:
            FIND FIRST bline-vatlist NO-LOCK NO-ERROR.
            IF AVAILABLE bline-vatlist THEN DO:
                str3 = str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                       + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").
                FIND FIRST t-str3 NO-ERROR.
                IF AVAILABLE t-str3 THEN
                    t-str3.str3 = t-str3.str3 + LnLDelimeter + STRING(bline-vatlist.bezeich, "x(25)")
                                  + LnLDelimeter + STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").              
            END.
        END.    
    END.
    ELSE IF curr-status = "print" THEN DO:
        FOR EACH bline-list NO-LOCK:
    
            IF NUM-ENTRIES(bline-list.bezeich, "/") GT 1 THEN
                bl-voucher   = ENTRY(2, bline-list.bezeich, "/").
    
            ASSIGN
                bl-descript = bline-list.bezeich
                bl-descript0 = ENTRY(1, bl-descript, "/")
                amount-bef-tax = bline-list.saldo
                amount-bef-tax = amount-bef-tax / (1 + service + vat)
                bl-balance     = bl-balance + bline-list.saldo
                str3 =  STRING(bline-list.datum) + LnLDelimeter + 
                        bl-descript + LnLDelimeter + 
                        STRING(bline-list.anzahl, "->>>") + LnLDelimeter +
                        bline-list.zinr + LnLDelimeter + 
                        STRING(bline-list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter + 
                        bline-list.userinit + LnLDelimeter +  
                        bl-guest + LnLDelimeter + 
                        bl-descript0 + LnLDelimeter + 
                        bl-voucher + LnLDelimeter +
                        STRING(amount-bef-tax, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        STRING(bline-list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        STRING(bl-balance, "->>>,>>>,>>>,>>>,>>9.99") + LnLDelimeter +
                        in-word + LnLDelimeter + 
                        STRING(" ") + LnLDelimeter + 
                        STRING(" ").
    
            CREATE t-str3.
            ASSIGN t-str3.str3 = str3.
        END.

        IF do-it THEN DO:
            FOR EACH bline-vatlist WHERE bline-vatlist.vatnr NE 0 
                NO-LOCK BY bline-vatlist.seqnr BY bline-vatlist.vatnr:
                str3 =  STRING(" ") + LnLDelimeter + 
                        " "         + LnLDelimeter + 
                        STRING(" ") + LnLDelimeter +
                        " "         + LnLDelimeter + 
                        STRING(" ") + LnLDelimeter + 
                        " "         + LnLDelimeter +  
                        " "         + LnLDelimeter + 
                        " "         + LnLDelimeter + 
                        " "         + LnLDelimeter +
                        STRING(" ") + LnLDelimeter +
                        STRING(" ") + LnLDelimeter +
                        STRING(" ") + LnLDelimeter +
                        " "         + LnLDelimeter +
                        STRING(bline-vatlist.bezeich, "x(25)")+ LnLDelimeter + 
                        STRING(bline-vatlist.betrag, "->>>,>>>,>>9.99").

                CREATE t-str3.
                ASSIGN t-str3.str3 = str3.              
            END.
       END.   
    END.
END.


PROCEDURE calc-bl-balance1:
DEF INPUT PARAMETER datum           AS DATE      NO-UNDO.
DEF INPUT PARAMETER betrag          AS DECIMAL   NO-UNDO.
DEF INPUT PARAMETER fremdwbetrag    AS DECIMAL   NO-UNDO.
DEF INPUT-OUTPUT PARAMETER fbetrag  AS DECIMAL   NO-UNDO.
DEFINE VARIABLE billdate            AS DATE.
DEFINE VARIABLE resline-exrate      AS DECIMAL NO-UNDO INIT 0.
DEF BUFFER rline FOR res-line.

    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
    billdate = vhp.htparam.fdate. 

    IF resnr = 0 THEN
    DO:
      fbetrag = fbetrag + fremdwbetrag.
      RETURN.
    END.    
    FIND FIRST rline WHERE rline.resnr = resnr
        AND (rline.resstatus = 6 OR rline.resstatus = 8)
        AND rline.reserve-dec GT 0 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE rline THEN fbetrag = fbetrag + fremdwbetrag.
    ELSE 
    DO:
        IF rline.reserve-dec NE 0 THEN
        DO:
            IF rline.ankunft = billdate THEN 
            DO: 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = rline.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN resline-exrate = waehrung.ankauf / waehrung.einheit. 
              ELSE resline-exrate = rline.reserve-dec. 
            END. 
            ELSE 
            DO: 
              FIND FIRST exrate WHERE exrate.datum = rline.ankunft 
                AND exrate.artnr = rline.betriebsnr NO-LOCK NO-ERROR. 
              IF AVAILABLE exrate THEN resline-exrate = exrate.betrag. 
              ELSE resline-exrate = rline.reserve-dec. 
            END. 
        END.

      IF resline-exrate NE 0 THEN fbetrag = fbetrag + betrag / resline-exrate.
      ELSE fbetrag = fbetrag + betrag / rline.reserve-dec.
    END.
END.

