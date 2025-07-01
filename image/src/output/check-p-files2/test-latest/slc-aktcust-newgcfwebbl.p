
DEFINE TEMP-TABLE t-guest LIKE guest.  

DEFINE INPUT PARAMETER gname        AS CHARACTER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE OUTPUT PARAMETER gastnr      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-guest.

DEFINE VARIABLE curr-gastnr AS INTEGER.    
DEFINE VARIABLE del-gastnr  AS INTEGER.    
DEFINE VARIABLE dd          AS INTEGER.  
DEFINE VARIABLE mm          AS INTEGER.  
DEFINE VARIABLE yy          AS INTEGER.  
DEFINE VARIABLE len         AS INTEGER.  
DEFINE VARIABLE Fullfname   AS CHARACTER INITIAL ?.  
DEFINE VARIABLE province    AS CHARACTER.  
DEFINE VARIABLE city        AS CHARACTER.  
DEFINE VARIABLE succes-flag AS LOGICAL.

RUN new-gcfnrbl.p(OUTPUT curr-gastnr).

create t-guest. 
ASSIGN  
    t-guest.gastnr    = curr-gastnr    
    t-guest.name      = gname    
    t-guest.char1     = user-init  
    t-guest.karteityp = sorttype    
    t-guest.phonetik3 = user-init.

gastnr = t-guest.gastnr.
