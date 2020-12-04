<!DOCTYPE html>
<html>
    
<head>
    <!-- CSS -->
    <link rel = "stylesheet" type = "text/css" href = "css/style.css">
    <link rel = "stylesheet" type = "text/css" href = "css/footer.css">
    <link rel = "stylesheet" type = "text/css" href = "css/style_nav.css">
    <link rel = "stylesheet" type = "text/css" href = "css.css">
     
    
    <!-- Base -->
    <meta charset="utf-8">
    <title>Main</title>
   <style>
   body {
    background: #c7b39b url(img/board.jpg); /* Цвет фона и путь к файлу */
    }
    ul {
    list-style-image: url(images/kn.png); /* Путь к изображению маркера */
   }
   table.enter_form {
       position: absolute;
       top: 400px;
       right: 30px;
       background: #c7b39b url(img/back_5.jpg);
   } 
   table.enemy {
       position: absolute;
       top: 150px;
       left: 30px;
       background: #c7b39b url(img/back_4.jpg);
   } 
   table.you {
       position: absolute;
       top: 150px;
       right: 30px;
       background: #c7b39b url(img/back_4.jpg);
   } 
   </style>
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <script src="js.js"></script>
</head>

<body>
    <div id="div_menu"></div><script src="http://mychess.xyz/JS/return_menu.js"></script> <!-- create menu-->
  
         <tabel align='left'><font color="white">Party id: </font><font color="white" id="div_text">123</font><font color="white">></font></tabel>
        <tabel align='left'><font color="white">Server response: </font><font color="white" id="r_text"></font><font color="white">></font></tabel>
        <font color="white">
            <div id="div_move"></div>
            <div id="div_ans"></div>
            <p>-</p>
            <p>-</p>
            <p>-</p>
            <p>-</p>
            <p>-</p>
            <p>-</p>

            <div id="div_e_move">e_move: </div>
            
        </font>
        
        <script src="get_text.js"></script>
        
        
        <div id="container"></div>

    
    <table  border = '2' class = "enemy"><tr><td>
            <h1 align="center"><font color="white">Your Enemy</font></h1>
                <p align="center"><font color="white">Name: Magnus Karlsen</font></p>
                <p align="center"><font color="white">Rate: 2800</font></p>
                <p align="center"><font color="white">Color: black</font></p>
    </td></tr></table>
    
    <table border = '2' class = "you"><tr><td>
            <h1 align="center"><font color="white">Your  Profile</font></h1>
                <p align="center"><font color="white">Name: st2257</font></p>
                <p align="center"><font color="white">Rate: 1500</font></p>
                <p align="center"><font color="white">Color:white </font></p>
    </td></tr></table>

    <table align = 'right' border = '2' class = "enter_form"><tr><td>
            <h1 align="center"><font color="white">Join party!</font></h1>
            <form action='index.php' method='post' enctype='multipart/form-data'>
                <p align="center"><font color="white">Enter party id</p></font>
                <textarea id = 'party_id' rows='2' cols='45' name = 'id' placeholder ='If you want to join a random party enter 0'></textarea>
                <p align="center"><font color="white">Enter color</p></font>
                <textarea id = 'color' rows='2' cols='45' name = 'color' placeholder ='White'></textarea>

                <p></p>
                <input align='center' type='submit' name='upload' value='Sign up'>
            </form>
    </td></tr></table>
    
    
    
    
    
</body>
</html>
