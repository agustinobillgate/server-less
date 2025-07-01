DEFINE TEMP-TABLE q1-list
    FIELD resnr       LIKE res-line.resnr
    FIELD zinr        LIKE res-line.zinr
    FIELD code        LIKE res-line.code
    FIELD resstatus   LIKE res-line.resstatus
    FIELD erwachs     LIKE res-line.erwachs
    FIELD kind1       LIKE res-line.kind1
    FIELD gratis      LIKE res-line.gratis
    FIELD bemerk      LIKE res-line.bemerk
    FIELD billnr      LIKE bill.billnr
    FIELD g-name      LIKE guest.name
    FIELD vorname1    LIKE guest.vorname1
    FIELD anrede1     LIKE guest.anrede1
    FIELD anredefirma LIKE guest.anredefirma
    FIELD bill-name   LIKE bill.NAME
    FIELD ankunft     LIKE res-line.ankunft
    FIELD abreise     LIKE res-line.abreise
    FIELD nation1     LIKE guest.nation1
    FIELD parent-nr   LIKE bill.parent-nr
    FIELD reslinnr    LIKE res-line.reslinnr
    FIELD resname     LIKE res-line.NAME
    FIELD name-bg-col AS INT INIT 15
    FIELD name-fg-col AS INT 
    FIELD bill-bg-col AS INT INIT 15
    FIELD bill-fg-col AS INT.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER zinr           AS CHAR.
DEF INPUT  PARAMETER h-resnr        AS INT.
DEF INPUT  PARAMETER h-reslinnr     AS INT.
DEF INPUT  PARAMETER balance        AS DECIMAL.

DEF OUTPUT PARAMETER dept-mbar      AS INT.
DEF OUTPUT PARAMETER dept-ldry      AS INT.
DEF OUTPUT PARAMETER bilrecid       AS INT.
DEF OUTPUT PARAMETER mc-pos1        AS INT.
DEF OUTPUT PARAMETER mc-pos2        AS INT.
DEF OUTPUT PARAMETER mc-flag        AS LOGICAL.
DEF OUTPUT PARAMETER fl-code        AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str2       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-rzinr".

DEF VARIABLE bill-date AS DATE NO-UNDO.
DEF VARIABLE res-bemerk AS CHARACTER NO-UNDO.
DEF VARIABLE loopk AS INTEGER NO-UNDO.

/*Alder - Serverless - Issue 401 - Start*/
/*IF NOT CONNECTED("vhp") THEN
DO:
  ASSIGN
    msg-str  = translateExtended ("DB not connected.",lvCAREA,"")  
    bilrecid = 0
    fl-code  = 2
  .
  RETURN.
END.*/
/*Alder - Serverless - Issue 401 - End*/

FIND FIRST htparam WHERE htparam.paramnr = 949 NO-LOCK.
IF htparam.feldtyp = 1 THEN dept-mbar = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 1081 NO-LOCK.
IF htparam.feldtyp = 1 THEN dept-ldry = htparam.finteger.

FIND FIRST bill WHERE bill.resnr = h-resnr 
  AND bill.reslinnr = h-reslinnr AND bill.zinr NE "" 
  AND bill.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE bill THEN 
DO: 
  FIND FIRST res-line WHERE res-line.resnr = h-resnr
      AND res-line.reslinnr = h-reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE res-line AND res-line.CODE NE "" THEN
  DO:
    FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = 
      INTEGER(res-line.code) NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.logi1 
      AND dept NE dept-mbar AND dept NE dept-ldry THEN 
    DO:
      msg-str = msg-str + CHR(2)
              + translateExtended ("CASH BASIS Billing Instruction :",lvCAREA,"")  
              + queasy.char1
              + CHR(10)
              + translateExtended ("Room Transfer not possible",lvCAREA,"").
      bilrecid = 0.
      fl-code = 1.
      RETURN.
    END.
  END.
  IF bill.flag = 0 THEN
  DO:
    bilrecid = RECID(bill). 
    RUN check-creditlimit. 
    fl-code = -1.
    /*RETURN.*/
  END.
