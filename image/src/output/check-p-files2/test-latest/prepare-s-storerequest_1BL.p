DEFINE TEMP-TABLE temp-l-artikel
    FIELD artnr         LIKE l-artikel.artnr
    FIELD betriebsnr    LIKE l-artikel.betriebsnr
    FIELD endkum        LIKE l-artikel.endkum
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD masseinheit   LIKE l-artikel.masseinheit
    FIELD vk-preis      LIKE l-artikel.vk-preis
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD traubensort   LIKE l-artikel.traubensort.    

DEF TEMP-TABLE t-parameters     LIKE parameters.
DEF TEMP-TABLE t-l-lager        LIKE l-lager.

DEF TEMP-TABLE art-list
    FIELD artnr                 LIKE l-artikel.artnr
    FIELD zwkum                 LIKE l-untergrup.zwkum
    FIELD endkum                LIKE l-hauptgrp.endkum
    FIELD zwkum-bezeich         LIKE l-hauptgrp.bezeich
    FIELD endkum-bezeich        LIKE l-untergrup.bezeich.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER req-flag AS LOGICAL.
DEF OUTPUT PARAMETER transdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR temp-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR art-list.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 


FIND FIRST htparam WHERE paramnr = 475 NO-LOCK. 
req-flag = NOT htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
transdate = htparam.fdate. 
 
FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" NO-LOCK:
    CREATE t-parameters.
    BUFFER-COPY parameters TO t-parameters.
END.

FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH l-artikel:
    CREATE temp-l-artikel.
    ASSIGN
    temp-l-artikel.artnr         = l-artikel.artnr
    temp-l-artikel.betriebsnr    = l-artikel.betriebsnr
    temp-l-artikel.endkum        = l-artikel.endkum
    temp-l-artikel.bezeich       = l-artikel.bezeich
    temp-l-artikel.masseinheit   = l-artikel.masseinheit
    temp-l-artikel.vk-preis      = l-artikel.vk-preis
    temp-l-artikel.lief-einheit  = l-artikel.lief-einheit
    temp-l-artikel.traubensort   = l-artikel.traubensort.
END.

FOR EACH l-artikel:
    FIND FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK NO-ERROR.
    IF AVAILABLE l-untergrup THEN
    DO:
        FIND FIRST l-hauptgrp WHERE l-hauptgrp.endkum EQ l-artikel.endkum NO-LOCK NO-ERROR.
        IF AVAILABLE l-hauptgrp THEN
        DO:
            CREATE art-list.
            ASSIGN 
                art-list.artnr          = l-artikel.artnr
                art-list.zwkum          = l-untergrup.zwkum
                art-list.endkum         = l-hauptgrp.endkum
                art-list.zwkum-bezeich  = l-untergrup.bezeich     
                art-list.endkum-bezeich = l-hauptgrp.bezeich.
        END.
    END.
END.

