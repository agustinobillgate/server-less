DEFINE TEMP-TABLE post-order    
    FIELD nr        AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD table-nr  AS INTEGER FORMAT ">>>>" 
    FIELD order-nr  AS INTEGER FORMAT ">>>" 
    FIELD bezeich   AS CHARACTER FORMAT "x(30)"
    FIELD qty       AS INTEGER FORMAT ">>>" 
    FIELD sp-req    AS CHARACTER FORMAT "x(16)"
    FIELD confirm   AS LOGICAL LABEL "Confirm"
    FIELD remarks   AS CHAR FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date AS CHAR FORMAT "x(20)"
    FIELD art-nr    AS INT
    FIELD posted    AS LOGICAL LABEL "Posted"
    .

DEFINE TEMP-TABLE od-cancel-list                        /*FD May 18, 2022*/
    FIELD nr        AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD table-nr  AS INTEGER FORMAT ">>>>" 
    FIELD order-nr  AS INTEGER FORMAT ">>>" 
    FIELD bezeich   AS CHARACTER FORMAT "x(30)"
    FIELD qty       AS INTEGER FORMAT ">>>" 
    FIELD sp-req    AS CHARACTER FORMAT "x(16)"
    FIELD confirm   AS LOGICAL LABEL "Confirm"
    FIELD remarks   AS CHAR FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date AS CHAR FORMAT "x(20)"
    FIELD art-nr    AS INT
    FIELD posted    AS LOGICAL LABEL "Posted"
    .

DEFINE TEMP-TABLE menu-list
    FIELD rec-id          AS INTEGER
    FIELD DESCRIPTION     AS CHARACTER
    FIELD qty             AS INTEGER
    FIELD price           AS DECIMAL
    FIELD special-request AS CHARACTER.

DEFINE INPUT PARAMETER TABLE FOR od-cancel-list.
DEFINE INPUT PARAMETER TABLE FOR post-order.
DEFINE INPUT PARAMETER TABLE FOR menu-list.
DEFINE INPUT PARAMETER case-type            AS INTEGER.
DEFINE INPUT PARAMETER user-init            AS CHARACTER.
DEFINE INPUT PARAMETER cancel-str           AS CHARACTER.
DEFINE INPUT PARAMETER post-curr-dept       AS INTEGER.
DEFINE INPUT PARAMETER post-order-no        AS INTEGER.
DEFINE INPUT PARAMETER post-tischnr         AS INTEGER.
DEFINE INPUT PARAMETER post-session-param   AS CHARACTER.
DEFINE INPUT PARAMETER post-language-code   AS INTEGER.
DEFINE INPUT PARAMETER post-bill-recid      AS INTEGER.
DEFINE INPUT PARAMETER post-gname           AS CHARACTER.
DEFINE INPUT PARAMETER post-pax             AS INTEGER.
DEFINE INPUT PARAMETER post-guestnr         AS INTEGER.
DEFINE INPUT PARAMETER post-curr-room       AS CHARACTER.
DEFINE INPUT PARAMETER post-resnr           AS INTEGER.
DEFINE INPUT PARAMETER post-reslinnr        AS INTEGER.
DEFINE OUTPUT PARAMETER post-mess-str       AS CHARACTER.
DEFINE OUTPUT PARAMETER post-bill-number    AS INTEGER.

/**************************************************************************
                                  PROCESS
**************************************************************************/

IF cancel-str EQ ? THEN cancel-str = "".
IF post-session-param EQ ? THEN post-session-param = "".
IF post-gname EQ ? THEN post-gname = "".
IF post-curr-room EQ ? THEN post-curr-room = "".

IF case-type EQ 1 THEN /*do-it False*/
DO:
    FOR EACH menu-list:
        DELETE menu-list.
    END.

    RUN pos-dashboard-cancel-reasonbl.p(TABLE od-cancel-list, user-init, cancel-str).
    
    FOR EACH post-order WHERE post-order.confirm EQ NO AND post-order.posted EQ NO:
        CREATE menu-list.
        ASSIGN menu-list.rec-id   = post-order.art-nr
        menu-list.DESCRIPTION     = post-order.bezeich
        menu-list.qty             = post-order.qty
        menu-list.special-request = post-order.sp-req
        .
    END.
    
    RUN pos-dashboard-cancel-orderbl.p 
        (INPUT TABLE menu-list,post-curr-dept,post-order-no,post-tischnr,post-session-param,
         OUTPUT post-mess-str).
END.
ELSE /*do-it True*/
DO:
    RUN pos-dashboard-cancel-reasonbl.p(TABLE od-cancel-list, user-init, cancel-str).

    RUN pos-dashboard-post-menubl.p(post-language-code, post-bill-recid, post-tischnr,      
                                    post-curr-dept, user-init, post-gname,        
                                    post-pax,post-guestnr,post-curr-room,post-resnr,        
                                    post-reslinnr, post-session-param, post-order-no, INPUT TABLE menu-list,
                                    OUTPUT post-bill-number, OUTPUT post-mess-str).
END.
