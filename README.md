# Genetic-Adversary

The point of this project is to attempt to write a genetic algorithm to consistently fool a classifier network into outputting the same label for stochastically generated data. In this case each 'specimen' has a 32x32 float array that represents the image to be input into the network. A generation represents a collection of these specimens. We define mutate methods to introduce random mutations into each specimen, and a breeding function to combine them. 

Evolving a generation consists of taking the top performing specimens (those that fool the classifier in the right way with the highest confidence) and breeding them to form the next generation.


##TODO
- Rewrite this in a faster language (will probably be go)
- Checkpoints for training
