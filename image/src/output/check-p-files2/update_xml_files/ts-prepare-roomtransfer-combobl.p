DEFINE TEMP-TABLE t-h-bill LIKE h-bill  
    FIELD rec-id AS INT.

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

DEFINE TEMP-TABLE roomtf-list 
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
    FIELD bill-fg-col AS INT
    .

DEFINE INPUT PARAMETER language-code    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER h-recid          AS INTEGER.
DEFINE INPUT PARAMETER balance          AS DECIMAL.
DEFINE INPUT PARAMETER pf-file1         AS CHARACTER.
DEFINE INPUT PARAMETER pf-file2         AS CHARACTER.
DEFINE OUTPUT PARAMETER mess-info       AS CHARACTER.
DEFINE OUTPUT PARAMETER dept-mbar       AS INTEGER.
DEFINE OUTPUT PARAMETER dept-ldry       AS INTEGER.
DEFINE OUTPUT PARAMETER bilrecid        AS INTEGER.
DEFINE OUTPUT PARAMETER htl-name        AS CHARACTER.
DEFINE OUTPUT PARAMETER vSuccess        AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER TABLE FOR roomtf-list.

DEFINE VARIABLE ASremoteFlag    AS LOGICAL INIT YES NO-UNDO.
DEFINE VARIABLE multi-vat       AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE splitted        AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE dept            AS INTEGER NO-UNDO.
DEFINE VARIABLE its-ok          AS LOGICAL NO-UNDO.  
DEFINE VARIABLE fl-code         AS INTEGER NO-UNDO. 
DEFINE VARIABLE connect-param   AS CHAR    NO-UNDO.
DEFINE VARIABLE connect-paramSSL AS CHAR   NO-UNDO.
DEFINE VARIABLE lreturn         AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE msg-str         AS CHARACTER.  
DEFINE VARIABLE msg-str2        AS CHARACTER.   
DEFINE VARIABLE mc-flag         AS LOGICAL INITIAL NO.   
DEFINE VARIABLE mc-pos1         AS INTEGER INITIAL 0.   
DEFINE VARIABLE mc-pos2         AS INTEGER INITIAL 0.
DEFINE VARIABLE flag            AS LOGICAL.
                                
/****************************************************************************************/
DEFINE VARIABLE hServer         AS HANDLE NO-UNDO.
CREATE SERVER hServer.

RUN prepare-ts-biltransferbl.p(h-recid, OUTPUT multi-vat, OUTPUT dept, OUTPUT splitted,  
    OUTPUT TABLE t-h-bill).  
FIND FIRST t-h-bill.

IF balance NE 0 THEN
DO:    
    RUN ts-restinv-btn-transferbl.p(t-h-bill.rechnr, t-h-bill.departement, OUTPUT flag).
    IF flag THEN
    DO:
        mess-info = "Bill has been splitted, use Split Bill's Transfer Payment".
        RETURN. 
    END.
END.

RUN ts-biltransfer-check-vatbl.p(h-recid, multi-vat, balance, NO, splitted,  
    OUTPUT fl-code, OUTPUT its-ok).  

IF fl-code EQ 1 THEN
DO:
    mess-info = "Transfer not allowed: Other Payment found.".
    RETURN.
END.

/*Connect to Other DB*/
connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
    + ENTRY(2, pf-file2, ":") 
    + " -DirectConnect -sessionModel Session-free".
connect-paramSSL = connect-param + " -ssl -nohostverify".

lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.

IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).

/*Disconnect Other DB*/
IF NOT hServer:CONNECTED() THEN
DO:
    mess-info = "Failed to connect to combo property's DB.".
    DELETE OBJECT hServer NO-ERROR.
    RETURN.
END.

RUN prepare-ts-rzinrbl.p  
    ON hServer(language-code, dept, "", 0, 0, balance,  
               OUTPUT dept-mbar, OUTPUT dept-ldry, OUTPUT bilrecid,  
               OUTPUT mc-pos1, OUTPUT mc-pos2, OUTPUT mc-flag, OUTPUT fl-code,  
               OUTPUT msg-str, OUTPUT msg-str2, OUTPUT TABLE q1-list).

IF fl-code EQ 1 THEN
DO:
    mess-info = SUBSTR(msg-str,2).
    bilrecid = 0.
    RETURN.
END.
IF msg-str2 NE "" THEN
DO:
    mess-info = SUBSTR(msg-str2,4).
END.

FOR EACH q1-list NO-LOCK BY q1-list.zinr BY q1-list.parent-nr BY q1-list.reslinnr BY q1-list.resname:        
    q1-list.g-name = q1-list.g-name + ", " + q1-list.vorname1 + " " + q1-list.anrede1 + q1-list.anredefirma.

    CREATE roomtf-list.
    BUFFER-COPY q1-list TO roomtf-list.
END.

/*Disconnect Other DB*/
DELETE OBJECT hServer NO-ERROR.
vSuccess = YES.
