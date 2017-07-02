var app = app || {}

app.events = {
    addEventsToButtons: function (url) {
        var $table;

        $table = $('#table');
        $table.on('click', 'button.residents-button', function () {
            var $button = $(this),
                $tr = $button.parents('tr');

            app.events.showResident(app.dataHandler.planets[$tr.attr('data-id')]);
        });

    },

    showResident: function (planet) {
        var residentString = "<tr>",
            residents = planet.residents,
            keyOfPeopleData = [
                "name",
                "height",
                "mass",
                "hair_color",
                "skin_color",
                "eye_color",
                "birth_year",
                "gender"
            ],
            urlOfResident,
            keyOfPerson,
            residentsDiv,
            listOfPromise = [];

        for (var i = 0; i < keyOfPeopleData.length; i++) {
            residentString += "<th>" + keyOfPeopleData[i] + "</th>";
        }
        residentString += "<tr>"
        for (var i = 0; i < residents.length; i++) {
            listOfPromise.push($.get(residents[i]));
        }
        $.when.apply($, listOfPromise).done(function () {
            var responses = Array.prototype.slice.call(arguments, 0),
                i = 0,
                length;

            if (listOfPromise.length === 1) {
                responses = [responses];
            }
            responses.forEach(function (response) {
                residentString += "<tr>";
                keyOfPeopleData.forEach(function (key) {
                    residentString += "<td>" + response[0][key] + "</td>";
                });
                residentString += "</tr>";

            });
            var modalContent = document.getElementById("modal-content");
            modalContent.innerHTML = "<table border='1'>" + residentString + "</table>";
            modal = document.getElementById("modal");
            modal.style.display = "block";
        });


    },
    changePage: function () {
        var nextUrl = app.dataHandler.data.next,
            previousUrl = app.dataHandler.data.previous,
            nextButton,
            previousButton;

        if (nextUrl !== null) {
            nextButton = document.getElementById("next-button");
            nextButton.addEventListener('click', function () {
                app.dataHandler.createData(nextUrl);
            })
        };
        if (previousUrl !== null) {
            previousButton = document.getElementById("previous-button");
            previousButton.addEventListener('click', function () {
                app.dataHandler.createData(previousUrl);
            })
        };



    },
    attachVoteButtonListener: function () {
        var $table;

        $table = $('#table');
        $table.on('click', 'button.vote', function () {
            var $button = $(this),
                $tr = $button.parents('tr'),
                name,
                hasClass,
                planetId,
                valami;

            planetId = app.dataHandler.planets[$tr.attr('data-id')].id;
            planetName = app.dataHandler.planets[$tr.attr('data-id')].name;
            hasClass = $tr.hasClass('voted');


            var change_sql = '/planet/vote';
            if (hasClass) {
                $.post(change_sql, { planet: planetName, planetId: planetId, addVote: 0 }).done(function () {
                    $tr.removeClass('voted');
                });
            } else {
                $.post(change_sql, { planet: planetName, planetId: planetId, addVote: 1 }).done(function () {
                    $tr.addClass("voted");
                });
            }

        });

    },
    clickOnVoteStatistic: function () {
        var voteStatisticButton = document.getElementById("vote-statistic");
        voteStatisticButton.addEventListener('click', function () {
            $.post("/vote_statistic").done(function (data) {
                var statisticString = "<table border='1'>",
                    modal,
                    modalContent,
                    dataObject;
                dataObject = JSON.parse(data);
                for (var i = 0; i < dataObject.length; i++) {
                    console.log(dataObject[i][0]);
                    statisticString += "<tr><td>" + dataObject[i][0] + "</td><td>" + dataObject[i][1] + "</td></tr>"
                }
                statisticString += "</table>";
                modalContent = document.getElementById("modal-content");
                modalContent.innerHTML = statisticString;
                modal = document.getElementById("modal");
                modal.style.display = "block";
            });

        });
    },
    hideModal: function () {
        var $modal = $("#modal");

        $modal.on('click', 'button.close', function () {
            $modal.css('display', 'none');
        });




    }

};
