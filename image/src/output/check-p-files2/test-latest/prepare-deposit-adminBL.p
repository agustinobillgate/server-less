
DEF OUTPUT PARAMETER fdate AS DATE.
DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER depo-foreign LIKE artikel.pricetab.
DEF OUTPUT PARAMETER depo-curr LIKE artikel.betriebsnr.
DEF OUTPUT PARAMETER foreign-curr LIKE waehrung.waehrungsnr.
DEF OUTPUT PARAMETER p-60 AS INT.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
fdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
bill-date = htparam.fdate.
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK.
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
    AND artikel.departement = 0 NO-LOCK.
depo-foreign = artikel.pricetab.
depo-curr  = artikel.betriebsnr.

FIND FIRST htparam WHERE paramnr = 144 NO-LOCK.
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK.
foreign-curr = waehrung.waehrungsnr.
 
RUN htpint.p (60, OUTPUT p-60).
