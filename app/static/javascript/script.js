// sidebar dropdown menu
const btn = document.getElementById("btn");
const arrowIcon = document.getElementById("arrow")
const dropdown = document.getElementById("dropdown");
const dropdownMenu = document.getElementById("dropdown-menu");

// navbar 
const btnNav = document.getElementById("btn-nav");
const arrowIconNav = document.getElementById("arrow-nav");
const dropdownNav = document.getElementById("dropdown-nav");


// ini digunakan untuk menambahkan class fa-arrow-up atau fa-arrow-down
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
        document.getElementById("dropdown-menu").style.backgroundColor = "rgb(217 217 217 / 40%)";
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

// sidebar mark
function getCurrentURL() {
    return window.location.href;
}

const url = getCurrentURL();
console.log(url);

// http://127.0.0.1:5000/land_predict/result-manual-data/dt/%5B%7B%22area%22:%22Ciawi%22,%22hum%22:55.4,%22soil_nitro1%22:22.0,%22soil_phos1%22:98.0,%22soil_pot1%22:90.0,%22soil_temp1%22:25.3,%22soil_ph1%22:5.5,%22temp%22:29.7,%22id_m%22:39%7D,%7B%22area%22:%22Rajapolah%22,%22hum%22:56.2,%22soil_nitro1%22:22.0,%22soil_phos1%22:98.0,%22soil_pot1%22:91.0,%22soil_temp1%22:25.4,%22soil_ph1%22:5.6,%22temp%22:29.3,%22id_m%22:38%7D,%7B%22area%22:%22Nanggeleng%22,%22hum%22:54.9,%22soil_nitro1%22:22.0,%22soil_phos1%22:98.0,%22soil_pot1%22:90.0,%22soil_temp1%22:25.3,%22soil_ph1%22:5.6,%22temp%22:29.6,%22id_m%22:37%7D,%7B%22area%22:%22Kolab%22,%22hum%22:60.0,%22soil_nitro1%22:200.0,%22soil_phos1%22:90.0,%22soil_pot1%22:100.0,%22soil_temp1%22:28.0,%22soil_ph1%22:5.7,%22temp%22:28.0,%22id_m%22:36%7D,%7B%22area%22:%22Warming%20up%22,%22hum%22:60.0,%22soil_nitro1%22:200.0,%22soil_phos1%22:90.0,%22soil_pot1%22:100.0,%22soil_temp1%22:28.0,%22soil_ph1%22:5.7,%22temp%22:28.0,%22id_m%22:35%7D,%7B%22area%22:%22Nanggeleng%22,%22hum%22:60.0,%22soil_nitro1%22:200.0,%22soil_phos1%22:98.0,%22soil_pot1%22:100.0,%22soil_temp1%22:28.0,%22soil_ph1%22:5.7,%22temp%22:28.0,%22id_m%22:33%7D,%7B%22area%22:%22Nagrog%22,%22hum%22:56.8,%22soil_nitro1%22:22.0,%22soil_phos1%22:97.0,%22soil_pot1%22:90.0,%22soil_temp1%22:25.1,%22soil_ph1%22:5.6,%22temp%22:29.1,%22id_m%22:32%7D,%7B%22area%22:%22Telkom%20University%22,%22hum%22:60.0,%22soil_nitro1%22:200.0,%22soil_phos1%22:90.0,%22soil_pot1%22:100.0,%22soil_temp1%22:28.0,%22soil_ph1%22:5.8,%22temp%22:28.0,%22id_m%22:31%7D%5D
// itu url yang didapatkan, jika didalam url terdapat kata "manual-data" maka sidebar akan menampilkan mark pada menu "Manual Data"
if (url.includes("manual-data")) {
    path = document.getElementById("manual-data").classList.add("mark");
    console.log(path)
} else if (url.includes("dataset")) {
    path = document.getElementById("dataset").classList.add("mark");
    console.log(path)
} else if (url.includes("dashboard")) {
    path = document.getElementById("dashboard").classList.add("mark");
    console.log(path)
} else if (url.includes("real-time")) {
    path = document.getElementById("real-time").classList.add("mark");
    console.log(path)
} else{
    console.log("notfound")
}