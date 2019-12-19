// This example requires the Visualization library. Include the libraries=visualization
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=visualization">
function updateTextInput(val) {
    document.getElementById('textInput').value = val + '%';
}

function get_distance_weight(val) {
    document.getElementById('distance_weight_input').value = val + '%';
    window.distance_weight = val/3000;
}

function get_duration_weight(val) {
    document.getElementById('duration_weight_input').value = val + '%';
    window.duration_weight = val/3000;
}

function get_score_weight(val) {
    document.getElementById('score_weight_input').value = val + '%';
    window.score_weight = val/3000;
}

function initMap() {
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: {lat: 41.872070, lng: -87.624302}
    });

    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('right-panel'));
    window.xdirectionsDisplay = directionsDisplay;


    var elmSubmitButton = document.getElementById('submit');

    elmSubmitButton.addEventListener('click', function () {
        calculateRoute(elmSubmitButton);
        toggle_divs();
    });
    function toggle_divs() {
      var weightsDiv = document.getElementById("weights");
      var submitDiv = document.getElementById("submit");
      var startOverDiv = document.getElementById("start-over");
        weightsDiv.style.display = "none";
        startOverDiv.style.display = "block";
    }
    var control = document.getElementById('floating-panel');

    control.style.display = 'block';
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);

    function calculateRoute(elmSubmitButton, selectedRouteIndex = 0) {
        var request = {
            origin: document.getElementById('start').value,
            destination: document.getElementById('end').value,
            travelMode: google.maps.DirectionsTravelMode.DRIVING,
            unitSystem: google.maps.UnitSystem.METRIC,
            provideRouteAlternatives: true
        };

        directionsService.route(request, function (result, status) {
            if (status === google.maps.DirectionsStatus.OK) {
                if (selectedRouteIndex === 0) {
                    directionsDisplay.setDirections(result);
                }

                var routes = result['routes'];

                var allRoutes = routes.map(function (route) {
                    return route.overview_polyline;
                });
                var allDistance = routes.map(function (route) {
                    return route.legs[0] ? route.legs[0].distance.value : 0;
                });
                var allDuration = routes.map(function (route) {
                    return route.legs[0] ? route.legs[0].duration.value : 0;
                });
                var allRoutesDecoded = allRoutes.map(function (encodedRoute) {
                    return decodePolyline(encodedRoute);
                });

                var buffer_input = parseFloat(document.getElementById("buffer_input").value) / 4000;
                var elmToken = document.querySelector('#csrf-token');

                $.ajax({
                    headers: {
                        "X-CSRFToken": elmToken.value
                    },
                    url: "/get_data/",
                    type: "POST",
                    contentType: 'application/json',
                    data: JSON.stringify({
                        routes: allRoutesDecoded,
                        buffer_input: buffer_input
                    }),
                    cache: false,
                    dataType: 'json',
                    timeout: 5000,
                    success: function (data) {
                        var heatmap_data = [];

                        Array.from(data[selectedRouteIndex]).forEach(function (heatMapData) {
                            heatmap_data.push({
                                location: new google.maps.LatLng(heatMapData[1], heatMapData[2]),
                                weight: heatMapData[3]
                            });
                        });

                        var crimeScoreAvgList = Array.from(data).map(function (dataList, index) {
                            var duration = allDuration[index];
                            var distance = allDistance[index];
                            var scoreList = Array.from(dataList).map(function (row) {
                                return row[3];
                            });

                            var scoreSum = scoreList.reduce(function (a, b) {
                                return a + b;
                            }, 0);

                            var wDistance = window.duration_weight ? window.duration_weight : 0.0029;
                            var wDuration = window.distance_weight ? window.distance_weight : 0.0030;
                            var wThreatScore = window.score_weight ? window.score_weight : 0.041;

                            var scoreAvg = scoreSum / scoreList.length;
                            var result = (wDuration * duration + wDistance * distance + wThreatScore * scoreAvg);
                            return result;
                        });

                        if (elmSubmitButton.heatmap) {
                            elmSubmitButton.heatmap.setMap(null);
                        }

                        elmSubmitButton.heatmap = new google.maps.visualization.HeatmapLayer({
                            data: heatmap_data,
                            map: map,
                            radius: 24,
                            max_intensity: 200
                        });

                        document.getElementById('toggleHeatmap').onclick = function () {
                            toggleHeatmap(elmSubmitButton.heatmap);
                        };
                        document.getElementById('changeGradient').onclick = function () {
                            changeGradient(elmSubmitButton.heatmap);
                        };
                        document.getElementById('changeRadius').onclick = function () {
                            changeRadius(elmSubmitButton.heatmap);
                        };
                        document.getElementById('changeOpacity').onclick = function () {
                            changeOpacity(elmSubmitButton.heatmap);
                        };

                        if (selectedRouteIndex === 0) {
                            var elmRightPanel = document.querySelector('#right-panel');
                            var suggestedRouteList = Array.from(elmRightPanel.querySelectorAll('[jsaction="directionsRouteList.selectRoute"]'));
                            var elmCustomDataList = Array.from(elmRightPanel.querySelectorAll('.custom-data'));
                            elmCustomDataList.map(function (elm) {
                                elm.remove();
                            });

                            suggestedRouteList.map(function (elm) {
                                var routeIndex = elm.dataset.routeIndex;

                                if (!elm.eventBinded) {
                                    elm.addEventListener('click', function (e) {
                                        calculateRoute(elmSubmitButton, routeIndex);
                                    });
                                    elm.eventBinded = true;
                                }

                                var elmCustomData = document.createElement('span');
                                elmCustomData.classList.add('custom-data');

                                /*                                var elmDistance = document.createElement('span');
                                                                elmDistance.innerText = allDistance[routeIndex];
                                                                elmDistance.style.border = '1px solid red';
                                                                elmDistance.style.marginLeft = '12px';
                                                                elmCustomData.appendChild(elmDistance);

                                                                var elmDuration = document.createElement('br');
                                                                elmDuration.innerText = allDuration[routeIndex];
                                                                elmDuration.style.border = '1px solid blue';
                                                                elmDuration.style.marginLeft = '12px';
                                                                elmCustomData.appendChild(elmDuration);*/

                                var elmBR = document.createElement('br');
                                elmCustomData.appendChild(elmBR);

                                var elmScore = document.createElement('span');
                                elmScore.innerText = crimeScoreAvgList[routeIndex].toFixed(2);
                                elmScore.style.border = '2px solid orange';
                                elmScore.style.marginLeft = '14px';
                                elmCustomData.appendChild(elmScore);

                                elm.appendChild(elmCustomData);
                            });
                        }
                    },
                    error: function (jqXhr, textStatus, errorMessage) { // error callback
                        console.log('Error: ' + errorMessage);
                    }
                });


            }
        });


    }

    function decodePolyline(encoded) {
        if (!encoded) {
            return [];
        }
        var poly = [];
        var index = 0, len = encoded.length;
        var lat = 0, lng = 0;

        while (index < len) {
            var b, shift = 0, result = 0;

            do {
                b = encoded.charCodeAt(index++) - 63;
                result = result | ((b & 0x1f) << shift);
                shift += 5;
            } while (b >= 0x20);

            var dlat = (result & 1) != 0 ? ~(result >> 1) : (result >> 1);
            lat += dlat;

            shift = 0;
            result = 0;

            do {
                b = encoded.charCodeAt(index++) - 63;
                result = result | ((b & 0x1f) << shift);
                shift += 5;
            } while (b >= 0x20);

            var dlng = (result & 1) != 0 ? ~(result >> 1) : (result >> 1);
            lng += dlng;

            var p = {
                latitude: lat / 1e5,
                longitude: lng / 1e5,
            };
            poly.push(p);
        }
        return poly;
    }

    function toggleHeatmap(heatmap) {
        heatmap.setMap(heatmap.getMap() ? null : map);
    }

    function changeGradient(heatmap) {
        var gradient = [
            'rgba(0, 255, 255, 0)',
            'rgba(0, 255, 255, 1)',
            'rgba(0, 191, 255, 1)',
            'rgba(0, 127, 255, 1)',
            'rgba(0, 63, 255, 1)',
            'rgba(0, 0, 255, 1)',
            'rgba(0, 0, 223, 1)',
            'rgba(0, 0, 191, 1)',
            'rgba(0, 0, 159, 1)',
            'rgba(0, 0, 127, 1)',
            'rgba(63, 0, 91, 1)',
            'rgba(127, 0, 63, 1)',
            'rgba(191, 0, 31, 1)',
            'rgba(255, 0, 0, 1)'
        ]
        heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
    }

    function changeRadius(heatmap) {
        heatmap.set('radius', heatmap.get('radius') === 40 ? 18 : 40);
    }

    function changeOpacity(heatmap) {
        heatmap.set('opacity', heatmap.get('opacity') ? null : 0.4);
    }
}
