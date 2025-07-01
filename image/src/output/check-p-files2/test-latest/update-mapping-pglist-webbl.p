DEFINE TEMP-TABLE payment-gateway-list
    FIELD pg-art-no         AS INT FORMAT ">>>>" LABEL "No"
    FIELD pg-art-name       AS CHARACTER FORMAT "x(42)" LABEL "PG Artikel Name"
    FIELD pg-grp-no         AS INT FORMAT ">>>" LABEL "Group No"
    FIELD pg-grp-name       AS CHARACTER FORMAT "x(30)" LABEL "PG Group Name"
    FIELD pg-art-activate   AS LOGICAL LABEL "Active"
    FIELD vhp-art-no        AS INT FORMAT ">>>>" LABEL "VHP Article No"
    FIELD vhp-art-name      AS CHARACTER FORMAT "x(35)" LABEL "VHP Artikel Name" 
    FIELD vhp-art-dept      AS INT FORMAT ">>9" LABEL "VHP Dept".

DEFINE TEMP-TABLE vhp-payment-list
    FIELD vhp-art-no         AS INT FORMAT ">>>>" LABEL "No"
    FIELD vhp-art-name       AS CHARACTER FORMAT "x(30)" LABEL "VHP Article Name"
    .

DEFINE TEMP-TABLE payment-gateway
    FIELD pg-art-no         AS INT FORMAT ">>>>" LABEL "No"                     
    FIELD pg-art-name       AS CHARACTER FORMAT "x(42)" LABEL "PG Artikel Name" 
    FIELD pg-grp-no         AS INT FORMAT ">>>" LABEL "Group No"                
    FIELD pg-grp-name       AS CHARACTER FORMAT "x(30)" LABEL "PG Group Name"   
    FIELD pg-art-activate   AS LOGICAL LABEL "Active"                           
    FIELD vhp-art-no        AS INT FORMAT ">>>>" LABEL "VHP Article No"         
    FIELD vhp-art-name      AS CHARACTER FORMAT "x(35)" LABEL "VHP Artikel Name"
    FIELD vhp-art-dept      AS INT FORMAT ">>9" LABEL "VHP Dept".               

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR payment-gateway-list.
DEFINE INPUT PARAMETER select-dept  AS CHARACTER.
DEFINE INPUT PARAMETER select-pg    AS CHARACTER.
DEFINE OUTPUT PARAMETER result-msg  AS CHARACTER.

DEFINE VARIABLE art-dept    AS INTEGER.
DEFINE VARIABLE pg-number   AS INTEGER.

/****************************************************
                       PROCESS
****************************************************/
FOR EACH payment-gateway:
    DELETE payment-gateway.
END.

FOR EACH payment-gateway-list:
    CREATE payment-gateway.
    BUFFER-COPY payment-gateway-list TO payment-gateway.
END.

art-dept  = INT(TRIM(ENTRY(1,select-dept,"-"))).
pg-number = INT(TRIM(ENTRY(1,select-pg,"-"))).

RUN mapping-pglistbl.p (2, 0,pg-number, select-pg,art-dept,"",
                        OUTPUT TABLE payment-gateway-list, OUTPUT TABLE vhp-payment-list).

FOR EACH payment-gateway:
    FIND FIRST vhp-payment-list WHERE vhp-payment-list.vhp-art-no EQ payment-gateway.vhp-art-no NO-LOCK NO-ERROR.
    IF AVAILABLE vhp-payment-list THEN
    DO:
        payment-gateway.vhp-art-name = vhp-payment-list.vhp-art-name.
        payment-gateway.vhp-art-dept = art-dept.
    END.
    ELSE
    DO:
        payment-gateway.vhp-art-no = 0.
        payment-gateway.pg-art-activate = NO.
    END.
END.

FOR EACH payment-gateway-list:
    DELETE payment-gateway-list.
END.

FOR EACH payment-gateway:
    CREATE payment-gateway-list.
    BUFFER-COPY payment-gateway TO payment-gateway-list.
END.

RUN update-mapping-pglistbl.p(pg-number,art-dept, INPUT TABLE payment-gateway-list).
result-msg = "MAPPING DONE".
