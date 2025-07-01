DEFINE TEMP-TABLE str3-list
    FIELD str       AS CHAR.

DEFINE TEMP-TABLE esign-print NO-UNDO
    FIELD sign-nr       AS INT FORMAT ">>>" LABEL "No"
    FIELD sign-name     AS CHARACTER FORMAT "x(35)" LABEL "Name"
    FIELD sign-img      AS BLOB 
    FIELD sign-date     AS CHAR FORMAT "x(20)"
    FIELD sign-position AS CHAR FORMAT "x(25)"
    .

DEFINE TEMP-TABLE str1
    FIELD bill-recv        AS CHARACTER                         
    FIELD address1         AS CHARACTER                         
    FIELD address2         AS CHARACTER                         
    FIELD cp-name          AS CHARACTER                                
    FIELD telp             AS CHARACTER                         
    FIELD fax-no           AS CHARACTER                         
    FIELD bill-no          AS CHARACTER                          
    FIELD bill-date        AS DATE                          
    FIELD refer            AS CHARACTER                          
    FIELD po-source        AS CHARACTER
    FIELD po-number        AS CHARACTER 
    FIELD dep-date         AS INT                          
    FIELD arr-date         AS DATE
    FIELD created-by       AS CHARACTER
    FIELD delivery-date    AS DATE                     
    FIELD remark           AS CHARACTER                    
    FIELD globaldisc       AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
    FIELD bank-name        AS CHARACTER                    
    FIELD account          AS CHARACTER                    
    FIELD rekening         AS CHARACTER                    
    FIELD companytitle     AS CHARACTER 
    FIELD vat-code         AS CHARACTER
    FIELD afterdisc        AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
    FIELD htl-name         AS CHARACTER
    FIELD htl-adr          AS CHARACTER
    FIELD htl-tel          AS CHARACTER.

DEFINE TEMP-TABLE str3
    FIELD bl-descript       AS CHARACTER                                   
    FIELD arr-date          AS CHARACTER                              
    FIELD bl-qty            AS CHARACTER                               
    FIELD d-unit            AS CHARACTER                              
    FIELD bl-price          AS CHARACTER                              
    FIELD bl-amount         AS CHARACTER                              
    FIELD c-exrate          AS CHARACTER                              
    FIELD bl-balance        AS CHARACTER                              
    FIELD remark            AS CHARACTER                        
    FIELD konto             AS CHARACTER                        
    FIELD disc              AS DECIMAL   FORMAT "->>9.99"   
    FIELD disc2             AS DECIMAL   FORMAT "->>9.99"
    FIELD vat               AS DECIMAL   FORMAT "->>>,>>>,>>9.99" 
    FIELD disc-value        AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
    FIELD disc2-value       AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
    FIELD epreis0           AS DECIMAL   FORMAT ">>>,>>>,>>9.99"
    FIELD bl-vat            AS CHARACTER                             
    FIELD artnr             AS INTEGER
    FIELD brutto            AS DECIMAL   FORMAT ">>>,>>>,>>9.99"
    FIELD po-nr             AS CHARACTER                             
    FIELD po-source         AS CHARACTER                              
    FIELD vat1              AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
    FIELD vat2              AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
    /* add additional VAT field by Oscar (15 Oktober 2024) - D934AC */
    FIELD add-vat           AS DECIMAL   FORMAT "->>9.99"
    FIELD bl-amount-add-vat AS CHARACTER .

DEFINE INPUT PARAMETER pvILanguage  AS INT      NO-UNDO.
DEFINE INPUT PARAMETER LnLDelimeter AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER docunr       AS CHAR NO-UNDO.
/*NA 301220 - add parameter for print closed/cancelled PO*/
DEFINE INPUT PARAMETER stattype     AS INTEGER   NO-UNDO.
DEFINE INPUT PARAMETER curr-status  AS CHAR      NO-UNDO.
/*
DEFINE VARIABLE pvILanguage     AS INTEGER NO-UNDO.
DEFINE VARIABLE LnLDelimeter    AS CHAR NO-UNDO.  
LnLDelimeter = CHR(2).
DEFINE VARIABLE docunr          AS CHAR NO-UNDO.
docunr = "P190114008".
DEFINE VARIABLE stattype        AS INTEGER NO-UNDO.
stattype = 0.
DEFINE VARIABLE curr-status     AS CHAR NO-UNDO.
curr-status = "print".
*/
DEFINE OUTPUT PARAMETER TABLE FOR str3-list.
DEFINE OUTPUT PARAMETER TABLE FOR esign-print.
DEFINE OUTPUT PARAMETER TABLE FOR str1.
DEFINE OUTPUT PARAMETER TABLE FOR str3.
/* Malik Sreverless 74 
DEFINE VARIABLE str1            AS CHAR NO-UNDO.
DEFINE VARIABLE str2            AS CHAR NO-UNDO.
*/

/**/
{ supertransbl.i }.

/*ragung perbaikan format qty 2 digit dibelakang koma*/

DEF VAR lvCAREA AS CHAR INITIAL "print-pchase-lnl". 

/***************************** WIDGETS *************************************/ 
 
DEFINE WORKFILE op-list 
  FIELD artnr             AS INTEGER 
  FIELD anzahl            AS DECIMAL 
  FIELD bezeich           AS CHAR 
  FIELD bez-aend          AS LOGICAL INITIAL NO 
  FIELD disc              AS DECIMAL 
  FIELD disc2             AS DECIMAL 
  FIELD vat               AS DECIMAL 
  FIELD epreis            AS DECIMAL 
  FIELD epreis0           AS DECIMAL 
  FIELD warenwert         AS DECIMAL 
  FIELD konto             AS CHAR 
  FIELD warenwert0        AS DECIMAL
  FIELD remark            AS CHAR
  FIELD disc-value        AS DECIMAL
  FIELD disc2-value       AS DECIMAL
  FIELD brutto            AS DECIMAL
  FIELD vat-value         AS DECIMAL
  FIELD po-nr             AS CHARACTER
  /*gerald*/      
  FIELD vat-code          AS CHARACTER
  FIELD vat1              AS DECIMAL  
  FIELD vat2              AS DECIMAL
  /* add additional VAT field by Oscar (15 Oktober 2024) - D934AC */
  FIELD add-vat           AS DECIMAL
  FIELD warenwert-add-vat AS DECIMAL
  .

