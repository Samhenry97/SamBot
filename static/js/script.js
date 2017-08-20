var totalMessages = 0;

$(document).ready(function() {
    $('.flash').delay(5000).fadeOut();
    $('input:text').first().focus();
    scrollMessages(false);
    
    $('#settings').hover(function(event) {
        var settings = $(this);
        $('#settings-dropdown').css('left', settings.position().left - settings.width() / 2);
        $('#settings-dropdown').fadeIn(200);
    });
    $('body').click(function(event) { $('#settings-dropdown').fadeOut(200); });
    
    $('.chatarea').keydown(function(event) {
        if(event.keyCode == 13) {
            event.preventDefault();
            userMessage();
        }
    });
    $('.chatbutton').click(function() { userMessage(); });
    
    $('#phone-reminders').click(function() {
        if(this.checked) {
            $('#phone').show();
        } else {
            $('#phone').hide();
            $('#phone').find('input').val('0');
        }
    });
    
    $('.messagearea').scroll(function() {
        if(this.scrollTop == 0) {
            $.ajax({
                url: '/messages?offset=' + totalMessages,
                type: 'POST',
                success: (data) => {
                    if(data.length) {
                        var oldHeight = this.scrollHeight;
                        for(var i = data.length - 1; i >=  0; i--) {
                            prependMessage(data[i].text, data[i].fromUser ? 'you' : 'bot');
                        }
                        scrollMessages(false, this.scrollHeight - oldHeight);
                    } else if(!$('.messagearea').find('.history').length) {
                        $('.messagearea').prepend('<p class="history">This is the beginning of your chat history with SamBot.</p>');
                    }
                },
                error: (data) => {
                    console.log(data);
                }
            });
        }
    });
    
    if($('.messagearea').length) { 
        totalMessages = $('.messagearea').find('li').length;
        setInterval(checkReminders, 1000);
    }
});

function userMessage() {
    var input = $('.chatarea');
    var text = input.val(); input.val('');
    input.focus();
    if(!$.trim(text)) { return; }
    
    appendMessage(text, 'you');
    
    $.ajax({
        dataType: 'json',
        url: '/message',
        headers: { 'Content-Type': 'application/json' },
        type: 'POST',
        data: JSON.stringify({text: text}),
        success: (data) => {
            if(data.response) { appendMessage(data.response, 'bot'); }
            scrollMessages();
        },
        error: (data) => {
            console.log(data);
        }
    });
}

function appendMessage(text, from) {
    totalMessages++;
    var fromText = from == 'you' ? 'You' : 'SamBot';
    var message = '<li><span class="' + from + '"><div>' + fromText + '</div><pre>' + text + '</pre></span></li>';
    $('.chatlist').append(message);
}

function prependMessage(text, from) {
    totalMessages++;
    var fromText = from == 'you' ? 'You' : 'SamBot';
    var message = '<li><span class="' + from + '"><div>' + fromText + '</div><pre>' + text + '</pre></span></li>';
    $('.chatlist').prepend(message);
}

function scrollMessages(smooth=true, scrollTop = null) {
    var messagearea = $('.messagearea');
    if(messagearea.length) {
        if(!scrollTop) { scrollTop = messagearea[0].scrollHeight; }
        if(smooth) { messagearea.animate({ scrollTop: scrollTop }, 500); }
        else { messagearea.scrollTop(scrollTop); }
    }
}

function checkReminders() {
    $.ajax({
        url: '/reminders',
        type: 'POST',
        success: (data) => {
            if(data.response.length) {
                data.response.forEach((message) => {
                    appendMessage(message, 'bot');
                });
                scrollMessages();
            }
        },
        error: (data) => {
            console.log(data);
        }
    });
}
