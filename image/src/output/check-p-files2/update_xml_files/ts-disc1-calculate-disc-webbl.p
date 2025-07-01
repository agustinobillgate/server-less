/*FD Dec 20, 2021 => BL VHP Web for calculate discount, similiary procedure calc-amount in TS-disc1UI*/
DEFINE TEMP-TABLE menu-disc LIKE h-bill-line.

DEFINE TEMP-TABLE disc-list  
    FIELD h-artnr       AS INTEGER  
    FIELD bezeich       AS CHAR  
    FIELD artnr         AS INTEGER  
    FIELD mwst          AS INTEGER  
    FIELD service       AS INTEGER  
    FIELD umsatzart     AS INTEGER INITIAL 0   
    FIELD defaultFlag   AS LOGICAL INITIAL NO  
    FIELD amount        AS DECIMAL INITIAL 0  
    FIELD netto-amt     AS DECIMAL INITIAL 0  
    FIELD service-amt   AS DECIMAL INITIAL 0  
    FIELD mwst-amt      AS DECIMAL INITIAL 0  
.

DEFINE TEMP-TABLE t-calc-disc    
    FIELD select-amt-taxserv    AS DECIMAL
    FIELD disc-taxserv          AS DECIMAL
    FIELD balance-taxserv       AS DECIMAL
    FIELD selected-amount       AS DECIMAL
    FIELD discount              AS DECIMAL
    FIELD balance               AS DECIMAL
.

DEFINE INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER dept AS INTEGER.
DEFINE INPUT PARAMETER procent AS DECIMAL.
DEFINE INPUT PARAMETER disc-value AS DECIMAL.
DEFINE INPUT PARAMETER TABLE FOR menu-disc.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-calc-disc.
DEFINE OUTPUT PARAMETER TABLE FOR disc-list.

DEFINE TEMP-TABLE t-hart LIKE h-artikel.
DEFINE TEMP-TABLE t-h-artikel  
    FIELD mwst          LIKE h-artikel.mwst-code  
    FIELD service       LIKE h-artikel.service-code  
    FIELD artnr         LIKE h-artikel.artnr  
    FIELD bezeich       LIKE h-artikel.bezeich  
    FIELD service-code  LIKE h-artikel.service-code  
    FIELD mwst-code     LIKE h-artikel.mwst-code
.  
  
DEFINE TEMP-TABLE t-artikel  
    FIELD umsatzart     LIKE artikel.umsatzart
