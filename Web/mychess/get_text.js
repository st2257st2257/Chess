function create() {
    //var pass = document.getElementById('103').innerHTML;
    var name = localStorage.getItem("name");
    var namee = sessionStorage.getItem("name");    
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("div_text").innerHTML = this.responseText;
        }
    };
    if (localStorage.getItem("name")==null){
        window.open("http://mychess.xyz/Signin", "_self");
    }
    else{
        xmlhttp.open("GET","http://mychess.xyz/PHP/create_party_get.php?white=" + String(name) 
        + "&black=wait&time=5",true);
        xmlhttp.send();
    }
}
create();
