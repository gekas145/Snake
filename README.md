# Snake

This repo contains python implementation of snake game as well as keras model trained to play it. The model was trained by DQN algorithm and is a cnn which considers last 3 frames of game enviroment in order to produce decision for the next frame. 

Although this cnn is not ideal(and is in fact beaten by simple greedy algotihm which just goes by the shortest path to the food), it demonstrated signs of rational "thinking" when being tested. Futher improvement may be achieved by training a deeper network with smaller kernels, increasing length of training(this model was trained on 700k frames, although around 1M is recommended; moreover majority of training frames was spent on exploration not exploitation) or by adjusting rewards and punishments system.

CNN | Greedy
:-------------------------:|:-------------------------:
![](images/cnn.gif)  |  ![](images/greedy.gif)

<p align="center">
<img src="images/boxplot.png" width="350" height="300"/>
</p>

The above plot shows distributions of cnn and greedy strategy results(1 point for each eaten food piece) obtained from 100 games. Food appearance was defined by sequence of different seeds which was same for both models.

Used sources:

[1] Berkeley RL bootcamp: https://www.youtube.com/playlist?list=PLAdk-EyP1ND8MqJEJnSvaoUShrAWYe51U

[2] RL keras examples: https://keras.io/examples/rl/

[3] OpenAI Baselines repository: https://github.com/openai/baselines
