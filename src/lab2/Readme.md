1.title:Implement eDSL for finite state machine (Mealy) about crossroad with a traffic light.
2.list of group members:
192050185 FanXulin
192050188 ZhaoQingbiao

3.laboratory work number:2

4.variant description:
	1.Visualization as a state diagram (GraphViz DOT) or table (ASCII).
	2.Provide complex an example like a controller for an elevator, crossroad with a traffic light, etc.

5.synopsis:
Source code of the lab2 work, the analysis of eDSL for finite state machine (Mealy), work demonstration

6.contribution summary for each group member
ZhaoQingbiao: Write input data control, state machine model visualization and the ReadMe file.
FanXulin: Write write and test the state machine(Mealy) for a traffic light.

7.explanation of taken design decisions and analysis
 We chose traffic lights. We simulated the traffic signal situation at a crossroad. We chose one of the intersections to simulate a green light, keep green light, green light turns yellow, keep yellow light, yellow light turns red, keep red light, red light turns green. We change to that state by judging by the clock and the current state.
 
8.work demonstration
Just open the file which starts with Test. Write click and click Run "UnitTest for xxxxxx".
Then we can see that the results are correct.
Open the file with suffix '.gv', we can the picture of state machine(Mealy)
 
9.conclusion
In this lab work, we Implemented eDSL for finite state machine (Mealy) about crossroad with a traffic light. In the process, we disscuss with each other and design the state machine for mealy about a traffic light. Deeply understanding them, we finally completed the source code. 