. 

    {SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "TS-disc1".

DEFINE VARIABLE incl-service    AS LOGICAL.   
DEFINE VARIABLE incl-mwst       AS LOGICAL.   
DEFINE VARIABLE service-tax     AS LOGICAL.                                                                           
DEFINE VARIABLE vat2            AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE fact            AS DECIMAL NO-UNDO INIT 1.                                
DEFINE VARIABLE fb-netto        AS DECIMAL.   
DEFINE VARIABLE f-dec           AS DECIMAL.                                  

DEFINE VARIABLE amount          AS DECIMAL.
DEFINE VARIABLE balance         AS DECIMAL.
DEFINE VARIABLE orig-amt        AS DECIMAL.

DEFINE VARIABLE disc-alert      AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE disc-service    AS LOGICAL.
DEFINE VARIABLE disc-tax        AS LOGICAL.   
DEFINE VARIABLE h-service       AS DECIMAL.   
DEFINE VARIABLE service         AS DECIMAL.   
DEFINE VARIABLE h-mwst          AS DECIMAL.   
DEFINE VARIABLE mwst            AS DECIMAL. 
DEFINE VARIABLE netto-betrag    AS DECIMAL.   
DEFINE VARIABLE nett-amount     AS DECIMAL.
DEFINE VARIABLE voucher-art     AS INTEGER NO-UNDO.   
DEFINE VARIABLE disc-art1       AS INTEGER NO-UNDO.   
DEFINE VARIABLE disc-art2       AS INTEGER NO-UNDO.   
DEFINE VARIABLE disc-art3       AS INTEGER NO-UNDO.
DEFINE VARIABLE price-decimal   AS INTEGER.
DEFINE VARIABLE b-billart       AS INTEGER.
DEFINE VARIABLE b2-billart      AS INTEGER.
DEFINE VARIABLE billart         AS INTEGER.
DEFINE VARIABLE o-artnrfront    AS INTEGER NO-UNDO.
DEFINE VARIABLE b-artnrfront    AS INTEGER NO-UNDO.
DEFINE VARIABLE description     AS CHARACTER.   
DEFINE VARIABLE tmp-count       AS DECIMAL NO-UNDO.             /* Rulita 070225 | Fixing serverless Tampung ke variable issue git 554 */

DEFINE VARIABLE servtax-use-foart AS LOGICAL. /*FD Dec 07, 2021*/

DEFINE VARIABLE tot-disc AS DECIMAL. /* Malik 247AD4, 17-09-2024 */

/*******************************************************************************************************/
RUN ts-disc1-get-articlebl.p  
    (dept, disc-value, procent, b-billart, b2-billart,  
    OUTPUT billart, OUTPUT description, OUTPUT b-artnrfront,  
    OUTPUT o-artnrfront, OUTPUT TABLE disc-list).

/* Rulita 040225 | Fixing serverless issue git 518 */
FIND FIRST htparam WHERE htparam.paramnr EQ 1203 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN 
DO:
    IF htparam.paramgr EQ 19 AND htparam.feldtyp EQ 4 THEN 
        disc-alert = htparam.flogical.
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 468 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-service = htparam.flogical. /* disc reduce service? */ 

FIND FIRST htparam WHERE htparam.paramnr EQ 469 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-tax = htparam.flogical. /* disc reduce vat? */ 

FIND FIRST htparam WHERE htparam.paramnr EQ 491 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr EQ 134 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN incl-mwst = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr EQ 135 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN incl-service = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr EQ 479 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN service-tax = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr EQ 1001 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN voucher-art = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr EQ 557 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art1 = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr EQ 596 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art2 = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr EQ 556 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art3 = htparam.finteger.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN servtax-use-foart = hoteldpt.defult.

/* End Rulita */

ASSIGN   
    netto-betrag    = 0 
    service         = 0 
    mwst            = 0
.

FOR EACH disc-list: 
    ASSIGN   
        disc-list.netto-amt   = 0  
        disc-list.amount      = 0  
        disc-list.service-amt = 0  
        disc-list.mwst-amt    = 0  
    .  
END.

FOR EACH t-calc-disc:
    DELETE t-calc-disc.
END.

CREATE t-calc-disc.

FOR EACH menu-disc WHERE menu-disc.artnr NE disc-art1
    AND menu-disc.artnr NE disc-art2 
    AND menu-disc.artnr NE disc-art3 NO-LOCK:    

    balance = balance + menu-disc.betrag.

    RUN ts-disc1-cal-amountbl.p 
        (menu-disc.artnr, menu-disc.departement, OUTPUT TABLE t-h-artikel, OUTPUT TABLE t-artikel).
    FIND FIRST t-h-artikel.  
    FIND FIRST t-artikel.
    
    netto-betrag = netto-betrag + menu-disc.anzahl * menu-disc.epreis.
    nett-amount = nett-amount + menu-disc.anzahl * menu-disc.epreis.

    FIND FIRST disc-list WHERE disc-list.umsatzart EQ t-artikel.umsatzart  
        AND disc-list.mwst EQ t-h-artikel.mwst-code                                               /* Rulita 040225 | Fixing serverless issue git 518 */
        AND disc-list.service EQ t-h-artikel.service-code NO-LOCK NO-ERROR.                       /* Rulita 040225 | Fixing serverless issue git 518 */
    IF NOT AVAILABLE disc-list THEN  
    DO:          
        IF disc-alert THEN
        DO:
            msg-str = translateExtended ("Discount Article [1] not found for menu item:",lvCAREA,"")  
                + " " + STRING(t-h-artikel.artnr) + " - " + t-h-artikel.bezeich.
        END.
                  
        FIND FIRST disc-list WHERE disc-list.umsatzart EQ t-artikel.umsatzart  
            AND disc-list.mwst EQ t-h-artikel.mwst-code NO-LOCK NO-ERROR.                         /* Rulita 040225 | Fixing serverless issue git 518 */           
        IF NOT AVAILABLE disc-list THEN   
        DO:              
            IF disc-alert THEN  
            DO:
                msg-str = translateExtended ("Discount Article [2] not found for menu item:",lvCAREA,"")  
                    + " " + STRING(t-h-artikel.artnr) + " - " + t-h-artikel.bezeich.
            END.
            
            FIND FIRST disc-list WHERE disc-list.umsatzart EQ t-artikel.umsatzart NO-ERROR.  
        END. 
    END.
    disc-list.netto-amt = disc-list.netto-amt + menu-disc.anzahl * menu-disc.epreis.

    /*FD Dec 07, 2021*/
    IF servtax-use-foart THEN
    DO:
        RUN read-h-artikelbl.p (1, disc-list.h-artnr, dept, "", 0, 0, YES, OUTPUT TABLE t-hart).
        FIND FIRST t-hart.
    
        RUN calc-servtaxesbl.p
            (1, t-hart.artnrfront, dept, ?, OUTPUT h-service, OUTPUT h-mwst, OUTPUT vat2, OUTPUT fact).
        ASSIGN h-mwst = h-mwst + vat2.
        IF incl-service OR NOT disc-service THEN h-service = 0.
        IF incl-mwst OR NOT disc-tax THEN h-mwst = 0.
        ASSIGN  
            h-service             = menu-disc.epreis * h-service
            disc-list.service-amt = disc-list.service-amt + h-service * menu-disc.anzahl    
            service               = service + h-service * menu-disc.anzahl  
            h-mwst                = menu-disc.epreis * h-mwst
            disc-list.mwst-amt    = disc-list.mwst-amt + h-mwst * menu-disc.anzahl    
            mwst                  = mwst + h-mwst * menu-disc.anzahl  
        .
    END.
    ELSE
    DO:     
        h-service = 0.
        IF NOT incl-service AND t-h-artikel.service-code NE 0 AND disc-service THEN   
        DO:  
            RUN htpdec.p(disc-list.service, OUTPUT f-dec).  
            IF f-dec NE 0 THEN  
            ASSIGN  
                h-service = menu-disc.epreis * f-dec / 100  
                disc-list.service-amt = disc-list.service-amt + h-service * menu-disc.anzahl    
                service = service + h-service * menu-disc.anzahl 
            .  
        END.  
                
        h-mwst = 0.
        IF NOT incl-mwst AND t-h-artikel.mwst-code NE 0 AND disc-tax THEN   
        DO:  
            RUN htpdec.p(disc-list.mwst, OUTPUT f-dec).  
            IF f-dec NE 0 THEN  
            DO:   
                h-mwst = f-dec.  
                tmp-count = menu-disc.epreis + h-service.                   /* Rulita 070225 | Fixing serverless Tampung ke variable issue git 554 */
                IF service-tax THEN h-mwst = h-mwst * tmp-count / 100.   
                ELSE h-mwst = h-mwst * menu-disc.epreis / 100.    
                ASSIGN  
                    disc-list.mwst-amt = disc-list.mwst-amt + h-mwst * menu-disc.anzahl    
                    mwst = mwst + h-mwst * menu-disc.anzahl  
                .  
            END.  
        END.             
    END.     
END.

fb-netto = netto-betrag.   
netto-betrag = - procent * netto-betrag / 100.   
/*netto-betrag = round(netto-betrag, price-decimal).   */
service =  - procent * service / 100.   
/*service = round(service, price-decimal).*/
mwst = - procent * mwst / 100.   
/*mwst = round(mwst, price-decimal).*/
amount = netto-betrag + service + mwst.       
      
IF disc-value EQ 0 THEN 
    /*amount = netto-betrag + service + mwst.     */      
    amount = ROUND(netto-betrag + service + mwst, price-decimal).
ELSE    
ASSIGN amount = - disc-value.

FOR EACH disc-list WHERE disc-list.netto-amt NE 0:  
    ASSIGN disc-list.amount = amount * (disc-list.netto-amt / fb-netto). 
    IF disc-list.netto-amt NE 0 AND disc-value EQ 0 THEN DO:
        ASSIGN   
            disc-list.netto-amt   = - procent * disc-list.netto-amt / 100   
            /*disc-list.netto-amt   = ROUND(disc-list.netto-amt, price-decimal)*/
            disc-list.service-amt =  - procent * disc-list.service-amt / 100   
            /*disc-list.service-amt = ROUND(disc-list.service-amt, price-decimal)   */
            disc-list.mwst-amt    = - procent * disc-list.mwst-amt / 100  
            /*disc-list.mwst-amt    = ROUND(disc-list.mwst-amt, price-decimal)   */
            disc-list.amount      = /*disc-list.amount +*/ disc-list.netto-amt   
                                  + disc-list.service-amt + disc-list.mwst-amt
            disc-list.amount      = ROUND(disc-list.amount, price-decimal) 
            tot-disc = tot-disc + disc-list.amount.
        .         
    END.
END.

/* Malik 247AD4, 17-09-2024 */
FOR EACH disc-list WHERE disc-list.netto-amt EQ 0 BY disc-list.h-artnr DESC:
    disc-list.amount = amount - tot-disc.
    LEAVE.
END.  

FOR EACH disc-list WHERE disc-list.netto-amt EQ 0 BY disc-list.h-artnr DESC:
    amount = amount - disc-list.amount.
    LEAVE.
END.
/* END Malik */

ASSIGN        
    t-calc-disc.select-amt-taxserv  = ROUND(balance, price-decimal)
    t-calc-disc.disc-taxserv        = ROUND(t-calc-disc.disc-taxserv + amount, price-decimal)        
    t-calc-disc.balance-taxserv     = ROUND(balance + t-calc-disc.disc-taxserv, price-decimal)

    t-calc-disc.selected-amount     = ROUND(nett-amount, price-decimal)
    t-calc-disc.discount            = ROUND(t-calc-disc.discount + netto-betrag, price-decimal)
    t-calc-disc.balance             = ROUND(nett-amount + t-calc-disc.discount, price-decimal)
.
