var STATUS = {
    UNREAD: 0,
    READING: 1,
    COMPLETE: 2,
    ABANDON: 3
}

var update_media = function(id, field, value) {
    $.ajax({
        url: '/media',
        type: 'GET',
        data: {id: id, field: field, value: value}
    });
};

var update_rating = function(id, value) {
    $.ajax({
        url: '/rate',
        type: 'GET',
        data: {id: id, rating: value},
    });
};

var update_recommend = function(id, user, value) {
    $.ajax({
        url: '/recommend',
        type: 'GET',
        data: {id: id, to_user: user, value: value},
    });
};

var update_status = function(id, status) {
    $.ajax({
        url: '/status',
        type: 'GET',
        data: {id: id, value: status}
    });
};

var init_event_listeners = function(id) {
    $('#author').on('input', function() {
        var new_content = $('#author').html();
        update_media(id, 'author', new_content);
    });

    $('#description').on('input', function() {
        var new_content = $('#description').html();
        update_media(id, 'description', new_content);
    });

    $('#reading').click(function(){
        update_status(id, STATUS.READING);
        location.reload();
    });

    $('#unabandon').click(function(){
        update_status(id, STATUS.READING);
        location.reload();
    });

    $('#abandon').click(function(){
        update_status(id, STATUS.ABANDON);
        location.reload();
    });

    $('#complete').click(function(){
        update_status(id, STATUS.COMPLETE);
        location.reload();
    });
}
