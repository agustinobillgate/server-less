DEFINE TEMP-TABLE t-faordheader     LIKE fa-ordheader.
DEFINE TEMP-TABLE t-lieferant       LIKE l-lieferant.
DEFINE TEMP-TABLE tfa-order     LIKE fa-order
    FIELD nr    AS INTEGER
    FIELD NAME  AS CHAR
    FIELD asset AS CHAR
    FIELD price AS DECIMAL
.

DEF TEMP-TABLE t-parameters
    FIELD varname LIKE parameters.varname
    FIELD vstring LIKE parameters.vstring
.

DEFINE INPUT  PARAMETER docu-nr                     AS CHAR    NO-UNDO.
DEFINE INPUT  PARAMETER user-init                   AS CHAR    NO-UNDO.
DEFINE INPUT  PARAMETER dept-nr                     AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER enforce-rflag               AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER show-price                  AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER price-decimal               AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER billdate                    AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER add-first-waehrung-wabkurz  AS CHAR INIT "" NO-UNDO.
DEFINE OUTPUT PARAMETER exchg-rate                  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER tot-amount                  AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER pr-21                       AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER pr-973                      AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-faordheader.
DEFINE OUTPUT PARAMETER TABLE FOR tfa-order.
DEFINE OUTPUT PARAMETER TABLE FOR t-lieferant.
DEFINE OUTPUT PARAMETER TABLE FOR t-parameters.

FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = docu-nr NO-LOCK NO-ERROR. 
CREATE t-faordheader.
BUFFER-COPY fa-ordheader TO t-faordheader.

FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
pr-21 = htparam.paramgr.
pr-973 = htparam.flogical.

FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" NO-LOCK :
    CREATE t-parameters.
    ASSIGN t-parameters.varname = parameters.varname
           t-parameters.vstring = parameters.vstring.
END.

RUN get-currency.
RUN create-tfa-order.

FOR EACH l-lieferant NO-LOCK:
    CREATE t-lieferant.
    BUFFER-COPY l-lieferant TO t-lieferant.

END.


PROCEDURE get-currency :

  FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
    fa-ordheader.currency NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    ASSIGN 
        add-first-waehrung-wabkurz = waehrung.wabkurz
        exchg-rate = waehrung.ankauf / waehrung.einheit.
  END. 
END.

PROCEDURE Create-tfa-order :
    FOR EACH tfa-order :
        DELETE tfa-order.
    END.

    FOR EACH fa-order WHERE fa-order.order-nr = docu-nr NO-LOCK BY fa-order.fa-pos:
        FIND FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK NO-ERROR.
        CREATE tfa-order.
        BUFFER-COPY fa-order TO tfa-order.
        ASSIGN tfa-order.nr    = mathis.nr
               tfa-order.NAME  = mathis.NAME
               tfa-order.asset = mathis.asset
               tfa-order.price = mathis.price
            .
        tot-amount = tot-amount + tfa-order.order-amount.
    END.

END PROCEDURE.

