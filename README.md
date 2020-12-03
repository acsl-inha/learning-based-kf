# learning-based-kf

## Discription


A discrete-time linear dynamical system consists of a sequence of state vectors x<sub>t</sub> ∈ R<sup>2</sup>  , indexed by time  t∈{0,…,N−1}  and dynamics equations

![image](https://user-images.githubusercontent.com/57785895/100959190-15df7d00-3561-11eb-998d-5b4189344629.png)

where  w<sub>t</sub> ∈ R<sup>m</sup>  is an input to the dynamical system (say, a drive force on the vehicle),  y<sub>t</sub> ∈R<sup>r</sup>  is a state measurement,  v<sub>t</sub> ∈R<sup>r</sup>  is noise,  A  is the drift matrix,  B  is the input matrix, and  C  is the observation matrix.

Given  A ,  B ,  C , and  yt  for  t=0,…,N−1 , the goal is to estimate  xt  for  t=0,…,N−1 .

We'll apply standard and Kalman filtering to a vehicle tracking problem with state  x<sub>t</sub>∈R<sup>4</sup> , where the first two states are the position of the vehicle in two dimensions, and the last two are the vehicle velocity. The vehicle has unknown drive force  w<sub>t</sub> , and we observe noisy measurements of the vehicle's position,  y<sub>t</sub>∈R<sup>2</sup> .

Then the following matrices the above dynamics.

![image](https://user-images.githubusercontent.com/57785895/100959212-22fc6c00-3561-11eb-8468-351c848c3ef7.png)


![image](https://user-images.githubusercontent.com/57785895/100959141-fba59f00-3560-11eb-8e66-39b00b497e5f.png)

problem 1 : Learning tau
result :
 - loss = 8.5167
 - learend tau = 0.6980

![Learning tau](https://user-images.githubusercontent.com/57785895/99908424-ef7e3e00-2d25-11eb-9573-9850b3e8df56.png)


problem 2 : Learning Q matrix
result :
 - loss =　8.4605  
 - Q　=　| 1.2696444 ,   0.45706612 |  
　　　 | 0.45706612 ,   1.9576418 |
 
![Learning Q_2](https://user-images.githubusercontent.com/57785895/100187865-5cfbbb80-2f2c-11eb-9ab8-fab581ee8ae5.png)


Learning Animation : tau 0.006 -> 0.69

![kf_animaint_1](https://user-images.githubusercontent.com/57785895/99908174-6dd9e080-2d24-11eb-841c-63a924860943.gif)


Learning Animation : tau 88 -> 0.69

![kf_animation_2](https://user-images.githubusercontent.com/57785895/99908182-7df1c000-2d24-11eb-8ed5-6c407660147d.gif)
