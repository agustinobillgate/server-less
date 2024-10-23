DEFINE TEMP-TABLE temp   
    FIELD pos AS int   
    FIELD bezeich AS CHAR   
    FIELD artnr AS int.   
  
DEFINE TEMP-TABLE Rhbline   
  FIELD nr AS INTEGER   
  FIELD rid AS INTEGER.   
  
DEF INPUT PARAMETER rec-id-h-bill-line AS INT.  
DEF INPUT PARAMETER rec-id AS INT.  
DEF INPUT PARAMETER curr-select AS INT.  
DEF INPUT PARAMETER dept AS INT.  
  
DEF OUTPUT PARAMETER max-Rapos AS INT INIT 0.  
DEF OUTPUT PARAMETER TABLE FOR temp.  
DEF OUTPUT PARAMETER TABLE FOR Rhbline.  
  
FIND FIRST vhp.h-bill-line WHERE RECID(vhp.h-bill-line) = rec-id-h-bill-line EXCLUSIVE-LOCK.   
vhp.h-bill-line.waehrungsnr = curr-select.   
FIND CURRENT vhp.h-bill-line NO-LOCK.   
RELEASE vhp.h-bill-line.  
  
RUN ts-splitbill-build-rmenubl.p  
    (rec-id, dept, curr-select, OUTPUT max-Rapos,   
     OUTPUT TABLE temp, OUTPUT TABLE Rhbline).  
