DEFINE INPUT PARAMETER  strcc   AS CHAR FORMAT "x(20)".
DEFINE OUTPUT PARAMETER cardOK  AS LOGICAL.
DEFINE VARIABLE nCheckSum       AS INTEGER.
DEFINE VARIABLE fDbl            AS LOGICAL.
DEFINE VARIABLE nCharPos        AS INTEGER.
DEFINE VARIABLE nChar           AS INTEGER.

IF LENGTH(strcc) NE 16 THEN
DO:
  cardOK = NO.
  RETURN.
END.

ASSIGN
  fDbl      = NO
  nCheckSum = 0
.
strCC = REPLACE(strCC, " ", "").

DO nCharPos = LENGTH( strCC ) TO 1 BY -1:
    nChar = ASC( SUBSTR( strCC, nCharPos, 1 ) ) - ASC( "0" ).
    IF 0 <= nChar And nChar <= 9 THEN
    DO:
      IF ( fDbl ) THEN nChar = nChar * 2.
      IF 10 <= nChar THEN nChar = nChar - 9.
    END.
    nCheckSum = nCheckSum + nChar.
    fdbl = NOT fdbl.
END.
cardOK = (nchecksum MOD 10) = 0.
