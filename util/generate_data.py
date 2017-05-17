import json
import numpy as np
from random import random
import pickle


class Datagen():
    def __init__(self, N, w, p, cross):
        """
        Data generator.
        The social network will have N people. At first, we assign each
        person a community with probability w_i. Secondly. we assign a second
        community to a portion (cross) of the community
        :param N: the total number of nodes in the graph
        :param w: assignment probability of a community on the first step
        :param p: p_i is the probability of an edge when two people share community i
        :param cross: portion of people to assign a second cluster
        """
        self.N = N
        self.w = w
        self.p = p
        self.cross = cross

        self.num_comm = len(w)
        assert self.num_comm == len(p)

    @property
    def adj(self):
        return self.A+self.A.T

    def gen_assignments(self):
        # First step
        W = len(self.w)
        initial_comm = np.random.choice(W,p=self.w, size=(self.N,))
        
        # Second
        person2comm = []
        for n, comm in enumerate(initial_comm):
            all_comm = {comm}
            if random() < self.cross:
                all_comm.add(np.random.randint(0,W))
            person2comm.append(all_comm)

        self.person2comm = person2comm
        return self

    def gen_adjacency(self):
        # TODO check if it is upper traingular
        A = np.zeros((self.N, self.N),dtype=np.int8)
        for i in range(self.N):
            for j in range(i+1, self.N):
                same_communities = self.person2comm[i].intersection(self.person2comm[j])
                p_nedge = 1.0
                at_least_one = False
                for comm_shared in same_communities:
                    at_least_one = True
                    p_nedge *= 1.-self.p[comm_shared]
                if not at_least_one:
                    p_nedge = 0.99

                p_edge = 1-p_nedge
                if random() < p_edge:
                    A[i,j] = 1
        self.A = A
        return self

def gen_json(A,p2c,F_argmax=None):
    N = A.shape[0]
    data = {'nodes':[],'links':[]}

    for i in range(N):
        grp = ''.join(map(str,sorted(p2c[i])))
        node = {'id': str(i), 'group': str(grp)}
        if F_argmax is not None:
            node.update({'assigned':str(F_argmax[i])})
        data['nodes'].append(node)
        friends = np.where(A[i])
        for friend in friends[0]:
            inter = 2-len(p2c[i].intersection(p2c[friend]))
            data['links'].append({'source':str(i), 'target':str(friend),'value':str(inter*5+1), 'distance':str(inter*15+1)})
    return data



if __name__ == "__main__":
    datagen = Datagen(40, [.3, .3, .2, .2],[.1, .5, .2, .2] , .05)
    datagen.gen_assignments()
    datagen.gen_adjacency()
    p2c = datagen.person2comm
    A = datagen.A
    print(np.sum(A))

    data = gen_json(A, p2c)

    # with open('../data/data.json','w') as f:
    with open('ui/assets/data.json','w') as f:
        json.dump(data,f, indent=4)

    np.save('data/adj.npy',A+A.T)
    pickle.dump(p2c, open( "data/p2c.pl", "wb" ) )

