/*FD Nov 17, 2020 => BL for vhp web based move from UI progress*/

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER usercode AS CHARACTER INITIAL "".
DEFINE INPUT-OUTPUT PARAMETER passwd AS CHARACTER INITIAL "".

IF passwd EQ ? THEN passwd = "".

IF case-type = 1 THEN RUN decode-string.
ELSE IF case-type = 2 THEN RUN encode-string.

PROCEDURE decode-string: 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = usercode. 
  j = asc(SUBSTR(s, 1, 1)) - 71. 
  len = length(usercode) - 1. 
  s = SUBSTR(usercode, 2, len). 
  DO len = 1 TO length(s): 
    passwd = passwd + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
  passwd = SUBSTR(passwd, 5, (length(passwd) - 4)). 
END. 

PROCEDURE encode-string: 
DEFINE VARIABLE s AS CHAR FORMAT "x(50)". 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE ch AS CHAR INITIAL "". 
 
  j = random(1,9). 
  passwd = STRING(j) + passwd. 
  j = random(1,9). 
  passwd = STRING(j) + passwd. 
  j = random(1,9). 
  passwd = STRING(j) + passwd. 
  j = random(1,9). 
  passwd = STRING(j) + passwd. 
 
  j = random(1,9). 
  ch = CHR(ASC(STRING(j)) + 23). 
  usercode = ch. 
  j = asc(ch) - 71. 
  DO len = 1 TO length(passwd): 
    usercode = usercode + chr(asc(SUBSTR(passwd,len,1)) + j). 
  END. 

  passwd = "".
END. 
