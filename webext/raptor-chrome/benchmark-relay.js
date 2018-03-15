// receives result from benchmark and relays onto our background runner

function receiveMessage(event) {
  console.log('received message!');
  console.log(event.origin);
  if (event.origin == 'http://localhost:8081') {
    sendResult("speedometer", event.data);
  }
}

function sendResult(_type, _value) {
  // send result back to background runner script
  console.log("sending result back to runner: " + _type + " " + _value);
  chrome.runtime.sendMessage({"type": _type, "value": _value}, function(response) {
    console.log(response.text);
  });
}

window.addEventListener("message", receiveMessage, false);
