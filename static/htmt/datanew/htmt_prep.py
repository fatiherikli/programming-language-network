import re





def main():
    filename="144cutoff.txt"
    fp=open(filename,'r')
    filename_out="144cufoff.csv"
    fout=open(filename_out,'w')
    
    for line in fp.readlines():
        line=re.sub(r'\n','',line)
        
        #"UYSAL M-NO PUB-9999" "APX J-NO PUB-9999" 11.0
        elem=re.split(r'\"',line)
        if len(elem)>3:
            try: mentions=int(float(re.sub(r'.*\" ','',line)))
            except:mentions=0
            
            ffrom=elem[1]
            tto=elem[3]
            
            from_name=re.sub(r' .*','',ffrom)
            from_pub=re.sub(r'^\w+ ','',ffrom)
            to_name=re.sub(r' .*','',tto)
            to_pub=re.sub(r'^\w+ ','',tto)

            liner=from_name+","+from_pub+","+to_name+","+to_pub+","+str(mentions)
            print liner
            fout.write(liner+"\n")
        
    fout.close()
    fp.close()
    return


if __name__ == '__main__':            
    main()
   



