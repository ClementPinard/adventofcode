import pandas as p;print((((a:=p.read_csv("input.txt",header=None,sep=" ",index_col=0,names=["b"])).b*(a.b*((a.index=="down") - (a.index=="up")*1)).cumsum())).loc["forward"].sum()*a.b.loc["forward"].sum())