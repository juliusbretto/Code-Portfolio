let request = false;

//window is a JS global object representing the browser window
//checks if the browser supports the XMLhttprequest, meaning updating the window asynchronously
if (window.XMLHttpRequest) { 
	  request = new XMLHttpRequest();
} else if (window && window.ActiveXObject) { //microsoft edge
	  request = new ActiveXObject("Microsoft.XMLHTTP");
	}

function endOtherSessions() {
	if (request) {
		request.open("GET", "endOtherSessions"); //opens a GET request to url endOtherSessions
		
		request.onreadeystatechange = function handleRequestStateChange() {
		//handleRequestStateChange, event handler function that handles changes in the request
			
			//if the request is completed (4) and response status is OK
			if (request.readyState === 4 && request.status === 200) { 
				document.getElementById("endSessions").style.visibility = "hidden"; //the endSessions-button is hidden
			}
		};
		//otherwise, send nothing
		request.send(null);
	}
}

module.exports = endOtherSessions;