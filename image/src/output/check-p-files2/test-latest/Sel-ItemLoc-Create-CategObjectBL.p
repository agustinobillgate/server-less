DEFINE TEMP-TABLE  CategObjectList
    FIELD categ-nr  AS INTEGER
    FIELD categ-nm  AS CHAR
    FIELD Object-nr AS INTEGER
    FIELD Object-nm AS CHAR
    FIELD Item-nr   AS INTEGER
    FIELD Item-nm   AS CHAR.

DEFINE TEMP-TABLE cObjectList
    FIELD categ-nr  AS INTEGER
    FIELD Object-nr AS INTEGER
    FIELD Object-nm AS CHAR.

DEFINE TEMP-TABLE CategList
    FIELD categ-nr  AS INTEGER
    FIELD categ-nm  AS CHAR.

DEF INPUT PARAMETER chrZinr AS CHAR.
DEF INPUT PARAMETER IntLocation AS INT.
DEF OUTPUT PARAMETER TABLE FOR CategObjectList.
DEF OUTPUT PARAMETER TABLE FOR cObjectList.
DEF OUTPUT PARAMETER TABLE FOR CategList.

RUN create-categObject.



PROCEDURE Create-CategObject :
DEF BUFFER propertyBuff     FOR eg-property.
DEF BUFFER quesBuff         FOR queasy.
DEF BUFFER quesBuff1        FOR queasy.

DEF VAR    IntCategOb      AS INTEGER.
DEF VAR    IntObjectNr   AS INTEGER.

