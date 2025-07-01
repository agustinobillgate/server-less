
DEF INPUT PARAMETER a-char AS CHAR.
DEF OUTPUT PARAMETER t-nationnr AS INT.
DEF OUTPUT PARAMETER t-bezeich AS CHAR.

FIND FIRST nation WHERE nation.kurzbez = a-char NO-LOCK.
ASSIGN t-nationnr = nation.nationnr
       t-bezeich = nation.bezeich.
