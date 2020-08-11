// Gets last value entered in form
function getLast() {
    var last = document.querySelector("#subreddit").value;
    var key = "result";

    localStorage.setItem(key, last);
}


// Pops input with last entry. Blank otherwise.
function popLast() {
    last = localStorage.getItem("result")
    if (last === null) {
        last = '';
    }
    document.querySelector("#inputfield").innerHTML = '<input type="text" list="subreddits" name="subreddit" id="subreddit" value=' + '\"' + last + '\">'
}

window.onload = popLast();