<?php

$id = intval($_GET['id']);
$move_number = intval($_GET['move_number']);


$mysqli = new mysqli("localhost","id14440505_assskristal","wacze000We?d","id14440505_img_v");
$mysqli->query("SET NAMES 'utf-8'");

# check move numer on the server and compare with curent vale
# if it is the same:
#   wait for a second
# else:
#   return last move
# 

$server_move_number = intval($mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()->move_number);

echo "<p>server: $server_move_number  local: $move_number</p>";


while (intval($server_move_number) == $move_number){
    $mysqli->close();
    sleep(1);
    echo "<p>Waiting...</p>";
    
    
    $mysqli = new mysqli("localhost","id14440505_assskristal","wacze000We?d","id14440505_img_v");
    $mysqli->query("SET NAMES 'utf-8'");
    $server_move_number = intval($mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()->move_number);
}



$ans = $mysqli->query("SELECT * FROM chess WHERE id = $id;")->fetch_object()->party_moves;
echo array_slice(str_split($ans), -6, -1)[0];
echo array_slice(str_split($ans), -6, -1)[1];
echo array_slice(str_split($ans), -6, -1)[2];
echo array_slice(str_split($ans), -6, -1)[3];
echo array_slice(str_split($ans), -6, -1)[4];

$mysqli->close();
?>
