$(document).ready(function() {
    function fetchData() {
        $.ajax({
            url: '/api/events',
            method: 'GET',
            dataType: 'json', // Ensures the response is parsed as JSON
            success: function(data) {
                let eventsContainer = $('#events');
                eventsContainer.empty();

                if (data.error) {
                    eventsContainer.html(`<p>Error: ${data.error}</p>`);
                    return;
                }

                data.forEach((event, index) => {
                    let eventDiv = $('<div>').addClass('event');

                    eventDiv.html(`
                        <p><strong>Request ID:</strong> ${event.request_id}</p>
                        <p><strong>Author:</strong> ${event.author}</p>
                        <p><strong>Action:</strong> ${event.action}</p>
                        <p><strong>From Branch:</strong> ${event.from_branch}</p>
                        <p><strong>To Branch:</strong> ${event.to_branch}</p>
                        <p><strong>Timestamp:</strong> ${event.timestamp}</p>
                    `);

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
    setInterval(fetchData, 5000);
});
