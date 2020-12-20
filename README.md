# learning-based-kf

## Note
This program requires CVXPY version 1.1.0 or greater
```
pip install cvxpy
pip install --upgrade cvxpy
```
and cvxpyLayer
```
pip install cvxpylayers
```
After importing the cvxpy, you can check the version as below
```
import cvxpy as cp
print(cp.__version__)
```

## Introduction
Parameters of the Kalman filter must be determined experimentally, but this process takes a long time and effort. So we intended to automate this process using machine learning.

This program learns parameters of the Kalman filter using **cvxpy**, **cvxpyLayer** and **pytorch**.

## Dynamic System Modeling

A discrete-time linear dynamical system consists of a sequence of state vectors <strong>x<sub>t</sub> ∈ R<sup>2</sup></strong>  , indexed by time  <strong>t∈{0,…,N−1}</strong>  and dynamics equations

![image](https://user-images.githubusercontent.com/57785895/100959190-15df7d00-3561-11eb-998d-5b4189344629.png)
  
where <strong>w<sub>t</sub> ∈ R<sup>m</sup></strong>  is an input to the dynamical system (say, a drive force on the vehicle),  <strong>y<sub>t</sub> ∈R<sup>r</sup></strong>  is a state measurement,  <strong>v<sub>t</sub> ∈R<sup>r</sup></strong>  is noise,  **A**  is the drift matrix,  **B**  is the input matrix, and  **C**  is the observation matrix.
Given  **A ,  B ,  C ,** and  <strong> y<sub>t</sub>  for  t=0,…,N−1 </strong>, the goal is to estimate  <strong>x<sub>t</sub>  for  t=0,…,N−1</strong> .

We'll apply standard and Kalman filtering to a vehicle tracking problem with state  <strong>x<sub>t</sub>∈R<sup>4</sup></strong> , where the first two states are the position of the vehicle in two dimensions, and the last two are the vehicle velocity. The vehicle has unknown drive force  <strong>w<sub>t</sub></strong> , and we observe noisy measurements of the vehicle's position,  <strong>y<sub>t</sub>∈R<sup>2</sup></strong> .

Then the following matrices the above dynamics.

![image](https://user-images.githubusercontent.com/57785895/100959212-22fc6c00-3561-11eb-8468-351c848c3ef7.png)


A Kalman filter estimates   <strong>x<sub>t</sub></strong>  by solving the optimization problems with some tuning parameters **τ** or **Q**

![image](https://user-images.githubusercontent.com/57785895/100961621-1595b080-3566-11eb-9f52-dbb18d07e178.png)

The 2x2 Q matrix is symmetric and semidefinite

### Typcial Solution of the Dynamics
Choosing values for the parameters, we can solve this problems by convex optimization.  
We simply assumed that **τ = 0.08** in the problem 1

![conventional_kf_1](https://user-images.githubusercontent.com/57785895/102709268-4b6bc080-42ec-11eb-9589-b44c83ab183c.png)

![conventional_kf_2](https://user-images.githubusercontent.com/57785895/102709272-4f97de00-42ec-11eb-871d-778c0aa20dba.png)

## Learning Steps

1. Define the convex opitmization problem using cvxpy and set it to Disciplined Parametrized Programming(DPP).
```
  ˙˙˙
  problem = cp.Problem(cp.Minimize(objective_fn), constraints)

  assert problem.is_dcp(dpp=True)
```
2. Create a learning model for DPP problems using CvxpyLayer.
```
  layer = CvxpyLayer(problem, parameters=[tau_dpp], variables=[x_dpp, w_dpp, v_dpp])
```

3. Derive **x̂** with Forward Propagation of the model.
```
  x_hat, w_hat, v_hat = layer(tau_hat)
```

4. The loss function is calculated as L2-norm  of (**x̂** - **x**)
```
  loss = (x_hat - x_true).norm()
```

5. Update the parameter (**τ** or **Q**).
```
  ˙˙˙
  loss.backward(retain_graph=True)
  opt.step()
  ...
```

## Result

### problem 1 : Learning tau
**result :**

![image](https://user-images.githubusercontent.com/57785895/100963280-63f87e80-3569-11eb-856f-c0785c1e3500.png)


![Learning tau](https://user-images.githubusercontent.com/57785895/99908424-ef7e3e00-2d25-11eb-9573-9850b3e8df56.png)


### problem 2 : Learning Q matrix
**result :**

![image](https://user-images.githubusercontent.com/57785895/100959769-58ee2000-3562-11eb-8c1f-27387b962be5.png)
 
![Learning Q_2](https://user-images.githubusercontent.com/57785895/100187865-5cfbbb80-2f2c-11eb-9ab8-fab581ee8ae5.png)


## Animation

#### Learning Animation : τ 0.006 → 0.69

![kf_animaint_1](https://user-images.githubusercontent.com/57785895/99908174-6dd9e080-2d24-11eb-841c-63a924860943.gif)


#### Learning Animation : τ 88 → 0.69

![kf_animation_2](https://user-images.githubusercontent.com/57785895/99908182-7df1c000-2d24-11eb-8ed5-6c407660147d.gif)
