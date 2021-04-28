 ### Question: 
 A typical architecture for a model-based navigation system involves 4 major components - Perception, Localisation, Planning, and Motion Control. Consider our VIRAT. It has sensors that determine its position and motion, as well as a model to predict its future positions. In the real world, predictive models and sensors aren’t perfect. There is always some uncertainty. For example, the weather can affect the incoming sensory data, so the bot can’t completely trust the information. Suggest a way on how you would refine the robot’s navigation stack to mitigate this uncertainty.
## Solutions Proposed:
### Sensor Measurement Uncertainity:
A possible solution to the above mentioned problem is to have many sensor, each based on different technologies(like mechanical sensors, vision-based sensors, etc) measuring the same parameter. 
The accuracy of sensors based on different technologies would vary due to different external factors. For example, mechanical sensors may be affected by moisture in the atmosphere while vision based sensors are not.
This setup would ensure that even one of the sensors is affected by some external factor we would have other sensors measuring the same parameter and giving us the accurate reading.
We can then remove any deviant reading(using methods like majority voting) and be less uncertain about the accuracy of sensor readings. We can even average 
measurements from different sensors to eliminate any random fluctuation/noise.

### Model Accuracy Uncertainity:
A solution I propose to mitigate the uncetainity about model prediction is to use **Active Learning Models** instead of pre-trained models. A pre-trained model will 
not be able to completely generalize to a real-world scenario since it has been trained with a fixed data and would not have got exposed to all the factors affecting 
the data in real world. An active learning model shall keep learning from each and every data point it is tested on. Hence, after sufficient number of trials, it 
would have beenn exposed to a wide range of real world situations and so would be much more accurate. Moreover, if it is put in a new environment, over some time, 
it would be able to learn from the new surrounding as well and generalize itself. This will surely improve the overall performance of the model and will help 
mitigate any uncertainity regarding the model.
