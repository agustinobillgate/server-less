
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER avail-l-untergrup AS LOGICAL INIT NO.

RUN htplogic.p (43, OUTPUT show-price).
FIND FIRST l-untergrup WHERE l-untergrup.betriebsnr = 1 NO-LOCK NO-ERROR.
IF AVAILABLE l-untergrup THEN avail-l-untergrup = YES.
