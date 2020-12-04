<?php

$id = intval($_GET['id']);
$move = strval($_GET['move']);


echo "id: " . $id . "  " . $move;


$mysqli = new mysqli("localhost","id14440505_assskristal","wacze000We?d","id14440505_img_v");

$mysqli->query("SET NAMES 'utf-8'");


if ($mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()){
    $new_last_move = intval($mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()->move_number)+1;

}
else{
    $new_last_move = 1;

}
 

if ($mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()){
    $new_move_ceq = $mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()->party_moves . $move . ';';
}
else{
    $new_move_ceq = $move . ';';
}

$mysqli->query("UPDATE chess SET party_moves = '$new_move_ceq', move_number=$new_last_move WHERE id=$id;");

$mysqli->close();
?>
