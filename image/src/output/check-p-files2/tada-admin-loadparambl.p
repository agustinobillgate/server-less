DEFINE TEMP-TABLE t-param
    FIELD dept      AS INTEGER   FORMAT ">>9"
    FIELD grup      AS INTEGER   FORMAT ">>9"
    FIELD number    AS INTEGER   FORMAT ">>9"   LABEL "No"
    FIELD bezeich   AS CHARACTER FORMAT "x(50)" LABEL "Description"
    FIELD typ       AS INTEGER 
    FIELD logv      AS LOGICAL 
    FIELD val       AS CHARACTER FORMAT "x(30)" LABEL "Value".

DEFINE INPUT PARAMETER dept-no AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-param.

FOR EACH t-param:
    DELETE t-param.
END.

dept-no = 1.

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 1 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    /*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 1
        queasy.char1    = "Username"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 2 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 2
        queasy.char1    = "Password"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 3 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 3
        queasy.char1    = "Interval Refresh Time"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 4 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 4
        queasy.char1    = "Department In TADA"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 5 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 5
        queasy.char1    = "Reserve Table For TADA"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 6 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 6
        queasy.char1    = "Program ID"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 7 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 7
        queasy.char1    = "Wallet ID TOPUP Points"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 8 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 8
        queasy.char1    = "Wallet ID TOPUP Balance"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 9 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 9
        queasy.char1    = "MID"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 10 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 10
        queasy.char1    = "Terminal ID FO"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 11 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 11
        queasy.char1    = "Terminal ID FB"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 12 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 12
        queasy.char1    = "SFTP Server Address"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 13 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 13
        queasy.char1    = "SFTP User ID"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 14 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 14
        queasy.char1    = "SFTP Private Key Filepath"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 15 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 15
        queasy.char1    = "SFTP PSCP Filepath"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 16 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 16
        queasy.char1    = "SFTP Server Filepath"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 17 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 17
        queasy.char1    = "SFTP Local Filepath"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 18 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 18
        queasy.char1    = "Segment For FO Transaction"
        queasy.number3  = 5
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 19 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 19
        queasy.char1    = "Department FO Transaction"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 20 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 20
        queasy.char1    = "Department FB Transaction 1"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 21 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 21
        queasy.char1    = "Department FB Transaction 2"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 22 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 22
        queasy.char1    = "Department FB Transaction 3"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 23 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 23
        queasy.char1    = "Department FB Transaction 4"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 24 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 24
        queasy.char1    = "Department FB Transaction 5"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 25 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 25
        queasy.char1    = "Dummy Guest Number For Payment FB"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.
/*num3 1=int, 2=decimal, 3=date, 4=logical, 5=char*/
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no 
    AND queasy.number2 EQ 26 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 270
        queasy.number1  = 1
        queasy.number2  = 26
        queasy.char1    = "Artikel Number For Guest Ledger"
        queasy.number3  = 1
        queasy.char2    = "" 
        queasy.betriebsnr = dept-no
        .  
END.

/*LOAD PARAM TO UI*/
FOR EACH queasy WHERE queasy.KEY EQ 270 AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept-no NO-LOCK BY queasy.number2:
    CREATE t-param.
    ASSIGN
        t-param.dept    = queasy.betriebsnr 
        t-param.grup    = queasy.number1
        t-param.number  = queasy.number2
        t-param.bezeich = queasy.char1
        t-param.typ     = queasy.number3.
    IF queasy.number3 EQ 1 THEN t-param.val = STRING(queasy.char2).
    ELSE IF queasy.number3 EQ 2 THEN t-param.val = STRING(queasy.deci1).
    ELSE IF queasy.number3 EQ 3 THEN t-param.val = STRING(queasy.date1).
    ELSE IF queasy.number3 EQ 4 THEN
    DO:
        t-param.val  = STRING(queasy.logi1).
        t-param.logv = queasy.logi1.
    END.
    ELSE IF queasy.number3 EQ 5 THEN t-param.val = STRING(queasy.char2).
END.


