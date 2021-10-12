from util import *
from os.path import join

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default="zachary.txt",
                        help='the filename of dataset [default: "zachary.txt"] ')
    parser.add_argument('--k', type=int, default=3,
                        help='3-clique blocks to initialize the partition [default: 3] ')
    parser.add_argument('--overlap', type=bool, default=True,
                        help='overlap=Ture is for identifying overlapping communities, otherwise non-overlapping '
                             'communities  [default: True]')
    parser.add_argument('--T', type=int, default=20,
                        help='The number of independent runs for each node in influence spread [default: 20]')
    parser.add_argument('--freq', type=int, default=8,
                        help='Expand blocks by added nodes with freq>=8 in influence spread. freq<=T [default: 8]')
    args = parser.parse_args()

    # read data
    dir1 = "/home/wu_xl/PycharmProjects/RaidB/graph/"
    file_read = open(dir1 + args.filename, "r")

    G = nx.Graph()
    G.clear()
    for line in file_read:  # read network
        line = line.split()
        line = [line[0], line[1].replace('\n', '')]
        G.add_edge(line[0], line[1])
    file_read.close()
    G.remove_edges_from(nx.selfloop_edges(G))

    Initial_Part = Initial_Blocks(G, args.k)

    Non_Overlap_Part = Reassemble_Modularity_Optimization(G, Initial_Part)

    if args.overlap:
        Overlap_Part = Reassemble_Influence_Spread(G, Non_Overlap_Part, args.T, args.freq)
        file_write = open(dir1 + args.filename + "_overlap.txt", "w")
        for Id, Comm in Overlap_Part.items():
            for node in Comm:
                file_write.write(str(node))
                file_write.write("\t")
                file_write.write(str(Id))
                file_write.write("\n")
        file_write.close()
    else:
        file_write = open(dir1 + args.filename + "_non_overlap.txt", "w")
        for node, Id in Non_Overlap_Part.items():
            file_write.write(str(node))
            file_write.write("\t")
            file_write.write(str(Id))
            file_write.write("\n")
        file_write.close()

    print('success')
