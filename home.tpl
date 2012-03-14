<head>
  <title>Pass Thrust</title>
  <style type="text/css">
      body {
	  color: #222;
	  background-color: #bbb;
	  margin: 10%;
	  margin-top: 5%;
	  text-align: center;
	  font-size: 1.5em;
	  font-family: Verdana, Verdana, Geneva, sans-serif;
      }

      .links {
	  margin-left: auto;
	  margin-right: auto;
	  width: 200px;
	  font-size: 15px;
      }

      a:* {
	  color: #300;
      }

      .syntax {
	  font-size:12px;
	  text-align:left;
	  margin-left:150px;
      }
  </style>
  <script type="text/javascript">
    function hide_and_show(id) {
	var thing = document.getElementById(id);
	if (thing.style.display == "none") {
	    thing.style.display = "inline";
	} else {
	    thing.style.display = "none";
	}
    }
  </script>
</head>
<body>
  <h2>Pass Thrust</h2>
  <form action="/search" method="get">
    <input type="text" name="q">
    <a href="#" style='font-size:12px' onclick='hide_and_show("help")'>Help</a>
  </form>
  <div id="help" style='display:none'>
    <h4>Example Queries</h4>
    <div class="syntax">
      <ul>
	<li>=1+1 &mdash; Go to Wolfram Alpha with 1+1 as input.</li>
	<li>cats//xkcd.com &mdash; Turns into a Bing search for cats site:xkcd.com</li>
	<li>pots and pans/a &mdash; turns into an amazon search for pots and pans <a href="#" onclick='hide_and_show("bang");'>Click here for the list of shortcuts</a>
	  <span id='bang' style='display:none'>
	    <ul>
	      <li>a - Amazon</li>
	      <li>b - Bing</li>
	      <li>d - DuckDuckGo</li>
	      <li>e - eBay</li>
	      <li>g - Google</li>
	      <li>q - Quora (via Google; equivalent to //quora)</li>
	      <li>r - Reddit</li>
	      <li>s - SoundCloud</li>
	      <li>t - Thesaurus</li>
	      <li>u - YouTube</li>
	      <li>w - Wikipedia (english)</li>
	      <li>y - Yahoo!</li>
	    </ul>
	  </span>
	<li>//bit.ly &mdash; go straight to bit.ly</li>
	<li>//reddit or //python.o &mdash; the .com is automatically added; .o becomes .org and .n becomes .net</li>
	<li>United States// &mdash; avoids the handy wikipedia redirect, instead searching Google for United States</li>
<!--	<li>Proposterous//define &mdash; scrapes Urban Dictionary, Wiktionary and the Free Dictionary for the definition(s) of proposterous.</li> -->
	<li>New York//map &mdash; Google Maps search for New York. New York//img is an Google Image search.</li>
	<li>require//code;l=ruby &mdash; Searches for ruby code containing the term require on GitHub.</li>
      </ul>
    </div>
  </div>
</body>
