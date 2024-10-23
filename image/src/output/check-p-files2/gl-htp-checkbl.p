

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER htp-number AS INT.
DEF INPUT  PARAMETER htgrp-number AS INT.
DEF INPUT  PARAMETER intval AS INT.
DEF INPUT  PARAMETER decval AS DECIMAL.
DEF INPUT  PARAMETER dateval AS DATE.
DEF INPUT  PARAMETER logval AS LOGICAL.
DEF INPUT  PARAMETER charval AS CHAR.
DEF INPUT  PARAMETER user-init AS CHAR.

DEF INPUT  PARAMETER i     AS INTEGER. 
DEF INPUT  PARAMETER d     AS DECIMAL. 
DEF INPUT  PARAMETER l     AS LOGICAL. 
DEF INPUT  PARAMETER dd    AS DATE. 
DEF INPUT  PARAMETER s     AS CHAR. 

DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER do-it AS LOGICAL INITIAL YES.
DEF OUTPUT PARAMETER wert   AS CHAR.
DEF OUTPUT PARAMETER logv   AS LOGICAL.
DEF OUTPUT PARAMETER flag   AS LOGICAL INIT NO.


{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "gl-htp-check-closing-date".

RUN check-closing-date.

IF msg-str NE "" OR NOT do-it THEN RETURN NO-APPLY.
ELSE 
DO:
  IF i NE intval OR d NE decval OR dd NE dateval 
    OR l NE logval OR s NE charval THEN RUN update-htparam.
END.
    

PROCEDURE check-closing-date:
  DEFINE VARIABLE d1            AS DATE.
  DEFINE VARIABLE d2            AS DATE.
  DEFINE VARIABLE mm            AS INTEGER.
  DEFINE VARIABLE yy            AS INTEGER.
  DEFINE VARIABLE close-date    AS DATE NO-UNDO.

  IF htp-number = 1118 OR htp-number = 1123 OR htp-number = 1003 OR
     htp-number = 1035 OR htp-number = 269 OR htp-number = 1014 THEN
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK.
    ASSIGN close-date = htparam.fdate.
    IF dateval LT (DATE(MONTH(close-date), 1, YEAR(close-date)) - 1) THEN
    DO:
      do-it = NO.
      msg-str = msg-str + CHR(2)
              + translateExtended ("Wrong date value in Parameter",lvCAREA,"")
              + " " + STRING(htp-number) + " - " + STRING(dateval)
              + CHR(10)
              + translateExtended ("Current G/L closing date:",lvCAREA,"")
              + " " + STRING(close-date).
      RETURN.
    END.
  END.

  IF htgrp-number = 38 AND htp-number = 597 THEN /*current accounting period*/
  DO:
      IF MONTH(dateval) = 12 THEN d2 = DATE(12, 31, YEAR(dateval)).
      ELSE d2 = DATE(MONTH(dateval) + 1, 1, YEAR(dateval)) - 1.
      d1 = DATE(MONTH(dateval), 1, YEAR(dateval)) .
      FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 1
          AND gl-jouhdr.datum  LE  d2
          AND gl-jouhdr.datum  GE d1
          NO-LOCK NO-ERROR.
      IF AVAILABLE gl-jouhdr THEN
      DO:
        do-it = NO.
        msg-str = msg-str + CHR(2)
                + translateExtended ("Closed GL journal(s) found for that period.",lvCAREA,"").
      END.              
  END.

  IF htgrp-number = 38 AND htp-number = 558 THEN /*last accounting closing period*/
  DO:
      mm = MONTH(dateval) + 1.
      yy = YEAR(dateval).
      IF mm GT 12 THEN
          ASSIGN
            mm = mm - 12
            yy = yy + 1.
      
      d1 = DATE(mm, 1, yy) .
      IF mm = 12 THEN
          d2 = DATE(12, 31, yy).
      ELSE d2 = DATE(mm + 1, 1, yy)  - 1.
      FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum GE d1 AND 
          gl-jouhdr.datum LE d2 AND gl-jouhdr.activeflag = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE gl-jouhdr THEN
      DO:
        do-it = NO.
        msg-str = msg-str + CHR(2)
                + translateExtended ("Closed GL journal(s) found for next period.",lvCAREA,"").
      END.
  END.
END.




PROCEDURE update-htparam: 
  FIND FIRST htparam WHERE htparam.paramnr = htp-number EXCLUSIVE-LOCK. 
  IF htparam.feldtyp = 1 THEN 
  DO: 
    htparam.finteger = intval. 
    wert = STRING(htparam.finteger). 
  END. 
  ELSE IF htparam.feldtyp = 2 THEN 
  DO: 
    htparam.fdecimal = decval. 
    wert = STRING(htparam.fdecimal). 
  END. 
  ELSE IF htparam.feldtyp = 3 THEN 
  DO: 
    htparam.fdate = dateval. 
    wert = STRING(htparam.fdate). 
  END. 
  ELSE IF htparam.feldtyp = 4 THEN 
  DO: 
    htparam.flogical = logval. 
    wert = STRING(htparam.flogical). 
    logv = htparam.flogical.
    flag = YES.
  END. 
  ELSE IF feldtyp = 5 THEN 
  DO: 
    htparam.fchar = charval. 
    wert = STRING(htparam.fchar). 
  END. 
  htparam.lupdate = today. 
  htparam.fdefault = user-init + " - " + STRING(time, "HH:MM:SS"). 
  FIND CURRENT htparam NO-LOCK. 
END.
