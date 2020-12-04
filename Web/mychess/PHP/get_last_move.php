<?php

$id = intval($_GET['id']);

$mysqli = new mysqli("localhost","id14440505_assskristal","wacze000We?d","id14440505_img_v");

$mysqli->query("SET NAMES 'utf-8'");

$ans = $mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()->party_moves;



$input = array("a", "b", "c", "d", "e", "f", "g");

echo array_slice(str_split($ans), -6, -1)[0];
echo array_slice(str_split($ans), -6, -1)[1];
echo array_slice(str_split($ans), -6, -1)[2];
echo array_slice(str_split($ans), -6, -1)[3];
echo array_slice(str_split($ans), -6, -1)[4];

$mysqli->close();
?>