DEFINE VARIABLE long-digit          AS LOGICAL  NO-UNDO. 
DEFINE VARIABLE foreign-currency    AS LOGICAL  INITIAL NO. 
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
DEFINE VARIABLE po-source   AS CHARACTER    NO-UNDO.
DEFINE VARIABLE dep-date    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE arr-date    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE delivery-date  AS CHARACTER    NO-UNDO.

DEFINE VARIABLE bl-descript       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-qty            AS CHARACTER    NO-UNDO.
DEFINE VARIABLE d-unit            AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-price          AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-amount         AS CHARACTER    NO-UNDO.
DEFINE VARIABLE c-exrate          AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-balance        AS CHARACTER    NO-UNDO.
DEFINE VARIABLE balance           AS DECIMAL      NO-UNDO.
DEFINE VARIABLE remark            AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bank-name         AS CHARACTER    NO-UNDO.
DEFINE VARIABLE account           AS CHARACTER    NO-UNDO.
DEFINE VARIABLE rekening          AS CHARACTER    NO-UNDO.
DEFINE VARIABLE i                 AS INTEGER      NO-UNDO.
DEFINE VARIABLE globaldisc        AS DECIMAL      NO-UNDO.
DEFINE VARIABLE companytitle      AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-vat            AS CHARACTER    NO-UNDO.
DEFINE VARIABLE po-number         AS CHARACTER    NO-UNDO.
DEFINE VARIABLE bl-amount-add-vat AS CHARACTER    NO-UNDO.

DEFINE VARIABLE htl-name        AS CHAR NO-UNDO.
DEFINE VARIABLE htl-adr         AS CHAR NO-UNDO.
DEFINE VARIABLE htl-tel         AS CHAR NO-UNDO.
/*Naufal - Tambah variable untuk print siapa yang membuat po (Req Pak Dwi FE1018)*/
DEFINE VARIABLE created-by      AS CHAR NO-UNDO.
/*gerald*/
DEFINE VARIABLE vat-code        AS CHARACTER    NO-UNDO.
DEFINE VARIABLE vat1            AS DECIMAL      NO-UNDO.
DEFINE VARIABLE vat2            AS DECIMAL      NO-UNDO.
DEFINE VARIABLE p-app           AS LOGICAL      NO-UNDO.
DEFINE VARIABLE img-id-name     AS CHAR EXTENT 4.
DEFINE VARIABLE img-id-date     AS CHAR EXTENT 4.
DEFINE VARIABLE img-id-pos      AS CHAR EXTENT 4.
DEFINE VARIABLE tmp-liefnr AS INTEGER. /* Malik Serverless 74 */ 
DEFINE VARIABLE isCreated  AS LOGICAL. /* Malik Serverless 74 */ 



DEFINE BUFFER b-queasy FOR queasy.

htl-name = "". 
FIND FIRST paramtext WHERE txtnr = 240 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND ptexte NE "" THEN RUN decode-string(ptexte, OUTPUT htl-name). 

htl-adr = "". 
FIND FIRST paramtext WHERE txtnr = 201 NO-ERROR.
IF AVAILABLE paramtext THEN htl-adr = paramtext.ptexte.

htl-tel = "". 
FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
IF AVAILABLE paramtext THEN htl-tel = paramtext.ptexte.

PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
    s = in-str. 
    j = ASC(SUBSTR(s, 1, 1)) - 70. 
    len = LENGTH(in-str) - 1. 
    s = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END. 
/****************************************************************************/
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
/*Naufal - read PO approval param*/
FIND FIRST htparam WHERE htparam.paramnr = 71 NO-LOCK.
p-app = htparam.flogical.

/* Malik Serverless 74 */
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docunr AND 
    l-orderhdr.lief-nr > 0 NO-LOCK NO-ERROR.
IF AVAILABLE l-orderhdr THEN 
DO:
    tmp-liefnr = l-orderhdr.lief-nr.
END.
ELSE
DO:
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docunr AND 
    l-orderhdr.lief-nr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-orderhdr THEN 
    DO:
        tmp-liefnr = l-orderhdr.lief-nr.
    END.
    ELSE
    DO:
        tmp-liefnr = ?.
    END.
