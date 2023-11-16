const button = document.getElementById("toggle")
const nodeElement = document.getElementById("stylesheet")
const mode = localStorage.getItem("mode")

window.addEventListener("load", ()=> {
    if (mode === "dark") {
        nodeElement.setAttribute("href", "/main.dark.css");
    }
    button.addEventListener("click", toggle_style);
})


function toggle_style() {
    if (nodeElement.getAttribute("href") === "/main.css") {
        nodeElement.setAttribute("href", "/main.dark.css");
        localStorage.setItem("mode", "dark")
    } else {
        nodeElement.setAttribute("href", "/main.css");
        localStorage.setItem("mode", "main");
        localStorage.removeItem
    }

}

