

function changeMyText() {
	var request = new XMLHttpRequest();
	request.open("GET", "changeParagraph?text=fromlinkedjs");
	request.send();
	request.onreadystatechange = function() {
		if(this.readyState === 4 && this.status === 200) {
			document.getElementById("par_1").innerHTML = this.responseText;
		}
	}
}

function changeMyText2() {
	var request = new XMLHttpRequest();
	request.open("GET", 
		"changeParagraph?text=Text+from+client+to+server+to+client.");
	request.send();
	request.onreadystatechange = function() {
		if(this.readyState === 4 && this.status === 200) {
			document.getElementById("par_1").innerHTML = this.responseText;
		}
	}
}

function changeMyText3() {
	var request = new XMLHttpRequest();
	request.open("GET", "changeParagraph?text=array");
	request.send();
	request.onreadystatechange = function() {
		if(this.readyState === 4 && this.status === 200) {
			var lst = JSON.parse(this.responseText);
			for (i = 0; i < lst.length; i++) {
				document.getElementById(lst[i][0]).innerHTML = lst[i][1];
			}
		}
	}
}
