
function changeCss() {
	document.getElementById("styleBright").href = "style2.css";
	document.getElementById("switcher").innerHTML = "Светлая тема";
	document.getElementById("switcher").onclick = changeCssToDefault;
}

function changeCssToDefault() {
    document.getElementById("styleBright").href = "style.css";
    document.getElementById("switcher").innerHTML = "Темная тема";
    document.getElementById("switcher").onclick = changeCss;
}