END.
/*
IF NOT AVAILABLE l-orderhdr THEN
    FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docunr AND 
    l-orderhdr.lief-nr = 0 NO-LOCK NO-ERROR.
*/    
IF tmp-liefnr NE ? THEN 
DO:
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK NO-ERROR. /* Malik Serverless 74 : l-lieferant.lief-nr = l-orderhdr.lief-nr -> l-lieferant.lief-nr = tmp-liefnr */
    IF AVAILABLE l-lieferant THEN 
    DO:
        DO i = 1 TO LENGTH(l-lieferant.bank):
            IF SUBSTR(l-lieferant.bank,i,3) MATCHES "a/n" THEN
            LEAVE.
        END.

        ASSIGN  
                bill-recv    = l-lieferant.firma         /** param 664 */
                address1     = l-lieferant.adresse1      /** param 643 */
                address2     = l-lieferant.adresse2      /** param 644 */
                cp-name      = l-lieferant.namekontakt + ", " + l-lieferant.vorname1 
                            + " " + l-lieferant.anrede1      /** param 637 */
                telp         = l-lieferant.telefon       /** param 382 */
                fax-no       = l-lieferant.fax           /** param 691 */
                bank-name    = SUBSTR(l-lieferant.bank,1, i - 2)
                account      = SUBSTR(l-lieferant.bank, i + 4, LENGTH(l-lieferant.bank))
                rekening     = l-lieferant.kontonr
                companytitle = l-lieferant.anredefirma.

        CREATE str1.
        ASSIGN 
            str1.bill-recv    = l-lieferant.firma
            str1.address1     = l-lieferant.adresse1 
            str1.address2     = l-lieferant.adresse2 
            str1.cp-name      = l-lieferant.namekontakt + ", " + l-lieferant.vorname1 + " " + l-lieferant.anrede1           
            str1.telp         = l-lieferant.telefon        
            str1.fax-no       = l-lieferant.fax            
            str1.bank-name    = SUBSTR(l-lieferant.bank,1, i - 2)                             
            str1.account      = SUBSTR(l-lieferant.bank, i + 4, LENGTH(l-lieferant.bank))     
            str1.rekening     = l-lieferant.kontonr      
            str1.companytitle = l-lieferant.anredefirma.  

        isCreated = YES. /* Malik Serverless 74, check if str1 is already created */    

        /*gerald*/
        FIND FIRST queasy WHERE queasy.KEY = 219 AND queasy.number1 = l-lieferant.lief-nr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                vat-code = queasy.char1
                vat1     = queasy.deci1
                vat2     = queasy.deci2.
            ASSIGN
                str1.vat-code = queasy.char1.
        END.
    END.
END.
/* END Malik */

IF AVAILABLE l-orderhdr THEN
DO:
    /** param 673 */
    bill-no = docunr.
    FIND FIRST l-order WHERE l-order.lief-nr = l-orderhdr.lief-nr AND
        l-order.docu-nr = docunr AND l-order.pos = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-order THEN
    DO:
        IF l-order.zeit > 0 THEN /*bill-no = bill-no + "*"*/ 
        DO:
          /*geral add queasy for reprint with parameter curr-status 8B3325*/
          IF curr-status = "design" THEN
          DO:
            bill-no = docunr + "-REPRINT". 
          END.
          ELSE
          DO:
            FIND FIRST queasy WHERE queasy.KEY = 240 AND queasy.char1 = l-order.docu-nr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
              CREATE queasy.
              ASSIGN 
                  queasy.KEY = 240
                  queasy.char1 = l-order.docu-nr.

              bill-no = docunr.
            END.
            ELSE 
            DO:
              FIND CURRENT queasy EXCLUSIVE-LOCK.
              queasy.number1 = queasy.number1 + 1.
              bill-no        = docunr + "-REPRINT" + STRING(queasy.number1).
              FIND CURRENT queasy NO-LOCK.
              RELEASE queasy.
            END.
          END.
          /*end geral*/
        END.
        /** param 652 */
        refer   = STRING(l-order.lief-fax[1]).
        ASSIGN globaldisc = l-order.warenwert.
        ASSIGN
            str1.refer      = refer
            str1.globaldisc = globaldisc
            str1.bill-no    = bill-no.
    END.   
    
    ASSIGN  
            bill-date     = STRING(l-orderhdr.bestelldatum)        /** param 672 */
            dep-date      = STRING(l-orderhdr.angebot-lief[2])       /** param 661 */
            remark        = l-orderhdr.lief-fax[3]                     /** param 692 */
            arr-date      = STRING(l-orderhdr.lieferdatum)              /** param 655 */
            delivery-date = STRING(l-orderhdr.lieferdatum)
            po-number     = l-order.docu-nr
            /*Naufal - Assign variable created by (Req Pak Dwi FE1018)*/
            created-by    = STRING(l-orderhdr.besteller).
    ASSIGN 
            str1.bill-date     = l-orderhdr.bestelldatum      
            str1.dep-date      = l-orderhdr.angebot-lief[2]
            str1.remark        = remark       
            str1.arr-date      = l-orderhdr.lieferdatum
            str1.delivery-date = l-orderhdr.lieferdatum
            str1.po-number     = po-number    
            str1.created-by    = l-orderhdr.besteller.

        
        
    /*FIND FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-order THEN
    DO:
        ASSIGN po-number = l-order.lief-fax[1].
    END.*/

    /** param 1088 */
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" AND
        parameters.SECTION = "Name" AND 
        INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] NO-LOCK NO-ERROR.
    IF AVAILABLE parameters THEN po-source = parameters.vstring.

    FIND FIRST waehrung WHERE waehrung.waehrungsnr = l-orderhdr.angebot-lief[3] 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
        IF htparam.fchar NE "" AND (htparam.fchar NE waehrung.wabkurz) THEN 
            foreign-currency = YES. 

        /** param 1107 */
        c-exrate = STRING(waehrung.wabkurz).
    END. 

    IF p-app THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ docunr NO-LOCK:
            FIND FIRST guestbook WHERE guestbook.gastnr EQ queasy.number2 AND guestbook.reserve-logic[2] NO-LOCK NO-ERROR.
            IF AVAILABLE guestbook THEN
            DO:
                CREATE esign-print.         
                ASSIGN 
                    esign-print.sign-nr         = queasy.number1
                    esign-print.sign-name       = ENTRY(2,guestbook.infostr,"|")
                    esign-print.sign-img        = guestbook.imagefile
                    esign-print.sign-date       = ENTRY(2,queasy.char3,"|")
                    esign-print.sign-position   = ENTRY(4,guestbook.infostr,"|")
                    img-id-name[queasy.number1] = ENTRY(2,guestbook.infostr,"|")
                    img-id-date[queasy.number1] = ENTRY(2,queasy.char3,"|")
                    img-id-pos[queasy.number1]  = ENTRY(4,guestbook.infostr,"|").
            END.
        END.
    END.
