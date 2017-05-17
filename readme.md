# Finding communities in a social network
This repo implements the bigCLAM algorithm. It finds communities in the graph from a social network Think of it like friend groups.
In university, you might have joined a music club, a sports club and a study group. let's think of the people as nodes and friendships
as edges. Then could an algorithm find the (overlapping) groups of nodes that form a community.

# How will this repo help me?
The code aims at people who want to learn about algorithms for social graphs. By far, this won't do for production code. We aim at
readable code for educational purposes. `main.py` implements the algorithm, `util/generate_data.py` generates data and `ui/index.html` helps us with plotting our social graph.

# What does the algorithm achieve? How is it different from finding cliques?
Your different peers and friends don'f partition into separate clusters. Probably, some friend from music class also plays the same sports and you have similar mutual friends.
Or by chance, two friends from different groups (in your perspective) happen to know each other. Therefore, bigCLAM finds overlapping communities.

This also indicates the difference with cliques. For a clique, some friend (node) can be assigned to only one node. Moreover, in a clique, all members must be friends. This doesn't
hold true for social communities.

# So how do we model such communities?
Let's say we knew the communities. Then we could calculate the probability of all the friendships. We can write this as the likelihood of the data. Then if we didn't knew
the communities, we just have to find the assignments to communities with the highest likelihood. Hence, the name: Maximum Likelihood Estimation

The likelihood for our graph looks like this:
![equation]( https://latex.codecogs.com/gif.latex?l(G)=\prod_{(u,v)&space;\in&space;E}&space;p_{uv}&space;\prod_{(u,v)not\&space;in&space;E}&space;1-p_{uv} )

<!---
[//](l(G)=\prod_{(u,v) \in E} p_{uv} \prod_{(u,v)not\ in E} 1-p_{uv})
-->

That leaves us to define `p_{uv}`, the probability of person `u` and `v` to be frieds. We model this by defining community preferences, `f`. For two `f` with large inner product, we want a high probability of friendship. Probabilities should be between 0 and 1. So we get:
![equation](https://latex.codecogs.com/gif.latex?p_{uv}&space;=&space;1-e^{-f_u&space;^T&space;f_v})

# And how do we find the commmunities?
We must assign people to communities with the highest likelihood. As we can differentiate all formulas, we can use gradient ascent. We start with some initial preference matrix, `F`. And we iteratively update this matrix to improve the likelihood. Note  that the likelihood is not convex, so we'll end in a local maximum, but that's okay for now.

# What does the algorithm look like?
For starters, here's an example of a social network. To see how we generate the data and plot it, look at `/util/generate_data.py` for the AGM and `ui/index.html` for the D3.js code.

![Social network](http://robromijnders.github.io)
An edge represents a friendship. This marks the starting point for any social graph problem, you're given a bunch of people (nodes) and their friendships (edges)


![Social network2](http://robromijnders.github.io)
Now, we plot the results of our algorithm. The fill represents the _true_ communtiy. The outer stroke 
 represents the community with highest preference. (_Note that we might as well plot multiple communities per node, but I'm not that proficient with D3.js. Please reach out if you can help me_)
 
I cherry picked these examples for the purposes of explaining. You can check `im/` for more plots or play with the code and make your own


As always, I am curious to any comments and questions. Reach me at romijndersrob@gmail.com
