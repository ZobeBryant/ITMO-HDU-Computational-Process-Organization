**1.title:Command line interface builder**

**2.list of group members:** 

​	192050185 FanXulin 

​	192050188 ZhaoQingbiao

**3.laboratory work number: 3**

**4.variant description:** 

Many programs have a complex command-line interface (CLI). For example, docker, apt-get, yam, npm, brew. In this variant, you should develop the library for building a command-line interface by decorators.

The main idea of a library is the separation of CLI and handlers implementation, like you can see in Flask web-framework separation of web API/route and handlers implementation .

Requirements:

1. Features of a library:
  - support of flags with default values ( python3 --version , python3 -V , python -v );
  - support of position arguments ( python3 module.py , cat file1 file2 );
  - support named arguments with default values ( python3 -m module_name );
  - support of sub-commands with a different set of arguments ( docker ps , docker exec );
  - automatic help and error message generation;
  - support type conversation for arguments value (e.g., head -n 5 conversation string “5” to int value 5 );
2. Your library should be well documented.
3. To proof correctness, you should use unit tests.
4. To proof usability, you should implement single command-line utilities that demonstrate all library features.

**5.synopsis:**

 Source code of the lab3 work, design command line interface builder, work demonstration

**6.contribution summary for each group member:** 

​	ZhaoQingbiao: Write "fz_cli".

​	FanXulin: Write "fz_cli_test" and "ReadMe".

**7.explanation of taken design decisions and analysis:**

```
Python fz_cli is a library for creating CLIs from absolutely any Python object.


Python fz_cli turns any Python object into a command line interface.
Simply call the fz_cli function as your main method to create a CLI.

When using fz_cli to build a CLI, your main method includes a call to Fz. Eg:

@cli.command(Option("","","",""))
def test(argv):
	print("This is for a test!")
  
```

**8.work demonstration:**

 Just open the file which starts with Test. Write click and click Run "UnitTest for xxxxxx". Then we can see that the results are correct. 

**9.conclusion :**

In this lab work, we  design command line interface builder. In the process, we disscuss with each other and understand how to build the command line interface. Deeply understanding them, we finally completed the source code.