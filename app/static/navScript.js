
    /* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
    function myFunction() {
        var x = document.getElementById("myTopnav");
        var previous_pallete= x.className;
        previous_pallete= previous_pallete.replace("responsive",'');
        previous_pallete= previous_pallete.slice(0, -1);
        if ((x.className === "indigo_pink topnav")||(x.className ===  "dark_grey topnav")||(x.className === "pink_blue_grey topnav")) {
          x.className += " responsive";
        }
        else{
          x.className = previous_pallete;
        }
      }