END.     
/*
str1 =  "$bill-recv"     + bill-recv                             + LnLDelimeter + 
        "$address1"      + address1                              + LnLDelimeter + 
        "$address2"      + address2                              + LnLDelimeter + 
        "$name"          + cp-name                               + LnLDelimeter + 
        "$telp"          + telp                                  + LnLDelimeter + 
        "$fax-no"        + fax-no                                + LnLDelimeter + 
        "$bill-no"       + bill-no                               + LnLDelimeter + 
        "$bill-date"     + bill-date                             + LnLDelimeter + 
        "$refer"         + refer                                 + LnLDelimeter + 
        "$source"        + po-source                             + LnLDelimeter + 
        "$dep-date"      + dep-date                              + LnLDelimeter +
        "$arr-date"      + arr-date                              + LnLDelimeter +
        "$delivery-date" + delivery-date                         + LnLDelimeter +
        "$remark"        + remark                                + LnLDelimeter +
        "$GlobDisc"      + STRING(globaldisc, "->>>,>>>,>>9.99") + LnLDelimeter +
        "$bankname"      + bank-name                             + LnLDelimeter +
        "$account"       + account                               + LnLDelimeter +
        "$rekening"      + rekening                              + LnLDelimeter +
        "$title"         + companytitle. 

str2 =  translateExtended("DESCRIPTION",lvCAREA, "")    + LnLDelimeter +
        translateExtended("DELIVDATE",lvCAREA, "")      + LnLDelimeter +
        translateExtended("QTY",lvCAREA, "")            + LnLDelimeter +
        translateExtended("UNIT",lvCAREA, "")           + LnLDelimeter +
        translateExtended("PRICE UNIT",lvCAREA, "")     + LnLDelimeter +
        translateExtended("AMOUNT",lvCAREA, "")         + LnLDelimeter +
        translateExtended("DISC",lvCAREA, "")           + LnLDelimeter +
        translateExtended("DISC2",lvCAREA, "")          + LnLDelimeter +
        translateExtended("VAT",lvCAREA, "")            + LnLDelimeter +
        translateExtended("PO Number",lvCAREA, "")     . /*wen*/
*/        

RUN do-billline.

FOR EACH op-list NO-LOCK :
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
         bl-qty = STRING(op-list.anzahl, "->>9.99").
       /* IF LENGTH(STRING(op-list.anzahl - ROUND(op-list.anzahl - 0.5,0))) GT 3 THEN
            bl-qty = STRING(op-list.anzahl, "->>9.999").
        ELSE bl-qty = STRING(op-list.anzahl, "->>9.99").*/
    END.

    /** param 2320 */
    FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-artikel THEN
        d-unit = l-artikel.traubensort.

    /** param 2316 */

    IF op-list.warenwert EQ op-list.warenwert-add-vat THEN
    DO:
      balance = balance + op-list.warenwert.
    END.
    ELSE
    DO:
      balance = balance + op-list.warenwert-add-vat.
    END.

    /*gerald if long-digit kebalik 12D7C7*/
    IF NOT long-digit THEN
    DO:
        /** param 2307 */
        IF price-decimal = 0 AND NOT foreign-currency THEN
        DO:
            ASSIGN  bl-amount         = STRING(op-list.warenwert, "->>>,>>>,>>>,>>9")    /** param 2308 */
                    bl-balance        = STRING(balance, "->>>,>>>,>>>,>>9")              /** param 2316 */
                    bl-amount-add-vat = STRING(op-list.warenwert-add-vat, "->>>,>>>,>>>,>>9")    
            .
            IF op-list.epreis GE 10000000 THEN
                bl-price = STRING(op-list.epreis, " >>>,>>>,>>>,>>9").
            ELSE
                bl-price = STRING(op-list.epreis, ">>>,>>>,>>>,>>9").
        END.
        ELSE IF price-decimal = 2 OR foreign-currency THEN
        DO:
            ASSIGN  bl-amount         = STRING(op-list.warenwert, "->,>>>,>>>,>>>,>>9.99")    /** param 2308 */
                    bl-balance        = STRING(balance, "->,>>>,>>>,>>>,>>9.99")              /** param 2316 */
                    bl-amount-add-vat = STRING(op-list.warenwert-add-vat, "->>>,>>>,>>>,>>9.99") /* Oscar (12/12/2024) - CACFD2 & F204C6 - show 2 digit decimal */             
                    .
            IF op-list.epreis GE 10000000 THEN
                bl-price = STRING(op-list.epreis, " >>,>>>,>>>,>>>,>>9.99").
            ELSE
                bl-price = STRING(op-list.epreis, ">>>,>>>,>>>,>>9.99").
        END.
        ASSIGN bl-vat      = STRING(op-list.vat-value, "->,>>>,>>>,>>9.99").
    END.
    ELSE        
        ASSIGN  bl-price          = STRING(op-list.epreis, ">,>>>,>>>,>>>,>>9")      /** param 2307 */
                bl-amount         = STRING(op-list.warenwert, "->>,>>>,>>>,>>>,>>9")  /** param 2308 */
                bl-amount-add-vat = STRING(op-list.warenwert-add-vat, "->>,>>>,>>>,>>>,>>9") /** param 2308 */
                bl-balance        = STRING(balance, "->>,>>>,>>>,>>>,>>9")            /** param 2316 */
                bl-vat            = STRING(op-list.vat-value, "->,>>>,>>>,>>9")
                po-nr             = op-list.po-nr.  
    
    CREATE str3-list.
    str3-list.str = bl-descript                                      + LnLDelimeter + 
                    arr-date                                         + LnLDelimeter +
                    bl-qty                                           + LnLDelimeter + 
                    d-unit                                           + LnLDelimeter + 
                    bl-price                                         + LnLDelimeter +  
                    bl-amount                                        + LnLDelimeter +
                    c-exrate                                         + LnLDelimeter +
                    bl-balance                                       + LnLDelimeter +
                    op-list.remark                                   + LnLDelimeter +
                    op-list.konto                                    + LnLDelimeter +
                    STRING(op-list.disc, "->>9.99")                  + LnLDelimeter +
                    STRING(op-list.disc2, "->>9.99")                 + LnLDelimeter +
                    STRING(op-list.vat, "->>9.99")                   + LnLDelimeter +
                    STRING(op-list.disc-value, "->>>,>>>,>>>,>>9")   + LnLDelimeter + 
                    STRING(op-list.disc2-value, "->>>,>>>,>>>,>>9")  + LnLDelimeter +
                    STRING(op-list.epreis0, ">>,>>>,>>>,>>>,>>9")    + LnLDelimeter +
                    bl-vat                                           + LnLDelimeter +
                    STRING(op-list.artnr, ">>>>>>>9")                + LnLDelimeter +
                    STRING(op-list.brutto, ">>>,>>>,>>>,>>9")        + LnLDelimeter +
                    po-nr                                            + LnLDelimeter +
                    po-source                                        + LnLDelimeter + 
                    STRING(vat1, "->,>>>,>>>,>>>,>>9.99")            + LnLDelimeter + 
                    STRING(vat2, "->,>>>,>>>,>>>,>>9.99")            + LnLDelimeter +
                    STRING(((op-list.add-vat - 1) * 100), "->>9.99") + LnLDelimeter +
                    bl-amount-add-vat.

    CREATE str3.
    ASSIGN
        str3.bl-descript   = bl-descript       
        str3.arr-date          = arr-date  
        str3.bl-qty            = bl-qty       
        str3.d-unit            = d-unit       
        str3.bl-price          = bl-price     
        str3.bl-amount         = bl-amount    
        str3.c-exrate          = c-exrate     
        str3.bl-balance        = bl-balance   
        str3.remark            = op-list.remark                                 
        str3.konto             = op-list.konto                                  
        str3.disc              = op-list.disc          
        str3.disc2             = op-list.disc2          
        str3.vat               = op-list.vat
        str3.disc-value        = op-list.disc-value
        str3.disc2-value       = op-list.disc2-value
        str3.epreis0           = op-list.epreis0
        str3.bl-vat            = bl-vat                                         
        str3.artnr             = op-list.artnr            
        str3.brutto            = op-list.brutto     
        str3.po-nr             = op-list.po-nr                                          
        str3.po-source         = po-source                                      
        str3.vat1              = vat1          
        str3.vat2              = vat2
        str3.add-vat           = ((op-list.add-vat - 1) * 100)
        str3.bl-amount-add-vat = bl-amount-add-vat.
