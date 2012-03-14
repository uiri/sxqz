<?php
function add_com_or_org($query) {
    if (preg_match('/\.o$/', $query)) {
	$query .= 'rg';
    } else if (preg_match('/\.n$/', $query)) {
	$query .= 'et';
    } else if (!preg_match('/\.$/', $query)) {
	$query .= '.com';
    } else {
	$query .= 'com';
    }
    return $query;
}

function single_letter_shortcut($query, $short) {
    $shortcuts = array(
	"a" => "amazon.com/s/?field-keywords=",
	"b" => "bing.com/search?q=",
	"d" => "duckduckgo.com/?q=",
	"e" => "www.ebay.com/sch/items/?_nkw=",
	"g" => "google.com/search?q=",
	"q" => "google.com/search?q=site%3Aquora.com+",
	"r" => "reddit.com/search?q=",
	"s" => "soundcloud.com/search?q[fulltext]=",
	"t" => "thesaurus.com/browse/",
	"u" => "youtube.com/results?search_query=",
	"w" => "en.wikipedia.org/w/index.php?search=",
	"y" => "search.yahoo.com/search?p="
	);
    if ($shortcuts[$short]) {
	if ($query != "") {
	    header('Location: http://' . $shortcuts[$short] . $query, TRUE, 302);
	} else {
	    if ($short != 'q') {
		header('Location: http://' . substr($shortcuts[$short], 0, strpos($shortcuts[$short], '/')),
		       TRUE, 302);
	    } else {
		header('Location: http://quora.com', TRUE, 302);
	    }
	}
	exit();
    }
}

$define = FALSE;

header('Content-Type: text/html;charset=utf-8');

if ($_GET['q']) {
    $query = $_GET['q'];
    if (preg_match("/^=/", $query)) {
	$query = substr($query, 1);
	$query = urlencode($query);
	header('Location: http://wolframalpha.com/input/?i=' . $query, TRUE, 302);
	exit();
    } else if (preg_match("/\/[A-Za-z]$/", $query)) {
	$short = substr($query, -1);
	$query = substr($query, 0, strlen($query)-2);
	single_letter_shortcut($query, $short);
    } else if (preg_match("/\//", $query)) {
	$query = preg_replace("/ \/\//", "//", $query);
	if (preg_match("/\/\/define$/", $query)) {
	    $define = TRUE;
	    $query = preg_replace("/\/\/define$/", "", $query);
	} else if (preg_match("/\/\/map$/", $query)) {
	    $query = preg_replace("/\/\/map$/", "", $query);
	    $query = urlencode($query);
	    header('Location: http://google.com/maps?q=' . $query, TRUE, 302);
	    exit();
	} else if (preg_match("/\/\/img$/", $query)) {
	    $query = preg_replace("/\/\/img$/", "", $query);
	    $query = urlencode($query);
	    header('Location: http://google.com/search?tbm=isch&q=' . $query, TRUE, 302);
	    exit();
	} else if (preg_match("/\/\/code$/", $query) || preg_match("/\/\/code;l=[A-Za-z]+/", $query)) {
	    if (preg_match("/\/\/code$/", $query)) {
		$params = "";
	    } else {
		$params = substr($query, strrpos($query, ';'));
		$params = preg_replace("/l=([A-Za-z]+)/", "&language=$1", $params);
	    }
	    $query = substr($query, 0, strrpos($query, "//"));
	    $query = urlencode($query);
	    header("Location: http://github.com/search?type=Code" . $params . "&q=" . $query, TRUE, 302);
	    exit();
	} else if (preg_match("/^\/\//", $query)) {
	    if (!preg_match('/\.[A-Za-z]{2,4}/', $query)) {
		$query = add_com_or_org($query);
	    }
	    if (file_get_contents('http:' . $query)) {
		header('Location: http:' . $query,TRUE,302);
		exit();
	    }
	} else if (preg_match('/\/\/$/', $query)) {
	    $query = substr($query, 0, strpos($query, '/'));
	    $query = urlencode($query);
	} else {
	    $query = preg_replace('/\/\//', ' site:', $query);
	    if (!preg_match('/site[^.]+\.[A-Za-z]{2,4}/', $query)) {
		$query = add_com_or_org($query);
	    }
	}
	$query = urlencode($query);
    } else {
	$query = urlencode($query);
	$opts = array('http' => array('user_agent' => 'PassThrust'));
	$context = stream_context_create($opts);
	$url = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles=" . $query;
	$json = file_get_contents($url, FALSE, $context);
	$jsonarr = json_decode($json, true);
	$keys = array_keys($jsonarr["query"]["pages"]);
	if ($keys[0] != -1) {
	    header('Location: http://en.wikipedia.org/wiki/' . $jsonarr["query"]["pages"][$keys[0]]["title"], TRUE, 302);
	    exit();
	}
    }
    if (!$define) {
	header('Location: http://bing.com/search?q=' . $query,TRUE,302);
	exit();
    }
}

if (!$define) {
    include("home.tpl");
} else {
    include("define.tpl");
}

?>
