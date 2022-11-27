**Very much deprecated software, do not use. Keeping for posterity only.**

<h1>CoarseGrind v0.2-β Readme</h1>
<h3><em>CoarseGrind, the automated Virginia Tech course grinding script.</em></h3>

<h2>0. Contents</h2>
<b><ol>
<li>Introduction</li>
<li>New features</li>
<li>Requirements</li>
<li>Getting started</li>
<li>Launching CoarseGrind</li>
<li>Using CoarseGrind</li>
<li>Troubleshooting</li>
<li>Other information</li>
</ol></b>

<h2>1. Introduction</h2>
<h3>Please read this document carefully</h3>
CoarseGrind is a Python script designed for Virginia Tech students to assist them during drop/add. Whether you have used CoarseGrind before or you're new to CoarseGrind, it is very important that you read the contents of this document carefully!

<h3>Disclaimer</h3>
CoarseGrind does not perform any sort of "hacking" (as some may call it) to accomplish its goal. CoarseGrind does exactly what a human being does when they are trying to add a class via drop/add; it's just much faster than any human. Due to this, CoarseGrind can in no way guarantee that you will be added to your desired courses. CoarseGrind can only increase the probability that you will be added if a seat opens up.

CoarseGrind was designed to work with Virginia Tech's HokieSPA and no other system. Additionally, Virginia Tech does not endorse and, in fact, discourages the use of software like CoarseGrind. Use CoarseGrind at your own risk.

This version of CoarseGrind is a beta, which means that it has not gone through thorough testing. Although this version of CoarseGrind is designed to be as strong and robust as possible, it is entirely possible that this version of CoarseGrind may:
<ul>
<li>Fail to perform it's duties</li>
<li>Crash unexpectedly</li>
<li>Deadlock itself</li>
</ul>
If any of the above occurs, <em>stop using v0.2-β immediately and switch to <a href="https://github.com/jballands/CoarseGrind/tree/0.1-Release" target="_blank">v0.1</a>!</em> 

<h3>About CoarseGrind</h3>
CoarseGrind is a Python script that can help make the process of waiting for a seat to open in a class easier and less stressful. CoarseGrind uses a technique known as "web scraping" to browse HokieSPA and perform tasks like:
<ul>
<li>Watching for seats to open in your desired classes.</li>
<li>Adding yourself quickly to a class when a seat becomes available.</li>
</ul>
CoarseGrind is completely automated, meaning that you don't have to be present as CoarseGrind works tirelessly to get you into your classes. No longer do you have to spend huge amounts of time sitting on HokieSPA, desperately waiting for a seat that may or may not open.

<h2>2. New features</h2>
CoarseGrind v0.2-β contains a number of new features over its predecessor, including:
<ul>
<li>Turbo Mode for ultra-fast course adding.</li>
<li>A new set of job tools that generates more feedback and provides finer control over CoarseGrind.</li>
<li>A more sophisticated grinding routing discovers open seats and adds yourself to a course faster while increasing overall program stability.</li>
<li>Completely reprogrammed from the ground up, v0.2-β is, dare I say, harder, better, faster, and stronger.</li>
</ul>

<h2>3. Requirements</h2>
<em>**If you are using a Unix-based operating system (OSX or Linux), you only require Python 2.7 or higher.</em>
<ol>
<li>A machine running Windows, OSX, or Linux</li>
<li><a href="http://www.python.org/download/" target="_blank">Python 2.7 or higher</a> (2.7 is preferred)</li>
<li><a href="http://wwwsearch.sourceforge.net/mechanize/" target="_blank">Mechanize</a>**</li>
<li><a href="http://www.crummy.com/software/BeautifulSoup/" target="_blank">BeautifulSoup 4</a>**</li>
<li><a href="https://github.com/html5lib/html5lib-python" target="_blank">HTML5Lib</a>**</li>
</ol>

<h2>4. Getting started</h2>
After downloading CoarseGrind, you should have a folder with the following contents inside:
<ul>
<li>cg_normal</li>
<li>cg_turbo</li>
<li>cg_unsafe</li>
<li>clean</li>
<li>install</li>
<li>config.txt</li>
<li>readme.md</li>
<li>src</li>
</ul>

