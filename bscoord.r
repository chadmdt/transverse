# Rscript orient.R pdbfile  chaines-anticorps chaines_antigènes demi-longueur-x demi-longueur-y nb-points-x nb-points-y fichier-coords
# Rscript bscoord.R NR_LH_Protein_Kabat/1A14_1.pdb  L,H N 10 10 100 100 coord.dat
#
# pdbfile="1A14.pdb"; abchains="L,H"; agchains="N"
library(bio3d)
library(e1071)

args=commandArgs(trailingOnly=TRUE)
pdbfile=args[1]
abchains=args[2]
agchains=args[3]
abchains=unlist(strsplit(abchains,split=","))
agchains=unlist(strsplit(agchains,split=","))
Lx=as.double(args[4])
Ly=as.double(args[5])
Nx=as.integer(args[6])
Ny=as.integer(args[7])
outfile=args[8]

pdb=read.pdb(pdbfile)
pdb=trim.pdb(pdb, string="protein")
cat("chains=", unique(pdb$atom$chain),"\n")
a.inds=atom.select(pdb, chain=abchains)
b.inds=atom.select(pdb, chain=agchains)
X=matrix(pdb$xyz,byrow=TRUE, ncol=3)
y=double(nrow(X))
y[a.inds$atom]=1
y[b.inds$atom]=-1
cat(sum(y==1), sum(y==-1),"\n")
# séparation linéaire entre L,H et N
wts=100 / table(y)
result=svm(X,y, type="C-classification", kernel="linear", class.weights=wts, scale=FALSE, cost=100)
Ta=table(fitted(result), y)
print(Ta)
beta0=coef(result)[1]
beta=coef(result)[2:4]
bnorm2=sum(beta**2)

h.inds=atom.select(pdb, chain="H")
Hc=apply(X[h.inds$atom,],2,mean)
l.inds=atom.select(pdb, chain="L")
Lc=apply(X[l.inds$atom,],2,mean)


Hc=(diag(3)-1/bnorm2*beta%*%t(beta))%*%Hc-beta0/bnorm2*beta
Lc=(diag(3)-1/bnorm2*beta%*%t(beta))%*%Lc-beta0/bnorm2*beta
Mc=(Hc+Lc)/2
u=(Hc-Lc)
A=cbind(u,beta)
v=c(det(A[-1,]),-det(A[-2,]),det(A[-3,]))
dx=u/sqrt(sum(u*u))*Lx
dy=v/sqrt(sum(v*v))*Ly
O=Mc-dx-dy
dx=dx/(Nx-1); dy=dy/(Ny-1)
x=matrix(0,Nx*Ny,3)
k=0
for (i in 1:Nx)
    for (j in 1:Ny) {
    	k=k+1	
    	x[k,]=O+(i-1)*dx+(j-1)*dy
    }
unlink(outfile)
write.table(x, quote=FALSE, row.names=FALSE, col.names=FALSE, sep=",",file=outfile)