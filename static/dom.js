var app = app || {};

app.dom = {
    addButton: function () {
        var buttonDiv = document.getElementById("button-div"),
            buttonString = "";
        if (app.dataHandler.data.previous !== null) {
            buttonString += "<button id='previous-button'> Previous page </button>";
        };
        if (app.dataHandler.data.next !== null) {
            buttonString += "<button id='next-button'> Next page </button>";
        };
        buttonDiv.innerHTML = buttonString;
    }


};