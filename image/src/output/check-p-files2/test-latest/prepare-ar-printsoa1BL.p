
DEF OUTPUT PARAMETER curr-date      AS DATE.
DEF OUTPUT PARAMETER foreign-rate   AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER local-curr     AS CHAR.
DEF OUTPUT PARAMETER p-417          AS CHAR.
DEF OUTPUT PARAMETER foreign-curr   AS CHAR.
DEF OUTPUT PARAMETER dollar-rate    AS DECIMAL. 
DEF OUTPUT PARAMETER curr-day       AS DATE.

RUN htpdate.p  (110, OUTPUT curr-date).
RUN htplogic.p (143, OUTPUT foreign-rate).
RUN htpint.p   (491, OUTPUT price-decimal). 

/*RUN htpchar.p  (144, OUTPUT local-curr).*/
RUN htpchar.p(152, OUTPUT local-curr). /*gerald*/
RUN htpchar.p  (417, OUTPUT p-417).

RUN htpdate.p  (110, OUTPUT curr-day).

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
foreign-curr = waehrung.wabkurz.
IF AVAILABLE waehrung THEN dollar-rate = waehrung.ankauf. 
