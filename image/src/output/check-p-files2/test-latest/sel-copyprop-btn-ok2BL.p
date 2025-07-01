DEFINE TEMP-TABLE tempcopy
    FIELD loc-nr  AS INTEGER
    FIELD loc-nm  AS CHAR       FORMAT "x(24)"
    FIELD zinr    AS CHAR       FORMAT "x(5)"
    FIELD qty     AS INTEGER
    FIELD temp-Selected AS LOGICAL INITIAL NO. 

DEF INPUT PARAMETER TABLE FOR tempcopy.
DEF INPUT PARAMETER property-nr AS INT.

DEF OUTPUT PARAMETER flag AS INT INIT 0.

DEFINE BUFFER propbuff  FOR eg-property.

DEF VAR blcopy       AS CHAR NO-UNDO.
DEF VAR nr           AS INT NO-UNDO.
DEF VAR asset        AS CHAR NO-UNDO.
DEF VAR bezeich      AS CHAR NO-UNDO.
DEF VAR location     AS INT NO-UNDO.
DEF VAR zinr         AS CHAR NO-UNDO.
DEF VAR brand        AS CHAR NO-UNDO.
DEF VAR capacity     AS CHAR NO-UNDO.
DEF VAR dimension    AS CHAR NO-UNDO.
DEF VAR TYPE         AS CHAR NO-UNDO.
DEF VAR maintask     AS INT NO-UNDO.
DEF VAR str-maintask AS CHAR NO-UNDO.
DEF VAR datum        AS DATE NO-UNDO.
DEF VAR price        AS DECIMAL NO-UNDO.
DEF VAR spec         AS CHAR NO-UNDO.
DEF VAR meterRec     AS LOGICAL NO-UNDO.
DEF VAR edBezeich    AS CHAR NO-UNDO.
DEF VAR i            AS INTEGER.
DEF VAR j            AS CHAR FORMAT "x(30)".
DEF VAR tmp-nr       AS INTEGER.

FIND FIRST eg-property WHERE eg-property.nr = property-nr NO-LOCK.
IF AVAILABLE eg-property THEN
DO:
    blcopy = "1".
    ASSIGN
        asset = eg-property.asset
        bezeich = eg-property.bezeich
        location = eg-property.location
        zinr = eg-property.zinr
        brand  = eg-property.brand
        capacity  = eg-property.capacity
        dimension = eg-property.dimension
        TYPE  = eg-property.TYPE
        maintask  = eg-property.maintask
        datum  = TODAY
        price  = eg-property.price
        spec  = eg-property.spec
        meterRec = eg-property.meterrec.

    i = NUM-ENTRIES(bezeich, "(").
    edBezeich =  trim(ENTRY (1 , bezeich , "(" )).

    FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = maintask NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
        str-maintask = queasy.CHAR1.

END.
ELSE
DO:
    blcopy = "0".
END.

IF blcopy = "1" THEN
DO:
    FOR EACH tempcopy WHERE tempcopy.temp-selected NO-LOCK:
    RUN init-nr (OUTPUT tmp-nr).
    nr = tmp-nr.

    if tempcopy.zinr = "" then
    do:
        FIND FIRST propbuff WHERE propbuff.bezeich = edBezeich
            AND propbuff.maintask = maintask
            AND propbuff.location = tempcopy.loc-nr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE propbuff THEN
        DO:
          CREATE eg-property.
          ASSIGN
            eg-property.nr = nr
            eg-property.asset = asset
            eg-property.bezeich = edBezeich /*/*str-maintask*/ + " (" + STRING(nr)+ ")" /*bezeich*/ */
            eg-property.location = tempcopy.loc-nr
            eg-property.zinr = ""
            eg-property.brand = brand 
            eg-property.capacity = capacity 
            eg-property.dimension = dimension
            eg-property.TYPE  = TYPE
            eg-property.maintask = maintask
            eg-property.datum = datum
            eg-property.price  = price
            eg-property.spec  = spec
            eg-property.activeflag = YES
            eg-property.meterrec = meterRec
          .
        END.
    end.
    else
    do:
      FIND FIRST propbuff WHERE propbuff.bezeich = edBezeich
          AND propbuff.maintask = maintask
          AND propbuff.location = tempcopy.loc-nr
          AND propbuff.zinr = tempcopy.zinr
          NO-LOCK NO-ERROR.
      IF NOT AVAILABLE propbuff THEN
      DO:
        CREATE eg-property.
        ASSIGN
            eg-property.nr = nr
            eg-property.asset = asset
            eg-property.bezeich = edBezeich /*/*str-maintask*/ + " (" + STRING(nr)+ ")" /*bezeich*/ */
            eg-property.location = tempcopy.loc-nr
            eg-property.zinr = tempcopy.zinr
            eg-property.brand = brand 
            eg-property.capacity = capacity 
            eg-property.dimension = dimension
            eg-property.TYPE  = TYPE
            eg-property.maintask = maintask
            eg-property.datum = datum
            eg-property.price  = price
            eg-property.spec  = spec
            eg-property.activeflag = YES
            eg-property.meterrec = meterRec .     
      END.
    end.

    END.

    FOR EACH tempcopy :
        DELETE tempcopy.
    END.
    
    flag = 1.
END.

PROCEDURE init-nr :
    DEFINE OUTPUT PARAMETER def-nr AS INTEGER.
    DEFINE VARIABLE temp-nr AS INTEGER INITIAL 0.

    FOR EACH eg-property BY eg-property.nr :
        IF temp-nr = 0 THEN
        DO:
            temp-nr = eg-property.nr.
        END.
        ELSE
        DO:
            IF temp-nr < eg-property.nr THEN
                temp-nr = eg-property.nr.
            ELSE temp-nr = temp-nr.
        END.
    END.
    def-nr = temp-nr + 1. 
END. 