END.

/*
str1 =  str1 + LnLDelimeter + "$AfterDisc"      + STRING(balance - globaldisc, "->>>,>>>,>>9.99")
             + LnLDelimeter + "$HN"        + htl-name 
             + LnLDelimeter + "$HA"        + htl-adr       
             + LnLDelimeter + "$HT"        + htl-tel
             /*Naufal - Tambah keyword untuk print created by (Req Pak Dwi FE1018)*/
             + LnLDelimeter + "$CreatedBy"  + created-by
             + LnLDelimeter + "$VC"         + vat-code
             + LnLDelimeter + "$n1"         + img-id-name[1]
             + LnLDelimeter + "$n2"         + img-id-name[2]
             + LnLDelimeter + "$n3"         + img-id-name[3]
             + LnLDelimeter + "$n4"         + img-id-name[4]
             + LnLDelimeter + "$d1"         + img-id-date[1]
             + LnLDelimeter + "$d2"         + img-id-date[2]
             + LnLDelimeter + "$d3"         + img-id-date[3]
             + LnLDelimeter + "$d4"         + img-id-date[4]
             + LnLDelimeter + "$p1"         + img-id-pos[1]
             + LnLDelimeter + "$p2"         + img-id-pos[2]
             + LnLDelimeter + "$p3"         + img-id-pos[3]
             + LnLDelimeter + "$p4"         + img-id-pos[4].

*/
/*
ASSIGN
    str1.afterdisc = balance - globaldisc
    str1.htl-name  = htl-name
    str1.htl-adr   = htl-adr 
    str1.htl-tel   = htl-tel.
*/    
/* Malik Serverless 74 */
IF isCreated THEN
DO:
    ASSIGN
        str1.afterdisc = balance - globaldisc
        str1.htl-name  = htl-name
        str1.htl-adr   = htl-adr 
        str1.htl-tel   = htl-tel.
END.
IF tmp-liefnr NE ? THEN
DO:
    FIND FIRST l-order WHERE l-order.lief-nr = l-orderhdr.lief-nr 
        AND l-order.docu-nr = docunr AND l-order.pos = 0 EXCLUSIVE-LOCK. 
    l-order.gedruckt = TODAY. 
    l-order.zeit = TIME. 
    FIND CURRENT l-order NO-LOCK. 
    RELEASE l-order.
END.
/* END Malik */


