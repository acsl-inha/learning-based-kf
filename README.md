# learning-based-kf


A discrete-time linear dynamical system consists of a sequence of state vectors  xt∈Rn , indexed by time  t∈{0,…,N−1}  and dynamics equations


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
