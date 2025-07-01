
DEFINE buffer usr FOR bediener.
DEF TEMP-TABLE q1-list
    FIELD monat         LIKE guestbud.monat
    FIELD jahr          LIKE guestbud.jahr
    FIELD argtumsatz    LIKE guestbud.argtumsatz
    FIELD f-b-umsatz    LIKE guestbud.f-b-umsatz
    FIELD sonst-umsatz  LIKE guestbud.sonst-umsatz
    FIELD room-nights   LIKE guestbud.room-nights
    FIELD userinit      LIKE usr.userinit
    FIELD rec-id        AS INT.

DEF INPUT PARAMETER gastnr AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
FIND FIRST bediener WHERE bediener.userinit = user-init. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
bill-date = htparam.fdate. 
from-date = DATE(month(bill-date), 1, year(bill-date)). 

FOR EACH guestbud WHERE 
    guestbud.gastnr = gastnr NO-LOCK, 
    FIRST usr WHERE usr.nr = guestbud.bediener-nr 
    BY guestbud.jahr BY guestbud.monat:
    CREATE q1-list.
    ASSIGN
    q1-list.monat         = guestbud.monat
    q1-list.jahr          = guestbud.jahr
    q1-list.argtumsatz    = guestbud.argtumsatz
    q1-list.f-b-umsatz    = guestbud.f-b-umsatz
    q1-list.sonst-umsatz  = guestbud.sonst-umsatz
    q1-list.room-nights   = guestbud.room-nights
    q1-list.userinit      = usr.userinit
    q1-list.rec-id        = RECID(guestbud).
END.