END. 
 
FIND FIRST htparam WHERE paramnr = 336 NO-LOCK. 
IF htparam.feldtyp = 4 THEN 
DO: 
  mc-flag = htparam.flogical. 
  FIND FIRST htparam WHERE paramnr = 337 NO-LOCK. 
  mc-pos1 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 338 NO-LOCK. 
  mc-pos2 = htparam.finteger. 
END.
DEFINE BUFFER guest2 FOR guest.
DEFINE BUFFER bbuff FOR bill.
FOR EACH res-line WHERE res-line.active-flag = 1 
    /* AND res-line.resstatus NE 12 */ AND res-line.zinr GE zinr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK,
    FIRST bbuff WHERE bbuff.resnr = res-line.resnr AND bbuff.reslinnr
    = res-line.reslinnr NO-LOCK BY res-line.zinr 
    BY bbuff.parent-nr  BY res-line.reslinnr BY res-line.name:
    CREATE q1-list.
    ASSIGN
    q1-list.resnr       = res-line.resnr
    q1-list.zinr        = res-line.zinr
    q1-list.code        = res-line.code
    q1-list.resstatus   = res-line.resstatus
    q1-list.erwachs     = res-line.erwachs
    q1-list.kind1       = res-line.kind1
    q1-list.gratis      = res-line.gratis
    q1-list.bemerk      = res-line.bemerk
    q1-list.billnr      = bbuff.billnr
    q1-list.g-name      = guest.name
    q1-list.vorname1    = guest.vorname1
    q1-list.anrede1     = guest.anrede1
    q1-list.anredefirma = guest.anredefirma
    q1-list.bill-name   = bbuff.NAME
    q1-list.ankunft     = res-line.ankunft
    q1-list.abreise     = res-line.abreise
    q1-list.nation1     = guest.nation1
    q1-list.parent-nr   = bbuff.parent-nr
    q1-list.reslinnr    = res-line.reslinnr
    q1-list.resname     = res-line.NAME
    .
    IF (dept NE dept-mbar AND dept NE dept-ldry) THEN
    IF res-line.code NE "" THEN
    DO:
      FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = 
        INTEGER(res-line.code) NO-LOCK NO-ERROR. 
      IF AVAILABLE queasy AND queasy.logi1 THEN 
        ASSIGN q1-list.name-bg-col = 12
               q1-list.name-fg-col = 15
        .
    END.
 
    IF res-line.resstatus = 12 THEN
    ASSIGN q1-list.bill-bg-col = 2
           q1-list.bill-fg-col = 15.

    /*FDL August 28, 2023 => Ticket 024948*/
    ASSIGN  
      q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(10),"").
      q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(13),"").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"~n","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"\n","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"~r","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"~r~n","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(10) + CHR(13),"").

    res-bemerk = "".
    DO loopk = 1 TO LENGTH(q1-list.bemerk):
        IF ASC(SUBSTR(q1-list.bemerk, loopk, 1)) = 0 THEN.
        ELSE res-bemerk = res-bemerk + SUBSTR(q1-list.bemerk, loopk, 1). 
    END.
    ASSIGN q1-list.bemerk = res-bemerk.

    IF LENGTH(q1-list.bemerk) LT 3 THEN q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(32),"").
    IF LENGTH(q1-list.bemerk) EQ ? THEN q1-list.bemerk = "".
    /*End FDL*/
END.

/* check if c/o with unbalanced bill is allowed */
FIND FIRST htparam WHERE htparam.paramnr = 974 NO-LOCK.
IF NOT htparam.flogical THEN RETURN.

RUN htpdate.p(110, OUTPUT bill-date).

