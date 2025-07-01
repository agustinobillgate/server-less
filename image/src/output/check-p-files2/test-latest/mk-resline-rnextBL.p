
DEF INPUT PARAMETER resnr     AS INT.
DEF INPUT PARAMETER reslinnr  AS INT.
DEF INPUT PARAMETER t-zipreis AS DECIMAL.

FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr
    EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
  ASSIGN res-line.zipreis = t-zipreis.    /*MT 01/03/13 */
