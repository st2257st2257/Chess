<?php

$id = strval($_GET['id']);
$data = strval($_GET['data']);

$mysqli = new mysqli("localhost","id14440505_assskristal","wacze000We?d","id14440505_img_v");

$mysqli->query("SET NAMES 'utf-8'");

$mysqli->query("UPDATE chess SET party_figures='$data' WHERE id=$id;");

$mysqli->close();

echo "data changed";
?>
