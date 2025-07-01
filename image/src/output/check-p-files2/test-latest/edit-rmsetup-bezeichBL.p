
DEF INPUT PARAMETER bk-list-bezeich AS CHAR.
DEF INPUT PARAMETER bk-list-raum AS CHAR.
DEF OUTPUT PARAMETER avail-bk-rset1 AS LOGICAL INIT NO.

DEFINE buffer bk-rset1 FOR bk-rset. 

FIND FIRST bk-rset1 WHERE bk-rset1.bezeich = bk-list-bezeich 
  AND bk-rset1.raum = bk-list-raum NO-LOCK NO-ERROR. 
IF AVAILABLE bk-rset1 THEN avail-bk-rset1 = YES.
