$(document).ready(function() {
    $('.flash').delay(5000).fadeOut();
    scrollMessages();
    
    $('.chatarea').keydown(function(event) {
        if(event.keyCode == 13) {
            event.preventDefault();
            userMessage();
        }
    });
    
    $('.chatbutton').click(function() {
        userMessage();
    });
    
    var page = 1;
    $('.messagearea').scroll(function() {
        if(this.scrollTop == 0) {
            page++;
            $.ajax({
                url: '/messages?page=' + page,
                type: 'POST',
                success: (data) => {
                    if(data.length) {
                        var oldHeight = this.scrollHeight;
                        data.forEach((message) => {
                            prependMessage(message.text, message.fromUser ? 'you' : 'bot');
                        });
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
});

function userMessage() {
    var input = $('.chatarea');
    var text = input.val(); input.val('');
    input.focus();
    appendMessage(text, 'you');
    
    $.ajax({
        dataType: 'json',
        url: '/message',
        headers: { 'Content-Type': 'application/json' },
        type: 'POST',
        data: JSON.stringify({text: text}),
        success: (data) => {
            if(data.response) { appendMessage(data.response, 'bot');  }
        },
        error: (data) => {
            console.log(data);
        }
    });
    
    scrollMessages();
}

function appendMessage(text, from) {
    var fromText = from == 'you' ? 'You' : 'SamBot';
    var message = '<li><span class="' + from + '"><div>' + fromText + '</div><pre>' + text + '</pre></span></li>';
    $('.chatlist').append(message);
}

function prependMessage(text, from) {
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
