DEFINE TEMP-TABLE output-list 
    FIELD rechnr AS INTEGER INITIAL 0
    FIELD dept   AS INTEGER INITIAL 0
    FIELD datum  AS DATE
    FIELD STR    AS CHAR. 

DEFINE TEMP-TABLE roomtransreportlist
    FIELD rechnr    AS INTEGER
    FIELD dept      AS INTEGER
    FIELD datum     AS DATE
    FIELD rmno      AS CHARACTER
    FIELD gname     AS CHARACTER
    FIELD bezeich   AS CHARACTER
    FIELD saldo     AS DECIMAL
    FIELD foreign   AS DECIMAL
    FIELD zeit      AS CHARACTER
    FIELD id        AS CHARACTER
    FIELD tb        AS CHARACTER
.

DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR roomtransreportlist.

RUN mbar-report-journal-listbl.p
    (from-date,to-date, curr-dept, long-digit,OUTPUT TABLE output-list).

EMPTY TEMP-TABLE roomtransreportlist.

FOR EACH output-list:
    CREATE roomtransreportlist.
    ASSIGN
        roomtransreportlist.rechnr  = output-list.rechnr
        roomtransreportlist.dept    = output-list.dept
        roomtransreportlist.datum   = output-list.datum
        roomtransreportlist.rmno    = SUBSTR(output-list.str,9,6)
        roomtransreportlist.gname   = SUBSTR(output-list.str,15,24)
        roomtransreportlist.bezeich = SUBSTR(output-list.str,48,24)
        roomtransreportlist.saldo   = DECIMAL(SUBSTR(output-list.str,72,14))
        roomtransreportlist.foreign = DECIMAL(SUBSTR(output-list.str,86,14))
        roomtransreportlist.zeit    = SUBSTR(output-list.str,100,5)
        roomtransreportlist.id      = SUBSTR(output-list.str,105,3)
        roomtransreportlist.tb      = SUBSTR(output-list.str,108,3)
    .
END.