DEF VAR    IntCategEx-nr      AS INTEGER INITIAL 0.
DEF VAR    IntObjectEx-nr     AS INTEGER INITIAL 0.

    IF chrZinr = "" THEN
    DO:
        FOR EACH propertyBuff WHERE propertybuff.location = IntLocation AND propertybuff.activeflag = YES 
            USE-INDEX location_ix NO-LOCK :
            FIND FIRST quesbuff WHERE quesbuff.KEY = 133 AND quesbuff.number1 = propertybuff.maintask NO-LOCK NO-ERROR.
            IF AVAILABLE quesbuff THEN
            DO:
                FIND FIRST quesbuff1 WHERE quesbuff1.KEY = 132 AND quesbuff1.number1 = quesbuff.number2 NO-LOCK NO-ERROR.
                IF AVAILABLE quesbuff1 THEN
                DO:
                    IF IntCategEx-nr = 0 THEN
                    DO:
                        IntCategEx-nr = quesbuff1.number1.
                        IntCategOb    = quesbuff1.number1.
                        CREATE CategList.
                        ASSIGN CategList.categ-nr = quesbuff1.number1
                            CategList.categ-nm = quesbuff1.char1.
                    END.
                    ELSE
                    DO:
                        IntCategOb    = quesbuff1.number1.
                        IF IntCategEx-nr NE quesbuff1.number1 THEN
                        DO:
                            IntCategEx-nr = quesbuff1.number1.
                            
                            FIND FIRST categList WHERE categList.categ-nr = quesbuff1.number1 NO-LOCK NO-ERROR.
                            IF AVAILABLE categList THEN
                            DO:
    
                            END.
                            ELSE
                            DO:
                                CREATE CategList.
                                ASSIGN CategList.categ-nr = quesbuff1.number1
                                       CategList.categ-nm = quesbuff1.char1.
                            END.
    
                        END.
                        ELSE
                        DO:
                        END.
                    END.
                END.
                ELSE
                DO:
                END.
    
                IF IntObjectEx-nr = 0 THEN
                DO:
                    IntObjectEx-nr = quesbuff.number1.
                    IntObjectNr  = quesbuff.number1.
                    CREATE cObjectList.
                    ASSIGN cObjectList.categ-nr  = IntCategOb 
                           cObjectList.Object-nr = quesbuff.number1 
                           cObjectList.Object-nm = quesbuff.char1.
                END.
                ELSE
                DO:
                    IF IntObjectEx-nr NE quesbuff.number1 THEN
                    DO:
                        IntObjectEx-nr = quesbuff.number1.
                        IntObjectNr  = quesbuff.number1.
    
                        FIND FIRST cObjectList WHERE cObjectList.Object-nr = quesbuff.number1 NO-LOCK NO-ERROR.
                        IF AVAILABLE cObjectList THEN
                        DO:
                        END.
                        ELSE
                        DO:
                            CREATE cObjectList.
                            ASSIGN
                                cObjectList.categ-nr  = IntCategOb 
                                cObjectList.Object-nr = quesbuff.number1 
                                cObjectList.Object-nm = quesbuff.char1.
                         END.
                    END.
                    ELSE
                    DO:
                    END.
                END.
            END.
            ELSE
            DO:
            END.
           
            CREATE categobjectList.
            ASSIGN categobjectList.categ-nr = IntCategOb
                categobjectList.Object-nr   = IntObjectNr
                categobjectList.Item-nr     = propertybuff.nr
                categobjectList.Item-nm     = propertybuff.bezeich.
        END.
    END.
    ELSE
    DO:
        FOR EACH propertyBuff WHERE propertyBuff.location = IntLocation AND propertyBuff.zinr = ChrZinr 
            AND propertybuff.activeflag = YES USE-INDEX mtloczin_x NO-LOCK :
            FIND FIRST quesbuff WHERE quesbuff.KEY = 133 AND quesbuff.number1 = propertybuff.maintask NO-LOCK NO-ERROR.
            IF AVAILABLE quesbuff THEN
            DO:
                FIND FIRST quesbuff1 WHERE quesbuff1.KEY = 132 AND quesbuff1.number1 = quesbuff.number2 NO-LOCK NO-ERROR.
                IF AVAILABLE quesbuff1 THEN
                DO:
                    IF IntCategEx-nr = 0 THEN
                    DO:
                        IntCategEx-nr = quesbuff1.number1.
                        IntCategOb    = quesbuff1.number1.
                        
                        CREATE CategList.
                        ASSIGN categList.categ-nr = quesbuff1.number1
                            categList.categ-nm = quesbuff1.char1.
                    END.
                    ELSE
                    DO:
                        IntCategOb    = quesbuff1.number1.
                        IF IntCategEx-nr NE quesbuff1.number1 THEN
                        DO:
                            IntCategEx-nr = quesbuff1.number1.
                            
                            FIND FIRST categList WHERE categList.categ-nr = quesbuff1.number1 NO-LOCK NO-ERROR.
                            IF AVAILABLE categList THEN
                            DO:
                            END.
                            ELSE
                            DO:
                                CREATE CategList.
                                ASSIGN categList.categ-nr = quesbuff1.number1
                                       categList.categ-nm = quesbuff1.char1.
                            END.
                        END.
                        ELSE
                        DO:
                        END.
                    END.
                END.
                ELSE
                DO:
                END.
    
                IF IntObjectEx-nr = 0 THEN
                DO:
                    IntObjectEx-nr = quesbuff.number1.
                    IntObjectNr  = quesbuff.number1.
                    CREATE cObjectList.
                    ASSIGN cObjectList.categ-nr  = IntCategOb 
                           cObjectList.Object-nr = quesbuff.number1 
                           cObjectList.Object-nm = quesbuff.char1.
                END.
                ELSE
                DO:
                    IF IntObjectEx-nr NE quesbuff.number1 THEN
                    DO:
                        IntObjectEx-nr = quesbuff.number1.
                        IntObjectNr  = quesbuff.number1.
    
                        FIND FIRST cObjectList WHERE cObjectList.Object-nr = quesbuff.number1 NO-LOCK NO-ERROR.
                        IF AVAILABLE cObjectList THEN
                        DO:
                        END.
                        ELSE
                        DO:
                            CREATE cObjectList.
                            ASSIGN
                                cObjectList.categ-nr  = IntCategOb 
                                cObjectList.Object-nr = quesbuff.number1 
                                cObjectList.Object-nm = quesbuff.char1.
                         END.
                    END.
                    ELSE
                    DO:
                    END.
                END.
            END.
            ELSE
            DO:
            END.
           
            CREATE categobjectList.
            ASSIGN categobjectList.categ-nr = IntCategOb
                categobjectList.Object-nr   = IntObjectNr
                categobjectList.Item-nr     = propertybuff.nr
                categobjectList.Item-nm     = propertybuff.bezeich.
        END.
    END.

END PROCEDURE.

