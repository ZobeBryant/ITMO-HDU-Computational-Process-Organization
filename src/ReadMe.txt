1.title:Implement dynamic array in mutable way and immutable way

2.list of group members:
192050185 FanXulin
192050188 ZhaoQingbiao

3.laboratory work number:2

4.variant description:
Implement dynamic array in both mutable and immutable ways.
For both ways, implement the following features :
	1. add a new element ( lst.add(3) , cons(lst, 3) , extend(lst, 3) );
	2. remove an element ( lst.remove(3) , remove(lst, 3) );
	3. size ( lst.size() , size(lst) );
	4. conversion from and to python lists ( lst.to_list() , lst.from_list([12, 99, 37]) , from_list([12, 99, 37]) );
	5. find element by specific predicate ( lst.find(is_even_) , );
	6. filter data structure by specific predicate ( lst.filter(is_even) );
	7. map structure by specific function ( lst.map(increment) );
	8. reduce – process structure elements to build a return value by specific functions ( lst.reduce(sum) );
	9. data structure should be a monoid and implement mempty and mconcat functions or methods;
	10. iterator:
		for the mutable version in Python style 
		for the immutable version by closure

5.synopsis:
Source code of the lab1 work, the analysis of mutable and immutable, work demonstration

6.contribution summary for each group member
ZhaoQingbiao: Write mutable version and the test of mutable version. Create git repository.
FanXulin: Write immutable version and the test of immutable version. Analysis the difference and write the ReadMe file.

7.explanation of taken design decisions and analysis
In my opinion, the most difference between mutable and immutable is that in mutable we need to do the job that change the variable after the variable reference but in immutable we need to create the copy then do the job of modifing the the copy and change the variable reference at last.

In dynamic array, the add/append insert remove map functions are different between the two ways. Other functions are actually the same. Because theye do not change the variables.
In mutable ways ,we can modify the value directly in the array. When the capacity is not enough, we also need to create a larger array ,copy the values to the new array at first. Then do the add or remove or insert work.
But in immutable ways, we should create the copy of the array initially. Then do the work on the copy.And finally, we change the variable conference.
 
8.work demonstration
Just open the file which starts with Test. Write click and click Run "UnitTest for xxxxxx".
Then we can see that the results are correct.

9.conclusion
In this lab work, we Implemented dynamic array in mutable and immutable ways. In the process, we disscuss with each other and find some difference between mutable and immutable. Deeply understanding them, we finally completed the source code. What's more, we find ways to distinguish  the two ways