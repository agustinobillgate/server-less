DEFINE INPUT PARAMETER rml-resnr    AS INT.
DEFINE INPUT PARAMETER rml-reslinnr AS INT.
DEFINE INPUT PARAMETER user-init    AS CHAR.
DEFINE INPUT PARAMETER chg-date     AS DATE.
DEFINE INPUT PARAMETER begin-time   AS CHAR.
DEFINE INPUT PARAMETER ending-time  AS CHAR.
DEFINE INPUT PARAMETER begin-i      AS INT.
DEFINE INPUT PARAMETER ending-i     AS INT.
DEFINE INPUT PARAMETER chg-room     AS CHAR.
DEFINE INPUT PARAMETER chg-table    AS CHAR.
DEFINE INPUT PARAMETER c-status     AS CHAR.
DEFINE INPUT PARAMETER r-status     AS INT.
DEFINE INPUT PARAMETER recid-rl     AS INT.
DEFINE INPUT PARAMETER bk-reser-resstatus AS INT.
DEFINE OUTPUT PARAMETER mess-str    AS CHAR.

RUN ba-plan-btn-timebl.p (rml-resnr, rml-reslinnr, user-init, chg-date, begin-time, ending-time, begin-i, ending-i).
RUN ba-plan-btn-roombl.p (rml-resnr,rml-reslinnr, chg-room,user-init, chg-table).
RUN ba-plan-btn-stat2_1bl.p (NO, rml-resnr, rml-reslinnr, c-status,r-status, recid-rl, bk-reser-resstatus, user-init).

mess-str = "Modify Event Done".
