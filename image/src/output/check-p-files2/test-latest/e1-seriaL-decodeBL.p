
FUNCTION CharToInt RETURNS INTEGER
  ( INPUT input-char AS CHAR) :
  RETURN ASC(input-char) - 65.
END FUNCTION.


FUNCTION IntToChar RETURNS CHAR
  ( INPUT input-int AS INTEGER) :
  RETURN CHR(input-int MODULO 26 + 65).
END FUNCTION.


FUNCTION HexToDec RETURNS INTEGER
  ( INPUT hexValue AS CHAR ) :

  DEFINE VARIABLE decValue AS INTEGER INIT 0.

  DEFINE VARIABLE i AS INTEGER.
  DEFINE VARIABLE j AS INTEGER.
  DEFINE VARIABLE tmp-dec AS INTEGER.

  DO i = 0 TO LENGTH(hexValue) - 1:
    tmp-dec = CharToInt(SUBSTRING(hexValue,LENGTH(hexValue) - i,1)).
    DO j = 1 TO i:
/*      tmp-dec = tmp-dec * 16.*/
      tmp-dec = tmp-dec * 26.

    END.
    decValue = decValue + tmp-dec.
  END.

  RETURN decValue.
END FUNCTION.


FUNCTION Unrandomize RETURNS CHAR
  (INPUT input-serial AS CHAR, INPUT input-rand AS CHAR, INPUT rand-pos AS INTEGER) :

  DEFINE VARIABLE j AS INTEGER.
  DEFINE VARIABLE i AS INTEGER.
  DEFINE VARIABLE k AS INTEGER.

  DEFINE VARIABLE jj AS INTEGER.
  DEFINE VARIABLE kk AS INTEGER.


  DEFINE VARIABLE numbers AS INTEGER EXTENT 15.

  DO i = 1 TO 15:
    numbers[i] = CharToInt(SUBSTRING(input-serial,i,1)).
  END.

  DO i = 5 TO 15:
    DO k = 1 TO 4:
      numbers[k] = (numbers[k] - numbers[i] + 4 * k) MODULO 26.
    END.
  END.

  DO j = 1 TO 15:
  
    i = 15 + 1 - j.
    DO k = 1 TO i - 1:
      numbers[k] = numbers[k] - numbers[i] + 2 * k.
    END.

    DO k = i + 1 TO 15:
      numbers[k] = numbers[k] - numbers[i] + k.
    END.
  END.


  input-serial = "".

  DO i = 1 TO 15:
    input-serial = input-serial + IntToChar(numbers[i] - 
        CharToInt(SUBSTRING(input-rand,rand-pos,1)) - i * 11).
  END.

  /*
  DO i = 1 TO 15:
    numbers[i] = CharToInt(SUBSTRING(input-serial,i,1)).
  END.

  DO j = 2 TO LENGTH(input-serial):
    i = LENGTH(input-serial) + 2 - j.

    numbers[i] = numbers[i] - numbers[i - 1].
  END.

  numbers[1] = numbers[1] - CharToInt(SUBSTRING(input-rand,rand-pos,1)).

  input-serial = "".

  DO i = 1 TO 15:
    input-serial = input-serial + IntToChar(numbers[i]).
  END.
    */
  RETURN input-serial.
END FUNCTION.

FUNCTION CombineNumber RETURNS INTEGER
  (INPUT number AS INTEGER) :

  IF number GT 9 THEN
  DO:
    number = number MODULO 10 + number - 10.
  END.
  RETURN number.
END FUNCTION.

FUNCTION CalcChecksum RETURNS CHAR
  (INPUT input-serial AS CHAR) :

  DEFINE VARIABLE checksum AS INTEGER INIT 0.
  DEFINE VARIABLE i AS INTEGER.

  DEFINE VARIABLE numbers AS INTEGER EXTENT 17.

  DO i = 1 TO 17:
    numbers[i] = CharToInt(SUBSTRING(input-serial,i,1)).
  END.

  DO i = 1 TO 16:
    checksum = (checksum + 
                CombineNumber(numbers[i] + numbers[i + 1])) MODULO 26.
  END.
  
  RETURN IntToChar(checksum).
END FUNCTION.


DEFINE INPUT PARAMETER serial-number  AS CHAR.
DEFINE OUTPUT PARAMETER license-nr    AS INTEGER.
DEFINE OUTPUT PARAMETER valid-until   AS DATE FORMAT "99/99/9999" INIT ?.
DEFINE OUTPUT PARAMETER case-id       AS INTEGER.
DEFINE OUTPUT PARAMETER parameter-int AS INTEGER.
DEFINE OUTPUT PARAMETER valid-flag    AS LOGICAL INIT NO.

/*
DEFINE VARIABLE serial-number AS CHAR.
serial-number = "RDZPMEUQXJDDRXXNGS".
DEFINE VARIABLE license-nr    AS INTEGER.
DEFINE VARIABLE valid-until   AS DATE FORMAT "99/99/9999".
DEFINE VARIABLE case-id       AS INTEGER.
DEFINE VARIABLE parameter-int AS INTEGER.
DEFINE VARIABLE valid-flag    AS LOGICAL INIT NO.
*/

DEFINE VARIABLE license-hex   AS CHAR.
DEFINE VARIABLE valid-hex     AS CHAR.
DEFINE VARIABLE case-hex      AS CHAR.
DEFINE VARIABLE parameter-hex AS CHAR.

DEFINE VARIABLE valid-str AS CHAR.

/*DEFINE VARIABLE serial-number AS CHAR.*/
DEFINE VARIABLE checksum      AS CHAR.
DEFINE VARIABLE randomizer    AS CHAR.

DEFINE VARIABLE the-serial     AS CHAR.
DEFINE VARIABLE the-randomizer AS CHAR.
DEFINE VARIABLE the-checksum   AS CHAR.



DEFINE VARIABLE i AS INTEGER.

the-serial = SUBSTRING(serial-number, 1, 15).
/*the-randomizer = SUBSTRING(serial-number, 16, 3).*/
the-randomizer = SUBSTRING(serial-number, 16, 2).
the-checksum = SUBSTRING(serial-number, 18, 1).
  

checksum = calcChecksum(serial-number + the-randomizer).

IF checksum NE the-checksum THEN 
DO:
  valid-flag = NO.
END.
ELSE 
DO:
  valid-flag = YES.
END.

/*the-serial = Unrandomize(the-serial,the-randomizer, 3).*/
the-serial = Unrandomize(the-serial,the-randomizer, 2).
the-serial = Unrandomize(the-serial,the-randomizer, 1).

license-hex   = SUBSTRING(the-serial,1,4).
valid-hex     = SUBSTRING(the-serial,5,6).
case-hex      = SUBSTRING(the-serial,11,2).
parameter-hex = SUBSTRING (the-serial,13,3).
license-nr  = HexToDec(license-hex).
valid-str    = STRING(HexToDec(valid-hex)).

DO WHILE LENGTH(valid-str) LT 8:
  valid-str = "0" + valid-str.
END.


/*valid-until  = DATE(SUBSTRING(valid-str,3,2) + "/" +
                  SUBSTRING(valid-str,1,2) + "/" +
                  SUBSTRING(valid-str,5,4)) NO-ERROR.*/

valid-until  = DATE(INTEGER(SUBSTRING(valid-str,1,2)), INTEGER(SUBSTRING(valid-str,3,2)),
                    INTEGER(SUBSTRING(valid-str,5,4))) NO-ERROR.

case-id     = HexToDec(case-hex).
parameter-int = HexToDec(parameter-hex).


/*
MESSAGE license-nr valid-until case-id parameter-int valid-flag.
*/
