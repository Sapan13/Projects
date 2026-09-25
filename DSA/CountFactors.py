def Count_Factores(n):
        count=0
        x=1
        while x*x<=n:
            if n%x==0:
                count+=1
                if n//x!=x:
                    count+=1
            x+=1
        return count
            
    
print(Count_Factores(78))