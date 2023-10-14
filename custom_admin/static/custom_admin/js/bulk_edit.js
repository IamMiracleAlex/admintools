function handleChangeEvent(event, type) {
    let nodeID = event.target.value;
    var url = $("#form").attr("data-extra-url");  // get the url of the `load_extra_data` view
    let encodedValue = encodeURIComponent(nodeID); // Encode the value in case of special characters like '&'
    url = url += `?node_id=${encodedValue}&level=${event.target.id}`; // I'm adding this level so it is easy to manipulate on the backend
    
    $.ajax({                      
        url: url,
        success: function(data) {
            loadData(data.data, event);
        }
    });
}

function handleToEvent(event, type) {
    let nodeID = event.target.value;
    var url = $("#form").attr("data-extra-url");  // get the url of the `load_extra_data` view
    url = url += `?node_id=${nodeID}`;
    
    $.ajax({                      
        url: url,
        success: function(data) {
            loadData(data.data, event);
        }
    });
}

function loadData(data, event) {
    let htmlData = '<option value="">--------Select--------</option>' // This ensures that the next level dropdown is reset
    data.forEach(function(node) {
        if (node.hasOwnProperty("id")) {
            htmlData += `<option value="${node.id}">${node.title}</option>` // populate the children data here
        } else {
            htmlData += `<option value="${node.title}">${node.title}</option>` // populate the children data here
        }
    })

    // Check where to render the json data
    if(event.target.id.toString().includes('from')) {
        if(event.target.id === "id_from_department"){
            $('#id_from_category').html(htmlData);
        }
        if(event.target.id === "id_from_category"){
            $('#id_from_subcategory').html(htmlData);
        }
        if(event.target.id === "id_from_subcategory"){
            $('#id_from_subset').html(htmlData);
        }
    } else if(event.target.id.toString().includes('to')) {
        if(event.target.id === "id_to_department"){
            $('#id_to_category').html(htmlData);
        }
        if(event.target.id === "id_to_category"){
            $('#id_to_subcategory').html(htmlData);
        }
        if(event.target.id === "id_to_subcategory"){
            $('#id_to_subset').html(htmlData);
        }
    }
}

$("#fetch_matches").on("click", function(e) { 
    var form = $("#form");
    var fetch_matches = $(this);

    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: "GET",
        dataType: 'json',
        beforeSend: function(){
            fetch_matches.text('Loading...')
        }, 
        success: function (data) {
            $('#matches_table').html(data.html_page);
            fetch_matches.text('Fetch matches')
        },
        error: function (request, error) {
            alert("Error occured: can not fetch matches, try again later");
            fetch_matches.text('Fetch matches')
        },    
    })
    return false;
});