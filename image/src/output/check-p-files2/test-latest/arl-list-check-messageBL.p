
DEF INPUT  PARAMETER arl-list-resnr     AS INT.
DEF INPUT  PARAMETER arl-list-reslinnr  AS INT.
DEF OUTPUT PARAMETER avail-msg          AS LOGICAL INIT NO.

FIND FIRST messages WHERE /* messages.gastnr = res-line.gastnrmember AND */ 
  messages.resnr = arl-list-resnr 
  AND messages.reslinnr = arl-list-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE messages THEN avail-msg = YES.
