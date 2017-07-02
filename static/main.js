var app = app || {};

app.init = function(url) {
    app.dataHandler.createData(url);
    app.events.attachVoteButtonListener();
    app.events.clickOnVoteStatistic();
    app.events.hideModal();
};

app.init("http://swapi.co/api/planets/");