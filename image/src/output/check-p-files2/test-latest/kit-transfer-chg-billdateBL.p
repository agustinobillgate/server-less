
DEF INPUT PARAMETER transdate       AS DATE.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER foreign-nr      AS INT.
DEF OUTPUT PARAMETER exchg-rate     AS DECIMAL INITIAL 1.

find first htparam where paramnr = 110 no-lock.
if fdate NE transdate and double-currency then
do:
    if foreign-nr NE 0 then find first exrate where exrate.artnr = foreign-nr 
        and exrate.datum = transdate no-lock no-error.
    else find first exrate where exrate.datum = transdate no-lock no-error.
    if available exrate then exchg-rate = exrate.betrag.
end.
