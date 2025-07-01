
DEF OUTPUT PARAMETER p-999      AS LOGICAL.
DEF OUTPUT PARAMETER p-43       AS LOGICAL.
DEF OUTPUT PARAMETER p-Log1080  AS LOGICAL.
DEF OUTPUT PARAMETER p-Int1080  AS INT.

DEF OUTPUT PARAMETER p-2000     AS LOGICAL.
DEF OUTPUT PARAMETER p-269      AS DATE.
DEF OUTPUT PARAMETER p-1035     AS DATE.
DEF OUTPUT PARAMETER p-224      AS DATE.
DEF OUTPUT PARAMETER p-221      AS DATE.
DEF OUTPUT PARAMETER p-852      AS INT.
DEF OUTPUT PARAMETER avail-l-ophis AS LOGICAL INIT NO.

FIND FIRST htparam WHERE paramnr = 999 NO-LOCK. 
p-999 =  htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK.
p-43  = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 1080 NO-LOCK.
p-Log1080 = htparam.flogical.
p-Int1080 = htparam.paramgr.

RUN htplogic.p(2000, OUTPUT p-2000).
RUN htpdate.p (269,  OUTPUT p-269).
RUN htpdate.p (1035, OUTPUT p-1035).
RUN htpdate.p (224,  OUTPUT p-224).
RUN htpdate.p (221,  OUTPUT p-221).
RUN htpint.p  (852,  OUTPUT p-852).

FIND FIRST vhp.l-ophis NO-LOCK NO-ERROR.
IF AVAILABLE vhp.l-ophis THEN avail-l-ophis = YES.

FIND FIRST l-artikel NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel AND NOT l-artikel.herkunft MATCHES ("*;*") THEN
  RUN add-sunits.
/*MT
FOR EACH l-artikel:
    CREATE temp-l-artikel.
    BUFFER-COPY l-artikel TO temp-l-artikel.
END.
*/
PROCEDURE add-sunits:
DEF BUFFER sbuff FOR l-artikel.
    FIND FIRST l-artikel NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-artikel:
        IF NOT l-artikel.herkunft MATCHES("*;*") THEN
        DO TRANSACTION:
            FIND FIRST sbuff WHERE RECID(sbuff) = RECID(l-artikel)
                EXCLUSIVE-LOCK.
            sbuff.herkunft = sbuff.herkunft + ";;".
            FIND CURRENT sbuff NO-LOCK.
        END.
        FIND NEXT l-artikel NO-LOCK NO-ERROR.
    END.
END.
