var app = app || {};

app.dataHandler = {
    createData: function (url) {
        $.when.apply($, [$.get(url), $.get('/get_current_user_votes')]).done(function (first, second) {
            var data = first[0],
                voted_ids = second[0];

            app.dataHandler.voted_ids = voted_ids
            app.dataHandler.planets = data.results.map(app.dataHandler.mapPlanet, app.dataHandler);
            app.dataHandler.data = data;
            app.dataHandler.createTable(url);
            app.dom.addButton();
            app.events.changePage();

        });
    },
    mapPlanet: function (planet) {
        planet.id = this.getIdByUrl(planet.url);
        return planet
    },
    getIdByUrl: function (url) {
        return parseInt(url.split("/")[5], 10);
    },
    createTable: function (url) {
        var dataAboutThePlanets = [
            "name",
            "diameter",
            "climate",
            "terrain",
            "surface_water",
            "population",
            "residents"
        ],
            tableString = "<tr>",
            planetsREsults,
            key,
            nextButton,
            previousButton,
            user;

        planetsREsults = app.dataHandler.planets;
        for (var i = 0; i < dataAboutThePlanets.length; i++) {
            tableString += "<th>" + dataAboutThePlanets[i] + "</th>";
        }
        tableString += "</tr>";
        for (var i = 0; i < planetsREsults.length; i++) {
            if (app.dataHandler.voted_ids.indexOf(planetsREsults[i]["name"]) !== -1) {
                tableString += "<tr class='voted' data-id='" + i + "'>";
            } else {

                tableString += "<tr data-id='" + i + "'>";
            }
            for (var j = 0; j < dataAboutThePlanets.length; j++) {
                key = dataAboutThePlanets[j];

                if (key === "residents") {
                    if (planetsREsults[i][key].length !== 0) {
                        if (planetsREsults[i][key].length === 1) {

                            tableString += " <td><button class='residents-button'> 1 Resident</button></td>";
                        } else {
                            tableString += " <td><button class='residents-button'>" + planetsREsults[i][key].length + " Residents</button></td>";
                        }
                    } else {
                        tableString += "<td>No known residents</td>";
                    }

                } else {
                    tableString += "<td>" + planetsREsults[i][key];

                    if (dataAboutThePlanets[j] === "diameter") {
                        tableString += " km";
                    } else if (dataAboutThePlanets[j] === "surface_water") {
                        tableString += " %";

                    } else if (dataAboutThePlanets[j] === "population") {
                        tableString += " population";
                    }
                    tableString += "</td>";
                }
            }
            user = document.getElementById("user").innerText
            if (user) {
                tableString += '<td><button class="vote">Vote</button></td>'

            }

            tableString += "</tr>"
        };
        document.getElementById("table").innerHTML = tableString;
        app.events.addEventsToButtons(url);

    }

};