<h3>For Unix-based users, including OSX</h3>
Locate the `install` executable shell script and double click it to install all of CoarseGrind's dependencies (Mechanize, BeautifulSoup 4, HTML5Lib). The terminal should appear and will prompt you for the password to your computer. Type your computer's password to grant the install script privilages to install the appropriate modules on your computer's hard disk.

<h3>For Windows users</h3>
After downloading Mechanize, BeautifulSoup 4, and HTML5Lib, install the modules using the following command on the Command Prompt:

    python setup.py install
    
You will have to perform this command a total of 3 times, once for each module. For more information on how to install Python modules, visit <a href="http://docs.python.org/2/install/" target="_blank">this link</a>.

<h2>5. Launching CoarseGrind</h2>
CoarseGrind v0.2-β runs entirely on the console and has three different modes. Each mode behaves differently from the others and it is important to know when to use which mode. Below is a description of each mode:
<ul>
<li><b>Normal mode</b><br/>
Runs CoarseGrind using the usual BASH-style interface. This mode will be familiar to v0.1 users.</li>
<li><b>Turbo mode</b><br/>
Using the config.txt as a reference, runs CoarseGrind in a so-called turbo mode that aggressively tries to add a single course to your schedule. This mode works best when you know that a seat will open up very soon and you want to beat the rush for the open seat. (For example, it is announced in your psychology class that a student is about to drop the course you want next semester because they realized that they won't have the prerequisites.)</li>
<li><b>Unsafe mode</b><br/>
Primarily for debugging, disables some of normal mode's safety features and forces CoarseGrind to watch for open seats. Use at your own risk. May cause CoarseGrind to unexpectedly crash or deadlock.</li>
</ul>

<h3>Easy launch (For Unix-based users, including OSX)</h3>
To execute in <b>normal mode</b>, locate the executable shell script named `cg-normal` and double click it to start CoarseGrind in normal mode.
To execute in <b>turbo mode</b>, make sure that you have filled the `config.txt` with the appropriate information. Then, locate the executable shell script named `cg-turbo` and double click it to start CoarseGrind in turbo mode.
To execute in <b>unsafe mode</b>, locate the executable shell script name `cg-unsafe` and double click it to start CoarseGrind in unsafe mode.

<h3>Standard launch</h3>
CoarseGrind takes command line parameters similar to how a C program is executed. To execute CoarseGrind, use the following command while in the `src` folder:

    python coarsegrind.py
    
Without specifying any switches, CoarseGrind will start in <b>normal mode</b>. You can also use the following command to start in normal mode:

    python coarsegrind.py -n
    
<b>Turbo mode</b> and <b>unsafe mode</b> can be started in a similar manner. For turbo mode, be sure to specify the config file as an argument after the turbo switch**:

    python coarsegrind.py -t config.txt
    
To start in unsafe mode, use:

    python coarsegrind.py -u

And of course, like any good program, to see usage information, use:

    python coarsegrind.py -h
    
<em>**You do not have to name the config file `config.txt`, but it is important to follow the config file syntax (described later in this readme).</em>

<h2>6. Using CoarseGrind</h2>

Although CoarseGrind will largely guide you, it is important to learn a few of its featured concepts.

A <b>job</b> is a work item that you assign CoarseGrind when you tell it that you want to add a course to your schedule. CoarseGrind is capable of handling many jobs simultaneously and asyncronously, meaning that job A will not affect the status of job B. A job is dead when you either <b>kill</b> the job, or when CoarseGrind successfully adds you to the course handled by the job. CoarseGrind provides a set of tools to help you add, view, and kill jobs.

<h3>The prompt</h3>
After logging into HokieSPA successfully, CoarseGrind will display the following:

    CG-v0.2-B$

This is known as the prompt. When the prompt appears, it means that CoarseGrind is ready to accept a command.

<h3>The commands</h3>
CoarseGrind understands the following commands:

<ul>
<li>Add</li>
<li>Jobs</li>
<li>Kill</li>
<li>Eval</li>
<li>Help</li>
<li>Debug</li>
<li>Quit</li>
</ul>

To <b>add</b> a class to your schedule, type the following at the prompt:

    CG-v0.2-B$ add

This will start series of sub-prompts that should be pretty self explanitory.

To see all the <b>jobs</b> that CoarseGrind is aware of, type the following at the prompt:

    CG-v0.2-B$ jobs

This will display a list of all running jobs sorted by which jobs are still alive and which jobs are dead. Once a job has died, you will see it appear exactly once after calling `jobs` under the `Done:` list. Subsequent calls to the jobs list will display nothing under the `Done:` list.

To <b>kill</b> a job, type the following at the prompt:

    CG-v0.2-B$ kill <job_num>

`job_num` is the job number (as displayed by `jobs`) of the job to kill. For example, to kill job number 2, you would type:

    CG-v0.2-B$ kill 2

By default, CoarseGrind will check for an open seat every 30 seconds. To change this <b>evaluation rate</b>, type the following at the prompt:

    CG-v0.2-B$ eval <rate>

`rate` is the amount of time in seconds that you want to pass before CoarseGrind rechecks the class for an open seat. For example, to change the evaluation rate to 10 seconds, you would type:

    CG-v0.2-B$ eval 10

Sometimes it is helpful (and even interesting) to see what CoarseGrind is doing behind the scenes. To see <b>debug</b> information as CoarseGrind has jobs running, type the following at the prompt:

    CG-v0.2-B$ debug

This will regurgitate a ton of information at you, including when a job is awake, when it's checking for an open seat, when it's found an open seat, and when it's going to sleep. You can press the `return` key at any time to exit this command.

To <b>quit</b> CoarseGrind, just type the following at the prompt:

    CG-v0.2-B$ quit
    
And of course, if you forget any of these commands, you can type the following at the prompt to get <b>help</b>:

    CG-v0.2-B$ help

<h3>Turbo mode and config.txt rules</h3>
After starting CoarseGrind in turbo mode, CoarseGrind will automatically begin searching for the specified config file and will return an error if it cannot find it. Once the config file has been found, CoarseGrind will begin a single job automatically and try aggressively to add the course. You can press the `return` key to exit turbo mode at any time.

In general, `config.txt` must contain the following:

    username>
    password>
    crn>
    term>

After `username>`, type your PID. After `password>`, type your password (be careful not to show this file to anybody). After `crn>`, type the 5-digit CRN code of the course you want to add. Finally, after `term>`, type the term code of the term the CRN exists in.

The <b>term code</b> can be created using the following rules:
<ul>
<li>For the semester:
<ul>
<li>Fall: F</li>
<li>Spring: S</li>
<li>Summer I: U</li>
<li>Summer II: W</li></ul></li>
<li>For the year, simply type the last two digits.</li>
</ul>
For example, the term code for Fall 2014 would look like `F14`, and the term code for Summer II 2020 would look like `W20`.

You can also type comments in the config file by using the the double-slash mark. Any line that has been commented will be ignored when CoarseGrind reads the config file.

The following is an example of a valid config file. User `imaHokie` tries to add CRN `12345` for Spring 2014:

    // config.txt
    // This is a comment and will be ignored!
    username>imaHokie
    password>iliketojump
    term>S14
    crn>12345
    
<h2>7. Troubleshooting</h2>
While this version of CoarseGrind was designed to be as strong and robust as possible, problems may still arise. Unfortunately, there isn't much you can do if CoarseGrind behaves abnormally, but I encourage you to try the following.

<h3>Clean CoarseGrind</h3>
Due to static, the weather, how long your computer has been on, etc., the small electrical pulses in your computer may screw up and interfere with CoarseGrind's execution. To fix this, you have to option to clean CoarseGrind.

For <b>Unix-based systems, including OSX</b>, locate the executable shell script name `clean` and double click it to clean CoarseGrind. Restart CoarseGrind once cleaning has completed.

For <b>Windows systems</b>, enter the `./src` folder and delete any file that ends in `.pyc` or `.pyo`. Restart CoarseGrind once you have deleted all of these files.

<h3>Run CoarseGrind in unsafe mode</h3>
Sometimes, the safety mechanisms in normal mode may be overprotective and prevent CoarseGrind from doing any work. Run CoarseGrind in unsafe mode and see if your problem persists. Be warned: there be monsters out there. New problems may arise when running in unsafe mode such as CoarseGrind unexpectedly crashing or even deadlocking. Use at your own risk!

<h3>CoarseGrind has deadlocked</h3>
> "CoarseGrind... what are you doing? CoarseGrind! STAHP!!"<br />
> <em>You when CoarseGrind deadlocks</em>

On <b>Unix-based machines, including OSX</b>, you will have to force quit CoarseGrind to end the deadlock. On <b>Windows machines</b>, you will have to use `Ctrl+Alt+Del` to end the deadlock.
