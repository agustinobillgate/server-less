DEFINE TEMP-TABLE fb-cost-report 
    FIELD departement   AS CHARACTER 
    FIELD qty           AS CHARACTER
    FIELD sales         AS CHARACTER
    FIELD cost          AS CHARACTER
    FIELD qty2          AS CHARACTER
    FIELD compliment    AS CHARACTER
    FIELD t-cost        AS CHARACTER
    FIELD ratio         AS CHARACTER
    FIELD m-qty         AS CHARACTER
    FIELD m-sales       AS CHARACTER
    FIELD m-cost        AS CHARACTER
    FIELD m-qty2        AS CHARACTER
    FIELD compliment2   AS CHARACTER
    FIELD t-cost2       AS CHARACTER
    FIELD ratio2        AS CHARACTER
.

DEFINE TEMP-TABLE output-list 
    FIELD anz         AS INTEGER FORMAT "->>>" 
    FIELD m-anz       AS INTEGER FORMAT "->>>>" 
    FIELD comanz      AS INTEGER FORMAT "->>>" 
    FIELD m-comanz    AS INTEGER FORMAT "->>>>" 
    FIELD s           AS CHAR.

DEFINE INPUT  PARAMETER language-code     AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER sorttype          AS INT.
DEFINE INPUT  PARAMETER detailed          AS LOGICAL.
DEFINE INPUT  PARAMETER from-dept         AS INT.
DEFINE INPUT  PARAMETER to-dept           AS INT.
DEFINE INPUT  PARAMETER from-date         AS DATE.
DEFINE INPUT  PARAMETER to-date           AS DATE.
DEFINE INPUT  PARAMETER fact1             AS INT.
DEFINE INPUT  PARAMETER short-flag        AS LOGICAL.
DEFINE INPUT  PARAMETER mi-compli-checked AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR fb-cost-report.

RUN hums-cost-btn-gobl.p
    (language-code, sorttype, detailed, from-dept, to-dept, from-date,
    to-date, fact1, short-flag, mi-compli-checked,OUTPUT TABLE output-list).

EMPTY TEMP-TABLE fb-cost-report.

FOR EACH output-list:
    CREATE fb-cost-report.
    ASSIGN             
        fb-cost-report.departement   = SUBSTR(output-list.s,1,23) 
        fb-cost-report.qty           = STRING(output-list.anz, ">>>>>")
        fb-cost-report.sales         = SUBSTR(output-list.s,24,20)
        fb-cost-report.cost          = SUBSTR(output-list.s,44,20)
        fb-cost-report.qty2          = STRING(output-list.comanz, ">>>>>")
        fb-cost-report.compliment    = SUBSTR(output-list.s,64,20)
        fb-cost-report.t-cost        = SUBSTR(output-list.s,84,20)
        fb-cost-report.ratio         = SUBSTR(output-list.s,104,6)
        fb-cost-report.m-qty         = STRING(output-list.m-anz, ">>>>>")
        fb-cost-report.m-sales       = SUBSTR(output-list.s,110,20)
        fb-cost-report.m-cost        = SUBSTR(output-list.s,130,20)
        fb-cost-report.m-qty2        = STRING(output-list.m-comanz, ">>>>>")
        fb-cost-report.compliment2   = SUBSTR(output-list.s,150,20)
        fb-cost-report.t-cost2       = SUBSTR(output-list.s,170,20)
        fb-cost-report.ratio2        = SUBSTR(output-list.s,190,6).
    .     .
END.


