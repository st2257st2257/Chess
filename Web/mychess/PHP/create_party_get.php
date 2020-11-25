<?php

$white = strval($_GET['white']);
$black = strval($_GET['black']);
$time = intval($_GET['time']);

$mysqli = new mysqli("localhost","id14440505_assskristal","wacze000We?d","id14440505_img_v");

$mysqli->query("SET NAMES 'utf-8'");

$mysqli->query("INSERT INTO chess (player_white_login, player_black_login, time) VALUES 
('$white','$black',$time);");


echo strval($mysqli->query("SELECT * FROM chess WHERE id = (SELECT MAX(id) FROM chess);")->fetch_object()->id);

$mysqli->close();
?>
