
DEFINE OUTPUT PARAMETER from-date AS DATE.
DEFINE OUTPUT PARAMETER to-date AS DATE.
DEFINE OUTPUT PARAMETER curr-local AS CHAR.
DEFINE OUTPUT PARAMETER curr-foreign AS CHAR.
DEFINE OUTPUT PARAMETER double-curr AS LOGICAL.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    from-date = htparam.fdate.
    to-date = htparam.fdate.
END.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN curr-local = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN curr-foreign = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 240 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN double-curr = htparam.flogical. /* Malik Serverless 577 htparam.flogi -> htparam.flogical */
