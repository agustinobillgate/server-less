DEFINE TEMP-TABLE rmplan
    FIELD nr    AS INTEGER
    FIELD str   AS CHAR.

DEFINE TEMP-TABLE hkdiscrepancy-list
    FIELD zinr          LIKE zimmer.zinr
    FIELD features      LIKE zimmer.features
    FIELD etage         LIKE zimmer.etage
    FIELD bezeich       LIKE zimmer.bezeich
    FIELD house-status  LIKE zimmer.house-status
    FIELD zistatus      LIKE zimmer.zistatus
    FIELD userinit      LIKE bediener.userinit
    FIELD nr            LIKE bediener.nr
    .

DEFINE TEMP-TABLE hk-discrepancy-list
    FIELD roomno        AS CHAR
    FIELD fo-status     AS CHAR
    FIELD fo-adult      AS INT
    FIELD fo-child      AS INT
    FIELD hk-status     AS CHAR
    FIELD hk-adult      AS INT
    FIELD hk-child      AS INT
    FIELD explanation   AS CHAR
    FIELD times         AS CHAR
    FIELD id            AS CHAR
    FIELD floor         AS INT
    FIELD room-descr    AS CHAR.

DEFINE OUTPUT PARAMETER TABLE FOR hk-discrepancy-list.

DEFINE VARIABLE msg-str     AS CHARACTER        NO-UNDO.
DEFINE VARIABLE fo-stat     AS CHARACTER FORMAT "x(12)" LABEL "F/O Status".
DEFINE VARIABLE hk-stat     AS CHARACTER FORMAT "x(12)" LABEL "H/K Status".

RUN hk-discrepancybl.p (0, "", "", 0, "", "", "", "", "", 0, 0, 0, 0,
                OUTPUT msg-str, OUTPUT fo-stat, OUTPUT hk-stat,
                OUTPUT TABLE hkdiscrepancy-list, OUTPUT TABLE rmplan).

FOR EACH hkdiscrepancy-list:
    CREATE hk-discrepancy-list.
    ASSIGN 
        roomno      = hkdiscrepancy-list.zinr                    
        fo-status   = SUBSTR(hkdiscrepancy-list.features, 1, 12) 
        fo-adult    = INTEGER(SUBSTR(hkdiscrepancy-list.features, 64, 2))
        fo-child    = INTEGER(SUBSTR(hkdiscrepancy-list.features, 66, 2))
        hk-status   = SUBSTR(hkdiscrepancy-list.features, 13, 12)
        hk-adult    = INTEGER(SUBSTR(hkdiscrepancy-list.features, 68, 2))
        hk-child    = INTEGER(SUBSTR(hkdiscrepancy-list.features, 70, 2))
        explanation = SUBSTR(hkdiscrepancy-list.features, 32, 32)
        times       = SUBSTR(hkdiscrepancy-list.features, 27, 5) 
        id          = SUBSTR(hkdiscrepancy-list.features, 25, 2) 
        floor       = hkdiscrepancy-list.etage
        room-descr  = hkdiscrepancy-list.bezeich
        .
END.
