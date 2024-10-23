
DEF INPUT PARAMETER h-bondruckernr AS INT.
DEF INPUT PARAMETER h-bondrucker   AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST PRINTER WHERE printer.nr = h-bondruckernr
  AND printer.bondrucker = YES NO-LOCK NO-ERROR. 
IF NOT AVAILABLE PRINTER AND h-bondrucker NE 0 THEN flag = 1.
