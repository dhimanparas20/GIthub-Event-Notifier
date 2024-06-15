$(document).ready(function() {
    function fetchData() {
        $.ajax({
            url: '/api/events',
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                let eventsContainer = $('#events');
                eventsContainer.empty();

                if (data.error) {
                    eventsContainer.html(`<p>Error: ${data.error}</p>`);
                    return;
                }

                data.forEach((event, index) => {
                    let eventDiv = $('<div>').addClass('event');
                    let eventContent;

                    if (event.action === "PUSH") {
                        eventContent = `<p><strong>${event.author}</strong> pushed to <strong>${event.to_branch}</strong> on <strong>${event.timestamp}</strong></p>`;
                    } else if (event.action === "PULL_REQUEST") {
                        eventContent = `<p><strong>${event.author}</strong> submitted a pull request from <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong> on <strong>${event.timestamp}</strong></p>`;
                    } else if (event.action === "MERGE") {
                        eventContent = `<p><strong>${event.author}</strong> merged branch <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong> on <strong>${event.timestamp}</strong></p>`;
                    }

                    eventDiv.html(eventContent);
                    eventsContainer.append(eventDiv);

                    // Add a horizontal rule if it's not the last element
                    if (index < data.length - 1) {
                        eventsContainer.append('<hr>');
                    }
                });
            },
            error: function(error) {
                console.error('Error fetching data:', error);
            }
        });
    }

    fetchData();
    setInterval(fetchData, 15000);
});
