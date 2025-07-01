DEFINE TEMP-TABLE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)"
  FIELD sorting AS CHAR FORMAT "x(1)" . 

DEFINE TEMP-TABLE w-list 
  FIELD nr AS INTEGER 
  FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE TEMP-TABLE username
    FIELD order-nr      AS CHAR FORMAT "x(30)"
    FIELD create-by     AS CHAR FORMAT "x(30)"
    FIELD modify-by     AS CHAR FORMAT "x(30)"
    FIELD close-by      AS CHAR FORMAT "x(30)"
    FIELD close-date    AS DATE  
    FIELD close-time    AS CHAR FORMAT "x(10)"
    FIELD last-arrival  AS DATE
    FIELD total-amount  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" .
DEFINE TEMP-TABLE l-supp LIKE l-lieferant.

DEFINE OUTPUT PARAMETER long-digit AS LOGICAL.
DEFINE OUTPUT PARAMETER billdate AS DATE.
DEFINE OUTPUT PARAMETER briefnr AS INT.
DEFINE OUTPUT PARAMETER p-464 AS INT.
DEFINE OUTPUT PARAMETER htl-name AS CHAR.
DEFINE OUTPUT PARAMETER htl-adr AS CHAR.
DEFINE OUTPUT PARAMETER htl-tel AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR cost-list.
DEFINE OUTPUT PARAMETER TABLE FOR w-list.
DEFINE OUTPUT PARAMETER TABLE FOR username.
DEFINE OUTPUT PARAMETER TABLE FOR l-supp.

FIND FIRST paramtext WHERE txtnr = 200 NO-ERROR. 
htl-name = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 201 NO-ERROR. 
htl-adr  = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
htl-tel  = paramtext.ptexte. 

FIND FIRST htparam WHERE paramnr = 1093 NO-LOCK. 
briefnr = htparam.finteger. 

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 464 NO-LOCK. 
p-464 = htparam.finteger.

RUN create-costlist.
RUN currency-list.
RUN create-bediener.
RUN create-supp.

PROCEDURE create-supp:
  FOR EACH l-lieferant:
    CREATE l-supp.
    BUFFER-COPY l-lieferant TO l-supp.
  END.
END.

PROCEDURE create-costlist :
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.nr = INTEGER(parameters.varname). 
    cost-list.bezeich = parameters.vstring. 
  END. 
END PROCEDURE.

PROCEDURE currency-list :
DEFINE VARIABLE local-nr AS INTEGER INITIAL 0. 
  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN local-nr = waehrung.waehrungsnr. 
 
  create w-list. 
  IF local-nr NE 0 THEN w-list.wabkurz = waehrung.wabkurz. 
 
  FOR EACH waehrung NO-LOCK BY waehrung.wabkurz: 
    create w-list. 
    w-list.nr = waehrung.waehrungsnr. 
    w-list.wabkurz = waehrung.wabkurz. 
  END.
END PROCEDURE.


PROCEDURE create-bediener :
  DEFINE VARIABLE temp-create AS CHAR FORMAT "x(30)".
  DEFINE VARIABLE temp-modify AS CHAR FORMAT "x(30)".
  DEFINE VARIABLE temp-close  AS CHAR FORMAT "x(30)".
  DEFINE VARIABLE temp-date   AS DATE.
  DEFINE VARIABLE temp-time   AS CHAR FORMAT "x(10)".
  DEFINE VARIABLE last-arrive AS DATE.
  DEF VAR total-amount  AS DECIMAL INITIAL 0.   

  FOR EACH username :
    DELETE username.
  END.

  FOR EACH fa-ordheader :
    FOR EACH fa-order WHERE fa-order.order-nr = fa-ordheader.order-nr NO-LOCK BY fa-order.delivered-date :
      IF last-arrive = ? THEN
        last-arrive = fa-order.delivered-date.
      ELSE
      DO:
        IF last-arrive <= fa-order.delivered-date THEN
          last-arrive = fa-order.delivered-date.
        ELSE last-arrive = last-arrive.
      END.
    END.

    IF fa-ordheader.activeflag = 2 THEN
    DO:
      FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.close-by NO-LOCK NO-ERROR.
      IF AVAILABLE bediener THEN temp-close = bediener.username.
      ELSE temp-close = "".   
      IF fa-ordheader.close-date NE ? THEN
        temp-date  = fa-ordheader.close-date.
      ELSE
        temp-date = ?.
      IF fa-ordheader.close-time NE 0 THEN
        temp-time  = string(fa-ordheader.close-time , "HH:MM").
      ELSE
        temp-time = "".
    END.
    ELSE
    DO:
      ASSIGN
        temp-close = ""
        temp-date  = ?
        temp-time  = "".
    END.
    FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.created-by NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN temp-create = bediener.username.
    ELSE temp-create = "".
    FIND FIRST bediener WHERE bediener.userinit = fa-ordheader.modified-by NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN temp-modify = bediener.username.
    ELSE temp-modify = "".
    FOR EACH fa-order WHERE fa-order.order-nr  = fa-ordheader.order-nr 
      AND fa-order.activeflag = 0 :   
      total-amount = total-amount + fa-order.order-amount.  
    END.

    CREATE username.
    ASSIGN 
      username.order-nr     = fa-ordheader.order-nr
      username.create-by    = temp-create
      username.modify-by    = temp-modify
      username.close-by     = temp-close 
      username.close-date   = temp-date
      username.close-time   = temp-time
      username.last-arrival = last-arrive
      username.total-amount = total-amount
      total-amount = 0
      temp-create  = ""
      temp-modify  = ""
      temp-close   = ""
      temp-date    = ?
      temp-time    = ""
      last-arrive  = ?.
  END.
END PROCEDURE.
