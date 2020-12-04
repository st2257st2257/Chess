<!doctype html>
<html>
    <head>
        <script src="http://mychess.xyz/JS/start.js"></script>
        
        <title>KE Games</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<style>
		    @import url(http://mychess.xyz/css/style_nav.css);
		    @import url(http://mychess.xyz/css/footer.css);
		    @import url(http://mychess.xyz/css/extra.css);
		</style>
		<link rel = "stylesheet" type = "text/css" href = "css/style_nav.css">
		<script src="js.js"></script>
		<style>
   body {
    background: #c7b39b url(img/board.jpg); /* Цвет фона и путь к файлу */
    }
   table {
       margin-top: 30px;
       background: #c7b39b url(img/back_1.jpg);
   } 
   </style>
   </head>
    <body>
        <din id="div_menu"></din><script src="http://mychess.xyz/JS/return_menu.js"></script> <!-- create menu-->
  
        
        <table align = 'center' border = '2' class = 'main'><tr><td>
            <h1 align="center">Registration</h1>
            <form action='index.php' method='post' enctype='multipart/form-data'>
                <p align="center">Enter name</p>
                <textarea id = '102' rows='2' cols='45' name = 'name' placeholder ='Enter login'></textarea>
                <p align="center">Enter password</p>
                <textarea id = '103' rows='2' cols='45' name = 'pass' placeholder ='Enter password'></textarea>
                <p align="center">Enter text</p>
                <textarea id = '104' rows='2' cols='45' name = 'text' placeholder ='Enter text'>Your text</textarea>
                <p></p>
                <input type='submit' name='upload' value='Sign up'>

            </form>
        </td></tr></table>



<?php

$server = "localhost";
$username = "id14440505_assskristal";
$password = "wacze000We?d";
$dbname = "id14440505_img_v";
$charset = 'utf8';

$connection = new mysqli($server, $username, $password, $dbname);

if($connection->connect_error){
	die("Ошибка соединения".$connection->connect_error);
}

if(!$connection->set_charset($charset)){
	echo "Ошибка установки кодировки UTF8";
}

	
if(isset($_POST['upload'])){
	$name = $_POST['name']; 
	$pass = $_POST['pass'];
	$text = $_POST['text'];
	
	$check = $connection->query("SELECT name FROM Users WHERE name = '$name'")->fetch_object();
	
	if (!($check)){
	    $request = "INSERT INTO chess_players (login, password, rate) VALUES ('$name', '$pass',800);";
	    $connection->query($request);
	    echo "<script>localStorage.setItem('name', `$name`);</script>";
        echo "<script>localStorage.setItem('pass', `$pass`);</script>";
    
        echo "<script>sessionStorage.setItem('name', `$name`);</script>";
        echo "<script>sessionStorage.setItem('pass', `$pass`);</script>";
	    echo "<script>window.open('http://mychess.xyz/','_self');</script>";
	}
	else{
	    echo "<p></p><p color ='blue'>Here is User with that name enter another one<p>";
	}
	$connection->close();
	
}
echo "<script>console.log('Ok_js_work')</script>";
?>
        
        
        
        
        <div id = "footer"></div>
        <script src="http://mychess.xyz/JS/return_footer.js"></script> <!-- create footer-->
        <script src="http://mychess.xyz/JS/base.js"></script>
    </body>
</html>
