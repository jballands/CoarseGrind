<h1>CoarseGrind v0.2</h1>
<h3><em>CoarseGrind: The automated Virginia Tech course grinding script.</em></h3>

<h2>As Drop/Add Nears...</h2>

<ul>
  <li>Virginia Tech's Drop/Add system will reopen at 12:00am EST on August 10, 2013.</li>
  <li>CoarseGrind v0.2 should be available as a beta on August 9, 2013.</li>
  <li>Check this repository regularly for updates as Drop/Add draws nearer.</li>
  <li>Once released, use CoarseGrind v0.2-beta at your own risk:
  <ul>
    <li>While pre-alpha testing has been performed, an alpha test will be completely skipped to release CoarseGrind as a beta in time for Drop/Add Fall 2013.</li>
    <li>Since testing a system of this nature is incredibly difficult, <em><b>it is entirely possible that v0.2 may behave abnormally!</b></em></li>
    <li>For your safety, download v0.1 from the "Releases" tab on the menu bar. Follow the instructions provided carefully.</li>
  </ul>
  <li>If you think that v0.2 is behaving abnormally:
  <ul>
    <li><em><b>Stop using v0.2-beta and use v0.1!</b></em> This is the only version I have officially released.</li>
    <li>Once you get v0.1 going, send me an email (<a href="mailto:jballands@gmail.com">jballands@gmail.com</a>) describing exactly what you did to make v0.2-beta behave badly. I will try and fix the problem as quickly as I possibly can!</li>
  </ul>
  <li>Good luck! I want you all to get the classes you want/need. :)</li>
</ul>

<h2>Introduction</h2>

For more information on CoarseGrind, please visit <a href='http://jonathanballands.me/portfolio/coarsegrind.html' target='_blank'>the official page</a> in my portfolio.<br />
For the lastest official version of CoarseGrind, click "Releases" from the menu bar and find "CoarseGrind v0.1".

CoarseGrind is a Python script that scrapes Virginia Tech's HokieSPA page to provide an advantage when waiting for a seat to open in a desired class. CoarseGrind does not use
any sort of "hacking", as some may call it, to accomplish its goal. It simply leverages the ability a computer has to perform a repeatitive task over and over in order to legitmately
add a student to a course when a seat becomes available. This allows the user of CoarseGrind to spend their time doing other things (like studying, exercising, partying, whatever) while
the computer does all the hard work. When a seat becomes available, CoarseGrind can add the user into the available seat quickly before the seat is taken by someone else.

CoarseGrind is a command-line application that appears similar to the BASH shell. CoarseGrind cannot guarantee that a student will be added into their desired course; it can only increase 
their chances of being added while freeing up time for the student to do other things.

<h2>What's new in v0.2?</h2>

<ul>
  <li><b>Turbo mode</b>
  <ul>
    <li>Sometimes you know that a seat is about to open in a class (such as when a student announces that they are dropping).</li>
    <li>Turbo mode allows you to fill in a config file with information such as PID, password, class of CRN desired, etc.
    before the rush starts.</li>
    <li>When the seat becomes available, start CoarseGrind in Turbo mode to quickly add the class to your schedule,
    smoking your competition.</li>
  </ul>
  </li>
  <li><b>More sophisticated grinding routine</b>
  <ul>
    <li>A more complex and sophisticated grinding mechanism allows courses with open seats to be discovered more
    quickly.</li>
    <li>When a seat becomes available, adding the course to your schedule also occurs more quickly.</li>
  </ul>
  <li><b>Resource recycling</b>
  <ul>
    <li>This version will use resources more frugally and recycle old resources to reuse later.</li>
    <li>This results in faster load times and lower system memory usage.</li>
  </ul>
  </li>
   <li><b>Numerous stability improvements and bug fixes</b>
  <ul>
    <li>Since this version's code will be completely refactored, CoarseGrind should be more stable and less buggy.</li>
  </ul>
  </li>
</ul>

<h2>Contribute to CoarseGrind</h2>

Are you a Hokie that wants to develop CoarseGrind further once I graduate? Maybe you aren't a Hokie but you want to create a similar script for your school's system? Submit a pull request or email me at <a href="mailto:jballands@gmail.com">jballands@gmail.com</a> if you have any questions! Don't be shy!
