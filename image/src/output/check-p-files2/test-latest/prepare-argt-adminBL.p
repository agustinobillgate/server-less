
DEF TEMP-TABLE t-arrangement LIKE arrangement
    FIELD waehrungsnr AS CHAR.

DEF TEMP-TABLE w-list
    FIELD bez AS CHAR
    FIELD first-bez AS CHAR.

DEF INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.

DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR w-list.
DEF OUTPUT PARAMETER TABLE FOR t-arrangement.

DEFINE VARIABLE foreign-rate        AS LOGICAL.
DEFINE VARIABLE local-nr            AS INTEGER.
DEFINE VARIABLE foreign-nr          AS INTEGER.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "prepare-argt-admin".

DEFINE BUFFER waehrung1    FOR waehrung. 

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended( "Local Currency Code incorrect! (Param 152 / Grp 7)", lvCAREA, "":U).
  RETURN.
END. 
local-nr = waehrung.waehrungsnr. 
IF foreign-rate THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE waehrung THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended( "Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvCAREA, "":U).
    RETURN. 
  END. 
  foreign-nr = waehrung.waehrungsnr. 
END.


RUN update-argt.


FOR EACH arrangement WHERE arrangement.segmentcode = 0
    NO-LOCK BY arrangement.argtnr:
    CREATE t-arrangement.
    BUFFER-COPY arrangement TO t-arrangement.

    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = arrangement.betriebsnr 
        NO-LOCK.
    ASSIGN t-arrangement.waehrungsnr = waehrung1.bezeich.
END.

PROCEDURE update-argt:
DEFINE BUFFER argt FOR arrangement. 
  IF foreign-rate THEN 
  DO: 
    FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE foreign-nr
        AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich:
        CREATE w-list.
        ASSIGN
          w-list.bez = waehrung1.bezeich.
    END. 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = foreign-nr NO-LOCK.
    IF AVAILABLE waehrung1 THEN
    DO:
        CREATE w-list.
        ASSIGN w-list.first-bez = waehrung1.bezeich.
    END.
  END.
  ELSE
  DO:
    FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE local-nr 
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
      CREATE w-list.
      ASSIGN
        w-list.bez = waehrung1.bezeich.
    END. 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = local-nr NO-LOCK. 
    IF AVAILABLE waehrung1 THEN
    DO:
        CREATE w-list.
        ASSIGN w-list.first-bez = waehrung1.bezeich.
    END.
  END. 
  FIND FIRST argt WHERE argt.betriebsnr = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE argt THEN RETURN. 
  FOR EACH argt WHERE argt.betriebsnr = 0: 
    IF NOT foreign-rate THEN argt.betriebsnr = local-nr. 
    ELSE argt.betriebsnr = foreign-nr. 
  END. 
END. 
