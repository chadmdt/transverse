library(bio3d)
library(argparser)
p=arg_parser("A basic program to select chains from a pdb")
p=add_argument(p, "pdbfile", help="input pdb file")
p=add_argument(p, "--chain",  default=NA, help="ligand chain selection")
p=add_argument(p, "--outfile", default="bs.pdb", help="output pdb file")
argv = parse_args(p)
pdbfile=argv$pdbfile
chains=argv$chain
outfile=argv$outfile

chains=unlist(strsplit(chains,split=","))
pdb=suppressWarnings(bio3d::read.pdb(pdbfile,verbose=FALSE))

pdb=trim.pdb(pdb, chains=chains)
write.pdb(pdb, file=outfile)