FOR EACH res-line WHERE res-line.resstatus = 8
  AND res-line.abreise = bill-date
  AND res-line.l-zuordnung[3] = 0
  AND res-line.zinr GE zinr NO-LOCK, 
  FIRST guest WHERE guest.gastnr = res-line.gastnrmember
  NO-LOCK BY res-line.zinr BY res-line.reslinnr BY res-line.name:
  FOR EACH bbuff WHERE bbuff.resnr = res-line.resnr 
    AND bbuff.parent-nr = res-line.reslinnr AND bbuff.saldo NE 0 
    NO-LOCK BY bbuff.reslinnr:
    CREATE q1-list.
    ASSIGN
    q1-list.resnr       = res-line.resnr
    q1-list.zinr        = res-line.zinr
    q1-list.code        = res-line.code
    q1-list.resstatus   = res-line.resstatus
    q1-list.erwachs     = res-line.erwachs
    q1-list.kind1       = res-line.kind1
    q1-list.gratis      = res-line.gratis
    q1-list.bemerk      = res-line.bemerk
    q1-list.billnr      = bbuff.billnr
    q1-list.g-name      = guest.name
    q1-list.vorname1    = guest.vorname1
    q1-list.anrede1     = guest.anrede1
    q1-list.anredefirma = guest.anredefirma
    q1-list.bill-name   = bbuff.NAME
    q1-list.ankunft     = res-line.ankunft
    q1-list.abreise     = res-line.abreise
    q1-list.nation1     = guest.nation1
    q1-list.parent-nr   = bbuff.parent-nr
    q1-list.reslinnr    = res-line.reslinnr
    q1-list.resname     = res-line.NAME 
    .
    IF (dept NE dept-mbar AND dept NE dept-ldry) THEN
    IF res-line.code NE "" THEN
    DO:
      FIND FIRST queasy WHERE queasy.key = 9 AND queasy.number1 = 
        INTEGER(res-line.code) NO-LOCK NO-ERROR. 
      IF AVAILABLE queasy AND queasy.logi1 THEN 
        ASSIGN q1-list.name-bg-col = 12
               q1-list.name-fg-col = 15
        .
    END.

    /*FDL August 28, 2023 => Ticket 024948*/
    ASSIGN  
      q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(10),"").
      q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(13),"").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"~n","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"\n","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"~r","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,"~r~n","").
      q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(10) + CHR(13),"").

    res-bemerk = "".
    DO loopk = 1 TO LENGTH(q1-list.bemerk):
        IF ASC(SUBSTR(q1-list.bemerk, loopk, 1)) = 0 THEN.
        ELSE res-bemerk = res-bemerk + SUBSTR(q1-list.bemerk, loopk, 1). 
    END.
    ASSIGN q1-list.bemerk = res-bemerk.

    IF LENGTH(q1-list.bemerk) LT 3 THEN q1-list.bemerk = REPLACE(q1-list.bemerk,CHR(32),"").
    IF LENGTH(q1-list.bemerk) EQ ? THEN q1-list.bemerk = "".
    /*End FDL*/
  END.
END.

PROCEDURE check-creditlimit: 
DEFINE VARIABLE klimit AS DECIMAL. 
  FIND FIRST  htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
  FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK. 
  IF guest.kreditlimit NE 0 THEN klimit = guest.kreditlimit. 
  ELSE 
  DO: 
    IF htparam.fdecimal NE 0 THEN klimit = htparam.fdecimal. 
    ELSE klimit = htparam.finteger. 
  END. 
  IF (bill.saldo + balance) GT klimit THEN 
  DO:
    msg-str2 = msg-str2 + CHR(2) + "&Q"
             + translateExtended ("OVER Credit Limit found: ",lvCAREA,"") 
             + translateExtended ("Given Limit  =",lvCAREA,"") + " " 
             + TRIM(STRING(klimit,">>>,>>>,>>>,>>9")) + " / " 
             + translateExtended ("Bill Balance =",lvCAREA,"") + " " 
             + TRIM(STRING(bill.saldo, "->>>,>>>,>>>,>>9.99")) 
             + CHR(10)
             + translateExtended ("Restaurant Balance =",lvCAREA,"") + " " 
             + TRIM(STRING(balance,"->>>,>>>,>>>,>>9.99")) 
             + CHR(10)
             + translateExtended ("Do you wish to CANCEL the room transfer?",lvCAREA,"").
  END. 
END. 