/*************************** PROCEDURES **************************************/
PROCEDURE do-billline: 
    DEFINE BUFFER l-art FOR l-artikel. 
    DEFINE VARIABLE create-it   AS LOGICAL      NO-UNDO. 
    DEFINE VARIABLE curr-bez    AS CHARACTER    NO-UNDO. 
    DEFINE VARIABLE bez-aend    AS LOGICAL      NO-UNDO. 
    DEFINE VARIABLE disc        AS DECIMAL      NO-UNDO. 
    DEFINE VARIABLE disc2       AS DECIMAL      NO-UNDO. 
    DEFINE VARIABLE disc-value  AS DECIMAL      NO-UNDO. 
    DEFINE VARIABLE disc2-value AS DECIMAL      NO-UNDO. 
    DEFINE VARIABLE tot-qty     AS DECIMAL      NO-UNDO.
    DEFINE VARIABLE vat         AS DECIMAL      NO-UNDO. 
    DEFINE VARIABLE vat-val     AS DECIMAL      NO-UNDO.
    DEFINE VARIABLE loeschflag  AS INTEGER      NO-UNDO. /* Naufal Afthar - 67A545*/
    /**
    saldo = 0. 
    bl-balance = 0. 
    */
    FOR EACH op-list: 
        DELETE op-list. 
    END. 

    /* Naufal Afthar - 67A545*/
    CASE stattype:
        WHEN 0 THEN ASSIGN loeschflag = 0.
        WHEN 1 THEN ASSIGN loeschflag = 1.
        WHEN 2 THEN ASSIGN loeschflag = 0.
        WHEN 3 THEN ASSIGN loeschflag = 2.
    END CASE.
    /* end Naufal Afthar*/

    IF stattype EQ 0 OR stattype EQ 2 THEN
    DO:
      FOR EACH l-order WHERE l-order.docu-nr = docunr AND l-order.loeschflag EQ loeschflag /* Naufal Afthar - 67A545*/
      AND l-order.pos GT 0 NO-LOCK BY l-order.pos: 
          create-it = NO. 
          bez-aend = NO. 
          FIND FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK NO-ERROR. 
          IF AVAILABLE l-art THEN
          DO:
              curr-bez = l-art.bezeich. 
              
              disc = 0. 
              disc2 = 0. 
              IF l-order.quality NE "" THEN 
              DO: 
                  ASSIGN 
                      disc = INTEGER(SUBSTR(l-order.quality,1,2)) + INTEGER(SUBSTR(l-order.quality,4,2)) * 0.01
                      disc-value = DECIMAL(SUBSTR(l-order.quality,19,18)).
      
                  IF LENGTH(l-order.quality) GT 12 THEN 
                      ASSIGN 
                          disc2 = INTEGER(SUBSTR(l-order.quality,13,2)) + INTEGER(SUBSTR(l-order.quality,16,2)) * 0.01
                          disc2-value = DECIMAL(SUBSTR(l-order.quality,37,18))
                          vat-val  = DECIMAL(SUBSTR(l-order.quality,55)) . 
              END. 
                  
              IF l-art.jahrgang = 0 OR LENGTH(l-order.stornogrund) LE 12 THEN 
              DO:            
                  FIND FIRST op-list WHERE op-list.artnr = l-order.artnr 
                  AND op-list.epreis EQ l-order.einzelpreis 
                  AND op-list.bezeich EQ l-art.bezeich 
                  AND op-list.disc EQ disc 
                  AND op-list.disc2 EQ disc2 
                  AND op-list.konto EQ l-order.stornogrund
                  AND op-list.remark EQ l-order.besteller NO-ERROR. 
              END.
              ELSE 
              DO: 
                  curr-bez = SUBSTR(l-order.stornogrund,13,LENGTH(l-order.stornogrund)). 
                  create-it = YES. 
                  bez-aend = YES.                                                     
              END.
                  
              IF LENGTH(l-order.stornogrund) GT 12 THEN 
                  curr-bez = SUBSTR(l-order.stornogrund, 13).
              
              IF NOT AVAILABLE op-list OR create-it THEN 
              DO: 
                  vat = 0. 
                  CREATE op-list.
                  ASSIGN  op-list.artnr       = l-order.artnr
                          op-list.bezeich     = curr-bez
                          op-list.bez-aend    = bez-aend 
                          op-list.epreis      = l-order.einzelpreis 
                          op-list.epreis0     = l-order.einzelpreis 
                          op-list.konto       = l-order.stornogrund
                          op-list.remark      = l-order.besteller
                          op-list.po-nr       = po-number /* Add by Gerald 201219 */
                          op-list.vat-code    = vat-code
                          op-list.vat1        = vat1
                          op-list.vat2        = vat2.

                  /* add additional VAT to calculation by Oscar (15 Oktober 2024) - D934AC */
                  FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 EQ l-order.docu-nr
                  AND queasy.number1 EQ l-order.artnr NO-LOCK NO-ERROR.
                  IF AVAILABLE queasy THEN 
                  DO:
                    op-list.add-vat = (1.0 + ( queasy.deci1 / 100)).
                  END.
                  ELSE
                  DO:
                    op-list.add-vat = 1.
                  END.
              
                  IF l-order.quality NE "" THEN 
                  DO: 
                      ASSIGN 
                          vat                 = INTEGER(SUBSTR(l-order.quality,7,2)) + INTEGER(SUBSTR(l-order.quality,10,2)) * 0.01
                          op-list.disc        = disc
                          op-list.disc2       = disc2 
                          op-list.disc-value  = disc-value 
                          op-list.disc2-value = disc2-value 
                          op-list.vat         = vat 
                          op-list.vat-value   = vat-val
                          disc                = disc / 100 
                          disc2               = disc2 / 100 
                          vat                 = vat / 100. 
                  END. 
              END. 
              
              /*op-list.epreis0 = l-order.einzelpreis / (1 - disc) / (1 - disc2) / (1 + vat). */
              op-list.anzahl = op-list.anzahl + l-order.anzahl. 
              op-list.warenwert = op-list.warenwert + l-order.warenwert. 
              op-list.warenwert-add-vat = op-list.warenwert-add-vat + (l-order.warenwert * op-list.add-vat).

              IF op-list.warenwert EQ op-list.warenwert-add-vat THEN
              DO:
                op-list.brutto = (op-list.warenwert + op-list.disc-value + op-list.disc2-value) - op-list.vat-value.
                op-list.epreis0 = ROUND((op-list.brutto /  op-list.anzahl),2). /*ragung change bruto*/
                op-list.warenwert0 = op-list.warenwert0 + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
              END.
              ELSE
              DO:
                op-list.brutto = (op-list.warenwert-add-vat + op-list.disc-value + op-list.disc2-value) - op-list.vat-value - (op-list.warenwert-add-vat - op-list.warenwert).
                op-list.epreis0 = ROUND((op-list.brutto /  op-list.anzahl),2). /*ragung change bruto*/
                op-list.warenwert0 = op-list.warenwert0 + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
              END.

              tot-qty = tot-qty + l-order.anzahl.
          END.
      END. 
    END.
    ELSE IF stattype EQ 1 OR stattype EQ 3 THEN
    DO:
        FOR EACH l-order WHERE l-order.docu-nr = docunr AND l-order.loeschflag EQ loeschflag /* Naufal Afthar - 67A545*/
            AND l-order.pos GT 0 NO-LOCK BY l-order.pos: 
            create-it = NO. 
            bez-aend = NO. 
            FIND FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK. 
            curr-bez = l-art.bezeich. 
            
            disc = 0. 
            disc2 = 0. 
            IF l-order.quality NE "" THEN 
            DO: 
                ASSIGN 
                    disc = INTEGER(SUBSTR(l-order.quality,1,2)) + INTEGER(SUBSTR(l-order.quality,4,2)) * 0.01
                    disc-value = DECIMAL(SUBSTR(l-order.quality,19,18)).
            
                IF LENGTH(l-order.quality) GT 12 THEN 
                    ASSIGN 
                        disc2 = INTEGER(SUBSTR(l-order.quality,13,2)) + INTEGER(SUBSTR(l-order.quality,16,2)) * 0.01
                        disc2-value = DECIMAL(SUBSTR(l-order.quality,37,18))
                        vat-val  = DECIMAL(SUBSTR(l-order.quality,55)) . 
            END. 
                
            IF l-art.jahrgang = 0 OR LENGTH(l-order.stornogrund) LE 12 THEN 
            DO:            
                FIND FIRST op-list WHERE op-list.artnr = l-order.artnr 
                AND op-list.epreis EQ l-order.einzelpreis 
                AND op-list.bezeich EQ l-art.bezeich 
                AND op-list.disc EQ disc 
                AND op-list.disc2 EQ disc2 
                AND op-list.konto EQ l-order.stornogrund
                AND op-list.remark EQ l-order.besteller NO-ERROR. 
            END.
            ELSE 
            DO: 
                curr-bez = SUBSTR(l-order.stornogrund,13,LENGTH(l-order.stornogrund)). 
                create-it = YES. 
                bez-aend = YES.                                                     
            END.
                
            IF LENGTH(l-order.stornogrund) GT 12 THEN 
                curr-bez = SUBSTR(l-order.stornogrund, 13).
            
            IF NOT AVAILABLE op-list OR create-it THEN 
            DO: 
                vat = 0. 
                CREATE op-list.
                ASSIGN  op-list.artnr       = l-order.artnr
                        op-list.bezeich     = curr-bez
                        op-list.bez-aend    = bez-aend 
                        op-list.epreis      = l-order.einzelpreis 
                        op-list.epreis0     = l-order.einzelpreis 
                        op-list.konto       = l-order.stornogrund
                        op-list.remark      = l-order.besteller
                        op-list.po-nr       = po-number /* Add by Gerald 201219 */
                        op-list.vat-code    = vat-code
                        op-list.vat1        = vat1
                        op-list.vat2        = vat2.

                /* add additional VAT to calculation by Oscar (15 Oktober 2024) - D934AC */
                FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 EQ l-order.docu-nr
                AND queasy.number1 EQ l-order.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN 
                DO:
                  op-list.add-vat = (1.0 + ( queasy.deci1 / 100)).
                END.
                ELSE
                DO:
                  op-list.add-vat = 1.
                END.
            
                IF l-order.quality NE "" THEN 
                DO: 
                    ASSIGN 
                        vat                 = INTEGER(SUBSTR(l-order.quality,7,2)) + INTEGER(SUBSTR(l-order.quality,10,2)) * 0.01
                        op-list.disc        = disc
                        op-list.disc2       = disc2 
                        op-list.disc-value  = disc-value 
                        op-list.disc2-value = disc2-value 
                        op-list.vat         = vat 
                        op-list.vat-value   = vat-val
                        disc                = disc / 100 
                        disc2               = disc2 / 100 
                        vat                 = vat / 100. 
                END. 
            END. 
            
            /*op-list.epreis0 = l-order.einzelpreis / (1 - disc) / (1 - disc2) / (1 + vat). */
            op-list.anzahl = op-list.anzahl + l-order.anzahl. 
            op-list.warenwert = op-list.warenwert + l-order.warenwert. 
            op-list.warenwert-add-vat = op-list.warenwert-add-vat + (l-order.warenwert * op-list.add-vat).

            IF op-list.warenwert EQ op-list.warenwert-add-vat THEN
            DO:
              op-list.brutto = (op-list.warenwert + op-list.disc-value + op-list.disc2-value) - op-list.vat-value.
              op-list.epreis0 = ROUND((op-list.brutto /  op-list.anzahl),2). /*ragung change bruto*/
              op-list.warenwert0 = op-list.warenwert0 + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
            END.
            ELSE
            DO:
              op-list.brutto = (op-list.warenwert-add-vat + op-list.disc-value + op-list.disc2-value) - op-list.vat-value - (op-list.warenwert-add-vat - op-list.warenwert).
              op-list.epreis0 = ROUND((op-list.brutto /  op-list.anzahl),2). /*ragung change bruto*/
              op-list.warenwert0 = op-list.warenwert0 + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
            END.

            tot-qty = tot-qty + l-order.anzahl.
        END.
    END.
    ELSE IF stattype EQ ? THEN
    DO:
        FOR EACH l-order WHERE l-order.docu-nr = docunr /*AND l-order.loeschflag GT 0*/
            AND l-order.pos GT 0 NO-LOCK BY l-order.pos: 
            create-it = NO. 
            bez-aend = NO. 
            FIND FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK. 
            curr-bez = l-art.bezeich. 
            
            disc = 0. 
            disc2 = 0. 
            IF l-order.quality NE "" THEN 
            DO: 
                ASSIGN 
                    disc = INTEGER(SUBSTR(l-order.quality,1,2)) + INTEGER(SUBSTR(l-order.quality,4,2)) * 0.01
                    disc-value = DECIMAL(SUBSTR(l-order.quality,19,18)).
            
                IF LENGTH(l-order.quality) GT 12 THEN 
                    ASSIGN 
                        disc2 = INTEGER(SUBSTR(l-order.quality,13,2)) + INTEGER(SUBSTR(l-order.quality,16,2)) * 0.01
                        disc2-value = DECIMAL(SUBSTR(l-order.quality,37,18))
                        vat-val  = DECIMAL(SUBSTR(l-order.quality,55)) . 
            END. 
                
            IF l-art.jahrgang = 0 OR LENGTH(l-order.stornogrund) LE 12 THEN 
            DO:            
                FIND FIRST op-list WHERE op-list.artnr = l-order.artnr 
                AND op-list.epreis EQ l-order.einzelpreis 
                AND op-list.bezeich EQ l-art.bezeich 
                AND op-list.disc EQ disc 
                AND op-list.disc2 EQ disc2 
                AND op-list.konto EQ l-order.stornogrund
                AND op-list.remark EQ l-order.besteller NO-ERROR. 
            END.
            ELSE 
            DO: 
                curr-bez = SUBSTR(l-order.stornogrund,13,LENGTH(l-order.stornogrund)). 
                create-it = YES. 
                bez-aend = YES.                                                     
            END.
                
            IF LENGTH(l-order.stornogrund) GT 12 THEN 
                curr-bez = SUBSTR(l-order.stornogrund, 13).
            
            IF NOT AVAILABLE op-list OR create-it THEN 
            DO: 
                vat = 0. 
                CREATE op-list.
                ASSIGN  op-list.artnr       = l-order.artnr
                        op-list.bezeich     = curr-bez
                        op-list.bez-aend    = bez-aend 
                        op-list.epreis      = l-order.einzelpreis 
                        op-list.epreis0     = l-order.einzelpreis 
                        op-list.konto       = l-order.stornogrund
                        op-list.remark      = l-order.besteller
                        op-list.po-nr       = po-number /* Add by Gerald 201219 */
                        op-list.vat-code    = vat-code
                        op-list.vat1        = vat1
                        op-list.vat2        = vat2.

                /* add additional VAT to calculation by Oscar (15 Oktober 2024) - D934AC */
                FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 EQ l-order.docu-nr
                AND queasy.number1 EQ l-order.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN 
                DO:
                  op-list.add-vat = (1.0 + ( queasy.deci1 / 100)).
                END.
                ELSE
                DO:
                  op-list.add-vat = 1.
                END.
            
                IF l-order.quality NE "" THEN 
                DO: 
                    ASSIGN 
                        vat                 = INTEGER(SUBSTR(l-order.quality,7,2)) + INTEGER(SUBSTR(l-order.quality,10,2)) * 0.01
                        op-list.disc        = disc
                        op-list.disc2       = disc2 
                        op-list.disc-value  = disc-value 
                        op-list.disc2-value = disc2-value 
                        op-list.vat         = vat 
                        op-list.vat-value   = vat-val
                        disc                = disc / 100 
                        disc2               = disc2 / 100 
                        vat                 = vat / 100. 
                END. 
            END. 
            
            /*op-list.epreis0 = l-order.einzelpreis / (1 - disc) / (1 - disc2) / (1 + vat). */
            op-list.anzahl = op-list.anzahl + l-order.anzahl. 
            op-list.warenwert = op-list.warenwert + l-order.warenwert. 
            op-list.warenwert-add-vat = op-list.warenwert-add-vat + (l-order.warenwert * op-list.add-vat).

            IF op-list.warenwert EQ op-list.warenwert-add-vat THEN
            DO:
              op-list.brutto = (op-list.warenwert + op-list.disc-value + op-list.disc2-value) - op-list.vat-value.
              op-list.epreis0 = ROUND((op-list.brutto /  op-list.anzahl),2). /*ragung change bruto*/
              op-list.warenwert0 = op-list.warenwert0 + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
            END.
            ELSE
            DO:
              op-list.brutto = (op-list.warenwert-add-vat + op-list.disc-value + op-list.disc2-value) - op-list.vat-value - (op-list.warenwert-add-vat - op-list.warenwert).
              op-list.epreis0 = ROUND((op-list.brutto /  op-list.anzahl),2). /*ragung change bruto*/
              op-list.warenwert0 = op-list.warenwert0 + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
            END.

            tot-qty = tot-qty + l-order.anzahl.
        END.
    END.
 
    FOR EACH op-list: 
        IF op-list.anzahl = 0 THEN DELETE op-list. 
    END. 
END. 


