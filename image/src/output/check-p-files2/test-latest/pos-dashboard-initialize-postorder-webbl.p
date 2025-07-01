DEFINE TEMP-TABLE order-item    
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

DEFINE INPUT PARAMETER TABLE FOR order-item.
DEFINE INPUT PARAMETER post-table-no AS INTEGER.
DEFINE INPUT PARAMETER post-order-no AS INTEGER.
DEFINE OUTPUT PARAMETER do-it AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR od-cancel-list.
DEFINE OUTPUT PARAMETER TABLE FOR post-order.
DEFINE OUTPUT PARAMETER TABLE FOR menu-list.

/**************************************************************************
                                  PROCESS
**************************************************************************/

FOR EACH od-cancel-list:
    DELETE od-cancel-list.
END.

FOR EACH post-order:
    DELETE post-order.
END.

FOR EACH menu-list:
    DELETE menu-list.
END.

/*FD May 18, 2022*/
FOR EACH order-item WHERE order-item.table-nr EQ post-table-no AND order-item.order-nr EQ post-order-no:
    CREATE od-cancel-list.
    BUFFER-COPY order-item TO od-cancel-list.
END.

FOR EACH order-item WHERE order-item.table-nr EQ post-table-no AND order-item.order-nr EQ post-order-no:
    CREATE post-order.
    BUFFER-COPY order-item TO post-order.
END.    

FOR EACH post-order WHERE post-order.confirm EQ YES AND post-order.posted EQ NO:
    do-it = YES.
    CREATE menu-list.
    ASSIGN menu-list.rec-id          = post-order.art-nr
           menu-list.DESCRIPTION     = post-order.bezeich
           menu-list.qty             = post-order.qty
           menu-list.special-request = post-order.sp-req
           .
END.
