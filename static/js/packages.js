function DeleteTrackId(trackid) {
    var trackidDelModalEl = new bootstrap.Modal(document.getElementById('trackidDelModal'))
    $('#deltrackid').html(trackid)
    $('#trackIdDelConfirmBtn').click(function(){
        $.ajax({
            url:'del',
            type: 'get',
            data: {
                package_id: trackid
            },
            success: function(response){
                trackidDelModalEl.hide()
                $('#track_'+response.id).fadeOut('slow', function(){
                    $(this).remove();
                    UpdateFilters();
                });

            }
        })
    })
    trackidDelModalEl.show()
}

function UpdateFilters(){
    $.ajax({
            url:'statuslist',
            type: 'get',
            success: function(response){
                let filterHTML = ''
                statuses = response
                $.each(statuses, function(status,statusname){
                    let currentcount = $('.card'+status).length
                    if (currentcount) {
                        filterHTML += '<span id="filter' + status + '" class="badge m-1 badge' + status
                        if ($('.card'+status+':hidden').length==currentcount) {
                            filterHTML += ' selectedfilter'
                        }
                        filterHTML +=  '" onclick="ToggleFilter(\'' + status + '\')">' + statusname + ' <span class="badge rounded-pill text-bg-light">' + currentcount + '</span></span>'
                    }
                })
                $('#filterwrap').html(filterHTML);
            }
        })

}

function ToggleFilter(status){
    $('.card'+status).toggle('fast')
    $('.badge'+status).toggleClass('selectedfilter')
    if (!$('.badge'+status).hasClass('selectedfilter')) {
        $('html, body').animate({
            scrollTop: $('.card'+status).first().offset().top - 100
        });
    }
}

$(document).ready(function(){
    var trackidAddModalEl = new bootstrap.Modal(document.getElementById('trackidAddModal'))

    UpdateFilters();

    CopyToClipBoard()

    $('#trackidAddOpenModalBtn').click(function(){
        trackidAddModalEl.show()
    })

    $('#id_trackid').bind("change keyup input click", function() {
            if ($(this).val().match(/[^\d\w]/g)) {
                errorAlert('Только латинские буквы и цифры','id_trackid')
                $(this).val($(this).val().replace(/[^\d\w]/g, ''))
                }
            $(this).val($(this).val().toUpperCase())
        })

    $('#addpackage').click(function(){
        packageData = $('#addpackageform').serialize();
        $.ajax({
            url: $('#addpackageform').data('url'),
            type: 'post',
            data: packageData,
            success: function(response){
                $('#notracks').remove()
                if (response.errorMessage==1){
                    errorAlert('Трек-номер уже был добавлен ранее', 'id_trackid')
                }
                else if (response.errorMessage==2){
                    errorAlert('Введите корректный трек-номер', 'id_trackid')
                }
                else {
                    trackidAddModalEl.hide()
                    formReset('addpackageform')
                    newTrackDiv = '<div class="card card' + response.status + ' mt-2 flex-row" id="track_' + response.packageid + '" style="display:none">'
                    newTrackDiv += '<div class="cardstart p-2 rounded-start"></div>'
                    newTrackDiv += '<div class="card-body"><button type="button" class="btn-close float-end btn-del" onclick="DeleteTrackId(\'' + response.packageid + '\')" aria-label="Удалить"></button>'
                    newTrackDiv += '<h3 class="card-title">' + response.packageid + '</h3>'
                    newTrackDiv += '<h6 class="card-subtitle mb-2 text-body-secondary status-'+ response.status +'">' + response.statusname + ' ' + response.changedate + '</h6>'
                    newTrackDiv += '<p class="card-text">' + response.desc + '</p></div></div>'
                    $('#addtrackwrap').before(newTrackDiv)
                    $('#track_' + response.packageid).fadeIn('slow')
                    UpdateFilters()
                    $('html, body').animate({
                        scrollTop: $('#track_' + response.packageid).offset().top
                    });
                }
            }

        })
    })

});