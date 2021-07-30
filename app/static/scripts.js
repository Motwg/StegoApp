
let openModal = img => {
  let modal = document.getElementById("modal-div");
  let modalImg = document.getElementById("modal-img");
  modal.style.display = "block";
  modalImg.src = img.src;
}

let openProgressModal = () => {
  let modal = document.getElementById("modal-bar");
  modal.style.display = "block";
}

let closeModal = mod_id => {
  let modal = document.getElementById(mod_id);
  modal.style.display = "none";
}

let slideDelta = (sl, id) => {
  document.getElementById(id).innerHTML = "Current value: " + sl.value;
}


$(document).ready(() => {
    var percentage = 0; // loading bar percentage

    socket = io.connect('http://' + document.domain + ':' + location.port + '/events');
    socket.on('progress', progress => {
        percentage = progress;
    });

    let startProgressBar = () => {
        console.log('STARTING')
        openProgressModal()
        let processProgressBar = (timer) => {
            $(".progress-bar").css("width", percentage + "%");
            if(percentage >= 100) {
                stopProgressBar(timer)
             }
        }

        let timer = setInterval(() => {
            socket.emit('check_progress_bar')
            processProgressBar(timer);
        }, 100);

        return timer
    }

    let stopProgressBar = timer => {
        clearInterval(timer);
        console.log('STOPPING')
        socket.emit('reset_progress_bar');
        closeModal("modal-bar")
        $('.progress-bar').css('width', '0%');
    }

    let scheme = {
        'lsb': ['channel'],
        'qim': ['channel', 'delta'],
        'dc_qim': ['channel', 'delta', 'alpha'],
        'show_watermark': ['channel']
    };

    // auto hiding/showing options
    $("form#embedding :input[name='algorithm']").each(function() {
        let alg = $(this);
        alg.change(() => {
            $("form#embedding :input[name!='algorithm'][name]").map(function() {
                let input = $(this);
                if(scheme[alg.val()] && scheme[alg.val()].includes(input.attr('name'))) {
                    input.parent().show();
                }
                else {
                    input.parent().hide();
                };
            });
        });
    });

    $("form#extract :input[name='algorithm']").each(function() {
        let alg = $(this);
        alg.change(() => {
            $("form#extract :input[name!='algorithm'][name]").map(function() {
                let input = $(this);
                if(scheme[alg.val()] && scheme[alg.val()].includes(input.attr('name'))) {
                    input.parent().show();
                }
                else {
                    input.parent().hide();
                };
            });
        });
    });


    $("#upload-image").change(e => {
        console.log('UPLOAD IMG')
        let file_data = $("#upload-image").prop("files")[0];
        let form_data = new FormData();
        form_data.append("upload-image", file_data);
        e.preventDefault();
        $.ajax({
            type:'POST',
            url:'/demo/uploader/image',
            data: form_data,
            processData: false,
            contentType: false,
            success: response => {
                // refresh standard img
                str = $("#upImg").attr("src").split("?")[0]
                $("#upImg").attr("src", str + "?" + Date.now());

                console.log(response)
            },
            error: err => {
                console.log(err.responseJSON)
                alert(err.responseJSON.msg);
            }
        });
    });


    $("#upload-mod").change(e => {
        console.log('UPLOAD MOD')
        let file_data = $("#upload-mod").prop("files")[0];
        let form_data = new FormData();
        form_data.append("upload-mod", file_data);
        e.preventDefault();
        $.ajax({
            type:'POST',
            url:'/demo/uploader/mod',
            data: form_data,
            processData: false,
            contentType: false,
            success: response => {
                // refresh modified img
                str = $("#modImg").attr("src").split("?")[0]
                $("#modImg").attr("src", str + "?" + Date.now());

                console.log(response)
            },
            error: err => {
                console.log(err.responseJSON)
                alert(err.responseJSON.msg);
            }
        });
    });


    $("#btn-embed").click(e => {
        console.log('EMBEDDING')

        // auto fill extraction options
        $("form#embedding :input").each(function() {
             let input = $(this);
             if (input.attr('name')) {
                $("form#extract :input[name=" + input.attr('name') + "]").val(input.val())
             }
        });
        $("form#extract :input[name='algorithm']").trigger("change")
        $("form#extract :input[name='delta']").trigger("change")
        $("form#extract :input[name='alpha']").trigger("change")

        let form_data = new FormData($('#embedding')[0]);
        e.preventDefault();
        timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/embedding',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                // refresh embedded img
                str = $("#embImg").attr("src").split("?")[0]
                $("#embImg").attr("src", str + "?" + Date.now());

                console.log(response)
            },
            error: err => {
                stopProgressBar(timer);
                console.log(err.responseJSON)
                alert(err.responseJSON.msg);
            }
        });
    });


    $("#btn-mod").click(e => {
        console.log('MODIFYING')
        let form_data = new FormData($('#modification')[0]);
        e.preventDefault();
        timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/modify',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                // refresh modified img
                str = $("#modImg").attr("src").split("?")[0]
                $("#modImg").attr("src", str + "?" + Date.now());

                console.log(response)
            },
            error: err => {
                stopProgressBar(timer);
                console.log(err.responseJSON)
                alert(err.responseJSON.msg);
            }
        });
    });


    $("#btn-extract").click(e => {
        console.log('EXTRACTING')
        let form_data = new FormData($('#extract')[0]);
        e.preventDefault();
        timer = startProgressBar();
        $.ajax({
            type:'POST',
            url:'/demo/extract',
            processData: false,
            contentType: false,
            data: form_data,
            success: response => {
                console.log(response);
                $("#ext-watermark").val(response.watermark);
            },
            error: err => {
                stopProgressBar(timer);
                console.log(err.responseJSON);
                alert(err.responseJSON.msg);
            }
        });
    });
});
