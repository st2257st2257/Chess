window.onload = function(){
    var w = (window.innerWidth) || 360;
    var h = (window.innerHeight - 50) || 500;
    
    // base party settings
    var party_id = 0;
    var move_number = 0;
    var one_player_game = 0;//true;
    var my_color = 0; // 0 -white, 1 - black
    
    
    var tsw = (w > h) ? h : w;
    var sw = (tsw - 16)/8;
    
    var container = document.getElementById("container");
    
    function sleep(milliseconds) {
        const date = Date.now();
        let currentDate = null;
        do {
            currentDate = Date.now();
        } while (currentDate - date < milliseconds);
    }
    
    
    for(var n = 0; n < 64; n++){
        var square = document.createElement("div");
        square.classList.add("square");
        square.classList.add("s"+n);
        square.style.height = sw + 'px';
        square.style.width = sw + 'px';
        square.style.top = 100 + 7+(h-tsw)/2+sw*(Math.floor(n/8)) + 'px';
        square.style.left = 7+(w-tsw)/2+sw*(Math.floor(n%8)) + 'px';
        square.style.fontSize = sw*3/4 + 'px';
        container.appendChild(square);
    }

    var fonts = {
        'k' : '&#9818;',
        'q' : '&#9819;',
        'r' : '&#9820',
        'b' : '&#9821',
        'n' : '&#9822',
        'p' : '&#9823',
        'l' : '&#9812;',
        'w' : '&#9813;',
        't' : '&#9814',
        'v' : '&#9815',
        'm' : '&#9816',
        'o' : '&#9817',
        
    };
    
    var values = ['r','n','b','q','k','b','n','r',
                  'p','p','p','p','p','p','p','p',
                   0,0,0,0,0,0,0,0,
                   0,0,0,0,0,0,0,0,
                   0,0,0,0,0,0,0,0,
                   0,0,0,0,0,0,0,0,
                   'o','o','o','o','o','o','o','o',
                   't','m','v','w','l','v','m','t'];
    
    function get_full_name(short_name){
        switch(short_name){
            case ("r"):
                return "black_rook";
                
            case ("n"):
                return "black_knight";
                
            case ("b"):
                return "black_bishop";
                
            case ("q"):
                return "black_queen";
                
            case ("k"):
                return "black_knight";
                
            case ("p"):
                return "black_pawn";

            case ("o"):
                return "white_pawn";

            case ("t"):
                return "white_rook";

            case ("m"):
                return "white_knight";

            case ("v"):
                return "white_bishop";

            case ("w"):
                return "white_queen";

            case ("l"):
                return "white_king";
            
            default:
                return "";
        }
    }
    
    
    function get_move(){
        var xmlhttp = new XMLHttpRequest();
        var req = "";
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("div_e_move").innerHTML = this.responseText;
            }
        };
        if (localStorage.getItem("name")==null){
            window.open("http://mychess.xyz/Signin", "_self");
        }
        else{
            xmlhttp.open("GET","http://mychess.xyz/PHP/get_move.php?id=" + party_id + 
                         "&move_number=" + move_number, true);
            xmlhttp.send();
        }
        //document.getElementById("div_e_move").innerHTML = req;
        //return req;
    }
    
    
    function arr_to_string(){
        var res = "";
        for (var i ; i<64; i++ ){
            res = res + String( 1 + i%8 ) + String( 1 + parseInt(i/8) );
            res = res + ",";
            console.log(res);
            if (values[i] == 0){
                res = res + "";
            }
            else{
                res = res + get_full_name(values[i]);
            }
            res = res + ";";
        }
        return res;
    }
    
    
    function update_web() {
        
        //var pass = document.getElementById('103').innerHTML;
        var xmlhttp = new XMLHttpRequest();
        
        party_id = String(document.getElementById("div_text").innerHTML).match(/\d+/)[0];
        
        // console.log(party_id);
        // console.log(arr_to_string());
        
        var res = "";
        for (var i = 0 ; i<64; i++ ){
            res = res + String( 1 + i%8 ) + String( 1 + parseInt(i/8) );
            res = res + ",";
            //console.log(res);
            if (values[i] == 0){
                res = res + "";
            }
            else{
                res = res + get_full_name(values[i]);
            }
            res = res + ";";
            
        }
        
        // console.log(res);
        
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("r_text").innerHTML = this.responseText;
            }
        };
        if (localStorage.getItem("name")==null){
            window.open("http://mychess.xyz/Signin", "_self");
        }
        else{
            xmlhttp.open("GET","http://mychess.xyz/PHP/update_party_get.php?id=" + party_id 
            + "&data=" + res,true);
            xmlhttp.send();
        }
    }
    update_web();
    
    
    var ck = false;
    var cr1 = false;
    var cr2 = false;
    var cl;
    

    var sqs = document.getElementsByClassName("square");

    for(var n = 0; n < 64; n++){
        if(values[n] !== 0){
           sqs[n].innerHTML = fonts[values[n]];
        }
        sqs[n].addEventListener("click",check);
    }
    
    
    
    // обновляем поля
    function updateSquarecolor(){
        for(var n = 0; n < 64; n++){
            if(Math.floor(n/8)%2 === 0){
                if(n%2 === 0){
                    sqs[n].style.background = '#fff5ff';
                }
                else {
                    sqs[n].style.background = '#208b52';
                }
            }
            else {
                if(n%2 === 1){
                    sqs[n].style.background = '#fff5ff';
                }
                else {
                    sqs[n].style.background = '#208b52';
                }
            }
        }
    }
    updateSquarecolor();





    var moveable = false;
    var moveTarget = "";
    var moveScopes = [];


    function checkBlack(n,values){
        // update_web();
        var target = values[n];
        var scopes = [];
        var x = n;
       
        if(target === "o"){
            x -= 8;
            if("prnbkq".indexOf(values[x-1]) >= 0 && x%8 != 0){
                scopes.push(x-1);
            }
            if("prnbkq".indexOf(values[x+1]) >= 0 && x%8 != 7){
                scopes.push(x+1);
            }
            if(x >= 0 && values[x] === 0){
                scopes.push(x);
                if(x >= 40){
                    if(x-8 >= 0 && values[x-8] === 0){
                        scopes.push(x-8);
                    }
                }
            }
        }
       
        else if(target === "t"){
            x = n;
            x -= 8;
            while(x >= 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 8;
            }
            x = n;
            x += 8;
            while(x < 64){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 8;
            }
            x = n;
            x++;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x++;
            }
            x = n;
            x--;
            while(x%8 != 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x--;
            }
        }
        
        else if(target === "m"){
            x = n;
            if(x%8 > 1 && x%8 < 6){
                x -= 17;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 15;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }

                x = n;
                x -= 10;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 6;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 6;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 10;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 15;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 17;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
            }
            else {
                x = n;
                if(x%8 <= 1){
                    x = n;
                    x -= 15;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x -= 6;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 10;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 17;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
                x = n;
                if(x%8 === 1){
                    x -= 17;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 15;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
                if(x%8 >= 6){
                    x = n;
                    x -= 17;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x -= 10;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 6;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 15;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
                x = n;
                if(x%8 === 6){
                    x = n;
                    x -= 15;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 17;
                    if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
            }
        }
        
        else if(target === "v"){
            x = n;
            x -= 9;
            while(x >= 0 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 9;
            }
            x = n;
            x += 7;
            while(x < 64 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 7;
            }
            x = n;
            x += 9;
            while(x%8 != 0 && x%8 !== 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 9;
            }
            x = n;
            x -= 7;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 7;
            }
        }
       
        else if(target === "w"){
            x = n;
            x -= 8;
            while(x >= 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 8;
            }
            x = n;
            x += 8;
            while(x < 64){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 8;
            }
            x = n;
            x++;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x++;
            }
            x = n;
            x--;
            while(x%8 != 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x--;
            }
            x = n;
            x -= 9;
            while(x >= 0 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 9;
            }
            x = n;
            x += 7;
            while(x < 64 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 7;
            }
            x = n;
            x += 9;
            while(x%8 != 0 && x%8 !== 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 9;
            }
            x = n;
            x -= 7;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("prnbqk".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 7;
            }
        }
        
        else if(target === "l"){
            x = n;
            x += 8;
            if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                scopes.push(x);
            }
            x = n;
            x -= 8;
            if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                scopes.push(x);
            }
            x = n;
            if(x%8 > 0){
                x = n;
                x -= 1;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 9;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }

                x = n;
                x += 7;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
            }
            x = n;
            if(x%8 < 7){
                x = n;
                x += 1;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 9;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 7;
                if(("prnbqk".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
            }
            x = n;
            if(!ck){
                cl = false;
                if(!cr2){
                //    cl = false;
                    if(values[n+1] === 0 && values[n+2] === 0 && values[n+3] === "t"){
                        scopes.push(x+2);
                        cl = true;
                    }
                }
                if(!cr1){
                //    cl = false;
                    if(values[n-1] === 0 && values[n-2] === 0 && values[n-3] === 0 && values[n-4] === "t"){
                        scopes.push(x-2);
                        cl = true;
                    }
                }
            }
        }
        if(scopes.length) return scopes;
    }

    function checkWhite(n,values){
        // update_web();
        var target = values[n];
        var scopes = [];
        var x = n;
        if(target === "p"){
            x += 8;
            if("otmvlw".indexOf(values[x-1]) >= 0 && x%8 != 0){
                scopes.push(x-1);
            }
            if("otmvlw".indexOf(values[x+1]) >= 0 && x%8 != 7){
                scopes.push(x+1);
            }
            if(x < 64 && values[x] === 0){
                scopes.push(x);
                if(x <= 23){
                    if(x+8 >= 0 && values[x+8] === 0){
                        scopes.push(x+8);
                    }
                }
            }
        }
        
        else if(target === "r"){
            x = n;
            x -= 8;
            while(x >= 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 8;
            }
            x = n;
            x += 8;
            while(x < 64){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 8;
            }
            x = n;
            x++;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x++;
            }
            x = n;
            x--;
            while(x%8 != 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x--;
            }
        }
        
        else if(target === "n"){
            x = n;
            if(x%8 > 1 && x%8 < 6){
                x -= 17;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 15;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }

                x = n;
                x -= 10;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 6;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 6;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 10;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 15;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 17;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
            }
            else {
                x = n;
                if(x%8 <= 1){
                    x = n;
                    x -= 15;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x -= 6;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 10;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 17;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
                x = n;
                if(x%8 === 1){
                    x -= 17;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 15;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
                if(x%8 >= 6){
                    x = n;
                    x -= 17;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x -= 10;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 6;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 15;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
                x = n;
                if(x%8 === 6){
                    x = n;
                    x -= 15;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                    x = n;
                    x += 17;
                    if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                        scopes.push(x);
                    }
                }
            }
        }
     
        else if(target === "b"){
            x = n;
            x -= 9;
            while(x >= 0 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 9;
            }
            x = n;
            x += 7;
            while(x < 64 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 7;
            }
            x = n;
            x += 9;
            while(x%8 != 0 && x%8 !== 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 9;
            }
            x = n;
            x -= 7;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 7;
            }
        }
        
        else if(target === "q"){
            x = n;
            x -= 8;
            while(x >= 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 8;
            }
            x = n;
            x += 8;
            while(x < 64){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 8;
            }
            x = n;
            x++;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x++;
            }
            x = n;
            x--;
            while(x%8 != 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x--;
            }
            x = n;
            x -= 9;
            while(x >= 0 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 9;
            }
            x = n;
            x += 7;
            while(x < 64 && x%8 !== 7){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 7;
            }
            x = n;
            x += 9;
            while(x%8 != 0 && x%8 !== 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x += 9;
            }
            x = n;
            x -= 7;
            while(x%8 != 0){
                if(values[x] === 0){
                    scopes.push(x);
                }
                else if("otmvlw".indexOf(values[x]) >= 0){
                    scopes.push(x);
                    break;
                }
                else {
                    break;
                }
                x -= 7;
            }
        }
        
        else if(target === "k"){
            x = n;
            x += 8;
            if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                scopes.push(x);
            }
            x = n;
            x -= 8;
            if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                scopes.push(x);
            }
            x = n;
            if(x%8 > 0){
                x = n;
                x -= 1;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 9;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }

                x = n;
                x += 7;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
            }
            x = n;
            if(x%8 < 7){
                x = n;
                x += 1;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x += 9;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
                x = n;
                x -= 7;
                if(("otmvlw".indexOf(values[x]) >= 0 || values[x] === 0) && x < 64 && x >= 0){
                    scopes.push(x);
                }
            }
        }
        if(scopes.length) return scopes;
    }
    var myTurn = true;


    function add_move(move_string){
        
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("div_ans").innerHTML = this.responseText;
            }
        };
        if (localStorage.getItem("name")==null){
            window.open("http://mychess.xyz/Signin", "_self");
        }
        else{
            xmlhttp.open("GET","http://mychess.xyz/PHP/add_move.php?id=" + party_id
            + "&move=" + move_string, true);
            xmlhttp.send();
        }
        move_number = parseInt(parseInt(move_number) + 1);
    }
    
    function get_last_move(){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("div_move").innerHTML = this.responseText;
            }
        };
        if (localStorage.getItem("name")==null){
            window.open("http://mychess.xyz/Signin", "_self");
        }
        else{
            xmlhttp.open("GET","http://mychess.xyz/PHP/get_last_move.php?id=" + String(party_id) ,true);
            xmlhttp.send();
        }
        return document.getElementById("div_move");
    }
    
    
    
    function check(){
        // update_web();
        if(myTurn){
            var n = Number(this.classList[1].slice(1));
            var target = values[n];

            var scopes = checkBlack(n,values) || [];

            var x = n;

            if(!moveable){
                if(scopes.length > 0){
                    moveable = true;
                    moveTarget = n;
                    moveScopes = scopes.join(",").split(",");
                }
                else {

                }
            }
            else {
                if(moveScopes.indexOf(String(n)) >= 0){
                    var checkArr = [];
                    var saveKing = false;
                    for(var z = 0; z < 64; z++){
                        checkArr[z] = values[z];
                    }
                    
                    checkArr[n] = checkArr[moveTarget];
                    checkArr[moveTarget] = 0;
                    
                    for(var y = 0; y < 64; y++){
                        if("prnbkq".indexOf(checkArr[y]) >= 0){
                            var checkScp = checkWhite(y,checkArr) || [];
                            for(var z = 0; z < checkScp.length; z++){
                                if(checkArr[checkScp[z]] === 'l'){
                                    if(!saveKing){
                                        alert('Save Your King');
                                        saveKing = true;
                                    }
                                }
                            }
                        }
                    }
                    
                    if(!saveKing){
                        values[n] = values[moveTarget];
                        values[moveTarget] = 0;
                        
                        if (1){
                            add_move(
                                String(1+parseInt(n%8))+ 
                               String(1+parseInt(n/8)) + 
                               "-"+
                               String(1+parseInt(parseInt(moveTarget)%8)) + 
                                String(1+parseInt(parseInt(moveTarget)/8)));
                        }
                        
                        
                        if(cl){
                            if(n === 62 && moveTarget === 60){
                                values[63] = 0;
                                values[61] = "t";
                            }
                            else if(n === 58 && moveTarget === 60){
                                values[59] = "t";
                                values[56] = 0;
                            }
                        }
                        if(moveTarget === 60){
                            ck = true;
                        }
                        else if(moveTarget === 63){
                            cr2 = true;
                        }
                        else if(moveTarget === 56){
                            cr1 = true;
                        }
                        if(values[n] === "o" && n < 8){
                            values[n] = "w";
                        }
                        moveable = false;
                        scopes = [];

                        myTurn = false;
                        setTimeout(chooseTurn,100);
                    }
                }
                else {
                    moveScopes = [];
                    moveable = false;    
                }
            }
            
            
            updateSquarecolor();
            
            for(var x = 0; x < 64; x++){
                sqs[x].innerHTML = fonts[values[x]];
                if(values[x] === 0){
                    sqs[x].innerHTML = "";
                }
            }

            for(var x = 0; x < scopes.length; x++){
                sqs[scopes[x]].style.background = "#f45";//.classList.add("scope");
            //    alert(scopes)
            }
        }
    }


    var arr = [];

    function chooseTurn(){
        var approved = [];
        var actions = [];
        var effects = [];


        for(var n = 0; n < 64; n++){
            if("prnbqk".indexOf(values[n]) >= 0){
                var scopes = checkWhite(n,values) || [];
                for(var x = 0; x < scopes.length; x++){
                    var tmp = []//values.join(',').split(',');
                    for(var xx = 0; xx < 64; xx++){
                        tmp[xx] = values[xx]
                    }
                    var effect = 0;
                    var action = Math.random()*3;
                    //Action value
                    var actionValue = tmp[scopes[x]];
                    if(actionValue === "l"){
                        action = 100 + Math.random()*3;
                    }
                    else if(actionValue === "w"){
                        action = 90 + Math.random()*3;
                    }
                    else if(actionValue === "v"){
                        action = 50 + Math.random()*3;
                    }
                    else if(actionValue === "m"){
                        action = 30 + Math.random()*3;
                    }
                    else if(actionValue === "t"){
                        action = 30 + Math.random()*3;
                    }
                    else if(actionValue === "o"){
                        action = 10 + Math.random()*3;
                    }
                    //Effect value
                    tmp[scopes[x]] = tmp[n];
                    tmp[n] = 0;
                    for(var y = 0; y < 64; y++){
                        if("otmvlw".indexOf(values[y]) >= 0){
                            var tmpScp = checkBlack(y,tmp) || [];
                            for(var z = 0; z < tmpScp.length; z++){
                                var effectValue = tmp[tmpScp[z]];
                                if(effectValue == "k"){
                                    if(effect < 100){
                                        effect = 100;
                                    }
                                }
                                else if(effectValue == "q"){
                                    if(effect < 50){
                                        effect = 50;
                                    }
                                }
                                else if(effectValue == "b"){
                                    if(effect < 50){
                                        effect = 50;
                                    }
                                }
                                else if(effectValue == "n"){
                                    if(effect < 30){
                                        effect = 30;
                                    }
                                }
                                else if(effectValue == "r"){
                                    if(effect < 30){
                                        effect = 30;
                                    }
                                }
                                else if(effectValue == "p"){
                                    if(effect < 10){
                                        effect = 10;
                                    }
                                }
                            }
                        }
                    }




                    actions.push(action);
                    effects.push(effect);
                    approved.push(n+"-"+scopes[x]);
                }
            }
        }

        //alert(actions);

        var bestEffect = Math.min.apply(null,effects);
        //alert(bestEffect);
        if(bestEffect >= 100){
            alert("You Win");
            setTimeout(function(){
                values = ['r','n','b','q','k','b','n','r','p','p','p','p','p','p','p','p',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'o','o','o','o','o','o','o','o','t','m','v','w','l','v','m','t'];
        },10);
        }

        var tmpA = [];
        var tmpB = [];
        var tmpC = [];
        var bestMove = "";

        for(var n = 0; n < effects.length; n++){
            if(effects[n] === bestEffect){
                tmpA.push(actions[n]);
                tmpB.push(approved[n]);
                tmpC.push(effects[n]);
            }
        }
        bestMove = tmpB[tmpA.indexOf(Math.max.apply(null,tmpA))];

        
        if(bestMove){
            // update_web();
            if (!one_player_game){
                //var req = get_move();
                while (!get_move()){
                    var req = get_last_move();
                    var start_pos = 8 * (parseInt(req[1]) - 1) + (parseInt(req[2]) - 1);
                    var last_pos = 8 * (parseInt(req[4]) - 1) + (parseInt(req[5]) - 1);
                    values[last_pos] = values[start_pos] 
                    values[start_pos] = 0
                    sleep(100);
                }
            }
            else{
                ////////////////////////////////////////////////////////////////////////////////////////////
                add_move(
                    String(1+parseInt(Number(bestMove.split("-")[0])%8))+ 
                    String(1+parseInt(Number(bestMove.split("-")[0])/8)) + 
                    "-"+
                    String(1+parseInt(Number(bestMove.split("-")[1])%8)) + 
                    String(1+parseInt(Number(bestMove.split("-")[1])/8)));
                
                values[Number(bestMove.split("-")[1])] = values[Number(bestMove.split("-")[0])];
                values[Number(bestMove.split("-")[0])] = 0;
                if(values[Number(bestMove.split("-")[1])] === "p" && Number(bestMove.split("-")[1]) >= 56){
                    values[Number(bestMove.split("-")[1])] = "q";
                }
                sqs[bestMove.split("-")[1]].style.background = '#aaf';
                sqs[bestMove.split("-")[0]].style.background = '#aaf';
            }
            for(var x = 0; x < 64; x++){
                //sqs[x].style.background = "#afa"//classList.add("scope");
                sqs[x].innerHTML = fonts[values[x]];
                if(values[x] === 0){
                    sqs[x].innerHTML = "";
                }
            }
            myTurn = true
            update_web();
        }
        else {
            //alert('You Win');
        }
    }
                        
}
//chooseTurn();
