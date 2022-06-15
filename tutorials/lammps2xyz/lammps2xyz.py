import sys
import pandas as pd 

##################################################################################################################################
# Function that converts an lammpstrj file into and xyz file
# Parameters:

# inputfile: name of the file without the extension
# Example: if the file is strain.lammpstrj, input just "strain"

def lammps2xyz(inputfile):
    with open(inputfile+".lammpstrj", "r") as f:
        with open(inputfile+".xyz", "w") as g:
            for line in f:
                if line.strip() == "ITEM: NUMBER OF ATOMS":
                    n_atoms = int(f.readline())
                    g.write(str(n_atoms)+"\n")
                    g.write("Comments\n")
                elif len(line.strip().split()) > 2:
                    if line.strip().split()[1] == "ATOMS":
                        index = list()
                        for i in line.split():
                            if i.strip() == "type":
                                index.append(line.split().index(i)-2)
                            elif i.strip() == "x" or i.strip() == "xu":
                                index.append(line.split().index(i)-2)  
                            elif i.strip() == "y" or i.strip() == "yu":
                                index.append(line.split().index(i)-2)
                            elif i.strip() == "z" or i.strip() == "zu":
                                index.append(line.split().index(i)-2)  
                        a = f.readline().split()
                        g.write(a[index[0]]+";"+a[index[1]]+";"+a[index[2]]+";"+a[index[3]]+"\n")
                        for i in range(n_atoms-1):
                            a = f.readline().split()
                            g.write(a[index[0]]+";"+a[index[1]]+";"+a[index[2]]+";"+a[index[3]]+"\n")
                        g.write("\n")

##################################################################################################################################
# Function that replace values with symbols in an xyz files
# Parameters:

# inputfile: name of the file without the extension
# Example: if the file is strain.xyz, input just "strain"

# atoms: symbols of the atoms in the file separated by commas
# Example: C,H,O

# values: numbers that are representing the atoms in the file
# Example: 123

def replace_xyz(inputfile, atoms, values):
    d = dict(Atoms = atoms, Values = values)
    df = pd.read_table(inputfile+".xyz", sep=";", names=["A", "B", "C", "D"])
    for i in range(len(d["Atoms"])):
        df = df.replace(d["Values"][i], d["Atoms"][i])
    df.to_csv(inputfile+".xyz", sep=" ", header=False, index=False)

##################################################################################################################################
# Function that reverses an xyz file and concatenate it with the original file
# Parameters:

# inputfile: name of the file without the extension
# Example: if the file is strain.xyz, input just "strain"

def reverse(inputfile):
    df1 = pd.read_table(inputfile+".xyz", sep=" ", names=[0, 1, 2, 3])
    n_atoms = df1[0][0]
    df2 = df1.values.tolist()
    df2.reverse()
    df2 = pd.DataFrame(data=df2)
    df2.replace([str(n_atoms), "Comments"], ["Comments", str(n_atoms)], inplace=True)
    header = pd.DataFrame(data=[[n_atoms, None, None, None], ["Comments", None, None, None]])
    x = pd.concat([header, df2.head(len(df2) - 2)], ignore_index=True)
    df = pd.concat([df1, x], ignore_index=True)
    df.to_csv(inputfile+".xyz", sep=" ", header=False, index=False)

##################################################################################################################################
# Calling the functions

lammps2xyz(sys.argv[1])
replace_xyz(sys.argv[1], sys.argv[2].split(sep=","), list(sys.argv[3]))
reverse(sys.argv[1])
