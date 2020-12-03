# learning-based-kf

## Discription

$$x_t \in \R^n$$
![image](https://user-images.githubusercontent.com/57785895/100954675-5e466d00-3558-11eb-9d24-1f3021621c34.png)

![image](https://user-images.githubusercontent.com/57785895/100954703-6bfbf280-3558-11eb-9037-b6fd9b90678c.png)

![image](https://user-images.githubusercontent.com/57785895/100954722-7918e180-3558-11eb-9874-f805494706eb.png)

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
