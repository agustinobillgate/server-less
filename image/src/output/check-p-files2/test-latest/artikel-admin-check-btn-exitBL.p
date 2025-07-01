
DEF INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER msg-str      AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "artikel-admin".

FOR EACH artikel NO-LOCK,
    FIRST hoteldpt WHERE hoteldpt.num = artikel.departement :
    FIND FIRST zwkum WHERE zwkum.zknr = artikel.zwkum
        AND zwkum.departement = artikel.departement NO-LOCK NO-ERROR.
    IF NOT AVAILABLE zwkum THEN
    DO:
        msg-str = translateExtended ("Wrong subgroup setup!",lvCAREA,"")
                + CHR(10) + translateExtended ("Artno : ",lvCAREA,"") + STRING(artikel.artnr)
                + CHR(10) + translateExtended ("Dept : ",lvCAREA,"") + STRING(artikel.departement).
    END.
    IF msg-str NE "" THEN LEAVE.
END.
