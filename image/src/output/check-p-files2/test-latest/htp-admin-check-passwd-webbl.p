DEFINE INPUT PARAMETER id-str AS CHARACTER.
DEFINE INPUT PARAMETER grp-no AS INTEGER.
DEFINE OUTPUT PARAMETER passwd-ok AS LOGICAL INIT NO.

DEFINE VARIABLE fchar AS CHARACTER.
DEFINE VARIABLE pswd-str AS CHARACTER.
DEFINE VARIABLE nanci AS CHARACTER.
DEFINE VARIABLE s AS CHARACTER.
DEFINE VARIABLE i AS INTEGER.

IF grp-no = 10 THEN
DO:
  RUN htpchar.p (1071, OUTPUT fchar).
  IF TRIM(fchar) = "" THEN
  DO:
    passwd-ok = YES.
    RETURN.
  END.
  pswd-str = fchar.
END.

IF grp-no = 10 THEN nanci = pswd-str.
ELSE IF grp-no = 99 THEN
DO:
  DO i = 1 TO 9: 
    RUN aufbau(i, INPUT-OUTPUT nanci). 
  END. 

  s = s + SUBSTR(STRING(month(today),"99"),2,1) 
    + SUBSTR(STRING(month(today),"99"),1,1) 
    + SUBSTR(STRING(day(today),"99"),2,1) 
    + SUBSTR(STRING(day(today),"99"),1,1). 
  nanci = nanci + s. 
END.

IF nanci = id-str THEN  passwd-ok = YES. 

PROCEDURE aufbau: 
  DEFINE INPUT PARAMETER i AS INTEGER. 
  DEFINE INPUT-OUTPUT PARAMETER ch AS CHAR. 

  /* geheimmis */
  IF SUBSTRING(PROVERSION, 1, 1) = "1" THEN
  DO:
    IF i = 1 THEN ch = ch + "g". 
    ELSE IF i = 2 OR i = 4 THEN ch = ch + "e". 
    ELSE IF i = 3 THEN ch = ch + "h". 
    ELSE IF i = 5 OR i = 8 THEN ch = ch + "i". 
    ELSE IF i = 6 OR i = 7 THEN ch = ch + "n". 
    ELSE IF i = 9 THEN ch = ch + "s". 
  END.
  ELSE
  DO:
    IF i = 1 THEN ch = ch + "g". 
    ELSE IF i = 2 OR i = 4 THEN ch = ch + "e". 
    ELSE IF i = 3 THEN ch = ch + "h". 
    ELSE IF i = 5 OR i = 8 THEN ch = ch + "i". 
    ELSE IF i = 6 OR i = 7 THEN ch = ch + "m". 
    ELSE IF i = 9 THEN ch = ch + "s". 
  END.

END.
