/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// start the 'control server' first, on port 8000, it will provide
// the test options, as well as receive test results, use:
// control-server/run_raptor_control_server.py

// note: currently the prototype assumes the test page(s) are
// already available somewhere independently; so for now locally
// inside the 'talos-pagesets' dir or 'heros' dir (tarek's github
// repo) or 'webkit/PerformanceTests' dir (for benchmarks) first run:
// 'python -m SimpleHTTPServer 8081'
// to serve out the pages that we want to prototype with. Also
// update the manifest content 'matches' accordingly

var testType;
var pageCycles = 0;
var pageCycle = 0;
var pageCycleDelay = 1000;
var testURL;
var testTabID = 0;
var results = {'page': '', 'measurements': {}};
var getHero = false;
var getFCP = false; // first contentful paint (google)
var isHeroPending = false;
var pendingHeroes = [];
var settings = {};
var isFCPPending = false;
var isBenchmarkPending = false;

// for prototype, choose appropriate settings file
var settingsURL = 'http://localhost:8000/raptor-chrome-tp7.json'
// var settingsURL = 'http://localhost:8000/raptor-speedometer.json'

function getTestSettings() {
  console.log("getting test settings from control server");
  return new Promise(resolve => {

    fetch(settingsURL).then(function(response) {
      response.text().then(function(text) {
        console.log(text);
        settings = JSON.parse(text)['raptor-options'];

        // parse the test settings
        testType = settings['type'];
        pageCycles = settings['page_cycles'];
        testURL = settings['test_url'];
        results['page'] = testURL;
        results['type'] = testType;

        if (testType == 'tp7') {
          getFCP = settings['measure']['fcp'];
          if (settings['measure']['hero'].length !== 0) {
            getHero = true;
          }
        }

        // write options to storage that our content script needs to know
        chrome.storage.local.clear(function() {
          chrome.storage.local.set({settings}, function(){
            resolve();
          });
        });
      });
    });
  });
}

function getBrowserInfo() {
  return new Promise(resolve => {
    results['browser'] = "Chrome";
    var browserInfo = window.navigator.userAgent.split(' ');
    for (x in browserInfo) {
      if (browserInfo[x].indexOf('Chrome') > -1) {
        results['browser'] = browserInfo[x];
        break;
      }
    }
    console.log('testing on ' + results['browser']);
    resolve();
  });
}

function testTabCreated(tab){
  testTabID = tab.id;
  console.log("opened new empty tab " + testTabID);
  nextCycle();
}

async function testTabUpdated(tab) {
  console.log('tab ' + tab.id + ' reloaded');
  // wait for pageload test result from content
  await waitForResult();
  // move on to next cycle (or test complete)
  nextCycle();
}

function waitForResult() {
  console.log("awaiting results...");
  return new Promise(resolve => {
    function checkForResult() {
      if (testType == 'tp7') {
        if (!isHeroPending && !isFCPPending) {
          resolve();
        } else {
          setTimeout(checkForResult, 5);
        }
      } else if (testType == 'benchmark') {
        if (!isBenchmarkPending) {
          resolve();
        } else {
          setTimeout(checkForResult, 5);
        }
      }
    }
    checkForResult();
  });
}

function nextCycle() {
  pageCycle++;
  if (pageCycle <= pageCycles) {
    setTimeout(function(){
      console.log("\nbegin pagecycle " + pageCycle);
      if (testType == 'tp7') {
        if (getHero)
          isHeroPending = true;
          pendingHeroes = Array.from(settings['measure']['hero']);
        if (getFCP)
          isFCPPending = true;
      } else if (testType == 'benchmark') {
        isBenchmarkPending = true;
      }
      // reload the test page
      chrome.tabs.update(testTabID, {url:testURL}, testTabUpdated);
    }, pageCycleDelay);
  } else {
    verifyResults();
  }
}

function resultListener(request, sender, sendResponse) {
  console.log("received message from " + sender.tab.url);
  if (request.type && request.value) {
    console.log("result: " + request.type + " " + request.value);
    sendResponse({text: "confirmed " + request.type});

    if (!(request.type in results['measurements']))
      results['measurements'][request.type] = [];

    if (testType == 'tp7') {
      // a single tp7 pageload measurement was received
      if (request.type.indexOf("hero") > -1) {
        results['measurements'][request.type].push(request.value);
        var _found = request.type.split('hero:')[1];
        var index = pendingHeroes.indexOf(_found);
        if (index > -1) {
          pendingHeroes.splice(index, 1);
          if (pendingHeroes.length == 0) {
            console.log("measured all expected hero elements");
            isHeroPending = false;
          }
        }
      } else if (request.type == 'fcp') {
        results['measurements']['fcp'].push(request.value);
        isFCPPending = false;
      }
    } else if (testType == 'benchmark') {
      // benchmark results received (all results for that complete benchmark run)
      console.log('received results from benchmark');
      results['measurements'][request.type].push(request.value);
      isBenchmarkPending = false;
    }
  } else {
    console.log("unknown message received from content: " + request);
  }
}

function verifyResults() {
  console.log("\nVerifying results:");
  console.log(results);
  for (var x in results['measurements']) {
    count = results['measurements'][x].length;
    if (count == pageCycles) {
      console.log('have ' + count + ' results for ' + x + ', as expected');
    } else {
      console.log('ERROR: expected ' + pageCycles + ' results for '
                  + x + ' but only have ' + count);
    }
  }
  postResults();
}

function postResults() {
  // requires 'control server' running at port 8000 to receive results
  // run utils/run_local_control_server.py
  var url = "http://127.0.0.1:8000/";
  var client = new XMLHttpRequest();
  client.onreadystatechange = function() {
    if (client.readyState == XMLHttpRequest.DONE && client.status == 200) {
      console.log("post success");
    }
  }

  client.open("POST", url, true);

  client.setRequestHeader("Content-Type", "application/json");
  if (client.readyState == 1) {
    console.log("posting results...");
    client.send(JSON.stringify(results));
  }
  cleanUp();
}

function cleanUp() {
  // close tab
  chrome.tabs.remove(testTabID);
  console.log("closed tab " + testTabID);
  if (testType == 'tp7') {
    // remove listeners
    chrome.runtime.onMessage.removeListener(resultListener);
    chrome.tabs.onCreated.removeListener(testTabCreated);
    console.log("pageloader test finished");
  } else if (testType == 'benchmark'){
    console.log('benchmark complete');
  }
  window.onload = null;
  // done
  return;
}

function runner() {
  getBrowserInfo().then(function() {
    getTestSettings().then(function() {
      if (testType == 'benchmark') {
        // webkit benchmark type of test
        console.log('benchmark test start');
      } else if (testType == 'tp7') {
        // standard 'tp7' pageload test
        console.log("pageloader test start");
      }
      // results listener
      chrome.runtime.onMessage.addListener(resultListener);
      // tab creation listener
      chrome.tabs.onCreated.addListener(testTabCreated);
      // create new empty tab, which starts the test
      chrome.tabs.create({url:"about:blank"});
    });
  });
}

window.onload = runner();
