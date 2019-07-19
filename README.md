<h1>Telescopy</h1>
<img src="https://github.com/enowars/Telescopy/blob/master/service/src/static/logo.svg" width="300" />

<p> A Web application wirtten in python using flask, jinja templates, redis and sqlite. </p>
<hr>
<h4> Run Service without docker</h4>
<ul>   
<li> Navigate to service/src/ </li>
<li> Install requirements using "pip install -r requirements.txt" </li>
<li> Run application using python3 "python main.py" </li>
<li> Navigate to localhost in your browser (port 80) </li> 
</ul>

<h3> ID/Ticket Vulnerability </h3>
<p> Generating plantes' IDs is possible since it doesn't require secret value </br>
Tickets are validated through given binary. <p>
<h4> Exploit: </h4>
This exploit is provided in "/exploits/reverse-engi-exploit.py" </br>
Tickets are big primenumbers >999.999.999 in negative value.

<h3> Template injection Vulnerability </h3> 
The planet name Parameter is given to the jinja template using %s formatter, and name is validated if it is contained in the parameter 
given through the url. </br>
Example: </br> 
Navigating to "http://localhost/planet_details?name=SAM23" will give back the first matching planet that its name is contained in 
the string "SAM23". </br>

<h4> Exploit: </h4> 
Appending dopple curly braces to the planet name will return the name and whatever the return value of the python script included inside the dobble curly braces.
</br>
The easiest possilbe exploit is to append "{{planet.flag}}" to the name: </br>
"http://localhost/planet_details?name=SAM23{{planet.flag}}"
</br> 
This will return the flag appended to the name. 

<h3> Write up </h3> 
Read <a href="https://saarsec.rocks/2019/07/16/telescopy.html"> here </a> for a write up of the service played in the Enowars3 2019 CTF. </br>
Interesting is how the Team could manage to run unintended Remote Code Execution out of the Templete injection Vulnerability. </br>

