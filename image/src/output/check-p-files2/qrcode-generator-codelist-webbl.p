DEFINE TEMP-TABLE code-list
    FIELD code-num  AS INTEGER
    FIELD img-name  AS CHARACTER
    FIELD code-str  AS CHARACTER
    FIELD code-type AS INTEGER
    .

DEFINE INPUT PARAMETER num-of-qr AS INTEGER.
DEFINE INPUT PARAMETER type-code AS INTEGER.
DEFINE INPUT PARAMETER licenseNr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR code-list.

DEFINE VARIABLE encodedtext     AS CHARACTER NO-UNDO.
DEFINE VARIABLE dataQR          AS CHARACTER NO-UNDO.
DEFINE VARIABLE pathQR          AS CHARACTER NO-UNDO.
DEFINE VARIABLE dirQR           AS CHARACTER NO-UNDO.
DEFINE VARIABLE msg-result      AS CHARACTER NO-UNDO.

DEFINE VARIABLE initial-date    AS DATE NO-UNDO.

DEFINE VARIABLE int-date        AS INTEGER NO-UNDO.
DEFINE VARIABLE int-time        AS INTEGER NO-UNDO.
DEFINE VARIABLE outlet-number   AS INTEGER NO-UNDO.    
DEFINE VARIABLE count-i         AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-zeit       AS INTEGER NO-UNDO.
DEFINE VARIABLE time-j          AS INTEGER NO-UNDO.    
DEFINE VARIABLE q248-count      AS INTEGER INITIAL 1 NO-UNDO.    
DEFINE VARIABLE num-qr          AS INTEGER NO-UNDO.

int-time = 0.    
initial-date = DATE(01,01,2022).
int-date = TODAY - initial-date.        

dirQR = "C:\e1-vhp\Zint\BarcodeData".

RUN qrcode-generatorbl.p(1, INPUT TABLE code-list, OUTPUT q248-count, OUTPUT msg-result).

IF q248-count NE 1 THEN num-qr = (q248-count + num-of-qr) - 1.
ELSE num-qr = num-of-qr.

DO count-i = q248-count TO num-qr:         
    int-time = TIME + count-i.
    encodedtext = STRING(licenseNr) + STRING(int-date, "9999") + STRING(int-time, "99999").      
    
    dataQR = encodedtext.
    pathQR = dirQR + "\NSCashless" + STRING(count-i, "999") + ".png".

    CREATE code-list.
    ASSIGN
        code-list.code-num  = count-i
        code-list.code-type = type-code
        code-list.img-name  = pathQR
        code-list.code-str  = dataQR
        .             
END.    
