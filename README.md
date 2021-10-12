## Requirements

- networkx
- Python 3
- numpy

## Example Experiments

This repository contains a subset of the experiments mentioned in the paper.

## Hyperparameters

- filename[default:"zachary.txt"]       : the filename of dataset(the network).
- k[default:3]                                     : k-clique blocks to initialize the partition.
- overlap[default:True]                      : overlap=Ture is for identifying overlapping communities, otherwise non-overlapping communities.
- T[default:20]                                   : The number of independent runs for each node in influence spread.
- freq[default:8]                                 : expand blocks by added nodes with freq>=8 in influence spread. freq<=T.



## Run this code

File in the directory 'graph'  is a demo of a data set.The parameters are set in file to achieve the result mentioned in the paper.You can simply run the code in the following way.
```
python RaidB.py
```
You can adjust some of the hyperparameters in the following ways:
```
python Raidb.py --filename "zachary.txt" --k 3 --overlap True --T 20 --freq 8
```
In this way, you can modify the filename(network), the value of k and other parameters.The filepath need to be modified in the file.

## Questions?

Please report any bugs and I will get to them ASAP. For any additional questions, feel free to email penggangsun@xidian.edu.cn & xunlianwu@stu.xidian.edu.cn.
