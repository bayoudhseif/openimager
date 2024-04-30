function addClass(component, className) {
    var e = document.getElementById(component);
    e.removeAttribute("class");
    e.classList.add(className);
}


// first transition by default
var btn = document.getElementsByTagName("button");
btn[0].classList.add("active");
value = btn[0].innerText;
addClass("component", value);