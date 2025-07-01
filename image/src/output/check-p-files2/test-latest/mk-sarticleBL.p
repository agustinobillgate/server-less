DEFINE INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER case-type        AS INT  NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER ioInt1    AS INT  NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER ioInt2    AS INT  NO-UNDO.
DEFINE INPUT PARAMETER inpInt           AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER opt             AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER outChar         AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER str-msg         AS CHAR NO-UNDO INIT "".

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "mk-sarticle". 
     
IF case-type = 1 THEN
DO:
    FIND FIRST l-untergrup WHERE l-untergrup.zwkum = ioInt1 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE l-untergrup THEN 
    DO: 
        opt = YES.
        FIND FIRST queasy WHERE queasy.KEY = 29 AND queasy.number2 = ioInt1
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.number1 NE inpInt THEN
        DO:
            str-msg = translateExtended ("Subgroup-No belongs to other Maingroup",
                                         lvCAREA,"").
            ioInt1 = ioInt2.
            RETURN.
        END.
        outChar = l-untergrup.bezeich. 
        ioInt2 = l-untergrup.zwkum. 
    END. 
    ELSE 
    DO: 
        ioInt1 = ioInt2.
        IF ioInt2 NE 0 THEN
            str-msg = translateExtended ("No such sub-group number found",
                                         lvCAREA,"").
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST l-hauptgrp WHERE l-hauptgrp.endkum = ioInt1 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-hauptgrp THEN 
        ASSIGN outChar = l-hauptgrp.bezeich
               ioInt2  = l-hauptgrp.endkum
               opt = YES.
    ELSE 
    DO: 
        ioInt1 = ioInt2. 
        IF ioInt2 NE 0 THEN 
            str-msg = translateExtended ("No such main-group number found",lvCAREA,""). 
    END. 
END.
ELSE IF case-type = 3 THEN
DO:
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = ioInt1 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-lieferant THEN 
        ASSIGN ioInt2 = ioInt1
               outChar = l-lieferant.firma
               opt = YES. 
    ELSE IF ioInt1 NE 0 THEN 
        ASSIGN ioInt1 = ioInt2
               str-msg = translateExtended ("No such Supplier Number found",lvCAREA,""). 
END.
ELSE IF case-type = 4 THEN
DO:
    FIND FIRST h-rezept WHERE h-rezept.artnrrezept = ioInt1 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE h-rezept THEN 
        ASSIGN str-msg = translateExtended ("Recipe does not exist",lvCAREA,"")
               ioInt1 = inpInt
               opt = YES. 
    ELSE outChar = h-rezept.bezeich. 
END.
