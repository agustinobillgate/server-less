DEFINE VARIABLE cPersonalKey   AS CHARACTER NO-UNDO.
DEFINE VARIABLE rKey           AS RAW.
DEFINE VARIABLE mMemptrOut     AS MEMPTR.
DEFINE VARIABLE encriptext   AS CHARACTER NO-UNDO.
DEFINE VARIABLE urlWeb  as char format "x(180)".

encriptext  = "ENG|DEMO".
/* format: "LANG|HOTELCODE" */

ASSIGN 
    cPersonalKey    = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
    rKey            = GENERATE-PBE-KEY(cPersonalKey)
    mMemptrOut      = ENCRYPT(encriptext, rKey )
    encriptext      = BASE64-ENCODE(MMEMPTROUT).    

urlWeb = "https://www.vhp-online.com/mobilecheckin?" + encriptext.

DISP urlWeb FORMAT "x(150)".
UPDATE urlWeb FORMAT "X(150)" WITH WIDTH 180.
