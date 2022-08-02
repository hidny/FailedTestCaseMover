# FailedTestCaseMover
Python scripts that move card game test cases in the TestCaseAndReplayData repo around to different folders, so I don't have to. The title is misleading because it could move more than failed test cases, but that's the main use-case.

I'm currently satisfied with all the scripts I made, but I didn't test it extensively, and there might still be bugs lurking.

I might add to this project if the need to automate file manipulation tasks arise.

## Current list of scripts to use

### AfterGameScript.py
to be run after a game is done, so it could automatically do the after-game rituals

### GetPrevTestcase.py
Opens previous testcase, so I could change it if I immediately realize that I missed something.
I'm hoping this is faster than refreshing the test folder in eclipse and scrolling down to edit the test case.

### LabelPrevTestcase.py
Same idea as GetPrevTestcase, but this is just for adding a TODO label to the test case.
That way, other scripts and I will remember to look into the test case.

### MLabelledTestcasesToFolder.py
Moves test cases having a specific label/keyword to a test folder for further analysis (like monte)

### PutTestcaseBackAndEmptyTestFolder.py
Moves test cases in tmp test folders back to the correct location in the main folders.
This used to be a manual process that was very annoying.

### MoveStatusChangedTestcasesToFolder.py
Moves test cases that had their outcomes change recently for further analysis (like monte).
I used to do this manually, and it was really annoying!



