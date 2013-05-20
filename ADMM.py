from numpy import *
import scipy
import solve
import sparse


def ADMM_BPDN(A,s,l):
   """
   Alternating Direction Method of Multipliers for Basis Pursuit Denoising
   Solve the problem:
      min 1/2 ||Ax-s||^2 + lambda*||x||_1
   """
   (M,N) = A.shape
   x,y,u = zeros((N,1)), zeros((N,1)), zeros((N,1))
   max_it = 1000
   rho = l 
   k = 0
   xks,yks,uks = [x],[y],[u]

   # Cached factorizations and computations
   C = dot(A,A.T) + rho*eye(M)
   PL,U = scipy.linalg.lu(C, permute_l=True)
   As = dot(A.T,s)

   prim_resid = 100
   dual_resid = 100
   prim_epsi = 0
   dual_epsi = 0
   epsi_rel = 0.001
   epsi_abs = 0.0001
   
   while k <= max_it and (prim_resid >= prim_epsi or dual_resid >= dual_epsi):
      # Update x
      rhs = As + rho*(yks[k] - uks[k])
      x_star = solve.lemma_solve(A,rhs,rho,PL,U)
      xks.append(x_star)
      
      # Update y
      z = xks[k+1] + uks[k]
      y_star = sparse.shrinkage(z,  l/rho)
      yks.append(y_star)
   
      # Update u
      u_star = uks[k] + xks[k+1] - yks[k+1]
      uks.append(u_star)
      
      prim_resid = linalg.norm(xks[k+1] - yks[k+1])
      dual_resid = linalg.norm(rho*(yks[k] - yks[k+1]))

      #print k, 1/2*linalg.norm(dot(A,x_star)-s) + l*linalg.norm(x_star,1)
 
      k += 1
      prim_epsi = sqrt(N)*epsi_abs + epsi_rel*max(linalg.norm(xks[k]),linalg.norm(yks[k]))
      dual_epsi = sqrt(N)*epsi_abs + epsi_rel*linalg.norm(uks[k])
      
      print prim_resid, dual_resid 
      print prim_epsi, dual_epsi
 
   return xks[k]


def ADMM_ConstrBP(A,s,epsilon):
   """
   Alternating Direction Method of Multipliers for Constrained Basis Pursuit
   Solve the problem:
      min ||x||_1 s.t. ||Ax-s||_2 <= epsilon
   i.e., find the minimum-norm vector s.t. the error from s is under epsilon
   """
   (M,N) = A.shape
   x,y,z,u,v = zeros((N,1)), zeros((N,1)), zeros((M,1)), zeros((N,1)), zeros((M,1))

   max_it = 200
   
   gamma = epsilon
   sigma = epsilon

   k = 0
   xks,yks,zks,uks,vks = [x],[y],[z],[u],[v]

   # Cached factorizations and computations
   C = dot(A,A.T) + gamma*eye(M)
   PL,U = scipy.linalg.lu(C, permute_l=True)

   prim_resid = 100
   dual_resid = 100
   prim_epsi = 0
   dual_epsi = 0
   epsi_rel = 0.001
   epsi_abs = 0.0001
   
   while k <= max_it:
      # Update x
      rhs = gamma*(yks[k] - uks[k]) + sigma*dot(A.T,(zks[k]-vks[k]))
      x_star = solve.lemma_solve(A,rhs,gamma,PL,U)
      xks.append(x_star)
      
      # Update y
      t = xks[k+1] + uks[k]
      y_star = sparse.shrinkage(t, 1/gamma)
      yks.append(y_star)
  
      # Update z
      b = dot(A,xks[k+1]) + vks[k]
      if linalg.norm(b-s) > epsilon:
         z_star = s + epsilon*(b - s)/linalg.norm(b-s) 
      else:
         z_star = b
      zks.append(z_star)

      # Update u
      u_star = uks[k] + xks[k+1] - yks[k+1]
      uks.append(u_star)
 
      # Update v
      v_star = vks[k] + dot(A,xks[k+1]) - zks[k+1]
      vks.append(v_star)
     
      #prim_resid = linalg.norm(xks[k+1] - yks[k+1])
      #dual_resid = linalg.norm(rho*(yks[k] - yks[k+1]))

      print k, linalg.norm(x_star,1)
      print linalg.norm(dot(A,x_star)-s)
 
      k += 1
      prim_epsi = sqrt(N)*epsi_abs + epsi_rel*max(linalg.norm(xks[k]),linalg.norm(yks[k]))
      dual_epsi = sqrt(N)*epsi_abs + epsi_rel*linalg.norm(uks[k])
      
      print prim_resid, dual_resid 
      print prim_epsi, dual_epsi
 
   return xks[k]

