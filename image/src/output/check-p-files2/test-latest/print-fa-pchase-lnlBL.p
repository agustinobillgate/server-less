/*+++++++++++++++++++++++++++++++++++++++++++++++
BL for print-fa-pchase-lnl
23 Desember 2014
Eko Prasetio
++++++++++++++++++++++++++++++++++++++++++++++++*/

DEFINE TEMP-TABLE tmp-tbl-data
FIELD str3 AS CHARACTER.

/*DEFINE VARIABLE docunr AS CHARACTER INITIAL "F130500003" NO-UNDO.*/

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER docunr       AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER LnLDelimeter AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER str1        AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER str2        AS CHARACTER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tmp-tbl-data.
    
{ Supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "print-fa-pchase-lnl".

/************************ Define Variables ****************************/
DEFINE VARIABLE long-digit          AS LOGICAL  NO-UNDO.
DEFINE VARIABLE foreign-currency    AS LOGICAL  INITIAL NO NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER.

DEFINE VARIABLE bill-recv   AS CHARACTER    NO-UNDO.
DEFINE VARIABLE address1    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE address2    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE cp-name     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE telp        AS CHARACTER    NO-UNDO.
DEFINE VARIABLE fax-no      AS CHARACTER    NO-UNDO.

DEFINE VARIABLE bill-no     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bill-date   AS CHARACTER    NO-UNDO.
DEFINE VARIABLE refer       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE fa-source   AS CHARACTER    NO-UNDO.
DEFINE VARIABLE dep-date    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE arr-date    AS CHARACTER    NO-UNDO.
/*MT 240512 */
DEFINE VARIABLE delivery-date  AS CHARACTER    NO-UNDO.

DEFINE VARIABLE bl-descript     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-qty          AS CHARACTER    NO-UNDO.
DEFINE VARIABLE d-unit          AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-price        AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-amount       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE c-exrate        AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-balance      AS CHARACTER    NO-UNDO.
DEFINE VARIABLE balance         AS DECIMAL      NO-UNDO.
DEFINE VARIABLE remark          AS CHARACTER    NO-UNDO.
/************************ WORKFILE ********************************************/

DEFINE WORKFILE op-list
    FIELD artnr AS INTEGER
    FIELD anzahl AS DECIMAL
    FIELD bezeich AS CHAR
    FIELD bez-aend AS LOGICAL INITIAL NO
    FIELD disc AS DECIMAL
    FIELD disc2 AS DECIMAL
    FIELD vat AS DECIMAL
    FIELD epreis AS DECIMAL
    FIELD epreis0 AS DECIMAL
    FIELD warenwert AS DECIMAL
    FIELD konto AS CHAR
    FIELD warenwert0 AS DECIMAL
    FIELD remark AS CHAR.

/*********************** Main Logic ************************************/
RUN str-header.
RUN str-data.

PROCEDURE str-header:
    FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
    long-digit = htparam.flogical. 
     
    FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
    price-decimal = htparam.finteger.
    
    FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = docunr AND fa-ordheader.supplier-nr > 0 
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE fa-ordheader THEN 
        FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = docunr AND fa-ordheader.supplier-nr = 0 
        NO-LOCK NO-ERROR.
    
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-ordheader.supplier-nr
        NO-LOCK NO-ERROR.
    
    IF AVAILABLE l-lieferant THEN
        ASSIGN  bill-recv   = l-lieferant.firma         /** param 664 */
                address1    = l-lieferant.adresse1      /** param 643 */
                address2    = l-lieferant.adresse2      /** param 644 */
                cp-name     = l-lieferant.namekontakt + ", " + l-lieferant.vorname1 
                              + " " + l-lieferant.anrede1      /** param 637 */
                telp        = l-lieferant.telefon       /** param 382 */
                fax-no      = l-lieferant.fax           /** param 691 */
                .
    IF AVAILABLE fa-ordheader THEN 
    DO:
       /** param 673 */
        bill-no = docunr.
        FIND FIRST fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-order THEN
        DO:
            IF fa-order.create-time > 0 THEN bill-no = bill-no + "*".
        END.
     ASSIGN  
         bill-date  = STRING(fa-ordheader.order-date)        /** param 672 */
         dep-date   = STRING(fa-ordheader.Credit-Term)       /** param 661 */
         remark     = fa-ordheader.Order-Desc                    /** param 692 */
         arr-date        = STRING(fa-ordheader.Expected-Delivery)              /** param 655 */
         delivery-date   = STRING(fa-ordheader.Expected-Delivery)
         refer           = STRING(fa-ordheader.pr-nr)
         .
    
     /** param 1088 */
        FIND FIRST parameters WHERE parameters.progname = "CostCenter" AND
            parameters.SECTION = "Name" AND 
            INTEGER(parameters.varname) = fa-ordheader.dept-nr NO-LOCK NO-ERROR.
        IF AVAILABLE parameters THEN fa-source = parameters.vstring.
    END.
    str1 =  "$bill-recv" + bill-recv + LnLDelimeter +
            "$address1" + address1 + LnLDelimeter +
            "$address2" + address2 + LnLDelimeter +
            "$name" + cp-name + LnLDelimeter +
            "$telp" + telp + LnLDelimeter +
            "$fax-no" + fax-no + LnLDelimeter +
            "$bill-no" + bill-no + LnLDelimeter +
            "$bill-date" + bill-date + LnLDelimeter +
            "$refer" + refer + LnLDelimeter +
            "$source" + fa-source + LnLDelimeter +
            "$dep-date" + dep-date + LnLDelimeter +
            "$arr-date" + arr-date + LnLDelimeter +
            "$delivery-date" + delivery-date + LnLDelimeter +
            "$remark" + remark
            .
  
    str2 =  translateExtended("DESCRIPTION",lvCAREA, "") + LnLDelimeter +
            translateExtended("DELIVDATE",lvCAREA, "") + LnLDelimeter +
            translateExtended("QTY",lvCAREA, "") + LnLDelimeter +
            /*translateExtended("UNIT",lvCAREA, "") + LnLDelimeter +*/
            translateExtended("PRICE UNIT",lvCAREA, "") + LnLDelimeter +
            translateExtended("AMOUNT",lvCAREA, "").
END PROCEDURE.

PROCEDURE str-data:
    /* Get data fa-pchase */
    DEFINE buffer l-art FOR l-artikel.
    DEFINE VARIABLE create-it AS LOGICAL.
    DEFINE VARIABLE curr-bez AS CHAR.
    DEFINE VARIABLE bez-aend AS LOGICAL.
    DEFINE VARIABLE disc AS DECIMAL.
    DEFINE VARIABLE disc2 AS DECIMAL.
    DEFINE VARIABLE tot-qty     AS DECIMAL      NO-UNDO.
    DEFINE VARIABLE vat AS DECIMAL.
    
    FOR EACH fa-order WHERE fa-order.order-nr = docunr AND
      fa-order.activeflag = 0 NO-LOCK BY fa-order.fa-pos :
      
      create-it = NO.
      bez-aend = NO.
      FIND FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK.
      curr-bez = mathis.NAME.
      
      disc = 0.
      disc2 = 0.
      
      FIND FIRST op-list WHERE op-list.artnr = fa-order.fa-nr
      AND op-list.epreis = fa-order.order-price
      AND op-list.bezeich = mathis.NAME
      AND op-list.disc = fa-order.discount1 AND op-list.disc2 = discount2
      /*AND op-list.konto = l-order.stornogrund*/  NO-ERROR.
      
      IF NOT AVAILABLE op-list OR create-it THEN
      DO:
        vat = 0.
        CREATE op-list.
        ASSIGN
            op-list.artnr = fa-order.fa-nr
            op-list.bezeich = curr-bez
            op-list.bez-aend = bez-aend
            op-list.epreis = fa-order.order-price
            op-list.epreis0 = fa-order.order-price
            /*op-list.konto = l-order.stornogrund*/
            op-list.remark = fa-order.fa-remarks
            .
            
            op-list.disc = fa-order.discount1.
            op-list.disc2 = fa-order.discount2.
            op-list.vat = fa-order.vat.
            
            disc = fa-order.discount1 / 100.
            disc2 = fa-order.discount2 / 100.
            vat = fa-order.vat / 100.
        
        /*END. */
      END.
      op-list.epreis0 = fa-order.order-price / (1 - disc) / (1 - disc2) / (1 + vat).
      op-list.anzahl = op-list.anzahl + fa-order.order-qty.
      op-list.warenwert = op-list.warenwert + fa-order.order-amount.
      op-list.warenwert0 = op-list.warenwert0
      + fa-order.order-amount / (1 - disc) / (1 - disc2) / (1 + vat).
      tot-qty = tot-qty + fa-order.order-qty.
    END.
    
    /* Converting data to TEMP-TABLE string */
    FOR EACH op-list NO-LOCK:
        /** param 2306 */
        bl-descript = op-list.bezeich.
        
        /** param 2305 */
        IF op-list.anzahl GE 10000 OR (- op-list.anzahl GE 10000) THEN
        bl-qty = STRING(op-list.anzahl, "->>>,>>9").
        ELSE IF op-list.anzahl GE 1000 OR (- op-list.anzahl GE 1000) THEN
        DO:
          IF op-list.anzahl GE 0 THEN bl-qty = STRING(op-list.anzahl, ">,>>9.99").
          ELSE bl-qty = STRING(op-list.anzahl, "->,>>9.9").
        END.
        ELSE
        DO:
          IF LENGTH(STRING(op-list.anzahl - ROUND(op-list.anzahl - 0.5,0))) GT 3 THEN
          bl-qty = STRING(op-list.anzahl, "->>9.999").
          ELSE bl-qty = STRING(op-list.anzahl, "->>9.99").
        END.
        
        /** param 2320
        FIND FIRST fa-artikel WHERE fa-artikel.nr = op-list.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-artikel THEN
        d-unit = STRING(fa-artikel.anzahl).*/
        
        /** param 2316 */
        balance = balance + op-list.warenwert.
        
        IF NOT long-digit THEN
        DO:
          /** param 2307 */
          IF op-list.epreis GE 10000000 THEN
                bl-price = STRING(op-list.epreis, "->>,>>>,>>>,>>>,>>9"). /*" >>>,>>>,>>9"*/ /*gerald tambah digit 1D9FD1*/
          ELSE
                bl-price = STRING(op-list.epreis, ">,>>>,>>9.99").  /*" >>>,>>>,>>9"*/ /*gerald tambah digit 1D9FD1*/
          
          IF price-decimal = 0 AND NOT foreign-currency THEN
          ASSIGN  bl-amount   = STRING(op-list.warenwert, "->>>,>>>,>>>,>>9.99")    /** param 2308 */  /*"->>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
                  bl-balance  = STRING(balance, "->>>,>>>,>>>,>>9.99")              /** param 2316 */  /*"->>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
          .
          ELSE IF price-decimal = 2 OR foreign-currency THEN
          ASSIGN  bl-amount   = STRING(op-list.warenwert, "->>>,>>>,>>>,>>9.99")    /** param 2308 */ /*"->>>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
                  bl-balance  = STRING(balance, "->>>,>>>,>>>,>>9.99")              /** param 2316 */ /*"->>>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
          . 
        END.
        ELSE
        ASSIGN  bl-price    = STRING(op-list.epreis, "->>>,>>>,>>>,>>9.99")      /** param 2307 */ /*">,>>>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
                bl-amount   = STRING(op-list.warenwert, "->>>,>>>,>>>,>>9.99")  /** param 2308 */ /*"->,>>>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
                bl-balance  = STRING(balance, "->>>,>>>,>>>,>>9.99")            /** param 2316 */ /*"->,>>>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
        .
        CREATE tmp-tbl-data.
        ASSIGN tmp-tbl-data.str3 = bl-descript + LnLDelimeter +
                                   arr-date + LnLDelimeter +
                                   bl-qty + LnLDelimeter +
                                   /*d-unit + LnLDelimeter + */
                                   bl-price + LnLDelimeter +
                                   bl-amount + LnLDelimeter +
                                   c-exrate + LnLDelimeter +
                                   bl-balance + LnLDelimeter +
                                   op-list.remark.
    END.
    
END PROCEDURE.
