from numpy import *

"""
Utility function for sparse representation
"""

def zero_norm(x, epsilon = 0.00001):
   """
   Compute 0-norm with precision epsilon
   """
   return sum(1 for i in x if abs(i) >= epsilon)

def zero_idx(x, epsilon = 0.00001):
   """
   Get indices of zero elements 
   """
   return [i for i in range(len(x)) if abs(x[i]) < epsilon]

def nonzero_idx(x, epsilon = 0.00001):
   """
   Get indices of nonzero elements 
   """
   return [i for i in range(len(x)) if abs(x[i]) >= epsilon]


def shrinkage(z,gamma):
   """
   Shrinkage
   """
   return sign(z) * maximum(zeros(z.shape), abs(z) - gamma)


def gen_rand_inst(M, N, noise=False):
   """
   Generate a MxN dictionary, a random sparse vector x 
   and the reconstructed signal s.
   If noise=True, noise is added to s (thus A*x != s)
   """
   A = random.random((M,N))
   x = random.random((N,1))
   for (i,val) in enumerate(x):
      if random.random() >= 0.5:
         x[i] = 0
   nu = 0
   if noise:
      nu = 0.03*random.random((M,1))
   s = dot(A,x) + nu
   return A,x,s

