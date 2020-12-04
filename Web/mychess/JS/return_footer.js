function showUser() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("footer").innerHTML = this.responseText;
        }
    };
    console.log("http://mychess.xyz/PHP/return_footer.php?q=1");
    xmlhttp.open("GET","http://mychess.xyz/PHP/return_footer.php?q=1",true);
    xmlhttp.send();
}
showUser();
