<h1>CoarseGrind v0.2</h1>
<h3><em>CoarseGrind: The automated Virginia Tech course grinding script.</em></h3>

<h2>Introduction</h2>

For more information on CoarseGrind, please visit <a href='http://jonathanballands.me/portfolio/coarsegrind.html' target='_blank'>the official page</a> in my portfolio.<br />
For the lastest release of CoarseGrind, please visit <a href'https://github.com/jballands/CoarseGrind/releases' target='_blank'>the release page for v0.1</a>.

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
  <li><b>Numerous stability improvements and bug fixes</b>
  <ul>
    <li>Since this version's code will be completely refactored, CoarseGrind should be more stable and less buggy.</li>
  </ul>
  </li>
  <li><b>More sophisticated grinding routine</b>
  <ul>
    <li>A more complex and sophisticated grinding mechanism allows courses with open seats to be discovered more
    quickly.</li>
    <li>When a seat becomes available, adding the course to your schedule also occurs more quickly.</li>
  </ul>
  </li>
</ul>

<h2>Release notes</h2>

CoarseGrind v0.2 should be released on or before August 26th (the first day of classes at Virginia Tech) this upcoming semester. However, depending upon my work load, this may occur
earlier or later!

Feel free to contribute to CoarseGrind by submitting a pull request.
