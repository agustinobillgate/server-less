DEFINE TEMP-TABLE t-list   
    FIELD dept        AS INTEGER FORMAT "99" LABEL "Dept"  
    FIELD tischnr     AS INTEGER FORMAT ">>>>" LABEL "Table"  
    FIELD bezeich     AS CHAR FORMAT "x(16)" LABEL "Description"   
    FIELD normalbeleg AS INTEGER FORMAT ">>9"   
    FIELD name        AS CHARACTER FORMAT "x(12)" INITIAL "" COLUMN-LABEL "Served by"   
    FIELD occupied    AS LOGICAL FORMAT "Yes/No" LABEL "OCC" INITIAL NO   
    FIELD belegung    AS INTEGER FORMAT ">>9" COLUMN-LABEL "Pax"   
    FIELD balance     AS DECIMAL FORMAT "->>>,>>>,>>9.99"  
    FIELD zinr        AS CHARACTER FORMAT "x(4)"
    FIELD gname       AS CHAR FORMAT "x(28)" LABEL "Guest Name"
    FIELD ask-bill    AS LOGICAL LABEL "Ask For Bill"
    FIELD bill-print  AS LOGICAL LABEL "Printed"
    FIELD platform    AS CHAR FORMAT "x(13)" LABEL "Platform"
    FIELD allow-ctr   AS CHAR FORMAT "x(13)" LABEL "Allow Room Charge"
    FIELD bill-number AS INTEGER FORMAT ">>>>>>>>"
    FIELD pay-status  AS CHARACTER FORMAT "x(10)" LABEL "Pay Status"
    .

DEFINE TEMP-TABLE pick-table
    FIELD dept      AS INT FORMAT "99" LABEL "Dept"
    FIELD tableno   AS INT FORMAT ">>>>" LABEL "Table"
    FIELD pax       AS INT FORMAT ">>>" LABEL "Pax"
    FIELD gname     AS CHAR FORMAT "x(25)" LABEL "Guest Name"
    FIELD occupied  AS LOGICAL LABEL "Occupied"
    FIELD session-parameter AS CHAR
    FIELD gemail    AS CHAR
    FIELD expired-session AS LOGICAL
    FIELD dataQR AS CHAR
    FIELD date-time AS DATETIME FORMAT "99/99/99 HH:MM:SS" LABEL "Picked Datetime"
    .
DEFINE TEMP-TABLE order-list   
    FIELD table-nr   AS INTEGER FORMAT ">>>>" 
    FIELD pax        AS INTEGER FORMAT ">>>"  
    FIELD order-nr   AS INTEGER FORMAT ">>>"
    FIELD guest-name AS CHAR FORMAT "x(30)"
    FIELD room-no    AS CHAR FORMAT "x(8)"
    FIELD order-date AS CHAR FORMAT "x(20)"
    FIELD posted     AS LOGICAL
    FIELD guest-nr   AS INT
    FIELD resnr      AS INT
    FIELD reslinnr   AS INT
    FIELD sessionprm AS CHAR
    FIELD billrecid  AS INT
    .                              

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

DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".

DEFINE TEMP-TABLE t-queasy222 LIKE queasy.

DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER init-posdept     AS INTEGER.
DEFINE INPUT PARAMETER bedi-username    AS CHARACTER.
DEFINE OUTPUT PARAMETER result-msg      AS CHARACTER INITIAL "".
DEFINE OUTPUT PARAMETER urlWS           AS CHAR.
DEFINE OUTPUT PARAMETER licenseNr       AS INT.
DEFINE OUTPUT PARAMETER dynamic-qr      AS LOGICAL.
DEFINE OUTPUT PARAMETER interval-time   AS INT.
DEFINE OUTPUT PARAMETER asroom-service  AS LOGICAL.
DEFINE OUTPUT PARAMETER cancel-exist    AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy222.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER TABLE FOR pick-table.
DEFINE OUTPUT PARAMETER TABLE FOR order-list.
DEFINE OUTPUT PARAMETER TABLE FOR order-item.

DEFINE VARIABLE active-waiter AS LOGICAL INITIAL NO.

/**************************************************************************
                                  PROCESS
**************************************************************************/

IF bedi-username EQ ? THEN bedi-username = "".

RUN pos-dashboard-check-waiteraccountbl.p(user-init, 1, bedi-username, OUTPUT active-waiter).
IF NOT active-waiter THEN
DO:    
    result-msg = "Waiter / Cashier Account not defined.".
    RETURN.
END.

RUN pos-dashboard-getparambl.p 
    (1, OUTPUT TABLE t-dept, OUTPUT TABLE t-queasy222, OUTPUT urlWS, OUTPUT licenseNr, 
     OUTPUT dynamic-qr, OUTPUT interval-time, OUTPUT asroom-service, OUTPUT cancel-exist).

FIND FIRST t-dept WHERE t-dept.nr EQ 1 NO-LOCK NO-ERROR.
RUN pos-dashboard-opened-tischbl.p(t-dept.nr, OUTPUT TABLE t-list, OUTPUT TABLE pick-table).

RUN pos-dashboard-load-orderbl.p(t-dept.nr, OUTPUT TABLE order-list, OUTPUT TABLE order-item).


