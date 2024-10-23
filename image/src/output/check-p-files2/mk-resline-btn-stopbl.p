
DEF INPUT PARAMETER avail-t-res-line AS LOGICAL.
DEF INPUT PARAMETER t-res-line-resnr AS INT.
DEF INPUT PARAMETER t-res-line-reslinnr AS INT.
DEF INPUT PARAMETER init-time-resline1 AS INT.
DEF INPUT PARAMETER init-date-resline1 AS DATE.
DEF INPUT PARAMETER inp-resNo AS INT.
DEF INPUT PARAMETER inp-resline AS INT.
DEF INPUT PARAMETER init-time-resline AS INT.
DEF INPUT PARAMETER init-date-resline AS DATE.
DEF INPUT PARAMETER init-time-rsv AS INT.
DEF INPUT PARAMETER init-date-rsv AS DATE.

DEF VAR flag-ok AS LOGICAL.
DEF VAR a AS INT.
DEF VAR b AS DATE.
DEF VAR check-time-str AS CHAR.
DEF VAR check-time-str2 AS CHAR.

check-time-str = "res-line". /*IT*/
IF avail-t-res-line THEN
RUN check-timebl.p 
    (2, t-res-line-resnr, t-res-line-reslinnr, check-time-str, 
     init-time-resline1, init-date-resline1,
     OUTPUT flag-ok, OUTPUT a, OUTPUT b).

RUN check-timebl.p 
    (2, inp-resNo, inp-resline, check-time-str, 
     init-time-resline, init-date-resline,
     OUTPUT flag-ok, OUTPUT a, OUTPUT b).

check-time-str2 =  "reservation". /*IT*/
RUN check-timebl.p 
    (2, inp-resNo, ?, check-time-str2, 
     init-time-rsv, init-date-rsv,
     OUTPUT flag-ok, OUTPUT a, OUTPUT b).
