<head>
	<title><?php echo $query; ?></title>
	<style type="text/css">
	  .NavFrame, .checktrans {
	      display:none;
	  }
	</style>
</head>
<body>
<?php
$urbanfile = file_get_contents("http://urbandictionary.com/define.php?term=" . $query);
$urbanhtml = substr($urbanfile, strpos($urbanfile, 'body'));
$urbanhtml = substr($urbanhtml, strpos($urbanhtml, 'content'));
$urbanhtml = substr($urbanhtml, strpos($urbanhtml, '<table'));
$urbanhtml = substr($urbanhtml, 0, strpos($urbanhtml, '<!-- google_ad_section_end'));
$urbanhtml = preg_replace("/\s(.+)\s<div class='greenery'>/", "", $urbanhtml);
$urbanhtml = preg_replace("/(\s)<a href=\"#(.+)\s/", "$1", $urbanhtml);
$urbanhtml = preg_replace("/(\s)(.+)video(.+)\s/", "$1", $urbanhtml);
$urbanhtml = preg_replace("/\s(.+)\s(.+)\s$/", "", $urbanhtml);
$urbanhtml = preg_replace("/<script\b[^>]*>(.*?)<\/script>/is", "SCRIPT", $urbanhtml);
$urbanhtml = preg_replace("/\s(.+)SCRIPT(.+)\s/", "", $urbanhtml);
$urbanhtml = preg_replace("/style='padding(.+)'/", "", $urbanhtml);
$urbanhtml = preg_replace("/\s(.+)urbanup(.+)>(.+)<(.+)\s/", "$3", $urbanhtml);
$urbanhtml = preg_replace("/\/define\.php\?term=([a-zA-Z]+)/", "/passthrust/?q=$1//define", $urbanhtml);
$urbanhtml = preg_replace("/\/(author\.php\?author=[a-zA-Z]+)/", "//urbandictionary.com/$1", $urbanhtml);
if ($urbanhtml != "") {
    echo "<h1>Urban Dictionary</h1>" . $urbanhtml;
}
$opts = array('http' => array('user_agent' => 'PassThrust'));
$context = stream_context_create($opts);
$url = "https://en.wiktionary.org/wiki/" . $query;
$wiktfile = file_get_contents($url, FALSE, $context);
$wikthtml = preg_replace("/<script\b[^>]*>(.*?)<\/script>/is", "SCRIPT", $wiktfile);
$wikthtml = substr($wikthtml, strpos($wikthtml, '<span class="mw-headline" id="Etym'));
$wikthtml = substr($wikthtml, 0, strrpos($wikthtml, 'bodycontent'));
$wikthtml = substr($wikthtml, 0, strrpos($wikthtml, 'Translations'));
$wikthtml = preg_replace("/\s(.+)\s$/", "", $wikthtml);
$wikthtml = preg_replace("/(\s<h\d>)<span(.+)<span(.+)\s/", "$1<span $3", $wikthtml);
$wikthtml = preg_replace("/(\s)(.+)Translations(.+)(<div class=\"NavFrame\">\s)/", "$1$4", $wikthtml);
if ($wikthtml != "") {
    echo "<h1>Wiktionary</h1>
<h2>English</h2>
<h3>" . $wikthtml . "</div></div>";
}
$freefile = file_get_contents("http://thefreedictionary.com/" . $query);
$freehtml = substr($freefile, strpos($freefile, "<table cellspacing=\"5\""));
$freehtml = substr($freehtml, 0, strpos($freehtml, "<div id=Translations"));
$freehtml = preg_replace("/<script\b[^>]*>(.*?)<\/script>/is", "SCRIPT", $freehtml);
$freehtml = str_replace("SCRIPT", "", $freehtml);
//if ($freehtml != "") {
     echo "<h1>The Free Dictionary</h1>" . $freehtml;
//}
 ?>
</body>
