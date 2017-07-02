var app = app || {};

app.init = function(url) {
    app.dataHandler.createData(url);
    app.events.hideModal();
    app.events.attachVoteButtonListener();
    app.events.clickOnVoteStatistic();
};

app.init("http://swapi.co/api/planets/");