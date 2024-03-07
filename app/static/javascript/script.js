console.log("Hello World from script.js!");
// sidebar dropdown menu
const btn = document.getElementById("btn");
const arrowIcon = document.getElementById("arrow")
const dropdown = document.getElementById("dropdown");
const dropdownMenu = document.getElementById("dropdown-menu");

// navbar 
const btnNav = document.getElementById("btn-nav");
const arrowIconNav = document.getElementById("arrow-nav");
const dropdownNav = document.getElementById("dropdown-nav");



const arrowToggle = (x) => {
    x.classList.toggle("fa-arrow-up");

    if (x.classList.contains("fa-arrow-up")) {
        x.classList.remove("fa-arrow-down");
    } else {
        x.classList.add("fa-arrow-down");
    }   
}

const dropdownToggle = (x) => {
    x.classList.toggle("dropdown-content-show");
    // jika dropdown-content-show tidak ada, maka tambahkan class dropdown-content
    // jika dropdown-content-show ada, maka hilangkan class dropdown-content
    if (x.classList.contains("dropdown-content-show")) {
        x.classList.remove("dropdown-content");
    } else {
        x.classList.add("dropdown-content");
    }
    
}

// sidebar
btn.addEventListener("click", (e) => {
    e.preventDefault();
    dropdownToggle(dropdown);
    arrowToggle(arrowIcon);
    // jika dropdown-content-show ada, maka ganti warna background dropdown-menu
    if (dropdown.classList.contains("dropdown-content-show")) {
        document.getElementById("dropdown-menu").style.backgroundColor = "rgb(217 217 217 / 40%)";
    } else {
        document.getElementById("dropdown-menu").style.backgroundColor = "#41644A";
    }
    console.log(arrowIcon)  

});


// navbar 
btnNav.addEventListener("click", (e) => {
    e.preventDefault();
    dropdownToggle(dropdownNav);
    arrowToggle(arrowIconNav);
    console.log(arrowIcon)

}
);

