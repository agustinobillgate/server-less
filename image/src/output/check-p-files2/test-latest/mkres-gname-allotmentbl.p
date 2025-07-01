DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-gastnr  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER ci-date     AS DATE    NO-UNDO.
DEF INPUT PARAMETER co-date     AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER allot-bemerk AS CHAR NO-UNDO INIT "".

DEF VARIABLE rmtype AS CHAR NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mkres-gname". 

FOR EACH kontline WHERE kontline.gastnr = inp-gastnr 
    AND kontline.kontignr GT 0 
    AND kontline.betriebsnr = 0 
    AND kontline.kontstatus = 1 
    AND kontline.ankunft LE ci-date
    AND kontline.abreise GE (co-date - 1)
    NO-LOCK BY kontline.CODE BY kontline.ankunft: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr 
        NO-LOCK NO-ERROR. 
    rmtype = "".
    IF AVAILABLE zimkateg THEN rmtype = zimkateg.kurzbez.
    IF allot-bemerk = "" THEN
        allot-bemerk = translateExtended("Allotment:",lvcAREA,"") + CHR(10).
    allot-bemerk = allot-bemerk
                 + STRING(kontline.kontcode, "x(10)  ")
                 + STRING(kontline.ankunft) + " - "
                 + STRING(kontline.abreise) + "  "
                 + STRING(rmtype, "x(6)  ")
                 + translateExtended("QTY:",lvcAREA,"")
                 + STRING(kontline.zimmeranz,">>9  ")
                 + translateExtended("A:",lvcAREA,"")
                 + STRING(kontline.erwachs, "9  ")
                 + STRING(kontline.ruecktage, ">9 ") 
                 + translateExtended("days",lvcAREA,"") + CHR(10).
END.
